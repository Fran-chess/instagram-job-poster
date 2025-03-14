"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { Toaster } from 'sonner'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Loader2, AlertCircle } from "lucide-react"
import { login } from '@/services/api'
import Image from 'next/image'

export default function LoginPage() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!username || !password) {
      toast.error("Error de validación", {
        description: "Usuario y contraseña son obligatorios",
        icon: <AlertCircle className="h-5 w-5" />
      })
      return
    }
    
    setIsLoading(true)
    
    try {
      await login({
        username,
        password
      })
      
      // Si llega aquí, la autenticación fue exitosa
      toast.success("Inicio de sesión exitoso", {
        description: "Redirigiendo al panel principal...",
      })
      
      // Redirigir al dashboard después de un breve retraso
      setTimeout(() => {
        router.push('/')
      }, 1000)
      
    } catch (error) {
      let errorMessage = "Error al iniciar sesión"
      
      if (error instanceof Error) {
        errorMessage = error.message
      }
      
      toast.error("Error de autenticación", {
        description: errorMessage,
        icon: <AlertCircle className="h-5 w-5" />
      })
      
      setIsLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4">
      <div className="mb-8">
        <div className="flex items-center space-x-2">
          <div className="bg-white p-2 rounded-full shadow-md">
            <Image 
              src="/logo-darsalud.png" 
              alt="DarSalud Logo" 
              width={48}
              height={48}
              className="h-12 w-12"
            />
          </div>
          <h1 className="text-3xl font-bold text-[#0066cc]">DarSalud</h1>
        </div>
      </div>
      
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center text-2xl">Iniciar Sesión</CardTitle>
          <CardDescription className="text-center">
            Accede al sistema de publicación en Instagram
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Usuario</Label>
              <Input 
                id="username" 
                placeholder="Ingresa tu nombre de usuario" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={isLoading}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Contraseña</Label>
              <Input 
                id="password" 
                type="password" 
                placeholder="Ingresa tu contraseña" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
                required
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button 
              type="submit" 
              className="w-full bg-[#0066cc] hover:bg-[#0055bb]"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Ingresando...
                </>
              ) : (
                'Iniciar Sesión'
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>
      
      <p className="mt-8 text-center text-sm text-gray-600">
        Contacta con el administrador si tienes problemas para acceder.
      </p>
      
      <Toaster richColors position="top-center" />
    </div>
  )
}