import { ref } from "vue";
import scheduleService from "../services/scheduleService";
import type {
  ScheduleFilters,
} from "../types/schedule";

interface ApiError extends Error {
  response?: {
    data?: {
      detail?: string;
    };
  };
}

export function useScheduleApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const handleError = (err: unknown): string => {
    console.error("API Error:", err);
    if (err instanceof Error) {
      const apiError = err as ApiError;
      const errorMessage = apiError.response?.data?.detail || apiError.message;
      console.error("Error details:", errorMessage);
      return `Помилка: ${errorMessage}`;
    }
    return "Помилка: Невідома помилка";
  };

  const fetchSchedule = async (filters: ScheduleFilters) => {
    try {
      loading.value = true;
      error.value = null;
      console.log("Fetching schedule with filters:", filters);
      const result = await scheduleService.fetchSchedule(filters);
      console.log("Schedule result:", result);
      return result;
    } catch (err) {
      error.value = handleError(err);
      return [];
    } finally {
      loading.value = false;
    }
  };

  const fetchRoomSchedule = async (room: string) => {
    try {
      loading.value = true;
      error.value = null;
      console.log("Fetching room schedule for:", room);
      const result = await scheduleService.fetchRoomSchedule(room);
      console.log("Room schedule result:", result);
      return result;
    } catch (err) {
      error.value = handleError(err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  const fetchFreeSlots = async (group: string, nominator?: string) => {
    try {
      loading.value = true;
      error.value = null;
      console.log("Fetching free slots for group:", group, "nominator:", nominator);
      const result = await scheduleService.fetchFreeSlots(group, nominator);
      console.log("Free slots result:", result);
      return result;
    } catch (err) {
      // Use the error message directly from the service if it's already formatted
      if (err instanceof Error && err.message.includes('Групу') || err instanceof Error && err.message.includes('Помилка')) {
        error.value = err.message;
      } else {
        error.value = handleError(err);
      }
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
    fetchFreeSlots,
  };
}
