<template>
  <div
    class="lesson-card"
    :class="featured ? 'featured' : `compact color-${colorIndex % 3}`"
    @click="!featured && $emit('click')"
  >
    <div class="label">
      Leçon {{ lesson.id }}
    </div>

    <div v-if="featured" class="featured-body">
      <div class="headline">
        {{ lesson.title }}
      </div>
      <p class="description">
        {{ description }}
      </p>
      <button class="cta" @click="$emit('click')">
        <svg
          class="play-icon"
          viewBox="0 0 12 14"
          fill="currentColor"
        >
          <path d="M0 0 L12 7 L0 14 Z" />
        </svg>
        Commencer la leçon
      </button>
    </div>

    <div v-else class="compact-body">
      <div class="headline">
        {{ lesson.title }}
      </div>
      <div
        class="icon"
        :class="`icon_${lesson.status}`"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Lesson } from "@/types/lesson"

withDefaults(
  defineProps<{
    lesson: Lesson
    featured?: boolean
    colorIndex?: number
    description?: string
  }>(),
  {
    featured: false,
    colorIndex: 0,
    description: "",
  },
)

defineEmits<{
  click: []
}>()
</script>
<style scoped>
.lesson-card {
  width: 100%;
  border-radius: 24px;
  font-family: var(--font-family);
}

.label {
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
}

.headline {
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-bold);
}

.lesson-card.featured {
  background-color: var(--color-darkpurple);
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.lesson-card.featured .description {
  margin: 0;
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
  line-height: 1.5;
  opacity: 0.85;
}
.lesson-card.featured .cta {
  margin-top: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background-color: var(--color-black);
  color: white;
  border: none;
  border-radius: 16px;
  padding: 14px;
  font-family: var(--font-family);
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-bold);
  cursor: pointer;
}
.lesson-card.featured .play-icon {
  width: 12px;
  height: 14px;
}

.lesson-card.compact {
  padding: 18px 20px;
  color: var(--color-black);
  cursor: pointer;
}
.lesson-card.compact.color-0 {
  background-color: var(--color-lightblue);
}
.lesson-card.compact.color-1 {
  background-color: var(--color-lightpink);
}
.lesson-card.compact.color-2 {
  background-color: var(--color-lightyellow);
}
.lesson-card.compact .compact-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 4px;
}
.lesson-card.compact .icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  background-color: var(--color-black);
}
.lesson-card.compact .icon.icon_locked {
  mask-image: url("@/assets/icons/lock.png");
}
.lesson-card.compact .icon.icon_unlocked {
  mask-image: url("@/assets/icons/unlock.png");
}
.lesson-card.compact .icon.icon_completed {
  mask-image: url("@/assets/icons/ok-hand.png");
}
</style>
