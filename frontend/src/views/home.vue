<template>
  <div class="home-container">
    <div class="list">
      <LessonCard
        v-for="(lesson, index) in lessons"
        :key="index"
        :lesson="lesson"
        :selected="selectedLesson === index + 1"
        @click="selectLesson(index + 1)"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import LessonCard from "@/components/cards/lessonCard.vue"
import { ref } from "vue"
import type { Lesson } from "@/types/lesson"

const lessons: Lesson[] = [
  { id: 1, title: "Apprendre les bases", status: "completed" },
  { id: 2, title: "Apprendre les bases", status: "unlocked" },
  { id: 3, title: "Apprendre les bases", status: "unlocked" },
  { id: 4, title: "Apprendre les bases", status: "locked" },
  { id: 5, title: "Apprendre les bases", status: "locked" },
]

const selectedLesson = ref<number | null>(0)
const selectLesson = (lessonId: number) => {
  selectedLesson.value = lessonId
}
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
