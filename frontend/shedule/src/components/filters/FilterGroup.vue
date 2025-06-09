<template>
  <div class="filter-item">
    <label for="name_group">Група:</label>
    <AutocompleteInput
      id="name_group"
      v-model="groupValue"
      placeholder="Введіть назву групи"
      :suggestions="suggestions"
      :is-loading="isLoading"
      no-results-text="Немає відповідних груп"
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
import { debounce } from '../../utils/debounce';
import groupService from '../../services/groupService';

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const groupValue: Ref<string> = ref(props.modelValue || '');
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);
const showSuggestions = ref(false);
const isFetching = ref(false);

watch(() => props.modelValue, (newValue: string | null) => {
  groupValue.value = newValue || '';
});

// Створюємо дебаунсовану функцію пошуку
const debouncedSearch = debounce(async (query: string) => {
  if (!query) {
    suggestions.value = [];
    return;
  }

  isFetching.value = true;
  try {
    suggestions.value = await groupService.getGroupSuggestions(query);
  } catch (error) {
    console.error('Error fetching group suggestions:', error);
    suggestions.value = [];
  } finally {
    isFetching.value = false;
  }
}, 300); // 300ms затримка

const handleInput = (value: string) => {
  emit('update:modelValue', value);
  debouncedSearch(value);
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