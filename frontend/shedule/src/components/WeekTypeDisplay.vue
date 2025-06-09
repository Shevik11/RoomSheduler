<script setup>
import { ref, onMounted } from 'vue'
import httpClient from '../services/httpClient'

const weekType = ref(null)
const weekStart = ref(null)
const weekEnd = ref(null)

onMounted(() => {
     console.log('onMounted WeekTypeDisplay');
     fetchWeekType();
   });

   const fetchWeekType = async () => {
     try {
       const response = await httpClient.get('/week-type');
       console.log('week-type response', response.data);
       weekType.value = response.data.week_type;
       weekStart.value = response.data.week_start;
       weekEnd.value = response.data.week_end;
     } catch (error) {
       console.error('Error fetching week type:', error);
     }
   }
</script>

<template>
  <div>
    <div class="week-type-display" v-if="weekType">
      <span class="label">Поточний тиждень:</span>
      <span class="week-type-badge">{{ weekType }}</span>
      <span class="week-dates">{{ weekStart }} – {{ weekEnd }}</span>
    </div>
  </div>
</template>

<style scoped>
.week-type-display {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.4rem 1rem;
  background-color: #fafbfc;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 1rem;
  font-weight: 500;
}
.label {
  color: #222;
  font-weight: 500;
  margin-right: 0.4rem;
  font-size: 1em;
}
.week-type-badge {
  background: #fff;
  color: #222;
  border: 1px solid #e0e0e0;
  border-radius: 14px;
  padding: 0.15em 0.8em;
  font-weight: 600;
  font-size: 1em;
  margin-right: 0.7rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.week-dates {
  color: #888;
  font-size: 0.95em;
  font-weight: 400;
}
</style>