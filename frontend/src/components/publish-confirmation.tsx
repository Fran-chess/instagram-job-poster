"use client"

import { memo, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Instagram, Save, Clock, Calendar } from "lucide-react"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"

interface PublishConfirmationProps {
  onConfirm: (publish: boolean, scheduleTime?: Date) => void
}

const PublishConfirmation = memo(function PublishConfirmation({ onConfirm }: PublishConfirmationProps) {
  const [publishOption, setPublishOption] = useState<"now" | "later" | "save">("now");
  const [scheduleDate, setScheduleDate] = useState<string>(() => {
    // Establecer la fecha a mañana por defecto
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  });
  const [scheduleTime, setScheduleTime] = useState<string>("12:00");

  const handleConfirm = () => {
    if (publishOption === "save") {
      onConfirm(false);
      return;
    }

    if (publishOption === "later") {
      const scheduledDateTime = new Date(`${scheduleDate}T${scheduleTime}`);
      onConfirm(true, scheduledDateTime);
      return;
    }

    // Publicar ahora
    onConfirm(true);
  };

  return (
    <Dialog open={true} onOpenChange={() => onConfirm(false)}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Opciones de Publicación</DialogTitle>
          <DialogDescription>
            Elija cómo desea proceder con esta oferta laboral.
          </DialogDescription>
        </DialogHeader>
        
        <div className="py-4">
          <RadioGroup 
            value={publishOption} 
            onValueChange={(value) => setPublishOption(value as "now" | "later" | "save")}
            className="space-y-4"
          >
            <div className="flex items-center space-x-2 rounded-md border p-3 hover:bg-gray-50">
              <RadioGroupItem value="now" id="option-now" />
              <Label htmlFor="option-now" className="flex flex-1 items-center gap-2 cursor-pointer">
                <Instagram className="h-4 w-4 text-[#0066cc]" />
                <div className="flex-1">
                  <p className="font-medium">Publicar ahora</p>
                  <p className="text-sm text-gray-500">La imagen será compartida inmediatamente en Instagram</p>
                </div>
              </Label>
            </div>
            
            <div className="flex items-start space-x-2 rounded-md border p-3 hover:bg-gray-50">
              <RadioGroupItem value="later" id="option-later" className="mt-1" />
              <Label htmlFor="option-later" className="flex flex-1 flex-col gap-2 cursor-pointer">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-[#0066cc]" />
                  <div>
                    <p className="font-medium">Programar publicación</p>
                    <p className="text-sm text-gray-500">Establecer fecha y hora para publicar</p>
                  </div>
                </div>
                
                {publishOption === "later" && (
                  <div className="grid grid-cols-2 gap-4 mt-2 pl-6">
                    <div>
                      <Label htmlFor="schedule-date" className="text-xs text-gray-500">Fecha</Label>
                      <div className="flex items-center border rounded-md mt-1">
                        <Calendar className="h-4 w-4 text-gray-500 ml-2" />
                        <input
                          type="date"
                          id="schedule-date"
                          className="flex-1 p-2 focus:outline-none text-sm"
                          value={scheduleDate}
                          onChange={(e) => setScheduleDate(e.target.value)}
                          min={new Date().toISOString().split('T')[0]}
                        />
                      </div>
                    </div>
                    <div>
                      <Label htmlFor="schedule-time" className="text-xs text-gray-500">Hora</Label>
                      <div className="flex items-center border rounded-md mt-1">
                        <Clock className="h-4 w-4 text-gray-500 ml-2" />
                        <input
                          type="time"
                          id="schedule-time"
                          className="flex-1 p-2 focus:outline-none text-sm"
                          value={scheduleTime}
                          onChange={(e) => setScheduleTime(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                )}
              </Label>
            </div>
            
            <div className="flex items-center space-x-2 rounded-md border p-3 hover:bg-gray-50">
              <RadioGroupItem value="save" id="option-save" />
              <Label htmlFor="option-save" className="flex flex-1 items-center gap-2 cursor-pointer">
                <Save className="h-4 w-4 text-[#0066cc]" />
                <div className="flex-1">
                  <p className="font-medium">Guardar como borrador</p>
                  <p className="text-sm text-gray-500">Guardar para editar y publicar más tarde</p>
                </div>
              </Label>
            </div>
          </RadioGroup>
        </div>
        
        <DialogFooter className="flex justify-end gap-2">
          <Button 
            variant="outline" 
            onClick={() => onConfirm(false)}
          >
            Cancelar
          </Button>
          <Button 
            className="bg-[#0066cc] hover:bg-[#0055bb]" 
            onClick={handleConfirm}
          >
            {publishOption === "now" ? "Publicar ahora" : 
             publishOption === "later" ? "Programar" : "Guardar como borrador"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
});

export default PublishConfirmation;