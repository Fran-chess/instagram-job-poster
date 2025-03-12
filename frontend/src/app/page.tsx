import { Suspense } from 'react';
import JobPostingForm from "@/components/job-posting-form"
import { Instagram, Calendar, History, Home, HelpCircle } from "lucide-react"
import { Toaster } from '@/components/ui/sonner';
import Image from 'next/image';

// Componente de carga para la suspense boundary
const Loading = () => (
  <div className="flex items-center justify-center min-h-[400px]">
    <div className="flex flex-col items-center">
      <div className="w-12 h-12 border-4 border-t-[#00cc99] border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
      <p className="mt-4 text-gray-600">Cargando...</p>
    </div>
  </div>
);

export default function HomePage() {
  // Función para manejar errores de imagen
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    e.currentTarget.src = "/placeholder.svg";
    e.currentTarget.alt = "DarSalud";
  };

  return (
    <main className="min-h-screen bg-gray-50 pb-12">
      <header className="bg-[#0066cc] text-white shadow-md">
        <div className="container mx-auto">
          <div className="flex items-center justify-between py-4 px-4 md:px-0">
            <div className="flex items-center gap-3">
              <div className="bg-white p-2 rounded-full">
                <Image 
                  src="/logo-darsalud.png" 
                  alt="DarSalud Logo" 
                  width={32}
                  height={32}
                  className="h-8 w-8"
                />
              </div>
              <h1 className="text-2xl font-bold">DarSalud</h1>
            </div>
            <nav className="hidden md:block">
              <ul className="flex space-x-6">
                <li>
                  <a href="#" className="flex items-center gap-2 hover:underline">
                    <Home className="h-4 w-4" />
                    <span>Inicio</span>
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center gap-2 hover:underline">
                    <Instagram className="h-4 w-4" />
                    <span>Publicaciones</span>
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center gap-2 hover:underline">
                    <Calendar className="h-4 w-4" />
                    <span>Programación</span>
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center gap-2 hover:underline">
                    <History className="h-4 w-4" />
                    <span>Historial</span>
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center gap-2 hover:underline">
                    <HelpCircle className="h-4 w-4" />
                    <span>Ayuda</span>
                  </a>
                </li>
              </ul>
            </nav>
            <button className="md:hidden text-white">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div className="bg-gradient-to-b from-[#0066cc]/10 to-transparent py-8">
        <div className="container mx-auto px-4 md:px-0">
          <div className="max-w-3xl mx-auto text-center mb-8">
            <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-4">
              Generador de Ofertas Laborales para Instagram
            </h1>
            <p className="text-gray-600">
              Crea y publica fácilmente ofertas de trabajo atractivas para aumentar el alcance de tus búsquedas laborales.
            </p>
          </div>
        </div>
      </div>
      
      <div className="container mx-auto px-4 md:px-0">
        <Suspense fallback={<Loading />}>
          <JobPostingForm />
        </Suspense>
      </div>
      
      <footer className="mt-16 bg-gray-100 border-t border-gray-200 py-6">
        <div className="container mx-auto px-4 md:px-0">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <span className="font-bold text-gray-700">DarSalud</span>
              <span className="text-gray-500 text-sm">© {new Date().getFullYear()}</span>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-600 hover:text-[#0066cc]">Términos y condiciones</a>
              <a href="#" className="text-gray-600 hover:text-[#0066cc]">Privacidad</a>
              <a href="#" className="text-gray-600 hover:text-[#0066cc]">Ayuda</a>
            </div>
          </div>
        </div>
      </footer>
      
      <Toaster />
    </main>
  )
}