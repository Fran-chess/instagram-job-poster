import { useState, useCallback, useMemo, useEffect } from "react";
import { toast } from "sonner";
import { CheckCircle2, AlertCircle, InfoIcon } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { 
  getTemplates, 
  generatePreview, 
  createPost, 
  publishPost, 
  schedulePost,
  Template
} from "@/services/api";

// Constantes para valores del formulario
export const PRIORITY_LIMITS = {
  MIN: 1,
  MAX: 10,
  DEFAULT_POSITION: 5,
  DEFAULT_LOCATION: 3,
  DEFAULT_EMAIL: 3,
  DEFAULT_REQUIREMENTS: 4
};

export interface FormData {
  template_id: number; // Nueva propiedad para seleccionar plantilla
  position: string;
  positionPriority: number;
  location: string;
  locationPriority: number;
  email: string;
  emailPriority: number;
  requirements: string;
  requirementsPriority: number;
  image: string | null;
}

export const INITIAL_FORM_DATA: FormData = {
  template_id: 1, // Por defecto, usar la primera plantilla
  position: "",
  positionPriority: PRIORITY_LIMITS.DEFAULT_POSITION,
  location: "",
  locationPriority: PRIORITY_LIMITS.DEFAULT_LOCATION,
  email: "",
  emailPriority: PRIORITY_LIMITS.DEFAULT_EMAIL,
  requirements: "",
  requirementsPriority: PRIORITY_LIMITS.DEFAULT_REQUIREMENTS,
  image: null,
};

