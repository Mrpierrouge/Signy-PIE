<template>
  <div class="Menu">
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
<style scoped></style>
