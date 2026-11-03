import { computed, ref } from "vue"
import { defineStore } from "pinia"

import { ApiClass } from "@/api/api"
import type { LoginCredentials, RegisterCredentials, User } from "@/types/auth"

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => user.value !== null)

  async function login(credentials: LoginCredentials) {
    isLoading.value = true

    try {
      user.value = await ApiClass.login(credentials)
      return user.value
    } finally {
      isLoading.value = false
    }
  }

  async function register(credentials: RegisterCredentials) {
    isLoading.value = true

    try {
      user.value = await ApiClass.register(credentials)
      return user.value
    } finally {
      isLoading.value = false
    }
  }

  async function loginWithGoogle(idToken: string) {
    isLoading.value = true

    try {
      user.value = await ApiClass.loginWithGoogle(idToken)
      return user.value
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    try {
      await ApiClass.logout()
    } finally {
      user.value = null
    }
  }

  async function initializeAuth() {
    if (initialized.value) {
      return
    }

    isLoading.value = true

    try {
      user.value = await ApiClass.getCurrentUser()
    } catch {
      user.value = null
    } finally {
      isLoading.value = false
      initialized.value = true
    }
  }

  return {
    user,
    isLoading,
    initialized,
    isAuthenticated,
    login,
    register,
    loginWithGoogle,
    logout,
    initializeAuth,
  }
})
