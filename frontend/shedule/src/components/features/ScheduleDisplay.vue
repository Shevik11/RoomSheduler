<template>
  <div class="schedule-container">
    <!-- <h3>Знайдено записів: {{ groupedScheduleData.length }}</h3> -->

    <div v-for="day in DAYS_OF_WEEK" :key="day" class="day-group">
      <h4 v-if="hasDayInSchedule(day)" class="day-title">{{ day }}</h4>

      <div v-if="!showFreeScheduleGrid" class="schedule">
        <div 
          v-for="item in filterByDay(day)" 
          :key="`${item.key}`" 
          :class="['schedule-item', {'busy': item.busy}]"
        >
          <div class="item-header">
            <span class="item-group">{{ item.groups.join(', ') }}</span>
            <span v-if="item.number_of_subgroup" class="item-subgroup">(підгрупа {{ item.number_of_subgroup }})</span>
          </div>

          <div class="item-details">
            <div class="item-para">
              <span class="para-number">Пара {{ item.namb_of_para }}</span>
              <span class="para-time">{{ item.time_of_para }}</span>
            </div>

            <div class="item-subject">{{ item.name_of_para }}</div>

            <div class="item-location">
              <span v-if="item.room" class="item-room">Аудиторія: {{ item.room }}</span>
            </div>

            <div class="item-teacher" v-if="item.teacher">
              <span>Викладач: {{ item.teacher }}</span>
            </div>

            <div class="item-nominator" v-if="item.nominator">
              <span>{{ item.nominator }}</span>
            </div>

            <div class="item-status">
              <span :class="item.busy ? 'status-busy' : 'status-free'">
                {{ item.busy ? 'Зайнято' : 'Вільно' }}
              </span>
            </div>

            <!-- Кнопка детальної інформації -->
            <div class="item-actions">
              <button 
                @click="showDetails(item)" 
                class="details-btn"
                type="button"
                v-if="shouldShowDetailsButton"
              >
                Інформація про аудиторію
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Free schedule grid -->
      <div v-if="showFreeScheduleGrid" class="free-schedule-grid">
        <div class="grid-header">
          <div class="grid-cell">Пара</div>
          <div class="grid-cell">Час</div>
          <div class="grid-cell">Статус</div>
          <div class="grid-cell">Дії</div>
        </div>
        <div 
          v-for="para in 8" 
          :key="para" 
          class="grid-row"
          :class="{'free-para': isParaFree(day, para)}"
        >
          <div class="grid-cell">{{ para }}</div>
          <div class="grid-cell">{{ getParaTime(para) }}</div>
          <div class="grid-cell">
            <span v-if="isParaFree(day, para)" class="status-free">Вільно</span>
            <span v-else class="status-busy">Зайнято</span>
          </div>
          <div class="grid-cell">
            <button 
              @click="showFreeParaDetails(day, para)" 
              class="details-btn-small"
              type="button"
              v-if="shouldShowDetailsButton"
            >
              Інформація
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальне вікно з детальною інформацією -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Інформація про аудиторію</h3>
          <span @click="closeModal" class="modal-cancel-icon">✕</span>
        </div>
        <div class="modal-body">
          <div v-if="selectedItem" class="details-content">
            <!-- Інформація про аудиторію -->
            <div class="room-info">
              <div v-if="selectedItem.room" class="detail-row">
                <strong>Аудиторія:</strong> {{ selectedItem.room }}
              </div>
              <div v-else class="detail-row">
                <strong>Аудиторія:</strong> 
                <span class="no-data">Не вказано</span>
              </div>
              <div class="detail-row">
                <strong>День тижня:</strong> {{ selectedItem.day_of_week }}
              </div>
              <div class="detail-row">
                <strong>Пара:</strong> {{ selectedItem.namb_of_para }}
              </div>
              <div class="detail-row">
                <strong>Час:</strong> {{ selectedItem.time_of_para }}
              </div>
              <div class="detail-row">
                <strong>Предмет:</strong> {{ selectedItem.name_of_para }}
              </div>
              <div class="detail-row">
                <strong>Статус:</strong> 
                <span :class="selectedItem.busy ? 'status-busy' : 'status-free'">
                  {{ selectedItem.busy ? 'Зайнято' : 'Вільно' }}
                </span>
              </div>
            </div>
          </div>
          <div v-else class="no-info">
            <p>На даний момент інформації немає</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { DAYS_OF_WEEK, PARA_TIMES } from '../../constants/schedule';
import type { ScheduleItem } from '../../types/schedule';

const props = defineProps<{
  scheduleData: ScheduleItem[];
  showFreeScheduleGrid: boolean;
  filters: {
    busy: boolean | null;
    room: string;
  };
}>();

// Reactive state for modal
const showModal = ref(false);
const selectedItem = ref<ScheduleItem | null>(null);

// Computed property to determine if details button should be shown
const shouldShowDetailsButton = computed(() => {
  return props.filters.busy === false; // Показуємо тільки при пошуку вільних аудиторій
});

// Calculated property for grouped schedule data
const groupedScheduleData = computed(() => {
  const groups: { [key: string]: ScheduleItem } = {};
  props.scheduleData.forEach(item => {
    const key = `${item.day_of_week}-${item.namb_of_para}-${item.name_of_para}-${item.room}-${item.teacher}-${item.number_of_subgroup}-${item.nominator}`;
    if (!groups[key]) {
      groups[key] = {
        ...item,
        key,
        groups: [item.name_group]
      };
    } else {
      groups[key].groups.push(item.name_group);
    }
  });
  return Object.values(groups);
});

