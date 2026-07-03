<template>
  <div class="card video-card">
    <video
      v-show="cameraActive"
      ref="cameraVideo"
      class="media mirrored"
      autoplay
      muted
      playsinline
    />
    <video v-if="!cameraActive" class="media" :src="videoSrc" controls playsinline />

    <div v-if="errorMessage" class="camera-error">{{ errorMessage }}</div>
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

async function activateCamera() {
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

defineExpose({ activateCamera, stopCamera, cameraActive })
</script>
<style scoped>
.video-card {
  background-color: var(--color-lightgray);
  width: 100%;
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

  .camera-error {
    position: absolute;
    bottom: 12px;
    left: 12px;
    right: 12px;
    background-color: rgba(17, 0, 3, 0.7);
    color: white;
    font-size: 13px;
    text-align: center;
    padding: 6px 10px;
    border-radius: 10px;
  }
}
</style>
