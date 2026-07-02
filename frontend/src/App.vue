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
}
.appLogo {
  /* from 172 */
  width: 43px;
  /* from 140 */
  position: absolute;
  top: 2vh;
  height: 35px;
  mask-image: url("@/assets/logo.png");
  mask-size: cover;
  background-color: var(--color-darkpurple);
}
.content {
  margin-top: 70px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
