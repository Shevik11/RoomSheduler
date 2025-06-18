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
    console.log('Sending request with params:', JSON.stringify(params, null, 2));
    const response: AxiosResponse<ScheduleItem[]> = await httpClient.get('/days/', { params });
    console.log('Received data:', JSON.stringify(response.data, null, 2));
    return response.data;
  }

  async fetchRoomSchedule(room: string): Promise<RoomSchedule> {
    const response = await httpClient.get('/rooms/schedule/', {
      params: {
        room: room
      }
    });
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
  getSubjectSuggestions = (query: string, filters: ScheduleFilters) => 
    subjectService.getSubjectSuggestions(query, filters);
  
  getAllTeachers = teacherService.getAllTeachers;
  getTeacherSuggestions = (query: string, filters: ScheduleFilters) => 
    teacherService.getTeacherSuggestions(query, filters);
  
  getAllRooms = roomService.getAllRooms;
  getRoomSuggestions = roomService.getRoomSuggestions;
}

export default new ScheduleService(); 