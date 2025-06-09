<template>
  <div class="filters-container">
    <h3>Фільтри розкладу</h3>
    <div class="filters">
      <FilterGroup v-model="filters.name_group" />
      
      <div class="filter-item">
        <label for="number_of_subgroup">Підгрупа:</label>
        <select 
          id="number_of_subgroup"
          v-model="filters.number_of_subgroup" 
          class="filter-select"
        >
          <option :value="null">Всі підгрупи</option>
          <option :value="1">1</option>
          <option :value="2">2</option>
        </select>
      </div>

      <div class="filter-item">
        <label for="day_of_week">День тижня:</label>
        <select 
          id="day_of_week"
          v-model="filters.day_of_week" 
          class="filter-select"
        >
          <option :value="null">Всі дні</option>
          <option v-for="day in DAYS_OF_WEEK" :key="day" :value="day">{{ day }}</option>
        </select>
      </div>

      <div class="filter-item">
        <label for="nominator">Тип тижня:</label>
        <select 
          id="nominator"
          v-model="filters.nominator" 
          class="filter-select"
        >
          <option :value="null">Будь-який</option>
          <option value="Чисельник">Чисельник</option>
          <option value="Знаменник">Знаменник</option>
        </select>
      </div>

      <div class="filter-item">
        <label for="namb_of_para">Номер пари:</label>
        <select 
          id="namb_of_para"
          v-model="filters.namb_of_para" 
          class="filter-select"
        >
          <option :value="null">Всі пари</option>
          <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
        </select>
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

      <div class="filter-item">
        <label for="busy">Статус:</label>
        <select 
          id="busy"
          v-model="filters.busy" 
          class="filter-select"
          @change="handleBusyChange"
        >
          <option :value="null">Всі</option>
          <option :value="true">Зайняті</option>
          <option :value="false">Вільні</option>
        </select>
      </div>

      <div class="filter-buttons">
        <button @click="resetFilters" class="reset-button">Скинути фільтри</button>
        <button @click="applyFilters" class="apply-button">Застосувати</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { DAYS_OF_WEEK, DEFAULT_FILTERS } from '../../constants/schedule';
import type { ScheduleFilters } from '../../types/schedule.ts';
import FilterGroup from '../filters/FilterGroup.vue';
import FilterSubject from '../filters/FilterSubject.vue';
import FilterTeacher from '../filters/FilterTeacher.vue';
import FilterRoom from '../filters/FilterRoom.vue';

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
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

h3 {
  margin-bottom: 1rem;
  color: #333;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.filter-item {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.filter-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: white;
}

.filter-buttons {
  grid-column: 1 / -1;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.reset-button,
.apply-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.reset-button {
  background-color: #f0f0f0;
  color: #333;
}

.apply-button {
  background-color: #4CAF50;
  color: white;
}

.reset-button:hover {
  background-color: #e0e0e0;
}

.apply-button:hover {
  background-color: #45a049;
}
</style> 