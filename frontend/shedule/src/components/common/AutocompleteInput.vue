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
      :class="{ 'has-value': hasValue }"
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
import { ref, watch, computed } from 'vue';

const props = defineProps<{
  id: string;
  modelValue: string;
  placeholder: string;
  suggestions: string[];
  isLoading: boolean;
  noResultsText: string;
  hasValue?: boolean;
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
  showSuggestions.value = true;
};

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 300);
};

watch(() => props.suggestions, (newSuggestions) => {
  if (newSuggestions.length > 0) {
    showSuggestions.value = true;
  }
});

const selectItem = (item: string) => {
  inputValue.value = item;
  emit('update:modelValue', item);
  emit('select', item);
  showSuggestions.value = false;
};

const hasValue = computed(() => !!inputValue.value);
</script>

<style scoped>
.autocomplete-container {
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

.filter-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-left: 4px solid #e74c3c;
  border-radius: 6px;
  font-size: 14px;
  color: #2c3e50;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  box-sizing: border-box;
  height: 35px;
}

.filter-input:focus {
  outline: none;
}

.filter-input.has-value {
  border-color: #e57373;
  box-shadow: 0 0 0 2px #e5737333;
}

.suggestions-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  color: #2c3e50;
  font-size: 14px;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
}

.suggestion-item.loading,
.suggestion-item.no-results {
  color: #666;
  cursor: default;
}
</style> 