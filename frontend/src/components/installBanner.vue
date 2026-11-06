<template>
  <div v-if="visible" class="install-banner" role="dialog" aria-label="Installer l'application">
    <img class="install-logo" src="/icons/icon-192.png" alt="" />
    <div class="install-text">
      <strong>Installer Signy</strong>
      <span v-if="isIos">Touchez « Partager » puis « Sur l'écran d'accueil »</span>
      <span v-else>Ajoutez l'appli sur votre écran d'accueil</span>
    </div>
    <button v-if="!isIos" class="install-button" @click="install">Installer</button>
    <button class="close-button" aria-label="Fermer" @click="dismiss">×</button>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue"

// Chrome-only event, not yet in TypeScript's DOM types
interface BeforeInstallPromptEvent extends Event {
  prompt(): Promise<void>
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>
}

const DISMISS_KEY = "signy-install-dismissed-at"
const DISMISS_DURATION_MS = 7 * 24 * 60 * 60 * 1000

const installPrompt = ref<BeforeInstallPromptEvent | null>(null)
const isIos = ref(false)
const dismissed = ref(false)

const visible = computed(() => !dismissed.value && (installPrompt.value !== null || isIos.value))

function isInstalled(): boolean {
  return (
    window.matchMedia("(display-mode: standalone)").matches ||
    (navigator as Navigator & { standalone?: boolean }).standalone === true
  )
}

function wasDismissedRecently(): boolean {
  try {
    const dismissedAt = Number(localStorage.getItem(DISMISS_KEY))
    return dismissedAt > 0 && Date.now() - dismissedAt < DISMISS_DURATION_MS
  } catch {
    return false
  }
}

function onBeforeInstallPrompt(event: Event) {
  // Hide Chrome's default install bar: this banner replaces it
  event.preventDefault()
  installPrompt.value = event as BeforeInstallPromptEvent
}

function onInstalled() {
  installPrompt.value = null
}

async function install() {
  const prompt = installPrompt.value
  if (!prompt) return
  await prompt.prompt()
  await prompt.userChoice
  // The event can only be used once
  installPrompt.value = null
}

function dismiss() {
  dismissed.value = true
  try {
    localStorage.setItem(DISMISS_KEY, String(Date.now()))
  } catch {
    // Storage unavailable (private mode): the banner will simply come back next visit
  }
}

onMounted(() => {
  const isMobile = window.matchMedia("(pointer: coarse)").matches
  if (!isMobile || isInstalled() || wasDismissedRecently()) return

  // iOS has no install prompt: we show instructions instead.
  // iPadOS identifies itself as a Mac, hence the touch check.
  isIos.value =
    /iphone|ipad|ipod/i.test(navigator.userAgent) ||
    (/macintosh/i.test(navigator.userAgent) && navigator.maxTouchPoints > 1)

  window.addEventListener("beforeinstallprompt", onBeforeInstallPrompt)
  window.addEventListener("appinstalled", onInstalled)
})

onUnmounted(() => {
  window.removeEventListener("beforeinstallprompt", onBeforeInstallPrompt)
  window.removeEventListener("appinstalled", onInstalled)
})
</script>
<style scoped>
.install-banner {
  position: fixed;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  box-sizing: border-box;
  width: calc(100% - 32px);
  max-width: 400px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: white;
  color: var(--color-black);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  font-family: var(--font-family);
}

.install-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  flex-shrink: 0;
}

.install-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: var(--font-size-body);

  strong {
    font-size: var(--font-size-h3);
  }
}

.install-button {
  flex-shrink: 0;
  background-color: var(--color-darkpurple);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
}

.close-button {
  flex-shrink: 0;
  background: none;
  border: none;
  padding: 4px;
  font-size: 22px;
  line-height: 1;
  color: var(--color-black);
  opacity: 0.5;
  cursor: pointer;
}
</style>
