<template>
  <div class="schedule-container">
    <h3>Знайдено записів: {{ groupedScheduleData.length }}</h3>

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
          </div>
        </div>
      </div>

      <!-- Сітка вільних пар -->
      <div v-if="showFreeScheduleGrid" class="free-schedule-grid">
        <div class="grid-header">
          <div class="grid-cell">Пара</div>
          <div class="grid-cell">Час</div>
          <div class="grid-cell">Статус</div>
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { DAYS_OF_WEEK, PARA_TIMES } from '../../constants/schedule';
import type { ScheduleItem } from '../../types/schedule';

const props = defineProps<{
  scheduleData: ScheduleItem[];
  showFreeScheduleGrid: boolean;
}>();

// Обчислене властивість для згрупованих даних розкладу
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

// Перевіряємо наявність даних для дня
const hasDayInSchedule = (day: string) => {
  if (props.showFreeScheduleGrid) return DAYS_OF_WEEK.includes(day);
  return groupedScheduleData.value.some(item => item.day_of_week === day);
};

// Фільтруємо розклад для дня
const filterByDay = (day: string) => groupedScheduleData.value.filter(item => item.day_of_week === day);

// Отримуємо час пари
const getParaTime = (paraNumber: number) => PARA_TIMES[paraNumber] || 'Невідомо';

// Перевіряємо, чи пара вільна
const isParaFree = (day: string, paraNumber: number) => {
  const busyItems = props.scheduleData.filter(item => 
    item.day_of_week === day && item.namb_of_para === paraNumber && item.busy === true
  );
  return busyItems.length === 0;
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
  grid-template-columns: 80px 150px 1fr;
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
</style> 