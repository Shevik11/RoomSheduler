<template>
  <div class="filter-item">
    <label for="busy">Статус:</label>
    <select 
      id="busy"
      :value="modelValue"
      @input="handleInput" 
      class="filter-select"
    >
      <option value="">Всі</option>
      <option :value="true">Зайняті</option>
      <option :value="false">Вільні</option>
    </select>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean | null): void;
}>();

const handleInput = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value;
  emit('update:modelValue', value === 'null' ? null : value === 'true');
};
</script>

<style scoped>
.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
  padding: 0 8px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 14px;
  color: #505050;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #222 !important;
}

.filter-select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.filter-input,
.filter-select {
  color: #222 !important;
}
</style> 