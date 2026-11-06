<template>
  <div class="lesson-card" :class="{ selected }" @click="$emit('click')">
    <div class="card-header">
      <div>
        <div class="label">Leçon {{ lesson.id }}</div>
        <div class="headline">
          {{ lesson.title }}
        </div>
      </div>

      <button
        v-if="selected && lesson.status !== 'locked'"
        class="action-button"
        type="button"
        @click.stop="$emit('start')"
      >
        <span class="play-placeholder" />
      </button>

      <div v-else class="status-icon" :class="{ locked: lesson.status === 'locked' }">
        <span v-if="lesson.status !== 'locked'" class="play-placeholder" />
      </div>
    </div>

    <div
      class="progress-track"
      :style="{
        opacity: selected ? 1 : 0,
      }"
    >
      <!-- TODO: replace this hardcoded progress with real lesson completion value -->
      <div class="progress-fill" />
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Lesson } from "@/types/lesson"

withDefaults(
  defineProps<{
    lesson: Lesson
    selected?: boolean
  }>(),
  {
    selected: false,
  },
)

defineEmits<{
  click: []
  start: []
}>()
</script>
<style scoped>
.lesson-card {
  width: 90%;
  padding: 18px 20px;
  border-radius: 20px;
  background-color: var(--color-babypurple);
  color: var(--color-black);
  cursor: pointer;
  font-family: var(--font-family);
  display: flex;
  flex-direction: column;
  gap: 12px;

  &.selected {
    background: var(--color-gradient-primary);
    color: white;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .label {
    font-size: var(--font-size-body);
    font-weight: var(--font-weight-regular);
    opacity: 0.9;
    margin-bottom: 2px;
  }

  .headline {
    font-size: var(--font-size-h3);
    font-weight: var(--font-weight-bold);
  }

  .action-button,
  .status-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    mask-size: contain;
    mask-repeat: no-repeat;
    mask-position: center;
    background-color: var(--color-darkpurple);

    mask-image: url("@/assets/icons/play-circle.png");

    &.locked {
      mask-image: url("@/assets/icons/lock.png");
    }
  }

  .action-button {
    border: none;
    background-color: white;
    cursor: pointer;
  }

  .progress-track {
    height: 6px;
    border-radius: 999px;
    background-color: rgba(255, 255, 255, 0.45);
    overflow: hidden;
  }

  .progress-fill {
    width: 20%;
    height: 100%;
    border-radius: 999px;
    background-color: white;
  }
}
</style>
