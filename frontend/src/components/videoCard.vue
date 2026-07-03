<template>
  <div class="card video-card">
    <video v-if="videoSrc" class="media" :src="videoSrc" controls playsinline />

    <template v-else>
      <video
        v-show="cameraActive"
        ref="cameraVideo"
        class="media mirrored"
        autoplay
        muted
        playsinline
      />

      <div v-if="!cameraActive" class="camera-prompt">
        <div class="text">
          {{ errorMessage || "Autoriser l'accès à la caméra" }}
        </div>
        <button class="camera-button" @click="requestCamera">Activer la caméra</button>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref, onBeforeUnmount } from "vue"

defineProps<{
  videoSrc?: string
}>()

const cameraVideo = ref<HTMLVideoElement | null>(null)
const cameraActive = ref(false)
const errorMessage = ref("")
let stream: MediaStream | null = null

async function requestCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (cameraVideo.value) {
      cameraVideo.value.srcObject = stream
    }
    cameraActive.value = true
    errorMessage.value = ""
  } catch {
    errorMessage.value = "Accès à la caméra refusé"
  }
}

function stopCamera() {
  stream?.getTracks().forEach((track) => track.stop())
  stream = null
  cameraActive.value = false
}

onBeforeUnmount(stopCamera)

defineExpose({ stopCamera })
</script>
<style scoped>
.video-card {
  background-color: var(--color-lightgray);
  width: 90%;
  aspect-ratio: 1 / 1;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;

  .media {
    width: 100%;
    height: 100%;
    object-fit: cover;
    &.mirrored {
      transform: scaleX(-1);
    }
  }

  .camera-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--color-black);
    padding: 20px;
    text-align: center;

    .camera-icon {
      width: 40px;
      height: 40px;
      color: var(--color-black);
    }

    .text {
      font-size: 14px;
    }

    .camera-button {
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
}
</style>
