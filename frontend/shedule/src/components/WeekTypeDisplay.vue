<script setup>
import { ref, onMounted } from 'vue'
import httpClient from '../services/httpClient'

const weekType = ref(null)
const weekStart = ref(null)
const weekEnd = ref(null)
const isEditing = ref(false)
const tempStart = ref('')
const tempEnd = ref('')

onMounted(() => {
  console.log('onMounted WeekTypeDisplay');
  fetchWeekType();
});

const fetchWeekType = async (start = null, end = null) => {
  try {
    if (start && end) {
      console.log('Sending request for custom dates:', { start, end });
      const response = await httpClient.get(`/week-type/range?start_date=${start}&end_date=${end}`);
      console.log('Custom date range response:', response.data);
      if (response.data.week_type) {
        weekType.value = response.data.week_type;
        weekStart.value = response.data.week_start;
        weekEnd.value = response.data.week_end;
      }
    } else {
      console.log('Fetching current week type');
      const response = await httpClient.get('/week-type');
      console.log('Current week response:', response.data);
      weekType.value = response.data.week_type;
      weekStart.value = response.data.week_start;
      weekEnd.value = response.data.week_end;
    }
  } catch (error) {
    console.error('Error fetching week type:', error);
    console.error('Error details:', error.response?.data);
  }
}

const startEditing = () => {
  tempStart.value = weekStart.value;
  tempEnd.value = weekEnd.value;
  isEditing.value = true;
}

const handleDateChange = () => {
  if (tempStart.value && tempEnd.value) {
    const start = new Date(tempStart.value);
    const end = new Date(tempEnd.value);
    
    if (start > end) {
      console.error('Start date cannot be later than end date');
      return;
    }
    
    console.log('Date range selected:', { 
      start: tempStart.value, 
      end: tempEnd.value 
    });
    fetchWeekType(tempStart.value, tempEnd.value);
    isEditing.value = false;
  }
}

const cancelEditing = () => {
  isEditing.value = false;
  tempStart.value = weekStart.value;
  tempEnd.value = weekEnd.value;
}
</script>

<template>
  <div>
    <div class="week-type-display" v-if="weekType">
      <div class="week-info">
        <span class="label">Поточний тиждень:</span>
        <span class="week-type-badge">{{ weekType }}</span>
        <div class="week-dates">
          <template v-if="!isEditing">
            <span class="dates-text" @click="startEditing">{{ weekStart }} – {{ weekEnd }}</span>
            <span class="edit-icon" @click="startEditing">✎</span>
          </template>
          <template v-else>
            <input 
              type="date" 
              v-model="tempStart" 
              @change="handleDateChange"
              class="date-input"
            >
            <span class="separator">–</span>
            <input 
              type="date" 
              v-model="tempEnd" 
              @change="handleDateChange"
              class="date-input"
            >
            <span class="cancel-icon" @click="cancelEditing">✕</span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.week-type-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.8rem 1rem;
  background-color: #fafbfc;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 1rem;
  font-weight: 500;
}

.week-info {
  display: flex;
  align-items: center;
  gap: 1rem;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dates-text {
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.dates-text:hover {
  background-color: #f0f0f0;
}

.edit-icon, .cancel-icon {
  font-size: 0.9em;
  opacity: 0.6;
  cursor: pointer;
  padding: 0.2rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.edit-icon:hover, .cancel-icon:hover {
  background-color: #f0f0f0;
  opacity: 0.8;
}

.separator {
  color: #888;
  margin: 0 0.2rem;
}

.date-input {
  padding: 0.2rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 0.9em;
  width: 130px;
}

.date-input:focus {
  outline: none;
  border-color: #999;
}
</style>