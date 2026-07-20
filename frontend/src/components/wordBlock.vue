<template>
  <div class="word-block">
    <div class="word-title">{{ word.string }}</div>
    <VideoCard :video-src="videoSrc" />
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue"
import VideoCard from "./cards/videoCard.vue"
import { ApiClass } from "@/api/api"
import type { Word } from "@/types/word"

const props = defineProps<{
  word: Word
}>()

const videoSrc = computed(() => ApiClass.getVideoUrl(props.word.video))
</script>
<style scoped>
.word-block {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 3px solid var(--color-lightblue);
  border-radius: 20px;

  .word-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--color-white);
  }
}
</style>
