<template>
  <div class="login-container page-container">
    <div class="login-header page-header">
      <TitleLogoBlock />
    </div>
    <h2 class="login-title">Connexion</h2>

    <div class="content-container">
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

        <div class="buttons">
          <!-- native-type="submit": the browser checks the fields, then the form calls handleSubmit -->
          <BigButton type="primary" native-type="submit">
            {{ authStore.isLoading ? "Connexion..." : "Se connecter" }}
          </BigButton>
          <BigButton type="secondary" @click="goToSignUp">Créer un compte</BigButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import BigButton from "@/components/buttons/bigButton.vue"
import TitleLogoBlock from "@/components/titleLogoBlock.vue"
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
    await router.push({ name: "profile" })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Identifiants invalides."
  }
}

function goToSignUp() {
  void router.push({ name: "profile" })
}
</script>

<style scoped>
.login-title {
  position: relative;
  z-index: 2;
  flex-shrink: 0;
  margin-bottom: 20px;
  background: var(--color-lightyellow);
}

.login-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 15px;

  .field {
    display: flex;
    flex-direction: column;
    gap: 5px;

    label {
      font-size: var(--font-size-h);
      font-weight: bold;
      color: var(--color-darkpurple);
    }
  }

  .error-message {
    color: #d43d3d;
    font-size: 14px;
    text-align: center;
  }

  .buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }
}
</style>