// Check if there is data for the day
const hasDayInSchedule = (day: string) => {
  if (props.showFreeScheduleGrid) return DAYS_OF_WEEK.includes(day);
  return groupedScheduleData.value.some(item => item.day_of_week === day);
};

// Filter schedule for the day
const filterByDay = (day: string) => groupedScheduleData.value.filter(item => item.day_of_week === day);

// Get the time of the para
const getParaTime = (paraNumber: number) => PARA_TIMES[paraNumber] || 'Невідомо';

// Check if the para is free
const isParaFree = (day: string, paraNumber: number) => {
  const busyItems = props.scheduleData.filter(item => 
    item.day_of_week === day && item.namb_of_para === paraNumber && item.busy === true
  );
  return busyItems.length === 0;
};

// Show details for schedule item
const showDetails = (item: ScheduleItem) => {
  selectedItem.value = item;
  showModal.value = true;
};

// Show details for free para
const showFreeParaDetails = (day: string, paraNumber: number) => {
  selectedItem.value = {
    day_of_week: day,
    namb_of_para: paraNumber,
    time_of_para: getParaTime(paraNumber),
    name_of_para: 'Вільно',
    name_group: '',
    room: '',
    teacher: '',
    number_of_subgroup: 0,
    nominator: '',
    busy: false,
    key: `${day}-${paraNumber}-free`,
    groups: []
  };
  showModal.value = true;
};

// Close modal
const closeModal = () => {
  showModal.value = false;
  selectedItem.value = null;
};
</script>

<style scoped>
.schedule-container {
  padding: 15px;
  margin-bottom: 0;
}

.day-group {
  margin-bottom: 15px;
}

.day-title {
  padding: 10px 15px;
  background-color: #f0f4f8;
  border-radius: 6px;
  margin-bottom: 10px;
  color: #2c3e50;
  font-weight: 600;
}

.schedule {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.schedule-item {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 290px;
}

.schedule-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.schedule-item.busy {
  border-left: 4px solid #e74c3c;
}

.item-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.item-group {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
}

.item-subgroup {
  margin-left: 5px;
  font-size: 14px;
  color: #7f8c8d;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-para {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.para-number {
  font-weight: 500;
  color: #34495e;
}

.para-time {
  font-size: 14px;
  color: #7f8c8d;
}

.item-subject {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
  margin: 5px 0;
}

.item-location, .item-teacher, .item-nominator {
  font-size: 14px;
  color: #7f8c8d;
}

.item-status {
  margin-top: 8px;
  font-size: 14px;
}

.item-actions {
  margin-top: 10px;
}

.details-btn {
  background-color: #d32f2f;
  color: #fff;
  border: 1.5px solid #d32f2f;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.details-btn:hover {
  background-color: #b71c1c;
  border-color: #b71c1c;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.details-btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.15);
}

.details-btn:active {
  background-color: #a31515;
  border-color: #a31515;
  color: #fff;
}

.details-btn-small {
  background-color: #d32f2f;
  color: #fff;
  border: 1.5px solid #d32f2f;
  padding: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.details-btn-small:hover {
  background-color: #b71c1c;
  border-color: #b71c1c;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

.details-btn-small:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(211, 47, 47, 0.15);
}

.details-btn-small:active {
  background-color: #a31515;
  border-color: #a31515;
  color: #fff;
}

.status-busy {
  color: #e74c3c;
  font-weight: 500;
}

.status-free {
  color: #27ae60;
  font-weight: 500;
}

/* Стилі для сітки вільних пар */
.free-schedule-grid {
  display: grid;
  grid-template-columns: 80px 150px 1fr 100px;
  gap: 1px;
  background-color: #e0e0e0;
  border: 1px solid #e0e0e0;
  margin-bottom: 0;
}

.grid-header {
  display: contents;
}

.grid-header .grid-cell {
  background-color: #4a90e2;
  color: white;
  padding: 10px;
  font-weight: 500;
  text-align: center;
}

.grid-row {
  display: contents;
}

.grid-row:nth-child(odd) .grid-cell {
  background-color: #f8f9fa;
}

.grid-row:nth-child(even) .grid-cell {
  background-color: #ffffff;
}

.grid-cell {
  padding: 10px;
  text-align: center;
}

.free-para .grid-cell {
  background-color: #e8f5e9 !important;
}

.free-para:hover .grid-cell {
  background-color: #d0e9d1 !important;
}

/* Стилі для модального вікна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 16px;
  max-width: 500px;
  width: 95%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(44, 62, 80, 0.18), 0 2px 8px rgba(44, 62, 80, 0.10);
  border: 1.5px solid #e0e0e0;
  padding: 0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px 16px 28px;
  border-bottom: 1.5px solid #f0f0f0;
  background: #f8f8f8;
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.modal-cancel-icon {
  font-size: 1.25em;
  opacity: 0.7;
  cursor: pointer;
  padding: 0.3rem 0.5rem;
  border-radius: 6px;
  transition: all 0.2s;
  color: #2c3e50;
  margin-left: 8px;
  margin-right: -8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-cancel-icon:hover {
  background-color: #f8f9fa;
  opacity: 1;
  color: #e74c3c;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.modal-body {
  padding: 28px 28px 24px 28px;
  background: #fff;
  border-radius: 0 0 16px 16px;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.room-info {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  font-size: 1.04rem;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-row strong {
  color: #2c3e50;
  min-width: 130px;
  font-weight: 600;
}

.no-info {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
  padding: 24px 0;
  font-size: 1.08rem;
}

.no-data {
  color: #7f8c8d;
  font-style: italic;
}
</style> 