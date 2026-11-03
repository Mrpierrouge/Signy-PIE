<template>
  <div class="login-container">
    <h1 class="title">Connexion</h1>

    <form class="login-form" @submit.prevent="handleSubmit">
      <div class="field">
        <label for="email">Email</label>
        <input id="email" v-model="email" type="email" required />
      </div>

      <div class="field">
        <label for="password">Mot de passe</label>
        <input id="password" v-model="password" type="password" required />
      </div>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <button type="submit" class="submit-button" :disabled="authStore.isLoading">
        {{ authStore.isLoading ? "Connexion..." : "Se connecter" }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "LoginPage",
})

import { ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const email = ref("")
const password = ref("")
const errorMessage = ref("")

async function handleSubmit() {
  errorMessage.value = ""

  try {
    await authStore.login({ email: email.value, password: password.value })
    await router.push("/home")
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Identifiants invalides."
  }
}
</script>

<style scoped>
.login-container {
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

.login-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;
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
