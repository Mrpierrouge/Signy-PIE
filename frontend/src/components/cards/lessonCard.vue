<template>
  <div
    class="card lesson-card"
    :class="{
      selected: selected,
    }"
    @click="$emit('click')"
  >
    <div class="content">
      <div class="texts">
        <div class="title">Lecon {{ lesson.id }}</div>
        <div class="subtitle">
          {{ lesson.title }}
        </div>
      </div>

      <div class="icon" :class="`icon_${lesson.status}`"></div>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Lesson } from "@/types/lesson"

defineProps<{
  selected: boolean
  lesson: Lesson
}>()
</script>
<style scoped>
.lesson-card {
  background-color: var(--color-lightgray);
  width: 90%;
  height: calc(90px - 20px - 20px);
  padding: 20px;
  border-radius: 20px;
  .content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: var(--color-black);
    .texts {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 5px;
      .title {
        font-size: 18px;
        font-weight: bold;
      }
      .subtitle {
        font-size: 14px;
        font-weight: normal;
      }
    }
    .icon {
      width: 24px;
      height: 24px;
      mask-size: cover;
      background-color: var(--color-black);
      &.icon_locked {
        mask-image: url("@/assets/icons/lock.png");
      }
      &.icon_unlocked {
        mask-image: url("@/assets/icons/unlock.png");
      }
      &.icon_completed {
        mask-image: url("@/assets/icons/ok-hand.png");
      }
    }
  }

  &.selected {
    background-color: var(--color-black);
    .content {
      color: white;
      .icon {
        background-color: white;
      }
    }
  }
}
</style>
