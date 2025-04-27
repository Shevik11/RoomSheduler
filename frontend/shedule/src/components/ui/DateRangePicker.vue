<template>
    <div class="date-range-picker">
      <input type="date" v-model="startDate" @change="updateRange">
      <span>до</span>
      <input type="date" v-model="endDate" @change="updateRange">
    </div>
  </template>
  
  <script setup>
  import { ref, defineEmits, defineProps } from 'vue'
  
  const props = defineProps({
    modelValue: Object
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  const startDate = ref(props.modelValue?.start || '')
  const endDate = ref(props.modelValue?.end || '')
  
  const updateRange = () => {
    emit('update:modelValue', {
      start: startDate.value,
      end: endDate.value
    })
  }
  </script>
  
  <style scoped>
  .date-range-picker {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .date-range-picker input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  </style>