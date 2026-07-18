<template>
  <div
    class="lesson-card"
    :class="[
      featured ? 'featured' : ['compact', `color-${colorIndex % 3}`],
      { selected: !featured && selected },
    ]"
    @click="!featured && $emit('click')"
  >
    <div class="label">Leçon {{ lesson.id }}</div>

    <div v-if="featured" class="featured-body">
      <div class="headline">
        {{ lesson.title }}
      </div>
      <p class="description">
        {{ description }}
      </p>
      <button class="cta" @click="$emit('click')">
        <svg class="play-icon" viewBox="0 0 12 14" fill="currentColor">
          <path d="M0 0 L12 7 L0 14 Z" />
        </svg>
        Commencer la leçon
      </button>
    </div>

    <template v-else>
      <div class="compact-body">
        <div class="headline">
          {{ lesson.title }}
        </div>
        <div class="icon" :class="`icon_${lesson.status}`" />
      </div>

      <div class="extra">
        <div class="extra-inner">
          <p class="extra-text">Découvrez les mots de cette leçon et entraînez-vous en LSF.</p>
          <button class="start-button" @click.stop="$emit('start')">Commencer la leçon</button>
        </div>
      </div>
    </template>
  </div>
</template>
<script setup lang="ts">
import type { Lesson } from "@/types/lesson"

withDefaults(
  defineProps<{
    lesson: Lesson
    selected?: boolean
    featured?: boolean
    colorIndex?: number
    description?: string
  }>(),
  {
    selected: false,
    featured: false,
    colorIndex: 0,
    description: "",
  },
)

defineEmits<{
  click: []
  start: []
}>()
</script>
<style scoped>
.lesson-card {
  width: 100%;
  padding: 20px;
  border-radius: 24px;
  cursor: pointer;
  font-family: var(--font-family);
  transition: background-color 0.35s ease;

  .label {
    font-size: var(--font-size-body);
    font-weight: var(--font-weight-bold);
    opacity: 0.6;
    margin-bottom: 6px;
  }

  .headline {
    font-size: var(--font-size-h2);
    font-weight: var(--font-weight-bold);
  }

  /* ── Featured (hero) card ──────────────────────────────────────────────── */
  &.featured {
    background-color: var(--color-darkpurple);
    color: white;

    .featured-body {
      display: flex;
      flex-direction: column;
      gap: 10px;

      .description {
        margin: 0;
        font-size: var(--font-size-body);
        font-weight: var(--font-weight-regular);
        line-height: 1.5;
        opacity: 0.85;
      }

      .cta {
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
        margin-top: 6px;

        .play-icon {
          width: 12px;
          height: 14px;
        }
      }
    }
  }

  /* ── Compact (list) card ───────────────────────────────────────────────── */
  &.compact {
    color: var(--color-black);

    &.color-0 {
      background-color: var(--color-lightblue);
    }
    &.color-1 {
      background-color: var(--color-lightpink);
    }
    &.color-2 {
      background-color: var(--color-lightyellow);
    }

    .compact-body {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 50px;

      .headline {
        flex-grow: 1;
      }

      .icon {
        width: 22px;
        height: 22px;
        flex-shrink: 0;
        mask-size: contain;
        mask-repeat: no-repeat;
        mask-position: center;
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
        font-family: var(--font-family);
        font-size: var(--font-size-body);
        font-weight: var(--font-weight-regular);
        color: var(--color-black);
      }

      .start-button {
        display: flex;
        align-items: center;
        justify-content: center;
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
    }

    &.selected {
      background-color: var(--color-black);
      color: white;
      .icon {
        background-color: white;
      }
      .extra {
        grid-template-rows: 1fr;
        .extra-text {
          color: white;
        }
      }
    }
  }
}
</style>
