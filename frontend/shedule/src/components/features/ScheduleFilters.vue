<template>
  <div class="filters-container">
    <h3>Фільтри розкладу</h3>
    <div class="filters">
      <FilterGroup
        v-model="filters.name_group"
        :filtered-items="filteredGroups"
        :is-fetching="isFetchingGroups"
        @input="(value) => handleGroupInput(value, filters)"
        @select="handleGroupSelect"
      />

      <FilterSubgroup
        v-model="filters.number_of_subgroup"
      />

      <FilterDayOfWeek
        v-model="filters.day_of_week"
      />

      <FilterNominator
        v-model="filters.nominator"
      />

      <FilterParaNumber
        v-model="filters.namb_of_para"
      />

      <FilterSubject
        v-model="filters.name_of_para"
        :filtered-items="filteredSubjects"
        :is-fetching="isFetchingSubjects"
        @input="(value) => handleSubjectInput(value, filters)"
        @select="selectSubject"
      />

      <FilterRoom
        v-model="filters.room"
        :filtered-items="filteredRooms"
        :is-fetching="isFetchingRooms"
        :group-name="filters.name_group"
        @input="(value) => handleRoomInput(value, filters)"
        @select="selectRoom"
      />

      <FilterTeacher
        v-model="filters.teacher"
        :filtered-items="filteredTeachers"
        :is-fetching="isFetchingTeachers"
        @input="(value) => handleTeacherInput(value, filters)"
        @select="selectTeacher"
      />

      <FilterBusy
        v-model="filters.busy"
        @update:modelValue="handleBusyChange"
      />

      <!-- Button to reset filters -->
      <div class="filter-buttons">
        <button @click="resetFilters" class="reset-button">Скинути фільтри</button>
        <button @click="applyFilters" class="apply-button">Застосувати</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { DEFAULT_FILTERS } from '../../constants/schedule';
import { useFilters } from '../../composables/useFilters';
import type { ScheduleFilters } from '../../types/schedule';
import FilterGroup from '../filters/FilterGroup.vue';
import FilterSubgroup from '../filters/FilterSubgroup.vue';
import FilterDayOfWeek from '../filters/FilterDayOfWeek.vue';
import FilterNominator from '../filters/FilterNominator.vue';
import FilterParaNumber from '../filters/FilterParaNumber.vue';
import FilterSubject from '../filters/FilterSubject.vue';
import FilterRoom from '../filters/FilterRoom.vue';
import FilterTeacher from '../filters/FilterTeacher.vue';
import FilterBusy from '../filters/FilterBusy.vue';

const props = defineProps<{
  modelValue: ScheduleFilters;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: ScheduleFilters): void;
  (e: 'apply'): void;
}>();

const filters = ref<ScheduleFilters>({ ...props.modelValue });

const {
  filteredGroups,
  isFetchingGroups,
  filteredSubjects,
  isFetchingSubjects,
  filteredRooms,
  isFetchingRooms,
  filteredTeachers,
  isFetchingTeachers,
  handleGroupInput,
  handleSubjectInput,
  handleRoomInput,
  handleTeacherInput
} = useFilters();

// Handlers for selection
const handleGroupSelect = (group: string) => {
  filters.value.name_group = group;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectSubject = (subject: string) => {
  filters.value.name_of_para = subject;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectRoom = (room: string) => {
  filters.value.room = room;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectTeacher = (teacher: string) => {
  filters.value.teacher = teacher;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Handler for change in occupation status
const handleBusyChange = () => {
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Reset filters
const resetFilters = () => {
  filters.value = { ...DEFAULT_FILTERS };
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Apply filters
const applyFilters = () => {
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Look for changes in the parent component
watch(() => props.modelValue, (newValue) => {
  filters.value = { ...newValue };
}, { deep: true });
</script>

<style scoped>
.filters-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  align-items: flex-start;
}

.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: stretch;
  padding: 0 8px;
}

.reset-button, .apply-button {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: background-color 0.2s;
  width: 100%;
  color: inherit;
  text-align: center;
  display: block;
}

.reset-button {
  background-color: #e0e0e0;
  color: #505050;
}

.apply-button {
  background-color: #4a90e2;
  color: white;
}

.reset-button:hover {
  background-color: #d0d0d0;
}

.apply-button:hover {
  background-color: #3a80d2;
}

.filter-input,
.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  color: #222 !important;
}
</style> 