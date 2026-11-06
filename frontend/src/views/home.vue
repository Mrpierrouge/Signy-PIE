<template>
  <div class="home-container">
    <div class="home-header page-header">
      <TitleLogoBlock />
      <div class="score-bubble"></div>
    </div>

    <h2 class="lessons-title">Tes leçons :</h2>
    <div class="list-container">
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
  </div>

</template>
<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import LessonCard from "@/components/cards/lessonCard.vue"
import TitleLogoBlock from "@/components/titleLogoBlock.vue"
import { ApiClass } from "@/api/api"
import type { Lesson, LessonWithWords } from "@/types/lesson"

const points = ref(440)

// Placeholder lessons so the list doesn't look empty while only a couple of
// real lessons exist in the backend. Negative ids keep them from ever
// colliding with real lesson ids. Always locked since there's no content behind them.
const placeholderLessons: Lesson[] = [
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

const router = useRouter()

function startLesson(lessonId: number) {
  const lesson = fetchedLessons.value.find((lesson) => lesson.id === lessonId)
  if (!lesson || lesson.words.length === 0) return
  router.push({ name: "lesson", params: { lessonId: String(lessonId) } })
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
.home-header {
  flex-direction: row;
  justify-content: space-between;
  flex-shrink: 0;
}
.score-bubble {
  width: 1px;
  height: 1px;
}
.home-container {
  width: 90%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}
.lessons-title {
  color: var(--color-darkpurple);
  position: relative;
  z-index: 2;
  flex-shrink: 0;
  margin-top: 5vh;
  margin-bottom: 20px;
  background: var(--color-lightyellow);
}

.points {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-pink);
  font-family: var(--font-family);
  font-size: var(--font-size-h4);
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
.list-container {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  overscroll-behavior-y: contain;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding-bottom: 30px;
}

.lesson-modal-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}
</style>
