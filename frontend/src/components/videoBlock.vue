<template>
  <div class="video-block">
    <videoCard
      ref="videoCardRef"
      :video-src="videoSrc"
      @recording-ready="onRecordingReady"
    />
    <button
      class="play-button"
      v-if="!videoCardRef?.cameraActive"
      @click="videoCardRef?.activateCamera()"
    >
      A moi de jouer
    </button>
    <template v-else>
      <button class="play-button" @click="videoCardRef?.stopCamera()">
        Revenir à la vidéo
      </button>
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
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue"
import VideoCard from "./cards/videoCard.vue"

defineProps<{
  videoSrc: string
}>()

const videoCardRef = ref<InstanceType<typeof VideoCard> | null>(null)

async function onRecordingReady(blob: Blob) {
  const formData = new FormData()
  formData.append("recording", blob, "recording.webm")

  try {
    // TODO: adapter l'URL une fois le backend disponible
    await fetch("/api/recordings", {
      method: "POST",
      body: formData,
    })
  } catch (error) {
    console.error("Échec de l'envoi de l'enregistrement", error)
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
}
</style>
