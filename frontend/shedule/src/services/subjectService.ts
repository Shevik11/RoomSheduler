import httpClient from './httpClient';
import type { ScheduleFilters } from '../types/schedule';

class SubjectService {
  async getAllSubjects(): Promise<string[]> {
    const response = await httpClient.get('/subjects/');
    return response.data;
  }

  async getSubjectSuggestions(query: string, filters: ScheduleFilters): Promise<string[]> {
    const params = {
      query,
      ...Object.fromEntries(
        Object.entries(filters)
          .filter(([key, value]) => 
            value !== null && 
            value !== '' && 
            key !== 'name_of_para'
          )
      )
    };
    console.log('Subject suggestions request params:', JSON.stringify(params, null, 2));
    const response = await httpClient.get('/lessons/suggestions/', { params });
    console.log('Subject suggestions response:', JSON.stringify(response.data, null, 2));
    return response.data;
  }
}

export default new SubjectService(); 