import httpClient from './httpClient';
import type { ScheduleFilters } from '../types/schedule';

class TeacherService {
  async getAllTeachers(): Promise<string[]> {
    const response = await httpClient.get('/teachers/suggestions/');
    return response.data;
  }

  async getTeacherSuggestions(query: string, filters: ScheduleFilters): Promise<string[]> {
    const params = {
      query,
      ...Object.fromEntries(
        Object.entries(filters)
          .filter(([key, value]) => 
            value !== null && 
            value !== '' && 
            key !== 'teacher'
          )
      )
    };
    // console.log('Teacher suggestions params:', params);
    const response = await httpClient.get('/teachers/suggestions/', { params });
    return response.data;
  }
}

export default new TeacherService(); 