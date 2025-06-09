<script setup>
// Імпортуємо необхідні компоненти
import { RouterView } from 'vue-router'
import { BaseLayout } from './components/layout'
import WeekTypeDisplay from './components/WeekTypeDisplay.vue'
</script>

<template>
  <BaseLayout>
    <template #header>
      <WeekTypeDisplay />
      <nav v-if="$route.path !== '/'" class="main-nav">
        <router-link to="/">До списку днів</router-link>
      </nav>
    </template>

    <RouterView />

    <template #footer>
      <div class="footer-content">
        <p>&copy; 2024 RoomScheduler. Всі права захищені.</p>
      </div>
    </template>
  </BaseLayout>
</template>

<style>
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.6;
  color: #333;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-nav {
  padding: 1rem 0;
  margin-bottom: 1rem;
}

.main-nav a {
  color: #2c3e50;
  text-decoration: none;
  font-weight: bold;
}

.main-nav a:hover {
  text-decoration: underline;
}

.app-content {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  flex: 1;
}

.footer-content {
  text-align: center;
  color: #666;
  padding: 1rem 0;
  margin-top: auto;
}

/* Анімація для переходів між сторінками */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>