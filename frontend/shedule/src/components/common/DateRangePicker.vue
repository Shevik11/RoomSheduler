<template>
  <div class="date-range-picker">
    <div class="input-wrapper">
      <input
        type="date"
        v-model="startDate"
        @change="updateRange"
        class="filter-input"
        :class="{ 'has-value': startDate }"
      />
    </div>
    <span class="separator">до</span>
    <div class="input-wrapper">
      <input
        type="date"
        v-model="endDate"
        @change="updateRange"
        class="filter-input"
        :class="{ 'has-value': endDate }"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  modelValue: Object,
});

const emit = defineEmits(["update:modelValue"]);

const startDate = ref(props.modelValue?.start || "");
const endDate = ref(props.modelValue?.end || "");

const updateRange = () => {
  emit("update:modelValue", {
    start: startDate.value,
    end: endDate.value,
  });
};
</script>

<style scoped>
.date-range-picker {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-wrapper {
  position: relative;
  flex: 1;
}

.separator {
  color: #2c3e50;
  font-size: 14px;
  font-weight: 500;
}

.filter-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-left: 4px solid #e74c3c;
  border-radius: 6px;
  font-size: 14px;
  color: #2c3e50 !important;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
  height: 35px;
  transition:
    transform 0.15s,
    box-shadow 0.15s;
}

.filter-input:hover {
  transform: translateY(-4px);
  box-shadow:
    0 6px 18px 0 rgba(44, 62, 80, 0.18),
    0 1.5px 6px 0 rgba(44, 62, 80, 0.1);
}

.filter-input:focus {
  outline: none;
}

.filter-input.has-value {
  border-color: #e57373;
  box-shadow: 0 0 0 2px #e5737333;
}

/* Стилі для календаря */
.filter-input::-webkit-calendar-picker-indicator {
  cursor: pointer;
  padding: 4px;
  margin-right: 4px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.filter-input::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}
</style>
