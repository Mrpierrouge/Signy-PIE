<template>
  <div>Lexique</div>
  <VideoBlock :video-src="franceVideo" />
  <VideoBlock :video-src="franceVideo2" />
</template>
<script setup lang="ts">
import VideoBlock from "@/components/videoBlock.vue"
import franceVideo from "@/assets/videos/france_nprop_10_1.mp4"
import franceVideo2 from "@/assets/videos/france_nprop_10_6.mp4"
</script>
<style scoped></style>
