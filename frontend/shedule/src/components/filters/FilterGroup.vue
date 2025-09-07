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
import { ref, watch } from "vue";
import type { Ref } from "vue";
import AutocompleteInput from "../common/AutocompleteInput.vue";
import { debounce } from "../../utils/debounce";
import groupService from "../../services/groupService";

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const groupValue: Ref<string> = ref(props.modelValue || "");
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);
const showSuggestions = ref(false);
const isFetching = ref(false);

watch(
  () => props.modelValue,
  (newValue: string | null) => {
    groupValue.value = newValue || "";
  },
);

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
    console.error("Error fetching group suggestions:", error);
    suggestions.value = [];
  } finally {
    isFetching.value = false;
  }
}, 150); 

const handleInput = (value: string) => {
  emit("update:modelValue", value);
  debouncedSearch(value);
};

const handleSelect = (value: string) => {
  emit("update:modelValue", value);
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
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.filter-select:focus {
  outline: none;
}

.filter-input,
.filter-select {
  color: #2c3e50 !important;
}
</style>
