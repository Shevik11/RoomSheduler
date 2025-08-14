import { ref } from "vue";
import scheduleService from "../services/scheduleService";
import type { ScheduleFilters } from "../types/schedule";

// Cache interface
interface Cache {
  [key: string]: {
    data: string[];
    timestamp: number;
  };
}

// Cache expiration time (5 minutes)
const CACHE_EXPIRATION = 5 * 60 * 1000;

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

  // Store all available data
  const allGroups = ref<string[]>([]);
  const allSubjects = ref<string[]>([]);
  const allRooms = ref<string[]>([]);
  const allTeachers = ref<string[]>([]);

  // Initialize caches
  const groupCache: Cache = {};
  const subjectCache: Cache = {};
  const roomCache: Cache = {};
  const teacherCache: Cache = {};

  // Check if cache is valid
  const isCacheValid = (cache: Cache, key: string): boolean => {
    const cached = cache[key];
    return cached && Date.now() - cached.timestamp < CACHE_EXPIRATION;
  };

  // Load all data on mount
  const loadAllData = async () => {
    try {
      // Load all groups
      const groups = await scheduleService.getAllGroups();
      allGroups.value = Array.isArray(groups) ? groups : [];

      // Load all subjects
      const subjects = await scheduleService.getAllSubjects();
      allSubjects.value = Array.isArray(subjects) ? subjects : [];

      // Load all rooms
      const rooms = await scheduleService.getAllRooms();
      allRooms.value = Array.isArray(rooms) ? rooms : [];

      // Load all teachers
      const teachers = await scheduleService.getAllTeachers();
      allTeachers.value = Array.isArray(teachers) ? teachers : [];
    } catch (err) {
      console.error("Error loading initial data:", err);
    }
  };

  // Load data immediately
  loadAllData();

  // Групи
  const handleGroupInput = async (input: string, filters: ScheduleFilters) => {
    if (!input) {
      filteredGroups.value = [];
      return;
    }
    isFetchingGroups.value = true;
    try {
      const suggestions = await scheduleService.getGroupSuggestions(input);
      filteredGroups.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      filteredGroups.value = [];
    } finally {
      isFetchingGroups.value = false;
    }
  };

  // Предмети
  const handleSubjectInput = async (
    input: string,
    filters: ScheduleFilters,
  ) => {
    if (!input) {
      filteredSubjects.value = [];
      return;
    }
    isFetchingSubjects.value = true;
    try {
      const suggestions = await scheduleService.getSubjectSuggestions(
        input,
        filters,
      );
      filteredSubjects.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      filteredSubjects.value = [];
    } finally {
      isFetchingSubjects.value = false;
    }
  };

  // Аудиторії
  const handleRoomInput = async (input: string, filters: ScheduleFilters) => {
    if (!input) {
      filteredRooms.value = [];
      return;
    }
    isFetchingRooms.value = true;
    try {
      const suggestions = await scheduleService.getRoomSuggestions(
        input,
        filters,
      );
      filteredRooms.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
      filteredRooms.value = [];
    } finally {
      isFetchingRooms.value = false;
    }
  };

  // Викладачі
  const handleTeacherInput = async (
    input: string,
    filters: ScheduleFilters,
  ) => {
    if (!input) {
      filteredTeachers.value = [];
      return;
    }
    isFetchingTeachers.value = true;
    try {
      const suggestions = await scheduleService.getTeacherSuggestions(
        input,
        filters,
      );
      filteredTeachers.value = Array.isArray(suggestions) ? suggestions : [];
    } catch (err) {
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
    handleTeacherInput,
  };
}
