import { ref } from 'vue';
import scheduleService from '../services/scheduleService';
import type { ScheduleFilters, ScheduleItem, RoomSchedule } from '../types/schedule';

export function useScheduleApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchSchedule = async (filters: ScheduleFilters) => {
    try {
      loading.value = true;
      error.value = null;
      return await scheduleService.fetchSchedule(filters);
    } catch (err) {
      error.value = `Помилка: ${err.response?.data?.detail || err.message}`;
      return [];
    } finally {
      loading.value = false;
    }
  };

  const fetchRoomSchedule = async (room: string) => {
    try {
      loading.value = true;
      error.value = null;
      return await scheduleService.fetchRoomSchedule(room);
    } catch (err) {
      error.value = `Помилка: ${err.response?.data?.detail || err.message}`;
      return null;
    } finally {
      loading.value = false;
    }
  };

  const fetchFreeSlots = async (group: string) => {
    try {
      loading.value = true;
      error.value = null;
      return await scheduleService.fetchFreeSlots(group);
    } catch (err) {
      error.value = `Помилка: ${err.response?.data?.detail || err.message}`;
      return [];
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    fetchSchedule,
    fetchRoomSchedule,
    fetchFreeSlots
  };
} 