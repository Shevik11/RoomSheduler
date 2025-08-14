import { createRouter, createWebHistory } from "vue-router";
import DaysList from "../components/features/DayList.vue";
// import DayForm from '../components/DayForm.vue' // Додамо форму

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: DaysList,
    },
  ],
});

export default router;
