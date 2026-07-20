import type { Lesson, LessonWithWords } from "@/types/lesson"
import type { Word } from "@/types/word"

class API {
  readonly baseUrl: string

  constructor() {
    this.baseUrl = "http://localhost:8000"
  }

  async getLessons(): Promise<LessonWithWords[]> {
    const response = await fetch(`${this.baseUrl}/lessons`)
    if (!response.ok) {
      throw new Error(`Failed to fetch lessons: ${response.statusText}`)
    }
    return response.json()
  }

  async getLessonById(id: number): Promise<LessonWithWords> {
    const response = await fetch(`${this.baseUrl}/lessons/${id}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch lesson with id ${id}: ${response.statusText}`)
    }
    return response.json()
  }

  async getWords(): Promise<Word[]> {
    const response = await fetch(`${this.baseUrl}/words`)
    if (!response.ok) {
      throw new Error(`Failed to fetch words: ${response.statusText}`)
    }
    return response.json()
  }

  async getWordById(id: number): Promise<{ word: Word }> {
    const response = await fetch(`${this.baseUrl}/words/${id}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch word with id ${id}: ${response.statusText}`)
    }
    return response.json()
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
}

export const ApiClass = new API()
