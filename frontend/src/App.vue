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
  justify-content: flex-start;
  height: 100dvh;
  min-height: 100dvh;
  background-color: var(--color-lightyellow);
  overflow: hidden;
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
  flex: 1;
  min-height: 0;
  width: 100%;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
  margin-bottom: 110px;
}
</style>
<style>
.page-header {
  position: sticky;
  top: 0;
  z-index: 10;
  width: 100%;
  padding-top: 5vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-lightyellow);
  margin-bottom: 5vh;
}
input {
  background-color: var(--color-lightyellow);
  border: 1px solid var(--color-darkpurple);
  border-radius: 8px;
  padding: 10px;
  font-family: var(--font-family);
  font-size: var(--font-size-body);
  color: var(--color-darkpurple);
}
h2 {
  font-family: var(--font-family);
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-bold);
  color: var(--color-darkpurple);
}
.page-container {
  width: 90%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}
.content-container {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior-y: contain;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
</style>
