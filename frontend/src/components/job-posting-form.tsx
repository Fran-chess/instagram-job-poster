"use client"

import { toast } from "sonner"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import { 
  Upload, 
  RefreshCw, 
  ImageIcon, 
  Loader2, 
  InfoIcon,
  AlertCircle 
} from "lucide-react"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import PostPreview from "@/components/post-preview"
import PublishConfirmation from "@/components/publish-confirmation"
import useJobPostingForm, { PRIORITY_LIMITS } from "@/hooks/useJobPostingForm"

export default function JobPostingForm() {
  const {
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
  } = useJobPostingForm();

  return (
    <div className="grid lg:grid-cols-5 gap-6">
      <div className="lg:col-span-3">
        <Card className="p-4 sm:p-6 bg-white border border-gray-200">
          <div className="flex justify-between items-center mb-4 sm:mb-6">
            <h2 className="text-xl sm:text-2xl font-semibold text-gray-900">Información del Puesto</h2>
            <Button 
              variant="outline" 
              className="border-gray-300 text-gray-700 hover:text-blue-600 hover:border-blue-300" 
              onClick={resetForm}
              type="button"
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Reiniciar
            </Button>
          </div>

          <div className="space-y-4 sm:space-y-6">
            {/* Selector de Plantilla */}
            <div>
              <div className="flex justify-between mb-2">
                <Label htmlFor="template_id" className="text-gray-800">Plantilla <span className="text-red-500">*</span></Label>
              </div>
              <Select
                value={formData.template_id.toString()}
                onValueChange={(value) => handleSelectChange("template_id", parseInt(value))}
                disabled={isLoadingTemplates}
              >
                <SelectTrigger className="w-full bg-white">
                  <SelectValue placeholder="Selecciona una plantilla" />
                </SelectTrigger>
                <SelectContent>
                  {isLoadingTemplates ? (
                    <SelectItem value="loading" disabled>
                      Cargando plantillas...
                    </SelectItem>
                  ) : templates.length === 0 ? (
                    <SelectItem value="empty" disabled>
                      No hay plantillas disponibles
                    </SelectItem>
                  ) : (
                    templates.map((template) => (
                      <SelectItem 
                        key={template.template_id} 
                        value={template.template_id.toString()}
                      >
                        {template.name}
                      </SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <Label htmlFor="position" className="text-gray-800">Perfil/Puesto <span className="text-red-500">*</span></Label>
                <span className="text-sm text-gray-600">Prioridad: {formData.positionPriority}</span>
              </div>
              <Input
                id="position"
                name="position"
                placeholder="Ej: Médico Cardiólogo"
                value={formData.position}
                onChange={handleInputChange}
                className="mb-2 bg-white"
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
                className="accent-blue-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <Label htmlFor="location" className="text-gray-800">Ubicación <span className="text-red-500">*</span></Label>
                <span className="text-sm text-gray-600">Prioridad: {formData.locationPriority}</span>
              </div>
              <Input
                id="location"
                name="location"
                placeholder="Ej: Buenos Aires"
                value={formData.location}
                onChange={handleInputChange}
                className="mb-2 bg-white"
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
                className="accent-blue-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <Label htmlFor="email" className="text-gray-800">Email de contacto <span className="text-red-500">*</span></Label>
                <span className="text-sm text-gray-600">Prioridad: {formData.emailPriority}</span>
              </div>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="Ej: rrhh@darsalud.com"
                value={formData.email}
                onChange={handleInputChange}
                className="mb-2 bg-white"
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
                className="accent-blue-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <Label htmlFor="requirements" className="text-gray-800">Requisitos</Label>
                <span className="text-sm text-gray-600">Prioridad: {formData.requirementsPriority}</span>
              </div>
              <Textarea
                id="requirements"
                name="requirements"
                placeholder="Ej: - Experiencia mínima de 3 años&#10;- Disponibilidad full-time&#10;- Residencia completa"
                value={formData.requirements}
                onChange={handleInputChange}
                className="min-h-[120px] mb-2 bg-white"
              />
              <Slider
                defaultValue={[formData.requirementsPriority]}
                max={PRIORITY_LIMITS.MAX}
                min={PRIORITY_LIMITS.MIN}
                step={1}
                onValueChange={(value) => handleSliderChange("requirementsPriority", value)}
                aria-label="Prioridad de requisitos"
                className="accent-blue-500"
              />
            </div>

            <div>
              <Label htmlFor="image" className="block mb-2 text-gray-800">
                Imagen (opcional)
              </Label>
              <div className="flex items-center gap-4">
                <Button
                  variant="outline"
                  className="w-full border-gray-300 text-gray-700 hover:text-blue-600 hover:border-blue-300"
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
                      onClick={() => handleSliderChange("image", [null as any])}
                      aria-label="Eliminar imagen"
                    >
                      ×
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 pt-4 mt-4">
            <Button 
              className="w-full bg-blue-600 hover:bg-blue-700 text-white" 
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
          </div>
        </Card>
      </div>

      <div className="lg:col-span-2">
        {previewGenerated ? (
          <Card className="p-4 sm:p-6 bg-white border border-gray-200 sticky top-4">
            <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-gray-900 flex items-center">
              <ImageIcon className="mr-2 h-5 w-5 text-blue-600" /> Vista Previa
            </h2>
            
            <div className="max-w-sm mx-auto mb-4">
              <PostPreview 
                formData={formData}
                imageUrl={previewUrl}
              />
            </div>
            
            <div className="flex flex-col sm:flex-row gap-2 sm:gap-4">
              <Button 
                className="w-full bg-blue-600 hover:bg-blue-700 text-white"
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
                className="w-full border-gray-300 text-gray-700 hover:text-blue-600 hover:border-blue-300"
                onClick={() =>
                  toast.info("Guardado", {
                    description: "La oferta laboral ha sido guardada como borrador.",
                    icon: <InfoIcon className="h-5 w-5" />
                  })
                }
              >
                Guardar
              </Button>
            </div>
          </Card>
        ) : (
          <div className="h-full flex items-center justify-center bg-gray-50 rounded-lg p-4 sm:p-6 border border-gray-200 sticky top-4">
            <div className="text-center">
              <ImageIcon className="h-12 sm:h-16 w-12 sm:w-16 mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-800">Vista previa no disponible</h3>
              <p className="text-gray-600 mt-2 text-sm sm:text-base">
                Complete el formulario y haga clic en "Generar Post" para ver la vista previa.
              </p>
            </div>
          </div>
        )}
      </div>

      {showConfirmation && <PublishConfirmation onConfirm={(publish) => confirmPublish(publish)} />}
    </div>
  )
}