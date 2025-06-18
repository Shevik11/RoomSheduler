<template>
  <div class="filter-item">
    <label for="name_room">Аудиторія:</label>
    <AutocompleteInput
      id="name_room"
      v-model="roomValue"
      placeholder="Введіть номер аудиторії"
      :suggestions="suggestions"
      :is-loading="isLoading"
      no-results-text="Немає відповідних аудиторій"
      @input="handleInput"
      @select="handleSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import type { Ref } from 'vue';
import AutocompleteInput from '../common/AutocompleteInput.vue';
import scheduleService from '../../services/scheduleService';
import type { ScheduleFilters } from '../../types/schedule';

const props = defineProps<{
  modelValue: string | null;
  filters: ScheduleFilters;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const roomValue: Ref<string> = ref(props.modelValue || '');
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);

watch(() => props.modelValue, (newValue) => {
  console.log('Model value changed:', newValue);
  roomValue.value = newValue || '';
  if (newValue) {
    handleInput(newValue);
  }
});

const handleInput = async (value: string) => {
  if (!value) {
    suggestions.value = [];
    emit('update:modelValue', null);
    return;
  }

  isLoading.value = true;
  try {
    suggestions.value = [];
    console.log('Fetching room suggestions with filters:', props.filters);
    const newSuggestions = await scheduleService.getRoomSuggestions(value, props.filters);
    console.log('Got room suggestions:', newSuggestions);
    suggestions.value = newSuggestions;
  } catch (error) {
    console.error('Error fetching room suggestions:', error);
    suggestions.value = [];
  } finally {
    isLoading.value = false;
  }
};

watch(() => props.filters, (newFilters) => {
  console.log('Filters changed:', newFilters);
  if (roomValue.value && roomValue.value.trim()) {
    nextTick(() => {
      handleInput(roomValue.value);
    });
  }
}, { deep: true, flush: 'post' });

const handleSelect = (value: string) => {
  console.log('Selected room:', value);
  emit('update:modelValue', value);
  suggestions.value = [];
};
</script>

<style scoped>
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

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-left: 4px solid #e74c3c;
  border-radius: 6px;
  font-size: 14px;
  color: #2c3e50 !important;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.filter-select:focus {
  outline: none;
}

.filter-input,
.filter-select {
  color: #2c3e50 !important;
}

.filter-input.has-value {
  border-color: #e57373;
  box-shadow: 0 0 0 2px #e5737333;
}
</style> 