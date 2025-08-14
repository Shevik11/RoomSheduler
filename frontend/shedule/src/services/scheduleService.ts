import httpClient from "./httpClient";
import type {
  ScheduleFilters,
  ScheduleItem,
  RoomSchedule,
} from "../types/schedule";
import type { AxiosResponse } from "axios";
import groupService from "./groupService";
import subjectService from "./subjectService";
import teacherService from "./teacherService";
import roomService from "./roomService";

class ScheduleService {
  async fetchSchedule(filters: ScheduleFilters): Promise<ScheduleItem[]> {
    const params: Record<string, any> = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== "") params[key] = value;
    });
    console.log(
      "Sending request with params:",
      JSON.stringify(params, null, 2),
    );
    const response: AxiosResponse<ScheduleItem[]> = await httpClient.get(
      "/days/",
      { params },
    );
    console.log("Received data:", JSON.stringify(response.data, null, 2));
    return response.data;
  }

  async fetchRoomSchedule(room: string): Promise<RoomSchedule> {
    const response = await httpClient.get("/rooms/schedule/", {
      params: {
        room: room,
      },
    });
    return response.data;
  }

  async fetchFreeSlots(group: string, nominator?: string): Promise<ScheduleItem[]> {
    try {
      // Properly encode the group name to handle special characters
      const encodedGroup = encodeURIComponent(group);
      
      const params: Record<string, any> = {};
      if (nominator) {
        params.nominator = nominator;
      }
      
      console.log(`Fetching free slots for group: ${group} (encoded: ${encodedGroup})`);
      
      const response = await httpClient.get(`/groups/${encodedGroup}/free-slots/`, {
        params
      });
      
      console.log(`Successfully fetched ${response.data.length} free slots for group ${group}`);
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching free slots for group ${group}:`, error);
      
      // Provide more specific error messages
      if (error.response?.status === 404) {
        throw new Error(`Групу "${group}" не знайдено або для неї немає розкладу`);
      } else if (error.response?.status === 500) {
        throw new Error(`Помилка сервера при отриманні вільних слотів для групи "${group}"`);
      } else if (error.code === 'NETWORK_ERROR' || !error.response) {
        throw new Error('Помилка мережі. Перевірте підключення до інтернету');
      }
      
      // Re-throw the original error if we can't handle it specifically
      throw error;
    }
  }

  // Делегуємо методи до відповідних сервісів
  getAllGroups = groupService.getAllGroups;
  getGroupSuggestions = groupService.getGroupSuggestions;

  getAllSubjects = subjectService.getAllSubjects;
  getSubjectSuggestions = (query: string, filters: ScheduleFilters) =>
    subjectService.getSubjectSuggestions(query, filters);

  getAllTeachers = teacherService.getAllTeachers;
  getTeacherSuggestions = (query: string, filters: ScheduleFilters) =>
    teacherService.getTeacherSuggestions(query, filters);

  getAllRooms = roomService.getAllRooms;
  getRoomSuggestions = roomService.getRoomSuggestions;
}

export default new ScheduleService();
