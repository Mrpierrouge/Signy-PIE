<template>
  <div class="home-container">
    <div class="stats-row">
      <span class="stats-text">Gagne des points, vite !</span>
      <div class="points">
        <svg class="star-icon" viewBox="0 0 20 20" fill="currentColor">
          <path
            d="M10 0 L12.6 6.9 L20 7.6 L14.4 12.4 L16.2 20 L10 15.9 L3.8 20 L5.6 12.4 L0 7.6 L7.4 6.9 Z"
          />
        </svg>
        <span> points</span>
      </div>
    </div>

    <div class="title">Tes leçons</div>

    <div class="list">
      <LessonCard
        v-for="lesson in lessons"
        :key="lesson.id"
        :lesson="lesson"
        :selected="selectedLesson === lesson.id"
        @click="selectLesson(lesson)"
        @start="startLesson(lesson.id)"
      />
    </div>
  </div>

  <ModalScreen v-model="showLessonModal">
    <VideoBlock v-if="firstWordVideoSrc" :video-src="firstWordVideoSrc" />
  </ModalScreen>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import LessonCard from "@/components/cards/lessonCard.vue"
import ModalScreen from "@/components/modalScreen.vue"
import VideoBlock from "@/components/videoBlock.vue"
import { ApiClass } from "@/api/api"
import type { Lesson, LessonWithWords } from "@/types/lesson"

// Placeholder lessons so the list doesn't look empty while only a couple of
// real lessons exist in the backend. Negative ids keep them from ever
// colliding with real lesson ids. Always locked since there's no content behind them.
const placeholderLessons: Lesson[] = [
  { id: -1, title: "Les salutations", status: "locked" },
  { id: -2, title: "Les couleurs", status: "locked" },
  { id: -3, title: "Les nombres", status: "locked" },
  { id: -4, title: "La famille", status: "locked" },
]

const fetchedLessons = ref<LessonWithWords[]>([])

const lessons = computed<Lesson[]>(() => [
  ...fetchedLessons.value.map((lesson) => ({
    id: lesson.id,
    title: lesson.title,
    status: "unlocked" as const,
  })),
  ...placeholderLessons,
])

const selectedLesson = ref<number | null>(null)

function selectLesson(lesson: Lesson) {
  if (lesson.status === "locked") return
  selectedLesson.value = lesson.id
}

const showLessonModal = ref(false)
const activeLesson = ref<LessonWithWords | null>(null)

const firstWordVideoSrc = computed(() => {
  const firstWord = activeLesson.value?.words[0]
  return firstWord ? ApiClass.getVideoUrl(firstWord.video) : ""
})

function startLesson(lessonId: number) {
  const lesson = fetchedLessons.value.find((lesson) => lesson.id === lessonId)
  if (!lesson || lesson.words.length === 0) return
  activeLesson.value = lesson
  showLessonModal.value = true
}

async function fetchLessons() {
  try {
    fetchedLessons.value = await ApiClass.getLessons()
  } catch (error) {
    console.error("Error fetching lessons:", error)
  }
}

onMounted(fetchLessons)
</script>
<style scoped>
.home-container {
  width: 90%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.stats-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.stats-text {
  font-family: var(--font-family);
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-regular);
}
.points {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-pink);
  font-family: var(--font-family);
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}
.points span {
  color: white;
}
.star-icon {
  width: 20px;
  height: 20px;
}
.list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  width: 100%;
}
</style>
