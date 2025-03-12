"use client"

import { useState, useCallback, useMemo } from "react"
import { toast } from "sonner" // [modificación] - Importamos toast directamente de sonner
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import { Upload, RefreshCw, ImageIcon, Loader2, CheckCircle2, AlertCircle, InfoIcon } from "lucide-react"
import PostPreview from "@/components/post-preview"
import PublishConfirmation from "@/components/publish-confirmation"

// Moviendo la interfaz a un lugar más accesible para reutilización
export interface FormData {
  position: string
  positionPriority: number
  location: string
  locationPriority: number
  email: string
  emailPriority: number
  requirements: string
  requirementsPriority: number
  image: string | null
}

// Constantes para valores del formulario
const PRIORITY_LIMITS = {
  MIN: 1,
  MAX: 10,
  DEFAULT_POSITION: 5,
  DEFAULT_LOCATION: 3,
  DEFAULT_EMAIL: 3,
  DEFAULT_REQUIREMENTS: 4
}

const INITIAL_FORM_DATA: FormData = {
  position: "",
  positionPriority: PRIORITY_LIMITS.DEFAULT_POSITION,
  location: "",
  locationPriority: PRIORITY_LIMITS.DEFAULT_LOCATION,
  email: "",
  emailPriority: PRIORITY_LIMITS.DEFAULT_EMAIL,
  requirements: "",
  requirementsPriority: PRIORITY_LIMITS.DEFAULT_REQUIREMENTS,
  image: null,
}

