<template>
  <div class="filter-item">
    <label for="day_of_week">День тижня:</label>
    <select 
      id="day_of_week"
      :value="modelValue"
      @input="handleInput" 
      class="filter-select"
    >
      <option value="">Всі дні</option>
      <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { DAYS_OF_WEEK } from '../../constants/schedule';

const props = defineProps<{
  modelValue: string | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const daysOfWeek = DAYS_OF_WEEK;

const handleInput = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value;
  emit('update:modelValue', value === 'null' ? null : value);
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
</style> 