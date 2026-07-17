<template>
  <div class="home-container">
    <div class="stats-row">
      <span class="stats-text">Gagne des points, vite !</span>
      <div class="points">
        <svg
          class="star-icon"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            d="M10 0 L12.6 6.9 L20 7.6 L14.4 12.4 L16.2 20 L10 15.9 L3.8 20 L5.6 12.4 L0 7.6 L7.4 6.9 Z"
          />
        </svg>
        <span>{{ points }} points</span>
      </div>
    </div>

    <div class="title">
      Tes leçons
    </div>

    <div class="list">
      <LessonCard
        v-for="(lesson, index) in lessons"
        :key="lesson.id"
        :lesson="lesson"
        :featured="index === 0"
        :color-index="index - 1"
        :description="introDescription"
        @click="selectLesson(lesson.id)"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import LessonCard from "@/components/cards/lessonCard.vue"
import { ref } from "vue"
import type { Lesson } from "@/types/lesson"

const points = ref(440)

const introDescription =
  "Découvrez les premiers signes essentiels pour débuter en LSF et apprendre à communiquer simplement."

const lessons: Lesson[] = [
  { id: 1, title: "Apprendre les bases", status: "unlocked" },
  { id: 2, title: "Apprendre les bases", status: "locked" },
  { id: 3, title: "Apprendre les bases", status: "locked" },
  { id: 4, title: "Apprendre les bases", status: "locked" },
]

const selectedLesson = ref<number | null>(null)
const selectLesson = (lessonId: number) => {
  selectedLesson.value = lessonId
}
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
