"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Instagram, Clock, Calendar, Save, Check as CheckIcon, Loader2 } from "lucide-react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"

interface PublishConfirmationProps {
  onConfirm: (publish: boolean) => void;
}

export default function PublishConfirmation({ onConfirm }: PublishConfirmationProps) {
  const [publishOption, setPublishOption] = useState<"now" | "later" | "save">("now");
  const [scheduleDate, setScheduleDate] = useState(() => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  });
  const [scheduleTime, setScheduleTime] = useState<string>("12:00");
  const [isPublishing, setIsPublishing] = useState<boolean>(false);

  const handleConfirm = () => {
    if (publishOption === "now") {
      setIsPublishing(true);
      // Simular publicación después de 2 segundos
      setTimeout(() => {
        onConfirm(true);
        setIsPublishing(false);
      }, 2000);
    } else {
      onConfirm(true);
    }
  };

  return (
    <Dialog open={true} onOpenChange={() => onConfirm(false)}>
      <DialogContent className="sm:max-w-md bg-white">
        <DialogHeader>
          <DialogTitle className="text-gray-900">Opciones de Publicación</DialogTitle>
          <DialogDescription className="text-gray-600">
            Elija cómo desea proceder con esta oferta laboral.
          </DialogDescription>
        </DialogHeader>
        
        <div className="py-4">
          <RadioGroup 
            value={publishOption} 
            onValueChange={(value) => setPublishOption(value as "now" | "later" | "save")}
            className="space-y-4"
          >
            <div className="flex items-center space-x-2 rounded-md border border-gray-200 p-3 hover:bg-gray-50">
              <RadioGroupItem value="now" id="option-now" className="text-blue-600" />
              <Label htmlFor="option-now" className="flex flex-1 items-center gap-2 cursor-pointer">
                <Instagram className="h-4 w-4 text-blue-600" />
                <div className="flex-1">
                  <p className="font-medium text-gray-800">Publicar ahora</p>
                  <p className="text-sm text-gray-600">La imagen será compartida inmediatamente en Instagram</p>
                </div>
              </Label>
            </div>
            
            <div className="flex items-start space-x-2 rounded-md border border-gray-200 p-3 hover:bg-gray-50">
              <RadioGroupItem value="later" id="option-later" className="mt-1 text-blue-600" />
              <Label htmlFor="option-later" className="flex flex-1 flex-col gap-2 cursor-pointer">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-blue-600" />
                  <div>
                    <p className="font-medium text-gray-800">Programar publicación</p>
                    <p className="text-sm text-gray-600">Establecer fecha y hora para publicar</p>
                  </div>
                </div>
                
                {publishOption === "later" && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-2 pl-6">
                    <div>
                      <Label htmlFor="schedule-date" className="text-xs text-gray-600">Fecha</Label>
                      <div className="flex items-center border border-gray-200 rounded-md mt-1 bg-white">
                        <Calendar className="h-4 w-4 text-gray-500 ml-2" />
                        <input
                          type="date"
                          id="schedule-date"
                          className="flex-1 p-2 focus:outline-none text-sm text-gray-800 bg-transparent"
                          value={scheduleDate}
                          onChange={(e) => setScheduleDate(e.target.value)}
                          min={new Date().toISOString().split('T')[0]}
                        />
                      </div>
                    </div>
                    <div>
                      <Label htmlFor="schedule-time" className="text-xs text-gray-600">Hora</Label>
                      <div className="flex items-center border border-gray-200 rounded-md mt-1 bg-white">
                        <Clock className="h-4 w-4 text-gray-500 ml-2" />
                        <input
                          type="time"
                          id="schedule-time"
                          className="flex-1 p-2 focus:outline-none text-sm text-gray-800 bg-transparent"
                          value={scheduleTime}
                          onChange={(e) => setScheduleTime(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                )}
              </Label>
            </div>
            
            <div className="flex items-center space-x-2 rounded-md border border-gray-200 p-3 hover:bg-gray-50">
              <RadioGroupItem value="save" id="option-save" className="text-blue-600" />
              <Label htmlFor="option-save" className="flex flex-1 items-center gap-2 cursor-pointer">
                <Save className="h-4 w-4 text-blue-600" />
                <div className="flex-1">
                  <p className="font-medium text-gray-800">Guardar como borrador</p>
                  <p className="text-sm text-gray-600">Guardar para editar y publicar más tarde</p>
                </div>
              </Label>
            </div>
          </RadioGroup>
        </div>
        
        <DialogFooter className="flex justify-end gap-2">
          <Button 
            variant="outline" 
            className="border-gray-300 text-gray-700 hover:text-blue-600 hover:border-blue-300"
            onClick={() => onConfirm(false)}
          >
            Cancelar
          </Button>
          <Button 
            className="bg-blue-600 hover:bg-blue-700 text-white" 
            onClick={handleConfirm}
            disabled={isPublishing}
          >
            {isPublishing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Publicando...
              </>
            ) : (
              publishOption === "now" ? "Publicar ahora" : 
              publishOption === "later" ? "Programar" : "Guardar como borrador"
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}