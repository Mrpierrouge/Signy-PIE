<template>
  <nav class="menu">
    <ul>
      <li>
        <RouterLink to="/home">
          <div class="menu-item home" :class="{ active: route.path === '/home' }"></div>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/lexique">
          <div class="menu-item lexique" :class="{ active: route.path === '/lexique' }"></div>
        </RouterLink>
      </li>
      <li>
        <RouterLink to="/profile">
          <div class="menu-item profile" :class="{ active: route.path === '/profile' }"></div>
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>
<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router"

const route = useRoute()
</script>
<style scoped>
.menu {
  position: fixed;
  bottom: -68px;
  display: flex;
  border-radius: 75px;
  background-color: var(--color-darkpurple);
  height: 122px;
  width: 100%;
  border: 1px solid black;
  ul {
    flex-grow: 1;
    display: flex;
    justify-content: space-around;
    padding: 0 20vw;
    list-style: none;
    .menu-item {
      width: 24px;
      height: 24px;
      mask-size: contain;
      background-color: black;
      &.home {
        mask-image: url("@/assets/icons/home.png");
      }
      &.profile {
        mask-image: url("@/assets/icons/user.png");
      }
      &.lexique {
        mask-image: url("@/assets/icons/book.png");
      }
      &.active {
        background-color: white;
      }
    }
  }
}
</style>
