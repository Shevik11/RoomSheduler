<template>
  <!-- Filters section -->
  <ScheduleFiltersComponent
    v-model="filters"
    :default-nominator="props.defaultNominator"
    @apply="fetchData"
  />

  <!-- Message about error -->
  <div v-if="error" class="error">
    <i class="error-icon">⚠️</i>
    <p>{{ error }}</p>
  </div>

  <!-- Message about missing filters -->
  <div v-if="!loading && !error && !hasSelectedFilters" class="no-data">
    <i class="no-data-icon">🔍</i>
    <p>Виберіть фільтр для відображення розкладу</p>
  </div>

  <!-- Message about missing data -->
  <div v-if="!loading && !error && hasSelectedFilters && !hasData" class="no-data">
    <i class="no-data-icon">📭</i>
    <p>Немає даних, що відповідають заданим фільтрам</p>
  </div>

  <!-- Display schedule -->
  <ScheduleDisplay
    v-if="!loading && !error && hasSelectedFilters && hasData"
    :schedule-data="scheduleData"
    :show-free-schedule-grid="showFreeScheduleGrid"
  />
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { DEFAULT_FILTERS } from '../../constants/schedule';
import { useScheduleApi } from '../../composables/useScheduleApi';
import type { ScheduleFilters, ScheduleItem, RoomSchedule } from '../../types/schedule';
import ScheduleFiltersComponent from './ScheduleFilters.vue';
import ScheduleDisplay from './ScheduleDisplay.vue';
import httpClient from '../../services/httpClient';

const props = defineProps<{
  defaultNominator: string | null;
}>();

// States
const scheduleData = ref<ScheduleItem[]>([]);
const showFreeScheduleGrid = ref(false);
const roomScheduleData = ref<RoomSchedule | null>(null);
const filters = ref<ScheduleFilters>({ ...DEFAULT_FILTERS });
const weekType = ref<string | null>(null);

// Use composable for API work
const { loading, error, fetchSchedule, fetchRoomSchedule, fetchFreeSlots } = useScheduleApi();

// Check if there is any data
const hasData = computed(() => {
  return scheduleData.value.length > 0 || (roomScheduleData.value && Object.keys(roomScheduleData.value).length > 0);
});

// Check if any filters are selected
const hasSelectedFilters = computed(() => {
  const f = filters.value;
  return f.name_group !== '' || 
         f.number_of_subgroup !== null || 
         f.day_of_week !== null || 
         f.nominator !== null || 
         f.namb_of_para !== null || 
         f.name_of_para !== '' || 
         f.room !== '' || 
         f.teacher !== '' || 
         f.busy !== null;
});

// Load data
const fetchData = async () => {
  try {
    if (filters.value.busy === false && filters.value.room) {
      const data = await fetchRoomSchedule(filters.value.room);
      if (data) {
        roomScheduleData.value = data;
        // Create scheduleData for free periods
        const freePeriodsData: ScheduleItem[] = [];
        for (const day in data) {
          data[day].forEach(para => {
            if (para.status === 'Вільно') {
              freePeriodsData.push({
                day_of_week: day,
                namb_of_para: para.para,
                time_of_para: para.time,
                name_of_para: 'Вільно',
                room: filters.value.room,
                teacher: '',
                number_of_subgroup: null,
                nominator: null,
                busy: false,
                name_group: '',
                key: `${day}-${para.para}-Вільно-${filters.value.room}`,
                groups: []
              });
            }
          });
        }
        scheduleData.value = freePeriodsData;
        showFreeScheduleGrid.value = false;
      }
    } else if (filters.value.busy === false && filters.value.name_group) {
      const data = await fetchFreeSlots(filters.value.name_group);
      scheduleData.value = data;
      showFreeScheduleGrid.value = true;
    } else {
      const data = await fetchSchedule(filters.value);
      if (data) {
        scheduleData.value = data;
        showFreeScheduleGrid.value = false;
      }
    }
  } catch (err) {
    console.error('Error fetching data:', err);
    scheduleData.value = [];
    roomScheduleData.value = null;
  }
};

// Look for changes in filters
watch(() => filters.value, (newVal) => {
  // If the status changed to "Free" and there is a room or group
  if (newVal.busy === false && (newVal.room || newVal.name_group)) {
    fetchData();
  }
  // If the status changed to "All" and there is a room
  else if (newVal.busy === null && newVal.room) {
    fetchData();
  }
}, { deep: true });

// Look for changes in room
watch(() => filters.value.room, (newVal) => {
  if (newVal && filters.value.busy === false) fetchData();
});

// Отримуємо поточний тип тижня
const fetchCurrentWeekType = async () => {
  try {
    const response = await httpClient.get('/week-type');
    weekType.value = response.data.week_type;
    // Якщо фільтр не був вибраний вручну, оновлюємо його
    if (filters.value.nominator === null) {
      filters.value = {
        ...filters.value,
        nominator: weekType.value
      };
    }
  } catch (e) {
    console.error('Не вдалося отримати поточний тип тижня', e);
  }
};

// Load data on start
onMounted(async () => {
  await fetchCurrentWeekType();
  fetchData();
});

// Слідкуємо за зміною типу тижня
watch(weekType, (newVal) => {
  if (filters.value.nominator === null && newVal) {
    filters.value = {
      ...filters.value,
      nominator: newVal
    };
  }
});

// Слідкуємо за зміною defaultNominator
watch(() => props.defaultNominator, (newVal) => {
  console.log('DayList received new nominator:', newVal);
  filters.value.nominator = newVal;
}, { immediate: true });
</script>

<style scoped>
.loading, .error, .no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  text-align: center;
  min-height: 100px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(74, 144, 226, 0.2);
  border-radius: 50%;
  border-top-color: #4a90e2;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
}

.error-icon, .no-data-icon {
  font-size: 32px;
  margin-bottom: 15px;
}
</style>
