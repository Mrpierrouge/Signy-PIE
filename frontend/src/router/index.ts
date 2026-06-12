import { createRouter, createWebHistory } from "vue-router"

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
      path: "/lexique",
      name: "lexique",
      component: () => import("../views/lexique.vue"),
    },
  ],
})

export default router
