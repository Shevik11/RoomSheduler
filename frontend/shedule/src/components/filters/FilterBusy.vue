<template>
  <div class="filter-item select-wrapper">
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

const emit = defineEmits<(e: "update:modelValue", value: boolean | null) => void>();

const handleInput = (event: Event) => {
  const value = (event.target as HTMLSelectElement).value;
  emit("update:modelValue", value === "" ? null : value === "true");
};
</script>

<style scoped>
@import "./dropdown-filter.css";
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
