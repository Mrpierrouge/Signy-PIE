<template>
  <div class="video-block">
    <h2 v-if="showTitle" class="word-title">{{ word.string }}</h2>
    <div v-if="showSuccess" class="success-view">
      <div class="success-icon" aria-hidden="true" />
      <p class="success-message">
        Bravo tu sais dire
        <strong>{{ word.string }} !</strong>
      </p>
      <BigButton type="primary" @click="emit('success-continue')">Je continue</BigButton>
    </div>
    <template v-else>
      <videoCard ref="videoCardRef" :video-src="videoSrc" @recording-ready="onRecordingReady" />

      <div v-if="isChecking" class="ai-result checking">Analyse en cours...</div>
      <div v-else-if="aiError" class="ai-result error">{{ aiError }}</div>
      <div
        v-else-if="aiResult"
        class="ai-result"
        :class="{ success: aiResult.is_valid, invalid: !aiResult.is_valid }"
      >
        <div class="status-badge">
          <span v-if="aiResult.is_valid">✓ Signe validé pour « {{ word.string }} » !</span>
          <span v-else>✗ Le modèle a deviné : « {{ aiResult.word }} »</span>
        </div>

        <div class="result-details">
          <p v-if="aiResult.message" class="result-message">{{ aiResult.message }}</p>

          <div
            v-if="aiResult.matched_words && aiResult.matched_words.length > 1"
            class="multi-words-info"
          >
            <span>Signe commun ({{ aiResult.label || aiResult.true_label }}) :</span>
            <strong>{{ aiResult.matched_words.join(", ") }}</strong>
          </div>

          <span v-if="aiResult.confidence !== null" class="confidence">
            Confiance IA : {{ (aiResult.confidence * 100).toFixed(0) }}%
          </span>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue"
import VideoCard from "./cards/videoCard.vue"
import BigButton from "./buttons/bigButton.vue"
import { ApiClass } from "@/api/api"
import type { AIWordResponse } from "@/types/word"

const props = withDefaults(
  defineProps<{
    videoSrc: string
    word: {
      id?: number
      string: string
      video: string
    }
    showTitle?: boolean
    showSuccess?: boolean
  }>(),
  {
    showTitle: true,
    showSuccess: false,
  },
)

const emit = defineEmits<{
  "validation-success": []
  "success-continue": []
}>()

const videoCardRef = ref<InstanceType<typeof VideoCard> | null>(null)
const isChecking = ref(false)
const aiResult = ref<AIWordResponse | null>(null)
const aiError = ref("")

async function onRecordingReady(blob: Blob) {
  const formData = new FormData()
  formData.append("video", blob, "recording.npy")

  aiResult.value = null
  aiError.value = ""
  isChecking.value = true
  try {
    aiResult.value = await ApiClass.tryWord(formData, props.word.string)
    if (aiResult.value.is_valid) {
      emit("validation-success")
    }
  } catch {
    aiError.value = "Impossible d'analyser l'enregistrement"
  } finally {
    isChecking.value = false
  }
}

async function activateCamera() {
  return (await videoCardRef.value?.activateCamera()) ?? false
}

function stopCamera() {
  videoCardRef.value?.stopCamera()
}

function cancelRecording() {
  videoCardRef.value?.cancelRecording()
}

function startRecording() {
  videoCardRef.value?.startRecording()
}

function stopRecording() {
  videoCardRef.value?.stopRecording()
}

defineExpose({
  activateCamera,
  stopCamera,
  cancelRecording,
  startRecording,
  stopRecording,
})
</script>
<style scoped>
.video-block {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;

  .word-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--color-black);
  }

  .success-view {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
    padding-top: 22px;
  }

  .success-icon {
    width: 270px;
    height: 250px;
    background-image: url("@/assets/icons/success-page-logo.svg");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
  }

  .success-message {
    color: var(--color-darkpurple);
    font-size: var(--font-size-h2);
    font-weight: var(--font-weight-bold);
    text-align: center;
    line-height: 1.25;

    strong {
      display: block;
      font-size: var(--font-size-title);
    }
  }

  .ai-result {
    background-color: var(--color-lightgray);
    color: var(--color-black);
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 14px;
    text-align: center;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 8px;

    &.checking {
      font-style: italic;
      opacity: 0.7;
    }

    &.error {
      background-color: #d43d3d;
      color: white;
    }

    &.success {
      background-color: #e8f5e9;
      border: 2px solid #4caf50;
      color: #1b5e20;

      .status-badge {
        font-weight: bold;
        font-size: 16px;
        color: #2e7d32;
      }
    }

    &.invalid {
      background-color: #ffebee;
      border: 2px solid #ef5350;
      color: #c62828;

      .status-badge {
        font-weight: bold;
        font-size: 16px;
        color: #c62828;
      }
    }

    .result-details {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 13px;
    }

    .result-message {
      margin: 0;
      line-height: 1.4;
    }

    .multi-words-info {
      background-color: rgba(0, 0, 0, 0.05);
      padding: 6px 10px;
      border-radius: 6px;
      display: flex;
      justify-content: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .confidence {
      font-size: 12px;
      opacity: 0.8;
    }
  }
}
</style>
