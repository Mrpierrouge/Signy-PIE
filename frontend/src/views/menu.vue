<template>
  <nav class="menu">
    <RouterLink to="/home" class="menu-item" :class="{ active: route.path === '/home' }">
      <div class="icon home" />
      <span>Accueil</span>
    </RouterLink>
    <RouterLink to="/lexique" class="menu-item" :class="{ active: route.path === '/lexique' }">
      <div class="icon lexique" />
      <span>Dictionnaire</span>
    </RouterLink>
    <RouterLink to="/profile" class="menu-item" :class="{ active: route.path === '/profile' }">
      <div class="icon profile" />
      <span>Mon compte</span>
    </RouterLink>
  </nav>
</template>
<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router"

const route = useRoute()
</script>
<style scoped>
.menu {
  z-index: 2;
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 8px;
  background-color: var(--color-lightyellow);
  border-radius: 75px 75px 0px 0px;
  border: 1px solid var(--color-darkpurple);
  width: 110%;
  max-width: 400px;
  padding: 14px 12px;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 67px;
  color: black;
  text-decoration: none;
  font-family: var(--font-family);
  font-size: var(--font-size-small);
}

.menu-item.active {
  color: var(--color-purple);
}

.menu-item .icon {
  width: 25px;
  height: 25px;
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  background-color: currentColor;
}

.menu-item .icon.home {
  mask-image: url("@/assets/icons/home.png");
}
.menu-item .icon.profile {
  mask-image: url("@/assets/icons/user.png");
}
.menu-item .icon.lexique {
  mask-image: url("@/assets/icons/book.png");
}
</style>
