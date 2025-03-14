import { Suspense } from 'react';
import JobPostingForm from "@/components/job-posting-form"
import { Instagram, Calendar, History, Home, HelpCircle } from "lucide-react"
import { Toaster } from '@/components/ui/sonner';
import Image from 'next/image';

// Componente de carga para la suspense boundary
const Loading = () => (
  <div className="flex items-center justify-center min-h-[400px]">
    <div className="flex flex-col items-center">
      <div className="w-12 h-12 border-4 border-t-blue-500 border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
      <p className="mt-4 text-gray-700">Cargando...</p>
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
    <main className="min-h-screen bg-white pb-12">
      <div className="container mx-auto max-w-5xl">
        {/* Título centrado */}
        <div className="bg-gray-100 py-4 text-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Creador de Ofertas Laborales
          </h1>
        </div>
        
        {/* Barra de navegación */}
        <nav className="bg-white py-3 border-b border-gray-200">
          <ul className="flex justify-center space-x-8 md:space-x-12">
            <li>
              <a href="#" className="flex items-center gap-2 hover:text-blue-600 transition-colors font-medium">
                <Home className="h-5 w-5" />
                <span>Inicio</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center gap-2 hover:text-blue-600 transition-colors">
                <Instagram className="h-4 w-4" />
                <span>Publicaciones</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center gap-2 hover:text-blue-600 transition-colors">
                <Calendar className="h-4 w-4" />
                <span>Programación</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center gap-2 hover:text-blue-600 transition-colors">
                <History className="h-4 w-4" />
                <span>Historial</span>
              </a>
            </li>
          </ul>
          
          {/* Menú móvil */}
          <div className="md:hidden flex justify-center mt-4">
            <button className="text-gray-800 p-2 border border-gray-300 rounded-md group relative">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
              </svg>
              <div className="hidden group-focus-within:block absolute left-0 right-0 mt-2 bg-white rounded-md shadow-lg z-10 w-48 mx-auto">
                <div className="py-1">
                  <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100 flex items-center gap-2">
                    <Home className="h-4 w-4" />
                    <span>Inicio</span>
                  </a>
                  <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100 flex items-center gap-2">
                    <Instagram className="h-4 w-4" />
                    <span>Publicaciones</span>
                  </a>
                  <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100 flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    <span>Programación</span>
                  </a>
                  <a href="#" className="block px-4 py-2 text-gray-800 hover:bg-gray-100 flex items-center gap-2">
                    <History className="h-4 w-4" />
                    <span>Historial</span>
                  </a>
                </div>
              </div>
            </button>
          </div>
        </nav>
        
        <div className="px-4 md:px-6 mt-6">
          <Suspense fallback={<Loading />}>
            <JobPostingForm />
          </Suspense>
        </div>
        
        <footer className="mt-12 bg-gray-50 border-t border-gray-200 py-4">
          <div className="px-4 md:px-6">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="flex items-center gap-2 mb-4 md:mb-0">
                <span className="font-bold text-gray-900">DarSalud</span>
                <span className="text-gray-600 text-sm">© {new Date().getFullYear()}</span>
              </div>
              <div className="flex flex-wrap gap-4 justify-center">
                <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Términos y condiciones</a>
                <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Privacidad</a>
                <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors flex items-center gap-1">
                  <HelpCircle className="h-4 w-4" />
                  <span>Ayuda</span>
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
      
      <Toaster />
    </main>
  )
}