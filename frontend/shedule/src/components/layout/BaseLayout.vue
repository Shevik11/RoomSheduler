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

<script setup lang="ts"></script>

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

/* Адаптивні стилі для менших екранів */
@media (max-width: 768px) {
  .layout__header {
    padding: 0.75rem;
  }

  .layout__main {
    padding: 0.75rem;
  }

  .layout__footer {
    padding: 0.75rem;
  }
}

@media (max-width: 480px) {
  .layout__header {
    padding: 0.5rem;
  }

  .layout__main {
    padding: 0.5rem;
  }

  .layout__footer {
    padding: 0.5rem;
  }
}
</style>
