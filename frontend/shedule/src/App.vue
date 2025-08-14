<script setup lang="ts">
// Імпортуємо необхідні компоненти
import { RouterView } from 'vue-router'
import { BaseLayout } from './components/layout'
import WeekTypeDisplay from './components/WeekTypeDisplay.vue'
import { ref } from 'vue'

const weekType = ref<string | null>(null);

const handleWeekTypeUpdate = (newType: string) => {
  console.log('App received new week type:', newType);
  // Перевіряємо, чи змінився тип тижня
  if (newType !== weekType.value) {
    weekType.value = newType;
  }
};
</script>

<template>
  <BaseLayout>
    <template #header>
      <WeekTypeDisplay @update:weekType="handleWeekTypeUpdate" />
      <nav v-if="$route.path !== '/'" class="main-nav">
        <router-link to="/">До списку днів</router-link>
      </nav>
    </template>

    <RouterView :default-nominator="weekType" />

    <template #footer>
      <div class="footer-content">
        <p>&copy; 2025 Dekanat Pro 🚀</p>
      </div>
    </template>
  </BaseLayout>
</template>

<style >
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  line-height: 1.6;
  color: #333;
}

#app {
  max-width: 1200px;
  margin: 0 auto 0 7.3rem;
  padding: 0;
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

/* Адаптивні стилі для менших екранів */
@media (max-width: 1200px) {
  #app {
    margin: 0 auto;
    padding: 0 1rem;
  }
}

@media (max-width: 768px) {
  #app {
    margin: 0;
    padding: 0 0.5rem;
  }
  
  .app-content {
    padding: 15px;
  }
  
  .main-nav {
    padding: 0.5rem 0;
    margin-bottom: 0.5rem;
  }
  
  .footer-content {
    padding: 0.5rem 0;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  #app {
    padding: 0 0.25rem;
  }
  
  .app-content {
    padding: 10px;
  }
  
  .main-nav a {
    font-size: 0.9rem;
  }
}
</style>