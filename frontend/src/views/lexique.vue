<template>
  <div>Lexique</div>
  <div class="word-list">
    <WordBlock v-for="word in words" :key="word.id" :word="word" />
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue"
import WordBlock from "@/components/wordBlock.vue"
import { ApiClass } from "@/api/api"
import type { Word } from "@/types/word"

const words = ref<Word[]>([])

async function fetchAllWords() {
  try {
    words.value = await ApiClass.getWords()
  } catch (error) {
    console.error("Error fetching words:", error)
  }
}

onMounted(fetchAllWords)
</script>
<style scoped>
.word-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
</style>