export default function JobPostingForm() {
  // [modificación] - Eliminamos el hook useToast
  const [formData, setFormData] = useState<FormData>(INITIAL_FORM_DATA)
  const [previewGenerated, setPreviewGenerated] = useState(false)
  const [showConfirmation, setShowConfirmation] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isPublishing, setIsPublishing] = useState(false)

  // Determinar si el formulario es válido
  const isFormValid = useMemo(() => {
    return Boolean(formData.position && formData.location && formData.email);
  }, [formData.position, formData.location, formData.email]);

  // Manejar cambios en los inputs de texto
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }, []);

  // Manejar cambios en los sliders
  const handleSliderChange = useCallback((name: string, value: number[]) => {
    setFormData((prev) => ({ ...prev, [name]: value[0] }))
  }, []);

  // Manejar la subida de imágenes
  const handleImageUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return;
    
    // Validar el tamaño del archivo (máximo 5MB)
    if (file.size > 5 * 1024 * 1024) {
      // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
      toast.error("Archivo demasiado grande", {
        description: "La imagen no debe superar los 5MB.",
        icon: <AlertCircle className="h-5 w-5" />
      });
      return;
    }

    const reader = new FileReader()
    reader.onload = () => {
      setFormData((prev) => ({ ...prev, image: reader.result as string }))
    }
    reader.readAsDataURL(file)
  }, []);

  // Generar el post
  const generatePost = useCallback(async () => {
    if (!isFormValid) {
      // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
      toast.error("Campos requeridos", {
        description: "Por favor complete los campos obligatorios: Puesto, Ubicación y Email.",
        icon: <AlertCircle className="h-5 w-5" />
      });
      return
    }

    setIsGenerating(true)
    
    try {
      // Simulando una llamada API para generar el post
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setPreviewGenerated(true)
      // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
      toast.success("Post generado", {
        description: "La vista previa ha sido generada correctamente.",
        icon: <CheckCircle2 className="h-5 w-5" />
      });
    } catch (error) {
      // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
      toast.error("Error", {
        description: "No se pudo generar la vista previa. Intente nuevamente.",
        icon: <AlertCircle className="h-5 w-5" />
      });
    } finally {
      setIsGenerating(false)
    }
  }, [isFormValid]);

  // Reiniciar el formulario
  const resetForm = useCallback(() => {
    setFormData(INITIAL_FORM_DATA)
    setPreviewGenerated(false)
    setShowConfirmation(false)
    // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
    toast.info("Formulario reiniciado", {
      description: "Todos los campos han sido reiniciados.",
      icon: <InfoIcon className="h-5 w-5" />
    });
  }, []);

  // Manejar la publicación
  const handlePublish = useCallback(() => {
    setShowConfirmation(true)
  }, []);

  // Confirmar la publicación
  const confirmPublish = useCallback(async (publish: boolean) => {
    setShowConfirmation(false)
    
    if (publish) {
      setIsPublishing(true)
      try {
        // Simulando una llamada API para publicar en Instagram
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
        toast.success("Publicado con éxito", {
          description: "La oferta laboral ha sido publicada en Instagram.",
          icon: <CheckCircle2 className="h-5 w-5" />
        });
      } catch (error) {
        // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
        toast.error("Error al publicar", {
          description: "No se pudo publicar en Instagram. Intente nuevamente.",
          icon: <AlertCircle className="h-5 w-5" />
        });
      } finally {
        setIsPublishing(false)
      }
    } else {
      // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
      toast.info("Guardado", {
        description: "La oferta laboral ha sido guardada para más tarde.",
        icon: <InfoIcon className="h-5 w-5" />
      });
    }
  }, []);

  return (
    <div className="grid md:grid-cols-2 gap-8">
      <Card className="p-6">
        <h2 className="text-2xl font-semibold mb-6 text-[#0066cc]">Información del Puesto</h2>

        <div className="space-y-6">
          <div>
            <div className="flex justify-between mb-2">
              <Label htmlFor="position">Perfil/Puesto <span className="text-red-500">*</span></Label>
              <span className="text-sm text-gray-500">Prioridad: {formData.positionPriority}</span>
            </div>
            <Input
              id="position"
              name="position"
              placeholder="Ej: Médico Cardiólogo"
              value={formData.position}
              onChange={handleInputChange}
              className="mb-2"
              required
              aria-required="true"
            />
            <Slider
              defaultValue={[formData.positionPriority]}
              max={PRIORITY_LIMITS.MAX}
              min={PRIORITY_LIMITS.MIN}
              step={1}
              onValueChange={(value) => handleSliderChange("positionPriority", value)}
              aria-label="Prioridad del puesto"
            />
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <Label htmlFor="location">Ubicación <span className="text-red-500">*</span></Label>
              <span className="text-sm text-gray-500">Prioridad: {formData.locationPriority}</span>
            </div>
            <Input
              id="location"
              name="location"
              placeholder="Ej: Buenos Aires"
              value={formData.location}
              onChange={handleInputChange}
              className="mb-2"
              required
              aria-required="true"
            />
            <Slider
              defaultValue={[formData.locationPriority]}
              max={PRIORITY_LIMITS.MAX}
              min={PRIORITY_LIMITS.MIN}
              step={1}
              onValueChange={(value) => handleSliderChange("locationPriority", value)}
              aria-label="Prioridad de la ubicación"
            />
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <Label htmlFor="email">Email de contacto <span className="text-red-500">*</span></Label>
              <span className="text-sm text-gray-500">Prioridad: {formData.emailPriority}</span>
            </div>
            <Input
              id="email"
              name="email"
              type="email"
              placeholder="Ej: rrhh@darsalud.com"
              value={formData.email}
              onChange={handleInputChange}
              className="mb-2"
              required
              aria-required="true"
            />
            <Slider
              defaultValue={[formData.emailPriority]}
              max={PRIORITY_LIMITS.MAX}
              min={PRIORITY_LIMITS.MIN}
              step={1}
              onValueChange={(value) => handleSliderChange("emailPriority", value)}
              aria-label="Prioridad del email"
            />
          </div>

          <div>
            <div className="flex justify-between mb-2">
              <Label htmlFor="requirements">Requisitos</Label>
              <span className="text-sm text-gray-500">Prioridad: {formData.requirementsPriority}</span>
            </div>
            <Textarea
              id="requirements"
              name="requirements"
              placeholder="Ej: - Experiencia mínima de 3 años&#10;- Disponibilidad full-time&#10;- Residencia completa"
              value={formData.requirements}
              onChange={handleInputChange}
              className="min-h-[120px] mb-2"
            />
            <Slider
              defaultValue={[formData.requirementsPriority]}
              max={PRIORITY_LIMITS.MAX}
              min={PRIORITY_LIMITS.MIN}
              step={1}
              onValueChange={(value) => handleSliderChange("requirementsPriority", value)}
              aria-label="Prioridad de requisitos"
            />
          </div>

          <div>
            <Label htmlFor="image" className="block mb-2">
              Imagen (opcional)
            </Label>
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                className="w-full"
                onClick={() => document.getElementById("image-upload")?.click()}
                type="button"
              >
                <Upload className="mr-2 h-4 w-4" /> Subir imagen
              </Button>
              <Input 
                id="image-upload" 
                type="file" 
                accept="image/*" 
                className="hidden" 
                onChange={handleImageUpload} 
                aria-label="Subir imagen"
              />
              {formData.image && (
                <div className="relative h-12 w-12 rounded overflow-hidden border border-gray-200">
                  <img
                    src={formData.image}
                    alt="Vista previa"
                    className="h-full w-full object-cover"
                  />
                  <button
                    type="button"
                    className="absolute top-0 right-0 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs hover:bg-red-600"
                    onClick={() => setFormData(prev => ({ ...prev, image: null }))}
                    aria-label="Eliminar imagen"
                  >
                    ×
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="flex gap-4 pt-4">
            <Button 
              className="w-full bg-[#00cc99] hover:bg-[#00bb88]" 
              onClick={generatePost}
              disabled={isGenerating || !isFormValid}
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generando...
                </>
              ) : (
                'Generar Post'
              )}
            </Button>
            <Button 
              variant="outline" 
              className="w-full" 
              onClick={resetForm}
              type="button"
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Reiniciar
            </Button>
          </div>
        </div>
      </Card>

      <div>
        {previewGenerated ? (
          <div className="space-y-6">
            <PostPreview formData={formData} />
            <div className="flex gap-4">
              <Button
                className="w-full bg-[#0066cc] hover:bg-[#0055bb]"
                onClick={handlePublish}
                disabled={isPublishing}
              >
                {isPublishing ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Publicando...
                  </>
                ) : (
                  'Publicar en Instagram'
                )}
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={() =>
                  // [modificación] - Reemplazamos la llamada a toast con la nueva sintaxis de sonner
                  toast.info("Guardado", {
                    description: "La oferta laboral ha sido guardada como borrador.",
                    icon: <InfoIcon className="h-5 w-5" />
                  })
                }
              >
                Guardar para después
              </Button>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center bg-gray-100 rounded-lg p-8">
            <div className="text-center">
              <ImageIcon className="h-16 w-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-700">Vista previa no disponible</h3>
              <p className="text-gray-500 mt-2">
                Complete el formulario y haga clic en "Generar Post" para ver la vista previa.
              </p>
            </div>
          </div>
        )}
      </div>

      {showConfirmation && <PublishConfirmation onConfirm={confirmPublish} />}
    </div>
  )
}