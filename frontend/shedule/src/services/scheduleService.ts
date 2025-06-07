import httpClient from './httpClient';
import type { ScheduleFilters, ScheduleItem, RoomSchedule } from '../types/schedule';
import type { AxiosResponse } from 'axios';

class ScheduleService {
  async fetchSchedule(filters: ScheduleFilters): Promise<ScheduleItem[]> {
    const params: Record<string, any> = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== '') params[key] = value;
    });
    const response: AxiosResponse<ScheduleItem[]> = await httpClient.get('/days/', { params });
    return response.data;
  }

  async fetchRoomSchedule(room: string): Promise<RoomSchedule> {
    const encodedRoom = encodeURIComponent(room);
    const response: AxiosResponse<RoomSchedule> = await httpClient.get(`/room_schedule/?room=${encodedRoom}`);
    return response.data;
  }

  async fetchFreeSlots(group: string): Promise<any> {
    const response = await httpClient.get('/free_slots/', {
      params: { name_group: group }
    });
    return response.data;
  }

  async getGroupSuggestions(query: string): Promise<string[]> {
    const response = await httpClient.get('/groups/suggestions/', {
      params: { query }
    });
    return response.data;
  }

  async getSubjectSuggestions(query: string, group?: string): Promise<string[]> {
    const params: Record<string, any> = { query };
    if (group) params.name_group = group;
    const response = await httpClient.get('/lessons/suggestions/', { params });
    return response.data;
  }

  async getRoomSuggestions(query: string, filters: ScheduleFilters): Promise<string[]> {
    const params = {
      query,
      ...Object.fromEntries(
        Object.entries(filters)
          .filter(([key, value]) => 
            value !== null && 
            value !== '' && 
            key !== 'room'
          )
      )
    };
    const response = await httpClient.get('/rooms/suggestions/', { params });
    return response.data;
  }

  async getTeacherSuggestions(query: string, group?: string, subject?: string): Promise<string[]> {
    const params: Record<string, any> = { query };
    if (group) params.name_group = group;
    if (subject) params.name_of_para = subject;
    const response = await httpClient.get('/teachers/suggestions/', { params });
    return response.data;
  }
}

export default new ScheduleService(); 