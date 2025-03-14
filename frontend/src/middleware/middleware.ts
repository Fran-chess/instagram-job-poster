// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Rutas que no requieren autenticación
const publicRoutes = [
  '/login',
  '/api/', // Para las llamadas API
  '/_next/', // Para recursos de Next.js
  '/favicon.ico',
]

export function middleware(request: NextRequest) {
  // Verificar si es ruta pública
  const isPublicRoute = publicRoutes.some(route => 
    request.nextUrl.pathname.startsWith(route)
  )
  
  // Si es ruta pública, continuar normalmente
  if (isPublicRoute) {
    return NextResponse.next()
  }
  
  // Verificar si hay token de autenticación
  const authToken = request.cookies.get('authToken')?.value || 
                   request.headers.get('Authorization')?.replace('Bearer ', '')
  
  // Si no hay token, redirigir a login
  if (!authToken) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', request.nextUrl.pathname)
    return NextResponse.redirect(loginUrl)
  }
  
  // Si hay token, continuar con la solicitud
  return NextResponse.next()
}

// Configurar rutas a las que se aplica el middleware
export const config = {
  matcher: [
    /*
     * Excepciones:
     * - api routes (/_next/*)
     * - static files (/public/*)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}