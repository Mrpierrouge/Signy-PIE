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

    <div class="extra">
      <div class="extra-inner">
        <p class="extra-text">Découvrez les mots de cette leçon et entraînez-vous en LSF.</p>
        <button class="start-button" @click.stop="$emit('start')">Commencer la leçon</button>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Lesson } from "@/types/lesson"

defineProps<{
  selected: boolean
  lesson: Lesson
}>()

defineEmits<{
  click: []
  start: []
}>()
</script>
<style scoped>
.lesson-card {
  background-color: var(--color-lightgray);
  width: 90%;
  padding: 20px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.35s ease;

  .content {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 50px;
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

  .extra {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.35s ease;

    .extra-inner {
      overflow: hidden;
    }

    .extra-text {
      margin: 0 0 15px;
      font-size: 14px;
      color: var(--color-black);
    }

    .start-button {
      background-color: var(--color-darkpurple);
      color: white;
      border: none;
      border-radius: 10px;
      padding: 10px 20px;
      font-size: 14px;
      font-weight: bold;
      cursor: pointer;
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
    .extra {
      grid-template-rows: 1fr;
      .extra-text {
        color: white;
      }
    }
  }
}
</style>
