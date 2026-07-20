<template>
  <div class="video-block">
    <h2 class="word-title">{{ word.string }}</h2>
    <videoCard ref="videoCardRef" :video-src="videoSrc" @recording-ready="onRecordingReady" />
    <button
      class="play-button"
      v-if="!videoCardRef?.cameraActive"
      @click="videoCardRef?.activateCamera()"
    >
      A moi de jouer
    </button>
    <template v-else>
      <button class="play-button" @click="videoCardRef?.stopCamera()">Revenir à la vidéo</button>
      <button
        class="play-button"
        v-if="!videoCardRef?.isRecording"
        @click="videoCardRef?.startRecording()"
      >
        Démarrer l'enregistrement
      </button>
      <button class="play-button stop-button" v-else @click="videoCardRef?.stopRecording()">
        Arrêter l'enregistrement
      </button>
    </template>

    <div v-if="isChecking" class="ai-result checking">Analyse en cours...</div>
    <div v-else-if="aiError" class="ai-result error">{{ aiError }}</div>
    <div v-else-if="aiResult" class="ai-result">
      L'IA a reconnu : <strong>{{ aiResult.word }}</strong>
      <span v-if="aiResult.confidence !== null">
        ({{ (aiResult.confidence * 100).toFixed(0) }}%)
      </span>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue"
import VideoCard from "./cards/videoCard.vue"
import { ApiClass } from "@/api/api.ts"

defineProps<{
  videoSrc: string
  word: {
    string: string
    video: string
  }
}>()

const videoCardRef = ref<InstanceType<typeof VideoCard> | null>(null)
const isChecking = ref(false)
const aiResult = ref<{ word: string; confidence: number | null } | null>(null)
const aiError = ref("")

async function onRecordingReady(blob: Blob) {
  const formData = new FormData()
  formData.append("video", blob, "recording.npy")

  aiResult.value = null
  aiError.value = ""
  isChecking.value = true
  try {
    aiResult.value = await ApiClass.tryWord(formData)
  } catch {
    aiError.value = "Impossible d'analyser l'enregistrement"
  } finally {
    isChecking.value = false
  }
}
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

    &.stop-button {
      background-color: #d43d3d;
    }
  }
  .word-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--color-black);
  }

  .ai-result {
    background-color: var(--color-lightgray);
    color: var(--color-black);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 14px;
    text-align: center;

    &.checking {
      font-style: italic;
      opacity: 0.7;
    }

    &.error {
      background-color: #d43d3d;
      color: white;
    }
  }
}
</style>
