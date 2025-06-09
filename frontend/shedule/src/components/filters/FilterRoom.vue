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
import { ref, watch } from 'vue';
import type { Ref } from 'vue';
import AutocompleteInput from '../common/AutocompleteInput.vue';
import scheduleService from '../../services/scheduleService';

const props = defineProps<{
  modelValue: string | null;
  filters: {
    name_group: string;
    number_of_subgroup: number | null;
    day_of_week: string | null;
    nominator: string | null;
    namb_of_para: number | null;
    name_of_para: string;
    room: string;
    teacher: string;
    busy: boolean | null;
  };
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const roomValue: Ref<string> = ref(props.modelValue || '');
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);

watch(() => props.modelValue, (newValue: string | null) => {
  roomValue.value = newValue || '';
});

const handleInput = async (value: string) => {
  if (!value) {
    suggestions.value = [];
    return;
  }

  isLoading.value = true;
  try {
    suggestions.value = await scheduleService.getRoomSuggestions(value, props.filters);
  } catch (error) {
    console.error('Error fetching room suggestions:', error);
    suggestions.value = [];
  } finally {
    isLoading.value = false;
  }
};

const handleSelect = (value: string) => {
  emit('update:modelValue', value);
};
</script>

<style scoped>
.filter-item {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
</style> 