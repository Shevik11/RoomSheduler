<template>
  <div class="filter-item">
    <label for="name_teacher">Викладач:</label>
    <AutocompleteInput
      id="name_teacher"
      v-model="teacherValue"
      placeholder="Введіть ПІБ викладача"
      :suggestions="suggestions"
      :is-loading="isLoading"
      no-results-text="Немає відповідних викладачів"
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
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | null): void;
}>();

const teacherValue: Ref<string> = ref(props.modelValue || '');
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);

watch(() => props.modelValue, (newValue: string | null) => {
  teacherValue.value = newValue || '';
});

const handleInput = async (value: string) => {
  if (!value) {
    suggestions.value = [];
    return;
  }

  isLoading.value = true;
  try {
    suggestions.value = await scheduleService.getTeacherSuggestions(value);
  } catch (error) {
    console.error('Error fetching teacher suggestions:', error);
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