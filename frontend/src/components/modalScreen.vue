<template>
  <div class="modal-screen" :class="{ open: modelValue }">
    <button class="close-button" @click="close">Fermer</button>
    <div class="modal-content">
      <slot />
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  "update:modelValue": [value: boolean]
}>()

function close() {
  emit("update:modelValue", false)
}
</script>
<style scoped>
.modal-screen {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 782px;
  max-height: 100vh;
  background-color: white;
  border: 1px solid black;
  border-radius: 75px 75px 0px 0px;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15);
  z-index: 200;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;
  transform: translateY(100%);
  transition: transform 0.4s ease;

  &.open {
    transform: translateY(0);
  }

  .close-button {
    align-self: flex-end;
    margin: 20px 20px 0 0;
    background-color: var(--color-darkpurple);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
  }

  .modal-content {
    width: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    padding: 15px 0 30px;
  }
}
</style>
