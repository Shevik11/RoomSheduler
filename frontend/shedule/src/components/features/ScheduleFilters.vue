<template>
  <div class="filters-container">
    <h3>Фільтри розкладу</h3>
    <div class="filters">
      <FilterGroup v-model="filters.name_group" />
      <FilterSubgroup v-model="filters.number_of_subgroup" />
      <FilterDayOfWeek v-model="filters.day_of_week" />
      <FilterNominator v-model="filters.nominator" />
      <FilterParaNumber v-model="filters.namb_of_para" />
      <div class="filter-buttons">
        <button @click="resetFilters" class="reset-button">Скинути фільтри</button>
        <button @click="applyFilters" class="apply-button">Застосувати</button>
      </div>
      <FilterSubject 
        v-model="filters.name_of_para"
        :group="filters.name_group"
      />
      <FilterRoom 
        v-model="filters.room"
        :filters="filters"
      />
      <FilterTeacher 
        v-model="filters.teacher"
        :group="filters.name_group"
        :subject="filters.name_of_para"
      />
      <FilterBusy 
        v-model="filters.busy"
        @change="handleBusyChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { DAYS_OF_WEEK, DEFAULT_FILTERS } from '../../constants/schedule';
import type { ScheduleFilters } from '../../types/schedule.ts';
import {
  FilterGroup,
  FilterSubject,
  FilterTeacher,
  FilterRoom,
} from '../filters';
import FilterBusy from '../filters/FilterBusy.vue';
import FilterDayOfWeek from '../filters/FilterDayOfWeek.vue';
import FilterNominator from '../filters/FilterNominator.vue';
import FilterParaNumber from '../filters/FilterParaNumber.vue';
import FilterSubgroup from '../filters/FilterSubgroup.vue';

const props = defineProps<{
  modelValue: ScheduleFilters;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: ScheduleFilters): void;
  (e: 'apply'): void;
}>();

const filters = ref<ScheduleFilters>({ ...props.modelValue });

watch(() => props.modelValue, (newValue) => {
  filters.value = { ...newValue };
});

const handleBusyChange = () => {
  if (filters.value.busy === true) {
    filters.value.room = '';
  }
};

const resetFilters = () => {
  filters.value = { ...DEFAULT_FILTERS };
  emit('update:modelValue', filters.value);
};

const applyFilters = () => {
  emit('update:modelValue', filters.value);
  emit('apply');
};
</script>

<style scoped>
.filters-container {
  padding: 1.5rem;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  margin: 1rem 0;
  width: 100%;
  max-width: 1200px;
}
h3 {
  margin-bottom: 1.5rem;
  color: #1a1a1a;
  font-size: 1.5rem;
  font-weight: 600;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.75rem;
  text-align: center; /* Center the heading text */
}

.filters {
  display: grid;
  grid-template-columns: repeat(5, minmax(200px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem;
  align-items: start;
  justify-items: center;
  width: 100%;
}

.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  grid-column: 5 / 6;
  grid-row: 2;
  justify-self: center;
  align-self: center;
  margin: 0;
  padding: 0;
  border: none;
  width: 100%;
}

.filter-item {
  margin-bottom: 0.5rem;
  width: 100%;
  min-width: 200px;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
  font-size: 0.95rem;
  text-align: center; /* Center the label text */
}

.filter-select, select {
  width: 100%;
  padding: 10px 36px 10px 12px;
  border: 1.5px solid #d32f2f;
  border-radius: 8px;
  background-color: #fff;
  color: #2c3e50;
  font-size: 15px;
  font-weight: 500;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='16' height='10' viewBox='0 0 16 10' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2 2L8 8L14 2' stroke='%23d32f2f' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem top 55%;
  background-size: 1.2rem auto;
  box-shadow: 0 2px 8px rgba(211,47,47,0.08);
  outline: none;
  box-sizing: border-box;
  height: 40px;
  background-clip: padding-box;
}

select::-ms-expand {
  display: none;
}

/* Safari/Edge/IE: прибираємо стандартний outline і квадратність */
select:focus-visible {
  outline: none;
}

/* Додаємо плавне заокруглення для стрілки */
.filter-select, select {
  border-radius: 8px;
}

/* Для Firefox: прибираємо квадратність */
select:-moz-focusring {
  color: transparent;
  text-shadow: 0 0 0 #2c3e50;
}

/* Style for options within the select dropdown */
select option, .filter-select option {
  font-weight: 500;
  color: #2c3e50;
  background: #fff;
  padding: 8px;
}

/* Style for options when hovered */
select option:hover, .filter-select option:hover {
  background-color: #f5f5f5;
}

/* Style for options when selected */
select option:checked, .filter-select option:checked {
  background-color: #e0e0e0;
}

.reset-button,
.apply-button {
  padding: 0.4rem 0.8rem;
  min-width: 90px;
  font-size: 0.95rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.reset-button {
  background-color: #fff;
  color: #d32f2f;
  border: 1.5px solid #d32f2f;
}

.apply-button {
  background-color: #d32f2f;
  color: #fff;
  border: 1.5px solid #d32f2f;
}

.reset-button:hover {
  background-color: #ffeaea;
  border-color: #b71c1c;
  color: #b71c1c;
}

.apply-button:hover {
  background-color: #b71c1c;
  border-color: #b71c1c;
}

.reset-button:focus,
.apply-button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.15);
}

.reset-button:active {
  background-color: #ffd6d6;
  border-color: #b71c1c;
  color: #b71c1c;
}

.apply-button:active {
  background-color: #a31515;
  border-color: #a31515;
}

@media (max-width: 1200px) {
  .filters {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .filters {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .filters {
    grid-template-columns: 1fr;
  }
}
</style>