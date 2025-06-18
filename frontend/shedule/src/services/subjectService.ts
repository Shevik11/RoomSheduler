import httpClient from './httpClient';

class SubjectService {
  async getAllSubjects(): Promise<string[]> {
    const response = await httpClient.get('/subjects/');
    return response.data;
  }

  async getSubjectSuggestions(query: string, group?: string): Promise<string[]> {
    const params: Record<string, string> = { query };
    if (group) params.group = group;
    
    const response = await httpClient.get('/lessons/suggestions/', { params });
    return response.data;
  }
}

export default new SubjectService(); 