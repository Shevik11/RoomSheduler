<template>
  <div class="filter-item">
    <label for="name_subject">Предмет:</label>
    <AutocompleteInput
      id="name_subject"
      v-model="subjectValue"
      placeholder="Введіть назву предмету"
      :suggestions="suggestions"
      :is-loading="isLoading"
      no-results-text="Немає відповідних предметів"
      @input="handleInput"
      @select="handleSelect"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import type { Ref } from "vue";
import AutocompleteInput from "../common/AutocompleteInput.vue";
import scheduleService from "../../services/scheduleService";
import type { ScheduleFilters } from "../../types/schedule";
import { debounce } from "../../utils/debounce";

const props = defineProps<{
  modelValue: string | null;
  filters: ScheduleFilters;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string | null];
}>();

const subjectValue: Ref<string> = ref(props.modelValue || "");
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);

watch(
  () => props.modelValue,
  (newValue: string | null) => {
    subjectValue.value = newValue || "";
  },
);

const debouncedSearch = debounce(async (query: string) => {
  if (!query) {
    suggestions.value = [];
    return;
  }

  isLoading.value = true;
  try {
    suggestions.value = await scheduleService.getSubjectSuggestions(
      query,
      props.filters,
    );
  } catch (error) {
    console.error("Error fetching subject suggestions:", error);
    suggestions.value = [];
  } finally {
    isLoading.value = false;
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
