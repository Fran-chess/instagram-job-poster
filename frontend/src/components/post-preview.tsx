import { memo } from 'react';
import { Card } from "@/components/ui/card"
import { MapPin, Mail } from "lucide-react"
import { FormData } from '@/hooks/useJobPostingForm';

interface PostPreviewProps {
  formData: FormData;
  imageUrl?: string | null;
}

// Función para calcular el tamaño del texto basado en la prioridad pero con límites más estrictos
const calculateFontSize = (priority: number, baseSize: number, factor: number): string => {
  return `${Math.min(baseSize + priority * factor, baseSize * 1.5)}rem`;
};

// Memoizamos el componente para evitar renderizados innecesarios
const PostPreview = memo(function PostPreview({ formData, imageUrl }: PostPreviewProps) {
  // Split requirements into an array for better formatting
  const requirementsList = formData.requirements
    ? formData.requirements.split("\n").filter((req) => req.trim() !== "")
    : [];

  // Limitamos la cantidad de requisitos a mostrar para reducir altura
  const displayRequirements = requirementsList.slice(0, 3);
  const hasMoreRequirements = requirementsList.length > 3;

  // Formato de fecha actual para mostrar en el post
  const currentDate = new Date().toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  // Si hay una imagen proporcionada por el backend, usarla, de lo contrario mostrar la vista previa local
  const displayImageUrl = imageUrl || formData.image;

  return (
    <Card className="overflow-hidden shadow-lg border border-gray-200">
      {imageUrl ? (
        // Si hay una imagen generada por el backend, mostrarla directamente
        <div className="w-full h-full">
          <img 
            src={imageUrl} 
            alt="Vista previa generada por el servidor" 
            className="w-full h-auto"
          />
        </div>
      ) : (
        // Si no hay imagen del backend, mostrar la vista previa como antes pero más compacta
        <div className="relative bg-white p-0">
          {/* Preview Header */}
          <div className="bg-blue-600 text-white text-center py-2 px-4">
            <h2 className="text-md font-bold">Buscamos Profesionales</h2>
          </div>

          {/* Main Content */}
          <div className="p-3 sm:p-4">
            {/* Position */}
            {formData.position && (
              <div className="text-center mb-2">
                <h3 
                  style={{ 
                    fontSize: calculateFontSize(formData.positionPriority, 1.1, 0.1),
                    lineHeight: "1.2"
                  }} 
                  className="font-bold text-blue-600"
                >
                  {formData.position}
                </h3>
              </div>
            )}

            {/* Location */}
            {formData.location && (
              <div className="flex items-center justify-center text-gray-800 mb-2">
                <MapPin className="h-4 w-4 mr-1 text-blue-600" />
                <span 
                  className="font-medium"
                  style={{ 
                    fontSize: calculateFontSize(formData.locationPriority, 0.9, 0.05) 
                  }}
                >
                  {formData.location}
                </span>
              </div>
            )}

            {/* Requirements - versión compacta */}
            {displayRequirements.length > 0 && (
              <div className="mb-2 text-gray-900">
                <h4 
                  className="font-semibold mb-1 text-center"
                  style={{ 
                    fontSize: calculateFontSize(formData.requirementsPriority, 0.9, 0.05) 
                  }}
                >
                  Requisitos:
                </h4>
                <ul className="list-disc list-inside space-y-0.5 text-xs sm:text-sm">
                  {displayRequirements.map((requirement, index) => (
                    <li key={index}>{requirement}</li>
                  ))}
                  {hasMoreRequirements && (
                    <li className="text-gray-500">Y {requirementsList.length - 3} más...</li>
                  )}
                </ul>
              </div>
            )}

            {/* Contact */}
            {formData.email && (
              <div className="flex items-center justify-center gap-1 text-gray-800 mt-2">
                <Mail className="h-3 w-3 text-blue-600" />
                <span 
                  className="font-medium text-center text-xs"
                  style={{ 
                    fontSize: calculateFontSize(formData.emailPriority, 0.75, 0.03) 
                  }}
                >
                  {formData.email}
                </span>
              </div>
            )}

            {/* Background Image */}
            {formData.image && (
              <div className="absolute inset-0 -z-10 opacity-10">
                <img src={formData.image} alt="" className="w-full h-full object-cover" />
              </div>
            )}
          </div>

          {/* Footer with Logo - versión compacta */}
          <div className="bg-gray-50 p-2 flex justify-between items-center border-t border-gray-200 text-xs">
            <div className="text-gray-600">
              <div>#{formData.position.replace(/\s+/g, '')} #Salud</div>
              <div className="text-gray-500 text-xs">{currentDate}</div>
            </div>
            <div className="font-bold text-blue-600">DarSalud</div>
          </div>
        </div>
      )}
    </Card>
  );
});

export default PostPreview;