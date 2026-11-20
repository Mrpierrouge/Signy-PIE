<template>
  <button class="button" :class="type" :type="nativeType" @click="props.onClick">
    <div
      v-if="props.icon"
      class="icon"
      :style="{ maskImage: `url(@/assets/icons/${props.icon}.png)` }"
    ></div>
    <slot></slot>
  </button>
</template>
<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    type: "primary" | "secondary"
    // HTML type of the button. "button" by default so it never submits a form by accident;
    // use native-type="submit" for a form's send button.
    nativeType?: "button" | "submit"
    id?: string
    icon?: string
    onClick?: () => void
  }>(),
  {
    nativeType: "button",
    onClick: () => undefined,
  },
)
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
