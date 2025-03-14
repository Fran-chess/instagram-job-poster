/**
 * Servicio API para interactuar con el backend FastAPI
 */

// Configuración base para la API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Token de autenticación
let authToken: string | null = null;

// Función para establecer el token de autenticación
export function setAuthToken(token: string) {
  authToken = token;
  // También lo guardamos en localStorage para persistencia
  if (typeof window !== 'undefined') {
    localStorage.setItem('authToken', token);
  }
}

// Función para obtener el token de autenticación
export function getAuthToken(): string | null {
  // Si no tenemos token en memoria, intentamos recuperarlo del localStorage
  if (!authToken && typeof window !== 'undefined') {
    authToken = localStorage.getItem('authToken');
  }
  return authToken;
}

// Función para limpiar el token (logout)
export function clearAuthToken() {
  authToken = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
  }
}

// Configuración básica para las solicitudes autenticadas
const getAuthHeaders = (): HeadersInit => {
  const token = getAuthToken();
  return token
    ? {
        Authorization: `Bearer ${token}`,
      }
    : {};
};

// Tipos de datos para la API
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Template {
  template_id: number;
  name: string;
  description?: string;
  background_color: string;
  text_color: string;
  footer_text?: string;
  is_active: boolean;
  image_url?: string;
}

export interface PostCreateRequest {
  template_id: number;
  job_title: string;
  location: string;
  email: string;
  requirements?: string;
  position_priority: number;
  location_priority: number;
  email_priority: number;
  requirements_priority: number;
}

export interface PostPreviewRequest {
  template_id: number;
  job_title: string;
  location: string;
  email: string;
  requirements?: string;
  position_priority: number;
  location_priority: number;
  email_priority: number;
  requirements_priority: number;
}

export interface PostScheduleRequest {
  scheduled_for: string; // ISO datetime string
  frequency?: string; // "once", "daily", "weekly", "monthly"
  recurrence_pattern?: string;
  end_date?: string; // ISO datetime string
}

export interface Post {
  post_id: number;
  template_id: number;
  job_title: string;
  location: string;
  email: string;
  requirements?: string;
  position_priority: number;
  location_priority: number;
  email_priority: number;
  requirements_priority: number;
  status: string;
  image_url?: string;
  instagram_post_id?: string;
  created_at: string;
  scheduled_for?: string;
  published_at?: string;
}

/**
 * Autenticación: Iniciar sesión
 */
export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  try {
    // Para el endpoint de login usamos x-www-form-urlencoded según la implementación del backend
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    const data = await response.json();
    
    // Guardar token para futuras peticiones
    setAuthToken(data.access_token);
    
    return data;
  } catch (error) {
    console.error('Error de autenticación:', error);
    throw error;
  }
}

/**
 * Obtener todas las plantillas disponibles
 */
export async function getTemplates(): Promise<Template[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/templates`, {
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al obtener plantillas:', error);
    throw error;
  }
}

/**
 * Generar vista previa de una publicación
 */
export async function generatePreview(data: PostPreviewRequest): Promise<{ image_url: string }> {
  try {
    // Construir la URL con los parámetros de consulta
    const url = new URL(`${API_BASE_URL}/posts/preview`);
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, value.toString());
      }
    });

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al generar vista previa:', error);
    throw error;
  }
}

/**
 * Crear una nueva publicación
 */
export async function createPost(data: PostCreateRequest): Promise<Post> {
  try {
    const response = await fetch(`${API_BASE_URL}/posts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al crear publicación:', error);
    throw error;
  }
}

/**
 * Publicar inmediatamente en Instagram
 */
export async function publishPost(postId: number): Promise<{ success: boolean; message: string; instagram_post_id?: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/publish`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al publicar en Instagram:', error);
    throw error;
  }
}

/**
 * Programar una publicación
 */
export async function schedulePost(postId: number, scheduleData: PostScheduleRequest): Promise<{ success: boolean; message: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(scheduleData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al programar la publicación:', error);
    throw error;
  }
}

/**
 * Obtener todas las publicaciones
 */
export async function getPosts(status?: string): Promise<Post[]> {
  try {
    const url = new URL(`${API_BASE_URL}/posts`);
    if (status) {
      url.searchParams.append('status', status);
    }

    const response = await fetch(url.toString(), {
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al obtener publicaciones:', error);
    throw error;
  }
}

/**
 * Obtener publicaciones programadas para próximos días
 */
export async function getUpcomingPosts(hours: number = 24): Promise<any[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/scheduler/upcoming?hours=${hours}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error al obtener publicaciones programadas:', error);
    throw error;
  }
}