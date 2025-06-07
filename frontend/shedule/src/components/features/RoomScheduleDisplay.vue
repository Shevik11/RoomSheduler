<template>
  <div v-if="roomScheduleData" class="room-schedule">
    <h3>Розклад аудиторії {{ room }}</h3>

    <div v-for="(day, dayName) in roomScheduleData" :key="dayName" class="day-schedule">
      <h4>{{ dayName }}</h4>

      <div v-for="para in day" :key="para.para" class="para-item" :class="{'free': para.status === 'Вільно'}">
        <div class="para-header">
          <span class="para-number">{{ para.para }} пара</span>
          <span class="para-time">{{ para.time }}</span>
          <span class="para-status" :class="{'free': para.status === 'Вільно', 'busy': para.status === 'Зайнято'}">
            {{ para.status }}
          </span>
        </div>

        <div v-if="para.status === 'Зайнято'" class="para-details">
          <div>Групи: {{ Array.isArray(para.group) ? para.group.join(', ') : para.group }}</div>
          <div>Предмет: {{ para.subject }}</div>
          <div v-if="para.teacher">Викладач: {{ para.teacher }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RoomSchedule } from '../../types/schedule';
import { PARA_TIMES } from '../../constants/schedule';

defineProps<{
  room: string;
  roomScheduleData: RoomSchedule | null;
}>();
</script>

<style scoped>
.room-schedule {
  padding: 15px;
  margin-bottom: 0;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.day-schedule {
  margin-bottom: 15px;
}

.para-item {
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  background-color: #fff;
  border-left: 4px solid #e74c3c;
}

.para-item.free {
  border-left-color: #27ae60;
}

.para-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 500;
}

.para-number {
  font-weight: 600;
}

.para-status.free {
  color: #27ae60;
}

.para-status.busy {
  color: #e74c3c;
}

.para-details {
  font-size: 14px;
  color: #555;
}
</style> 