<template>
  <div class="video-block">
    <videoCard ref="videoCardRef" :video-src="videoSrc" />
    <button
      class="play-button"
      v-if="!videoCardRef?.cameraActive"
      @click="videoCardRef?.activateCamera()"
    >
      A moi de jouer
    </button>
    <button class="play-button" v-else @click="videoCardRef?.stopCamera()">
      Revenir à la vidéo
    </button>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue"
import VideoCard from "./cards/videoCard.vue"

defineProps<{
  videoSrc: string
}>()

const videoCardRef = ref<InstanceType<typeof VideoCard> | null>(null)
</script>
<style scoped>
.video-block {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;

  .play-button {
    background-color: var(--color-darkpurple);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
  }
}
</style>
