<template>
  <div class="menu">
    <nav>
      <ul>
        <li><RouterLink to="/home">Home</RouterLink></li>
        <li><RouterLink to="/lexique">Lexique</RouterLink></li>
        <li><RouterLink to="/profile">Profile</RouterLink></li>
      </ul>
    </nav>
  </div>
</template>
<script setup lang="ts">
import { RouterLink } from "vue-router"
</script>
<style scoped>
.menu {
  background-color: var(--color-darkpurple);
  height: 68px;
  width: 100%;
}
</style>
