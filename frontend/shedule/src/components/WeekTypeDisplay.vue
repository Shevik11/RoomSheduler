<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import httpClient from '../services/httpClient'

const weekType = ref<string | null>(null)
const weekStart = ref<string | null>(null)
const weekEnd = ref<string | null>(null)
const isEditing = ref(false)
const tempStart = ref<string | null>(null)
const tempEnd = ref<string | null>(null)
const dateRange = ref({
  start: '',
  end: ''
})

const emit = defineEmits(['update:weekType'])

onMounted(() => {
  console.log('onMounted WeekTypeDisplay')
  fetchWeekType()
})

const fetchWeekType = async (start: string | null = null, end: string | null = null) => {
  try {
    if (start && end) {
      console.log('Sending request for custom dates:', { start, end })
      const response = await httpClient.get(`/week-type/range?start_date=${start}&end_date=${end}`)
      console.log('Custom date range response:', response.data)
      if (response.data.week_type) {
        const newWeekType = convertWeekType(response.data.week_type)
        if (newWeekType !== weekType.value) {
          weekType.value = newWeekType
          weekStart.value = response.data.week_start
          weekEnd.value = response.data.week_end
          console.log('Emitting new week type:', weekType.value)
          emit('update:weekType', weekType.value)
        }
      }
    } else {
      console.log('Fetching current week type')
      const response = await httpClient.get('/week-type')
      console.log('Current week response:', response.data)
      const newWeekType = convertWeekType(response.data.week_type)
      if (newWeekType !== weekType.value) {
        weekType.value = newWeekType
        weekStart.value = response.data.week_start
        weekEnd.value = response.data.week_end
        console.log('Emitting new week type:', weekType.value)
        emit('update:weekType', weekType.value)
      }
    }
  } catch (error: any) {
    console.error('Error fetching week type:', error)
    console.error('Error details:', error.response?.data)
  }
}

const convertWeekType = (type: string): string => {
  if (type === 'Чисельник') return 'nominator'
  if (type === 'Знаменник') return 'denominator'
  return type
}

const startEditing = () => {
  tempStart.value = weekStart.value
  tempEnd.value = weekEnd.value
  isEditing.value = true
}

const handleDateChange = () => {
  if (tempStart.value && tempEnd.value) {
    const start = new Date(tempStart.value)
    const end = new Date(tempEnd.value)
    
    if (start > end) {
      console.error('Start date cannot be later than end date')
      return
    }
    
    console.log('Date range selected:', { 
      start: tempStart.value, 
      end: tempEnd.value 
    })
    fetchWeekType(tempStart.value, tempEnd.value)
    isEditing.value = false
  }
}

const cancelEditing = () => {
  isEditing.value = false
  tempStart.value = weekStart.value
  tempEnd.value = weekEnd.value
}

const weekTypeDisplay = computed(() => {
  if (weekType.value === 'nominator') return 'Чисельник'
  if (weekType.value === 'denominator') return 'Знаменник'
  return weekType.value
})
</script>

<template>
  <div>
    <div class="week-type-display" v-if="weekType">
      <div class="week-info">
        <span class="label">Поточний тиждень:</span>
        <span class="week-type-badge">{{ weekTypeDisplay }}</span>
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
  padding: 1.2rem 1.5rem;
  background-color: #ffffff;
  border-radius: 10px;
  margin: 1rem 0;
  font-size: 1rem;
  font-weight: 500;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
}

.week-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.label {
  color: #2c3e50;
  font-weight: 600;
  margin-right: 0.4rem;
  font-size: 1em;
}

.week-type-badge {
  background-color: transparent;
  color: #2c3e50;
  padding: 0.15em 0.8em;
  font-size: 0.95rem;
  font-weight: 600;
  margin-right: 0.3rem;
  margin-left: -1.4rem;
  text-shadow: 
    0 0 1px rgba(44, 62, 80, 0.3);
  transition: all 0.2s;
}

.week-dates {
  color: #2c3e50;
  font-size: 0.95em;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dates-text {
  cursor: pointer;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  transition: all 0.2s;
  border: 1px solid #e0e0e0;
  border-left: 4px solid #d32f2f;
  background: #fff;
}

.dates-text:hover {
  background-color: #f8f9fa;
  border-color: #e74c3c;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.edit-icon, .cancel-icon {
  font-size: 0.9em;
  opacity: 0.7;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 6px;
  transition: all 0.2s;
  color: #2c3e50;
}

.edit-icon:hover, .cancel-icon:hover {
  background-color: #f8f9fa;
  opacity: 1;
  color: #e74c3c;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.separator {
  color: #2c3e50;
  margin: 0 0.2rem;
  font-weight: 500;
}

.date-input {
  padding: 0.3rem 0.6rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.95em;
  width: 130px;
  color: #2c3e50;
  transition: all 0.2s;
}

.date-input:hover {
  border-color: #e74c3c;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.date-input:focus {
  outline: none;
  border-color: #e74c3c;
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.15);
}

.filters {
  width: 100%;
  max-width: 650px;
  margin: 0 auto;
}

/* Адаптивні стилі для менших екранів */
@media (max-width: 768px) {
  .week-type-display {
    padding: 1rem;
    margin: 0.75rem 0;
  }
  
  .week-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .label {
    font-size: 0.95rem;
    margin-right: 0;
  }
  
  .week-type-badge {
    font-size: 0.9rem;
    margin-left: 0;
  }
  
  .week-dates {
    font-size: 0.9rem;
    width: 100%;
    justify-content: space-between;
  }
  
  .dates-text {
    flex: 1;
    text-align: center;
  }
  
  .date-input {
    width: 120px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .week-type-display {
    padding: 0.75rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
  }
  
  .week-info {
    gap: 0.5rem;
  }
  
  .label {
    font-size: 0.9rem;
  }
  
  .week-type-badge {
    font-size: 0.85rem;
  }
  
  .week-dates {
    font-size: 0.85rem;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }
  
  .dates-text {
    width: 100%;
    text-align: center;
    padding: 0.25rem 0.5rem;
  }
  
  .date-input {
    width: 100%;
    font-size: 0.85rem;
    padding: 0.25rem 0.5rem;
  }
  
  .separator {
    display: none;
  }
  
  .edit-icon, .cancel-icon {
    font-size: 0.8rem;
    padding: 0.25rem;
  }
}
</style>