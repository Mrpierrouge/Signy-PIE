<template>
  <div class="Signy-app">
    <div class="content">
      <RouterView />
    </div>
  </div>
  <Menu />
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
</style>
