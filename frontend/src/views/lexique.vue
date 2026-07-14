<template>
  <div>Lexique</div>
  <div class="word-list">
    <div v-for="group in groupedWords" :key="group.letter" class="letter-section">
      <div class="letter-banner">{{ group.letter }}</div>
      <WordBlock v-for="word in group.words" :key="word.id" :word="word" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import WordBlock from "@/components/wordBlock.vue"
import { ApiClass } from "@/api/api"
import type { Word } from "@/types/word"

const words = ref<Word[]>([])

const DIACRITICS_PATTERN = /\p{Diacritic}/gu

function firstLetterOf(str: string): string {
  return str.normalize("NFD").replace(DIACRITICS_PATTERN, "").charAt(0).toUpperCase()
}

const groupedWords = computed(() => {
  const sorted = [...words.value].sort((a, b) =>
    a.string.localeCompare(b.string, "fr", { sensitivity: "base" }),
  )

  const groups: { letter: string; words: Word[] }[] = []
  for (const word of sorted) {
    const letter = firstLetterOf(word.string)
    const lastGroup = groups[groups.length - 1]
    if (lastGroup?.letter === letter) {
      lastGroup.words.push(word)
    } else {
      groups.push({ letter, words: [word] })
    }
  }
  return groups
})

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
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.letter-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  padding-bottom: 30px;
}

.letter-banner {
  position: sticky;
  top: 0;
  z-index: 1;
  width: 100%;
  background-color: var(--color-darkpurple);
  color: white;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  padding: 8px 0;
}
</style>
