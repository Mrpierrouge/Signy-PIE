<template>
  <div class="profile-container page-container">
    <div class="profile-header page-header">
      <TitleLogoBlock />
    </div>

    <template v-if="authStore.user">
      <h2 class="profile-title">Bonjour {{ authStore.user.firstName }} !</h2>

      <div class="content-container">
        <div class="profile-authenticated">
          <p class="profile-email">{{ authStore.user.email }}</p>
          <BigButton type="secondary" @click="handleLogout">Se déconnecter</BigButton>
        </div>
      </div>
    </template>

    <template v-else>
      <h2 class="profile-title">Créer un compte</h2>

      <div class="content-container">
        <form class="signup-form" @submit.prevent="handleSubmit">
          <div class="field">
            <label for="firstName">Prénom</label>
            <input id="firstName" v-model="form.firstName" type="text" required />
          </div>

          <div class="field">
            <label for="lastName">Nom</label>
            <input id="lastName" v-model="form.lastName" type="text" required />
          </div>

          <div class="field">
            <label for="email">Email</label>
            <input id="email" v-model="form.email" type="email" required />
          </div>

          <div class="field">
            <label for="password">Mot de passe</label>
            <input id="password" v-model="form.password" type="password" required minlength="8" />
          </div>

          <div class="field">
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
          <div class="buttons">
            <!-- native-type="submit": the browser checks the fields, then the form calls handleSubmit -->
            <BigButton type="primary" native-type="submit">
              {{ authStore.isLoading ? "Création..." : "Créer mon compte" }}
            </BigButton>
            <BigButton type="secondary" @click="goToLogin">J'ai déjà un compte</BigButton>
          </div>
        </form>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import BigButton from "@/components/buttons/bigButton.vue"
import TitleLogoBlock from "@/components/titleLogoBlock.vue"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

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

  if (form.password !== form.confirmPassword) {
    errorMessage.value = "Les mots de passe ne correspondent pas."
    return
  }

  errorMessage.value = ""
  try {
    // On success the user is logged in and the page switches to the logged-in view
    await authStore.register({
      firstName: form.firstName,
      lastName: form.lastName,
      email: form.email,
      password: form.password,
    })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Impossible de créer le compte."
  }
}

async function handleLogout() {
  await authStore.logout()
  successMessage.value = "Vous êtes déconnecté."
}

function goToLogin() {
  void router.push({ name: "login" })
}
</script>
<style scoped>
.profile-title {
  position: relative;
  z-index: 2;
  flex-shrink: 0;
  margin-bottom: 20px;
  background: var(--color-lightyellow);
}

.signup-form {
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

  .success-message {
    color: var(--color-darkpurple);
    font-size: 14px;
    text-align: center;
  }

  .buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }
}

.profile-authenticated {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.profile-email {
  color: var(--color-darkpurple);
  font-size: var(--font-size-body);
}
</style>
