<script setup>
// Імпортуємо необхідні компоненти
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <!-- Основне меню (можна додати за потреби) -->
    <nav v-if="$route.path !== '/'" class="main-nav">
      <router-link to="/">До списку днів</router-link>
    </nav>

    <!-- Контейнер для контенту -->
    <main class="app-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Глобальні стилі */
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
}

.main-nav {
  padding: 1rem 0;
  margin-bottom: 2rem;
  border-bottom: 1px solid #eee;
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