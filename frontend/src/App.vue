<template>
  <div class="Signy-app">
    <!-- <div class="appLogo"></div> -->
    <div class="content">
      <RouterView />
    </div>
    <Menu />
    <InstallBanner />
  </div>
</template>
<script setup lang="ts">
import Menu from "./views/menu.vue"
import InstallBanner from "./components/installBanner.vue"
</script>
<style scoped>
.Signy-app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--color-lightyellow);
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
  margin-bottom: 110px;
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
<style>
.page-header {
  position: sticky;
  top: 0;
  z-index: 10;
  width: 100%;
  padding: 15px;
  padding-top: 5vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
