<template>
  <div class="lesson-page">
    <header class="lesson-header page-header">
      <div class="lesson-header-title">
        <span class="lesson-title-label">Leçon {{ lessonId }}</span>
      </div>

      <button
        class="header-close"
        type="button"
        aria-label="Fermer la leçon"
        @click="closeLesson"
      ></button>
    </header>

    <main v-if="lesson" class="lesson-content">
      <div class="sticky-block">
        <div v-if="lesson.words.length > 1" class="stepper" aria-label="Progression de la leçon">
          <div
            v-for="(word, index) in lesson.words"
            :key="word.id"
            class="step-indicator"
            :class="{ active: index === currentWordIndex, done: index < currentWordIndex }"
            :aria-label="`Étape ${index + 1}`"
          />
        </div>

        <div class="lesson-copy">
          <p class="focus-label">Découvre le signe :</p>
          <h1 class="word-title">{{ currentWord?.string }}</h1>
        </div>
      </div>

      <VideoBlock
        v-if="currentWord"
        ref="videoBlockRef"
        :key="`${currentWord.id}-${videoReplayKey}`"
        :video-src="currentWordVideoSrc"
        :word="currentWord"
        :show-title="false"
        :show-success="lessonStep === 'success'"
        @validation-success="handleValidationSuccess"
        @success-continue="continueAfterSuccess"
      />

      <div
        v-if="lessonStep !== 'success'"
        class="lesson-actions"
        :class="{ 'single-action': lessonStep === 'preview' }"
      >
        <template v-if="lessonStep === 'preview'">
          <BigButton type="primary" @click="activateCameraStep">A moi de jouer</BigButton>
        </template>
        <template v-else-if="lessonStep === 'camera-ready'">
          <BigButton type="secondary" @click="replayCurrentWord">Revoir la vidéo</BigButton>
          <BigButton type="primary" @click="startRecordingStep"
            >Démarrer l'enregistrement</BigButton
          >
        </template>
        <template v-else>
          <BigButton type="secondary" @click="replayCurrentWord">Revoir la vidéo</BigButton>
          <BigButton type="primary" @click="stopRecordingStep">Arrêter l'enregistrement</BigButton>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import BigButton from "@/components/buttons/bigButton.vue"
import VideoBlock from "@/components/videoBlock.vue"
import { ApiClass } from "@/api/api"
import type { LessonWithWords } from "@/types/lesson"

const route = useRoute()
const router = useRouter()

const lesson = ref<LessonWithWords | null>(null)
const currentWordIndex = ref(0)
const videoReplayKey = ref(0)
const lessonStep = ref<"preview" | "camera-ready" | "recording" | "success">("preview")
const videoBlockRef = ref<{
  activateCamera: () => Promise<boolean>
  stopCamera: () => void
  cancelRecording: () => void
  startRecording: () => void
  stopRecording: () => void
} | null>(null)

const lessonId = computed(() => Number(route.params.lessonId ?? 0))
const currentWord = computed(() => lesson.value?.words[currentWordIndex.value] ?? null)
const currentWordVideoSrc = computed(() =>
  currentWord.value ? ApiClass.getVideoUrl(currentWord.value.video) : "",
)

async function loadLesson() {
  const id = lessonId.value

  if (!Number.isInteger(id) || id <= 0) {
    await router.push({ name: "home" })
    return
  }

  try {
    lesson.value = await ApiClass.getLessonById(id)
    currentWordIndex.value = 0
    lessonStep.value = "preview"
  } catch (error) {
    console.error("Error fetching lesson details:", error)
    await router.push({ name: "home" })
  }
}

async function activateCameraStep() {
  if (!videoBlockRef.value) return
  const granted = await videoBlockRef.value.activateCamera()
  if (granted) {
    lessonStep.value = "camera-ready"
  }
}

function replayCurrentWord() {
  lessonStep.value = "preview"
  videoBlockRef.value?.stopCamera()
  videoReplayKey.value += 1
}

function startRecordingStep() {
  if (!videoBlockRef.value) return
  lessonStep.value = "recording"
  videoBlockRef.value.startRecording()
}

function stopRecordingStep() {
  if (!videoBlockRef.value) return
  lessonStep.value = "camera-ready"
  videoBlockRef.value.stopRecording()
}

function handleValidationSuccess() {
  lessonStep.value = "success"
}

function continueAfterSuccess() {
  if (!lesson.value) return

  if (currentWordIndex.value >= lesson.value.words.length - 1) {
    closeLesson()
    return
  }

  currentWordIndex.value += 1
  replayCurrentWord()
}

function closeLesson() {
  replayCurrentWord()
  void router.push({ name: "home" })
}

watch(
  () => route.params.lessonId,
  () => {
    void loadLesson()
  },
)

onMounted(() => {
  void loadLesson()
})
</script>

<style scoped>
.lesson-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--color-lightyellow);
}

.lesson-header {
  width: 90%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
  padding-top: 5vh;
  margin-bottom: 12px;
  position: sticky;
  top: 0;
  z-index: 20;
  background: var(--color-lightyellow);
}

.lesson-header-title {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  flex: 1;
}

.lesson-title-label {
  font-size: var(--font-size-title);
  font-weight: var(--font-weight-bold);
  color: var(--color-darkpurple);
}

.header-close {
  width: 25px;
  height: 25px;
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  background-color: var(--color-darkpurple);
  mask-image: url("@/assets/icons/cross.png");
}

.lesson-content {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  overflow: auto;
  padding-bottom: 32px;
}

.sticky-block {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 10;
  padding-top: 8px;
  background: var(--color-lightyellow);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stepper {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
  gap: 10px;
}

.step-indicator {
  width: 100%;
  height: 10px;
  background: rgba(42, 0, 107, 0.2);
  border-radius: 999px;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.step-indicator.active {
  background: var(--color-purple);
}

.step-indicator.done {
  background: var(--color-darkpurple);
}

.lesson-copy {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.focus-label {
  color: var(--color-darkpurple);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-bold);
  line-height: 1.3;
}

.word-title {
  color: var(--color-darkpurple);
  font-size: clamp(2rem, 3vw, 2.6rem);
  font-weight: var(--font-weight-bold);
  line-height: 1.1;
}

.lesson-actions {
  width: 80%;
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: space-between;
}

.lesson-actions.single-action {
  justify-content: flex-end;
}

.lesson-actions :deep(.button) {
  flex: 1;
}

.lesson-actions.single-action :deep(.button) {
  flex: 0 0 auto;
}

@media (max-width: 420px) {
  .lesson-actions {
    flex-direction: column;
  }
}
</style>
