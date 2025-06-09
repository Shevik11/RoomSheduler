import httpClient from './httpClient';
import type { ScheduleFilters } from '../types/schedule';

class RoomService {
  async getAllRooms(): Promise<string[]> {
    const response = await httpClient.get('/rooms/');
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
}

export default new RoomService(); 