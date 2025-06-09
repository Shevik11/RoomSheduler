<template>
  <div class="filter-item">
    <label for="teacher">Викладач:</label>
    <div class="autocomplete-container">
      <input 
        id="teacher"
        :value="modelValue"
        @input="handleInput" 
        placeholder="Введіть ім'я викладача"
        class="filter-input"
        @focus="showSuggestions = true"
        @blur="handleBlur"
        autocomplete="off"
      />
      <div v-if="showSuggestions" class="suggestions-list">
        <div v-if="isFetching" class="suggestion-item loading">
          Завантаження...
        </div>
        <template v-else>
          <div v-if="filteredItems.length === 0" class="suggestion-item no-results">
            Немає відповідних викладачів
          </div>
          <div 
            v-for="item in filteredItems" 
            :key="item"
            class="suggestion-item"
            @mousedown.prevent="selectItem(item)"
          >
            {{ item }}
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  modelValue: string;
  filteredItems: string[];
  isFetching: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'input', value: string): void;
  (e: 'select', value: string): void;
}>();

const showSuggestions = ref(false);

const handleInput = (event: Event) => {
  const input = (event.target as HTMLInputElement).value;
  emit('update:modelValue', input);
  emit('input', input);
  showSuggestions.value = true;
};

const selectItem = (item: string) => {
  emit('update:modelValue', item);
  emit('select', item);
  showSuggestions.value = false;
};

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
};
</script>

<style scoped>
.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
  padding: 0 8px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 14px;
  color: #505050;
}

.filter-input,
.filter-select {
  color: #222 !important;
}

.filter-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.filter-input:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.autocomplete-container {
  position: relative;
  width: 100%;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #f0f4f8;
}

.suggestion-item.loading {
  color: #666;
  font-style: italic;
  cursor: default;
}

.suggestion-item.loading:hover {
  background-color: transparent;
}

.suggestion-item.no-results {
  color: #666;
  font-style: italic;
  cursor: default;
}

.suggestion-item.no-results:hover {
  background-color: transparent;
}
</style> 