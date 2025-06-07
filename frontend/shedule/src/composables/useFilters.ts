import { ref } from 'vue';
import scheduleService from '../services/scheduleService';
import type { ScheduleFilters } from '../types/schedule';

export function useFilters() {
  const showGroupSuggestions = ref(false);
  const filteredGroups = ref<string[]>([]);
  const isFetchingGroups = ref(false);

  const showSubjectSuggestions = ref(false);
  const filteredSubjects = ref<string[]>([]);
  const isFetchingSubjects = ref(false);

  const showRoomSuggestions = ref(false);
  const filteredRooms = ref<string[]>([]);
  const isFetchingRooms = ref(false);

  const showTeacherSuggestions = ref(false);
  const filteredTeachers = ref<string[]>([]);
  const isFetchingTeachers = ref(false);

  const handleGroupInput = async (input: string, filters: ScheduleFilters) => {
    try {
      isFetchingGroups.value = true;
      const suggestions = await scheduleService.getGroupSuggestions(input);
      filteredGroups.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      console.error('Error fetching group suggestions:', err);
      filteredGroups.value = [];
    } finally {
      isFetchingGroups.value = false;
    }
  };

  const handleSubjectInput = async (input: string, filters: ScheduleFilters) => {
    try {
      isFetchingSubjects.value = true;
      const suggestions = await scheduleService.getSubjectSuggestions(input, filters.name_group);
      filteredSubjects.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      console.error('Error fetching subject suggestions:', err);
      filteredSubjects.value = [];
    } finally {
      isFetchingSubjects.value = false;
    }
  };

  const handleRoomInput = async (input: string, filters: ScheduleFilters) => {
    try {
      isFetchingRooms.value = true;
      const suggestions = await scheduleService.getRoomSuggestions(input, filters);
      filteredRooms.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      console.error('Error fetching room suggestions:', err);
      filteredRooms.value = [];
    } finally {
      isFetchingRooms.value = false;
    }
  };

  const handleTeacherInput = async (input: string, filters: ScheduleFilters) => {
    try {
      isFetchingTeachers.value = true;
      const suggestions = await scheduleService.getTeacherSuggestions(
        input,
        filters.name_group,
        filters.name_of_para
      );
      filteredTeachers.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      console.error('Error fetching teacher suggestions:', err);
      filteredTeachers.value = [];
    } finally {
      isFetchingTeachers.value = false;
    }
  };

  return {
    showGroupSuggestions,
    filteredGroups,
    isFetchingGroups,
    showSubjectSuggestions,
    filteredSubjects,
    isFetchingSubjects,
    showRoomSuggestions,
    filteredRooms,
    isFetchingRooms,
    showTeacherSuggestions,
    filteredTeachers,
    isFetchingTeachers,
    handleGroupInput,
    handleSubjectInput,
    handleRoomInput,
    handleTeacherInput
  };
} 