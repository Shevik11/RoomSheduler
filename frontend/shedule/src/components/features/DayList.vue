<template>
  <!-- Секція фільтрів -->
  <ScheduleFiltersComponent
    v-model="filters"
    @apply="fetchData"
  />

  <!-- Індикатор завантаження -->
  <div v-if="loading" class="loading">
    <div class="spinner"></div>
    <p>Завантаження даних...</p>
  </div>

  <!-- Повідомлення про помилку -->
  <div v-if="error" class="error">
    <i class="error-icon">⚠️</i>
    <p>{{ error }}</p>
  </div>

  <!-- Повідомлення про відсутність даних -->
  <div v-if="!loading && !error && !hasData" class="no-data">
    <i class="no-data-icon">📭</i>
    <p>Немає даних, що відповідають заданим фільтрам</p>
  </div>

  <!-- Відображення розкладу -->
  <ScheduleDisplay
    v-if="!loading && !error && hasData"
    :schedule-data="scheduleData"
    :show-free-schedule-grid="showFreeScheduleGrid"
  />

  <!-- Блок для відображення розкладу аудиторії -->
  <!-- <RoomScheduleDisplay
    v-if="!loading && !error && roomScheduleData"
    :room="filters.room"
    :room-schedule-data="roomScheduleData"
  /> -->
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { DEFAULT_FILTERS } from '../../constants/schedule';
import { useScheduleApi } from '../../composables/useScheduleApi';
import type { ScheduleFilters, ScheduleItem, RoomSchedule } from '../../types/schedule';
import ScheduleFiltersComponent from './ScheduleFilters.vue';
import ScheduleDisplay from './ScheduleDisplay.vue';
import RoomScheduleDisplay from './RoomScheduleDisplay.vue';

// Стани
const scheduleData = ref<ScheduleItem[]>([]);
const showFreeScheduleGrid = ref(false);
const roomScheduleData = ref<RoomSchedule | null>(null);
const filters = ref<ScheduleFilters>({ ...DEFAULT_FILTERS });

// Використовуємо composable для роботи з API
const { loading, error, fetchSchedule, fetchRoomSchedule, fetchFreeSlots } = useScheduleApi();

// Перевіряємо наявність даних
const hasData = computed(() => {
  return scheduleData.value.length > 0 || (roomScheduleData.value && Object.keys(roomScheduleData.value).length > 0);
});

// Завантаження даних
const fetchData = async () => {
  try {
    if (filters.value.busy === false && filters.value.room) {
      const data = await fetchRoomSchedule(filters.value.room);
      if (data) {
        roomScheduleData.value = data;
        // Створюємо scheduleData для вільних періодів
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

// Слідкуємо за змінами фільтрів
watch(() => filters.value, (newVal) => {
  // Якщо змінився статус на "Вільні" і є аудиторія або група
  if (newVal.busy === false && (newVal.room || newVal.name_group)) {
    fetchData();
  }
  // Якщо змінився статус на "Всі" і є аудиторія
  else if (newVal.busy === null && newVal.room) {
    fetchData();
  }
}, { deep: true });

// Слідкуємо за змінами room
watch(() => filters.value.room, (newVal) => {
  if (newVal && filters.value.busy === false) fetchData();
});

// Завантажуємо дані при старті
onMounted(fetchData);
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
