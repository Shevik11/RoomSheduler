<template>
  <div class="filter-item select-wrapper">
    <label for="namb_of_para">Номер пари:</label>
    <select 
      id="namb_of_para"
      :value="modelValue"
      @input="handleInput" 
      class="filter-select"
    >
      <option value="">Всі пари</option>
      <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
    </select>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: number | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: number | null): void;
}>();

const handleInput = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value;
  emit('update:modelValue', value === 'null' ? null : Number(value));
};
</script>

<style scoped>
@import './dropdown-filter.css';
.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
  padding: 0 8px;
  margin-bottom: 15px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: 600;
  font-size: 14px;
  color: #2c3e50;
}

.filter-input,
.filter-select {
  color: #2c3e50 !important;
}
</style> 