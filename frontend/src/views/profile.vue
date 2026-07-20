<template>
  <div class="profile-container">
    <h1 class="title">Créer un compte</h1>

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

      <button type="submit" class="submit-button">Créer mon compte</button>
    </form>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue"

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
.profile-container {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;

  .title {
    font-size: 22px;
    font-weight: bold;
    color: var(--color-black);
    margin-bottom: 20px;
  }
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
      font-size: 14px;
      font-weight: bold;
      color: var(--color-black);
    }

    input {
      background-color: var(--color-lightgray);
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      font-size: 14px;
      color: var(--color-black);
      &:focus {
        outline: 2px solid var(--color-darkpurple);
      }
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
}
</style>
