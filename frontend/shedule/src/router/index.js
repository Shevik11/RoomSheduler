import { createRouter, createWebHistory } from 'vue-router'
import DaysList from '../components/DayList.vue'
// import DayForm from '../components/DayForm.vue' // Додамо форму

const routes = [
  {
    path: '/',
    name: 'DaysList',
    component: () => import('../components/DayList.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router