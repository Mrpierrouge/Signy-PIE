<template>
  <div class="card video-card" :style="{ aspectRatio }">
    <video
      v-show="cameraActive"
      ref="cameraVideo"
      class="media mirrored"
      autoplay
      muted
      playsinline
    />
    <video
      v-if="!cameraActive"
      ref="sourceVideo"
      class="media"
      :src="videoSrc"
      controls
      playsinline
      @loadedmetadata="onSourceLoaded"
    />

    <div v-if="isRecording" class="recording-indicator">● REC</div>
    <div v-if="errorMessage" class="camera-error">{{ errorMessage }}</div>
  </div>
</template>
<script setup lang="ts">
import { ref, onBeforeUnmount, watch } from "vue"
import { detectFrame, FEATURE_SIZE, normalizeSequence, preloadHolisticExtractor } from "@/lib/holisticExtractor"
import { encodeNpyFloat32 } from "@/lib/npy"

const props = defineProps<{
  videoSrc?: string
}>()

const emit = defineEmits<{
  "recording-ready": [blob: Blob]
}>()

const cameraVideo = ref<HTMLVideoElement | null>(null)
const sourceVideo = ref<HTMLVideoElement | null>(null)
const cameraActive = ref(false)
const isRecording = ref(false)
const errorMessage = ref("")
const aspectRatio = ref("1 / 1")
let stream: MediaStream | null = null

// Frames are captured at ~15fps by extracting MediaPipe Holistic keypoints
// live off the camera feed, instead of encoding a video file — the backend
// AI model expects a keypoint sequence, not raw video.
const CAPTURE_INTERVAL_MS = 1000 / 15
let capturedFrames: Float32Array[] = []
let captureTimer: ReturnType<typeof setTimeout> | null = null

function onSourceLoaded() {
  if (sourceVideo.value) {
    aspectRatio.value = `${sourceVideo.value.videoWidth} / ${sourceVideo.value.videoHeight}`
  }
}

// Changing the `src` attribute on an existing <video> element doesn't make the
// browser pick up the new source on its own — it needs an explicit reload.
watch(
  () => props.videoSrc,
  () => {
    sourceVideo.value?.load()
  },
  { flush: "post" },
)

async function activateCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (cameraVideo.value) {
      cameraVideo.value.srcObject = stream
    }
    cameraActive.value = true
    errorMessage.value = ""
    // Warm up the landmarker now so the first recording isn't stalled
    // waiting for the WASM runtime + model to load.
    preloadHolisticExtractor()
  } catch {
    errorMessage.value = "Accès à la caméra refusé"
  }
}

function stopCamera() {
  stopRecording()
  stream?.getTracks().forEach((track) => track.stop())
  stream = null
  cameraActive.value = false
}

async function captureTick() {
  if (!isRecording.value || !cameraVideo.value) return
  const features = await detectFrame(cameraVideo.value, performance.now())
  capturedFrames.push(features)
  if (isRecording.value) {
    captureTimer = setTimeout(captureTick, CAPTURE_INTERVAL_MS)
  }
}

function startRecording() {
  if (!stream || isRecording.value) return
  capturedFrames = []
  isRecording.value = true
  captureTick()
}

function stopRecording() {
  if (!isRecording.value) return
  isRecording.value = false
  if (captureTimer) {
    clearTimeout(captureTimer)
    captureTimer = null
  }

  const frameCount = capturedFrames.length
  if (frameCount === 0) return

  const flattened = new Float32Array(frameCount * FEATURE_SIZE)
  capturedFrames.forEach((frame, i) => flattened.set(frame, i * FEATURE_SIZE))

  normalizeSequence(flattened, frameCount)

  emit("recording-ready", encodeNpyFloat32(flattened, [frameCount, FEATURE_SIZE]))
}

onBeforeUnmount(stopCamera)

defineExpose({ activateCamera, stopCamera, startRecording, stopRecording, cameraActive, isRecording })
</script>
<style scoped>
.video-card {
  background-color: var(--color-lightgray);
  width: 100%;
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

  .recording-indicator {
    position: absolute;
    top: 12px;
    right: 12px;
    background-color: rgba(17, 0, 3, 0.7);
    color: #ff4d4d;
    font-size: 12px;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 10px;
  }
}
</style>
