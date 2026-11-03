import type { LoginCredentials, RegisterCredentials, User } from "@/types/auth"
import type { LessonWithWords } from "@/types/lesson"
import type { Word } from "@/types/word"

class API {
  readonly baseUrl: string

  constructor() {
    this.baseUrl = "http://localhost:8000"
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      credentials: "include",
    })

    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return undefined as T
    }

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const contentType = response.headers.get("content-type") ?? ""

    if (contentType.includes("application/json")) {
      return (await response.json()) as T
    }

    return undefined as T
  }

  async getLessons(): Promise<LessonWithWords[]> {
    return this.request<LessonWithWords[]>("/lessons")
  }

  async getLessonById(id: number): Promise<LessonWithWords> {
    return this.request<LessonWithWords>(`/lessons/${id}`)
  }

  async getWords(): Promise<Word[]> {
    return this.request<Word[]>("/words")
  }

  async getWordById(id: number): Promise<{ word: Word }> {
    return this.request<{ word: Word }>(`/words/${id}`)
  }

  // TODO: revert to `${this.baseUrl}${video}` once video files are served through the API
  getVideoUrl(video: string): string {
    return `backend${video}`
  }

  async tryWord(video: FormData): Promise<{ word: string; confidence: number | null }> {
    const response = await fetch(`${this.baseUrl}/ai/interrogate`, {
      method: "POST",
      body: video,
    })
    if (!response.ok) {
      throw new Error(`Failed to try word: ${response.statusText}`)
    }
    return response.json()
  }

  async login(credentials: LoginCredentials): Promise<User> {
    return this.request<User>("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })
  }

  async register(credentials: RegisterCredentials): Promise<User> {
    return this.request<User>("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    })
  }

  async loginWithGoogle(idToken: string): Promise<User> {
    return this.request<User>("/auth/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idToken }),
    })
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>("/auth/me")
  }

  async logout(): Promise<void> {
    await this.request<void>("/auth/logout", {
      method: "POST",
    })
  }
}

export const ApiClass = new API()
