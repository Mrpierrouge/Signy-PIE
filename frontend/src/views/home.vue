<template>
  <div class="home-container">
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
}
.list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  width: 100%;
}
</style>
