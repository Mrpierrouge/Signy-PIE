<template>
  <div class="Signy-app">
    <div class="appLogo"></div>
    <div class="content">
      <RouterView />
    </div>
    <Menu />
  </div>
</template>
<script setup lang="ts">
import Menu from "./views/menu.vue"
</script>
<style scoped>
.Signy-app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--color-black);
}
.appLogo {
  width: 43px;
  height: 35px;
  margin-top: 2vh;
  mask-image: url("@/assets/icons/logo.png");
  mask-size: cover;
  background-color: var(--color-darkpurple);
}
.content {
  margin-top: 24px;
  margin-bottom: 110px;
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
