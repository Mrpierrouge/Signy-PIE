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
      path: "/profile",
      name: "profile",
      component: () => import("../views/profile.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/login.vue"),
      meta: { guestOnly: true },
    },
    {
      path: "/lexique",
      name: "lexique",
      component: () => import("../views/lexique.vue"),
    },
    {
      path: "/lesson/:lessonId",
      name: "lesson",
      component: () => import("../views/lesson.vue"),
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // On first navigation, ask the backend who is logged in (session cookie)
  if (!authStore.initialized) {
    await authStore.initializeAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "login" }
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: "profile" }
  }
})

export default router
