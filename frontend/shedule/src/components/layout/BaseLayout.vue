<template>
  <div class="layout">
    <header class="layout__header">
      <slot name="header"></slot>
    </header>
    <main class="layout__main">
      <slot></slot>
    </main>
    <footer class="layout__footer">
      <slot name="footer"></slot>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Базовий layout компонент
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout__header {
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.layout__main {
  flex: 1;
  padding: 1rem;
}

.layout__footer {
  padding: 1rem;
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
}
</style> 