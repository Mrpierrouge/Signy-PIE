export interface User {
  id: number
  email: string
  firstName: string
  lastName: string
  avatarUrl?: string | null
  provider: "email" | "google"
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  firstName: string
  lastName: string
  email: string
  password: string
}
