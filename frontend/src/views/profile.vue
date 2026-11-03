<template>
  <div class="profile-container">
    <div v-if="authStore.isAuthenticated" class="profile-authenticated">
      <h1 class="title">Profil</h1>
      <p>TODO</p>
      <button type="button" class="submit-button" @click="handleLogout">Se déconnecter</button>
    </div>

    <div v-else class="auth-panel">
      <div class="mode-switch" role="tablist" aria-label="Choix d'authentification">
        <button
          type="button"
          class="switch-button"
          :class="{ active: mode === 'login' }"
          @click="mode = 'login'"
        >
          Connexion
        </button>
        <button
          type="button"
          class="switch-button"
          :class="{ active: mode === 'register' }"
          @click="mode = 'register'"
        >
          Créer un compte
        </button>
      </div>

      <h1 class="title">{{ mode === "login" ? "Connexion" : "Créer un compte" }}</h1>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div v-if="mode === 'register'" class="field-row">
          <div class="field">
            <label for="firstName">Prénom</label>
            <input id="firstName" v-model="form.firstName" type="text" required />
          </div>

          <div class="field">
            <label for="lastName">Nom</label>
            <input id="lastName" v-model="form.lastName" type="text" required />
          </div>
        </div>

        <div class="field">
          <label for="email">Email</label>
          <input id="email" v-model="form.email" type="email" required />
        </div>

        <div class="field">
          <label for="password">Mot de passe</label>
          <input id="password" v-model="form.password" type="password" required minlength="8" />
        </div>

        <div v-if="mode === 'register'" class="field">
          <label for="confirmPassword">Confirmer le mot de passe</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            minlength="8"
          />
        </div>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

        <button type="submit" class="submit-button" :disabled="authStore.isLoading">
          {{ mode === "login" ? "Se connecter" : "Créer mon compte" }}
        </button>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
defineOptions({
  name: "AccountProfile",
})

import { reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const mode = ref<"login" | "register">("login")

const form = reactive({
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  confirmPassword: "",
})

const errorMessage = ref("")
const successMessage = ref("")

async function handleSubmit() {
  successMessage.value = ""

  if (mode.value === "register" && form.password !== form.confirmPassword) {
    errorMessage.value = "Les mots de passe ne correspondent pas."
    return
  }

  try {
    errorMessage.value = ""

    if (mode.value === "login") {
      await authStore.login({ email: form.email, password: form.password })
      successMessage.value = "Connexion réussie."
    } else {
      await authStore.register({
        firstName: form.firstName,
        lastName: form.lastName,
        email: form.email,
        password: form.password,
      })
      successMessage.value = "Compte créé avec succès."
    }

    await router.push("/home")
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : mode.value === "login"
          ? "La connexion a échoué."
          : "L'inscription a échoué."
  }
}

async function handleLogout() {
  await authStore.logout()
}
</script>
<style scoped>
.profile-container {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 22px;
  font-weight: bold;
  color: var(--color-black);
  margin-bottom: 20px;
}

.auth-panel,
.profile-authenticated {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mode-switch {
  display: flex;
  width: 100%;
  background: var(--color-lightgray);
  border-radius: 10px;
  padding: 4px;
  gap: 4px;
  margin-bottom: 20px;
}

.switch-button {
  flex: 1;
  border: none;
  border-radius: 8px;
  padding: 10px 12px;
  background: transparent;
  color: var(--color-black);
  font-weight: bold;
  cursor: pointer;
}

.switch-button.active {
  background: var(--color-darkpurple);
  color: white;
}

.auth-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.field-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-size: 14px;
  font-weight: bold;
  color: var(--color-white);
}

input {
  background-color: var(--color-lightgray);
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--color-black);
}

input:focus {
  outline: 2px solid var(--color-darkpurple);
}

.error-message {
  color: #d43d3d;
  font-size: 14px;
  text-align: center;
}

.success-message {
  color: var(--color-darkpurple);
  font-size: 14px;
  text-align: center;
}

.submit-button {
  background-color: var(--color-darkpurple);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
}
</style>
