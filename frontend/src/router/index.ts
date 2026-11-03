import { createRouter, createWebHistory } from "vue-router"

import { useAuthStore } from "@/stores/auth"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/home",
    },
    {
      path: "/home",
      name: "home",
      component: () => import("../views/home.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login.vue"),
      meta: { guestOnly: true },
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("../views/profile.vue"),
    },
    {
      path: "/lexique",
      name: "lexique",
      component: () => import("../views/lexique.vue"),
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!authStore.initialized) {
    await authStore.initializeAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" }
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: "home" }
  }
})

export default router
