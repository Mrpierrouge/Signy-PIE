<template>
  <div class="profile-container page-container">
    <div class="profile-header page-header">
      <TitleLogoBlock />
    </div>
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
          <BigButton type="primary" id="submit-button" @click="handleSubmit">
            Créer mon compte
          </BigButton>
          <BigButton
            type="secondary"
            id="login-button"
            @click="console.log('Navigating to login page...')"
          >
            J'ai déjà un compte
          </BigButton>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue"
import BigButton from "@/components/buttons/bigButton.vue"
import TitleLogoBlock from "@/components/titleLogoBlock.vue"
const form = reactive({
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  confirmPassword: "",
})

const errorMessage = ref("")
const successMessage = ref("")

function handleSubmit() {
  successMessage.value = ""

  if (form.password !== form.confirmPassword) {
    errorMessage.value = "Les mots de passe ne correspondent pas."
    return
  }

  errorMessage.value = ""
  successMessage.value = `Compte créé pour ${form.firstName} ${form.lastName} (démo, aucune donnée envoyée).`
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
</style>
