<template>
  <div class="button" :class="type" @click="props.onClick">
    <div
      v-if="props.icon"
      class="icon"
      :style="{ maskImage: `url(/src/assets/icons/${props.icon}.png)` }"
    ></div>
    <slot></slot>
  </div>
</template>
<script setup lang="ts">
import { defineProps } from "vue"
const props = defineProps<{
  type: "primary" | "secondary"
  id?: string
  icon?: string
  onClick: () => void
}>()
</script>
<style scoped>
.button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  border-radius: 20px;
  width: 166px;
  font-size: var(--font-size-body);
  text-align: center;
}
.icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
  background-color: currentColor;
}
.button.primary {
  background: var(--color-gradient-primary);
  .icon {
    background-color: #fff;
  }
  color: #fff;
}

.button.secondary {
  background-color: var(--color-lightyellow);
  color: var(--color-darkpurple);
  border: 1px solid var(--color-darkpurple);
  .icon {
    background-color: var(--color-darkpurple);
  }
}
</style>
