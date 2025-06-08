<template>
  <div class="autocomplete-container">
    <input 
      :id="id"
      v-model="inputValue" 
      @input="handleInput" 
      :placeholder="placeholder"
      class="filter-input"
      @focus="showSuggestions = true"
      @blur="handleBlur"
      autocomplete="off"
    />
    <div v-if="showSuggestions" class="suggestions-list">
      <div v-if="isLoading" class="suggestion-item loading">
        Завантаження...
      </div>
      <template v-else>
        <div v-if="suggestions.length === 0" class="suggestion-item no-results">
          {{ noResultsText }}
        </div>
        <div 
          v-for="item in suggestions" 
          :key="item"
          class="suggestion-item"
          @mousedown.prevent="selectItem(item)"
        >
          {{ item }}
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  id: string;
  modelValue: string;
  placeholder: string;
  suggestions: string[];
  isLoading: boolean;
  noResultsText: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'select', value: string): void;
  (e: 'input', value: string): void;
}>();

const inputValue = ref(props.modelValue);
const showSuggestions = ref(false);

watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue;
});

const handleInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value;
  inputValue.value = value;
  emit('update:modelValue', value);
  emit('input', value);
};

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
};

const selectItem = (item: string) => {
  inputValue.value = item;
  emit('update:modelValue', item);
  emit('select', item);
  showSuggestions.value = false;
};
</script>

<style scoped>
.autocomplete-container {
  position: relative;
  width: 100%;
}

.filter-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

.suggestion-item {
  padding: 8px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f0f0f0;
}

.suggestion-item.loading,
.suggestion-item.no-results {
  color: #666;
  cursor: default;
}
</style> 