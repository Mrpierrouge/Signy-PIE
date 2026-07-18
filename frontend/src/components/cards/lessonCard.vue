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
