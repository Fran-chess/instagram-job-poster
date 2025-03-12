import { memo } from 'react';
import { Card } from "@/components/ui/card"
import { MapPin, Mail } from "lucide-react"
import { FormData } from '@/components/job-posting-form';

interface PostPreviewProps {
  formData: FormData;
}

// Función para calcular el tamaño del texto basado en la prioridad
const calculateFontSize = (priority: number, baseSize: number, factor: number): string => {
  return `${Math.min(baseSize + priority * factor, baseSize * 2)}rem`;
};

// Memoizamos el componente para evitar renderizados innecesarios
const PostPreview = memo(function PostPreview({ formData }: PostPreviewProps) {
  // Split requirements into an array for better formatting
  const requirementsList = formData.requirements
    ? formData.requirements.split("\n").filter((req) => req.trim() !== "")
    : [];

  // Formato de fecha actual para mostrar en el post
  const currentDate = new Date().toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <Card className="overflow-hidden shadow-lg">
      <div className="relative bg-white p-0">
        {/* Preview Header */}
        <div className="bg-[#0066cc] text-white text-center py-4 px-6">
          <h2 className="text-xl font-bold">Buscamos Profesionales</h2>
        </div>

        {/* Main Content */}
        <div className="p-6 space-y-6">
          {/* Position */}
          <div className="text-center">
            <div
              className="inline-block bg-[#00cc99] text-white px-6 py-3 rounded-md shadow-sm transition-all duration-200"
              style={{ 
                fontSize: calculateFontSize(formData.positionPriority, 1.5, 0.1),
                transform: `scale(${1 + formData.positionPriority * 0.02})`
              }}
            >
              {formData.position || "PUESTO"}
            </div>
          </div>

          {/* Location */}
          <div
            className="flex items-center justify-center gap-2 text-gray-700"
            style={{ fontSize: calculateFontSize(formData.locationPriority, 1, 0.05) }}
          >
            <MapPin className="text-[#0066cc]" />
            <span>{formData.location || "Ubicación"}</span>
          </div>

          {/* Requirements */}
          {requirementsList.length > 0 && (
            <div
              className="bg-gray-50 p-4 rounded-md"
              style={{ fontSize: calculateFontSize(formData.requirementsPriority, 0.9, 0.03) }}
            >
              <h3 className="font-semibold mb-2 text-[#0066cc]">Requisitos:</h3>
              <ul className="space-y-1 list-disc pl-5">
                {requirementsList.map((req, index) => (
                  <li key={index}>{req}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Email */}
          <div
            className="flex items-center justify-center gap-2 text-gray-700 bg-gray-50 p-3 rounded-md"
            style={{ fontSize: calculateFontSize(formData.emailPriority, 0.9, 0.05) }}
          >
            <Mail className="text-[#0066cc]" />
            <span>
              Dejanos tu CV: <strong>{formData.email || "email@ejemplo.com"}</strong>
            </span>
          </div>

          {/* Background Image */}
          {formData.image && (
            <div className="absolute inset-0 -z-10 opacity-10">
              <img src={formData.image} alt="" className="w-full h-full object-cover" />
            </div>
          )}
        </div>

        {/* Footer with Logo */}
        <div className="bg-gray-50 p-4 flex justify-between items-center">
          <div className="text-sm text-gray-500">
            <div>#{formData.position.replace(/\s+/g, '')} #Salud #Oportunidad</div>
            <div className="text-xs text-gray-400 mt-1">{currentDate}</div>
          </div>
          <div className="font-bold text-[#0066cc]">DarSalud</div>
        </div>
      </div>
    </Card>
  );
});

export default PostPreview;