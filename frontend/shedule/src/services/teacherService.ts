import httpClient from './httpClient';

class TeacherService {
  async getAllTeachers(): Promise<string[]> {
    const response = await httpClient.get('/teachers/');
    return response.data;
  }

  async getTeacherSuggestions(query: string, group?: string, subject?: string): Promise<string[]> {
    const params: Record<string, string> = { query };
    if (group) params.group = group;
    if (subject) params.subject = subject;
    
    const response = await httpClient.get('/teachers/suggestions/', { params });
    return response.data;
  }
}

export default new TeacherService(); 