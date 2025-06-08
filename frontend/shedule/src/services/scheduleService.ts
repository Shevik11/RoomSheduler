import httpClient from './httpClient';
import type { ScheduleFilters, ScheduleItem, RoomSchedule } from '../types/schedule';
import type { AxiosResponse } from 'axios';
import groupService from './groupService';
import subjectService from './subjectService';
import teacherService from './teacherService';
import roomService from './roomService';

class ScheduleService {
  async fetchSchedule(filters: ScheduleFilters): Promise<ScheduleItem[]> {
    const params: Record<string, any> = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== '') params[key] = value;
    });
    console.log('Sending request with params:', params);
    const response: AxiosResponse<ScheduleItem[]> = await httpClient.get('/days/', { params });
    console.log('Received data:', response.data);
    return response.data;
  }

  async fetchRoomSchedule(room: string): Promise<RoomSchedule> {
    const response = await httpClient.get(`/rooms/${room}/schedule/`);
    return response.data;
  }

  async fetchFreeSlots(group: string): Promise<ScheduleItem[]> {
    const response = await httpClient.get(`/groups/${group}/free-slots/`);
    return response.data;
  }

  // Делегуємо методи до відповідних сервісів
  getAllGroups = groupService.getAllGroups;
  getGroupSuggestions = groupService.getGroupSuggestions;
  
  getAllSubjects = subjectService.getAllSubjects;
  getSubjectSuggestions = subjectService.getSubjectSuggestions;
  
  getAllTeachers = teacherService.getAllTeachers;
  getTeacherSuggestions = teacherService.getTeacherSuggestions;
  
  getAllRooms = roomService.getAllRooms;
  getRoomSuggestions = roomService.getRoomSuggestions;
}

export default new ScheduleService(); 