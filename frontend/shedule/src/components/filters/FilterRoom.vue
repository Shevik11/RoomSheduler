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

const roomValue: Ref<string> = ref(props.modelValue || "");
const suggestions: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);
const justSelected: Ref<boolean> = ref(false);

watch(
  () => props.modelValue,
  (newValue) => {
    console.log("Model value changed:", newValue);
    roomValue.value = newValue || "";
    if (newValue) {
      handleInput(newValue);
    }
  },
);


const debouncedSearch = debounce(async (query: string) => {
  if (!query) {
    suggestions.value = [];
    emit("update:modelValue", null);
    return;
  }

  if (justSelected.value) {
    justSelected.value = false;
    return;
  }

  isLoading.value = true;
  try {
    suggestions.value = [];
    console.log("Fetching room suggestions with filters:", props.filters);
    const newSuggestions = await scheduleService.getRoomSuggestions(
      query,
      props.filters,
    );
    console.log("Got room suggestions:", newSuggestions);
    suggestions.value = newSuggestions;
  } catch (error) {
    console.error("Error fetching room suggestions:", error);
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
  console.log("Selected room:", value);
  justSelected.value = true;
  roomValue.value = value;
  emit("update:modelValue", value);
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
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
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