export default function useJobPostingForm() {
  const [formData, setFormData] = useState<FormData>(INITIAL_FORM_DATA);
  const [previewGenerated, setPreviewGenerated] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [createdPostId, setCreatedPostId] = useState<number | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [isLoadingTemplates, setIsLoadingTemplates] = useState(false);

  // Cargar plantillas al iniciar
  useEffect(() => {
    const fetchTemplates = async () => {
      setIsLoadingTemplates(true);
      try {
        const templatesData = await getTemplates();
        setTemplates(templatesData);
        
        // Si hay plantillas, usar la primera como predeterminada
        if (templatesData.length > 0) {
          setFormData(prev => ({
            ...prev,
            template_id: templatesData[0].template_id
          }));
        }
      } catch (error) {
        console.error("Error al cargar plantillas:", error);
        toast.error("Error al cargar plantillas", {
          description: "No se pudieron cargar las plantillas. Intenta recargar la página."
        });
      } finally {
        setIsLoadingTemplates(false);
      }
    };

    fetchTemplates();
  }, []);

  // Determinar si el formulario es válido
  const isFormValid = useMemo(() => {
    return Boolean(formData.position && formData.location && formData.email && formData.template_id);
  }, [formData.position, formData.location, formData.email, formData.template_id]);

  // Manejar cambios en los inputs de texto
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  }, []);

  // Manejar cambios en los selects
  const handleSelectChange = useCallback((name: string, value: number | string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  }, []);

  // Manejar cambios en los sliders
  const handleSliderChange = useCallback((name: string, value: number[]) => {
    setFormData((prev) => ({ ...prev, [name]: value[0] }));
  }, []);

  // Manejar la subida de imágenes
  const handleImageUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    // Validar el tamaño del archivo (máximo 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error("Archivo demasiado grande", {
        description: "La imagen no debe superar los 5MB."
      });
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setFormData((prev) => ({ ...prev, image: reader.result as string }));
    };
    reader.readAsDataURL(file);
  }, []);

  // Generar la vista previa del post
  const generatePost = useCallback(async () => {
    if (!isFormValid) {
      toast.error("Campos requeridos", {
        description: "Por favor complete los campos obligatorios: Puesto, Ubicación, Email y Plantilla."
      });
      return;
    }

    setIsGenerating(true);
    
    try {
      // Llamar al backend para generar la vista previa
      const previewData = await generatePreview({
        template_id: formData.template_id,
        job_title: formData.position,
        location: formData.location,
        email: formData.email,
        requirements: formData.requirements,
        position_priority: formData.positionPriority,
        location_priority: formData.locationPriority,
        email_priority: formData.emailPriority,
        requirements_priority: formData.requirementsPriority
      });
      
      // Guardar la URL de la imagen generada
      setPreviewUrl(previewData.image_url);
      setPreviewGenerated(true);
      
      toast.success("Post generado", {
        description: "La vista previa ha sido generada correctamente."
      });
    } catch (error) {
      console.error("Error al generar vista previa:", error);
      toast.error("Error", {
        description: "No se pudo generar la vista previa. Intente nuevamente."
      });
    } finally {
      setIsGenerating(false);
    }
  }, [formData, isFormValid]);

  // Crear el post (guardar en la base de datos)
  const createPostInBackend = useCallback(async () => {
    try {
      // Primero creamos el post en el backend
      const post = await createPost({
        template_id: formData.template_id,
        job_title: formData.position,
        location: formData.location,
        email: formData.email,
        requirements: formData.requirements,
        position_priority: formData.positionPriority,
        location_priority: formData.locationPriority,
        email_priority: formData.emailPriority,
        requirements_priority: formData.requirementsPriority
      });
      
      // Guardar el ID del post creado
      setCreatedPostId(post.post_id);
      
      return post.post_id;
    } catch (error) {
      console.error("Error al crear post:", error);
      throw error;
    }
  }, [formData]);

  // Reiniciar el formulario
  const resetForm = useCallback(() => {
    setFormData({
      ...INITIAL_FORM_DATA,
      template_id: templates.length > 0 ? templates[0].template_id : 1
    });
    setPreviewGenerated(false);
    setShowConfirmation(false);
    setPreviewUrl(null);
    setCreatedPostId(null);
    
    toast.info("Formulario reiniciado", {
      description: "Todos los campos han sido reiniciados."
    });
  }, [templates]);

  // Manejar la publicación
  const handlePublish = useCallback(() => {
    setShowConfirmation(true);
  }, []);

  // Confirmar la publicación
  const confirmPublish = useCallback(async (publish: boolean, scheduleTime?: Date) => {
    setShowConfirmation(false);
    
    try {
      // Si no hay ID de post, primero crearlo
      let postId = createdPostId;
      if (!postId) {
        postId = await createPostInBackend();
      }
      
      if (publish) {
        if (scheduleTime) {
          // Programar publicación
          setIsPublishing(true);
          
          await schedulePost(postId, {
            scheduled_for: scheduleTime.toISOString(),
            frequency: "once"
          });
          
          toast.success("Programado con éxito", {
            description: `La publicación será publicada el ${scheduleTime.toLocaleDateString()} a las ${scheduleTime.toLocaleTimeString()}.`
          });
        } else {
          // Publicar inmediatamente
          setIsPublishing(true);
          
          const result = await publishPost(postId);
          
          toast.success("Publicado con éxito", {
            description: "La oferta laboral ha sido publicada en Instagram."
          });
        }
      } else {
        // Solo guardar como borrador
        toast.info("Guardado", {
          description: "La oferta laboral ha sido guardada como borrador."
        });
      }
      
      // Reiniciar formulario después de guardar/publicar
      setTimeout(() => {
        resetForm();
      }, 2000);
      
    } catch (error) {
      console.error("Error en el proceso de publicación:", error);
      toast.error("Error", {
        description: "No se pudo completar la operación. Intente nuevamente."
      });
    } finally {
      setIsPublishing(false);
    }
  }, [createdPostId, createPostInBackend, resetForm]);

  return {
    formData,
    previewGenerated,
    showConfirmation,
    isGenerating,
    isPublishing,
    isFormValid,
    templates,
    isLoadingTemplates,
    previewUrl,
    handleInputChange,
    handleSelectChange,
    handleSliderChange,
    handleImageUpload,
    generatePost,
    resetForm,
    handlePublish,
    confirmPublish,
  };
}