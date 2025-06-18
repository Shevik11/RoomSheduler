import httpClient from './httpClient';
import type { ScheduleFilters } from '../types/schedule';

class RoomService {
  async getAllRooms(): Promise<string[]> {
    const response = await httpClient.get('/rooms/suggestions/');
    return response.data;
  }

  async getRoomSuggestions(query: string, filters: ScheduleFilters): Promise<string[]> {
    // Формуємо параметри запиту
    const params = {
      query: query, // Додаємо параметр пошуку
      ...Object.fromEntries(
        Object.entries(filters)
          .filter(([key, value]) => 
            value !== null && 
            value !== '' && 
            key !== 'room' // Виключаємо поточну кімнату з параметрів
          )
      )
    };

    console.log('Room suggestions request params:', JSON.stringify(params, null, 2));
    
    // Отримуємо рекомендації аудиторій з урахуванням всіх фільтрів
    const response = await httpClient.get('/rooms/suggestions/', { params });
    const suggestedRooms = response.data;
    console.log('Room suggestions response:', JSON.stringify(suggestedRooms, null, 2));

    // Якщо вказано фільтр зайнятості, фільтруємо додатково по зайнятості
    if (filters.busy !== null) {
      const busyRoomsResponse = await httpClient.get('/rooms/busy_rooms/', { params });
      const busyRooms = busyRoomsResponse.data;
      console.log('Busy rooms response:', JSON.stringify(busyRooms, null, 2));

      if (filters.busy === false) {
        // Повертаємо тільки вільні аудиторії зі списку рекомендованих
        return suggestedRooms.filter((room: string) => !busyRooms.includes(room));
      } else {
        // Повертаємо тільки зайняті аудиторії зі списку рекомендованих
        return suggestedRooms.filter((room: string) => busyRooms.includes(room));
      }
    }

    // Якщо не вказана зайнятість, повертаємо всі рекомендовані аудиторії
    return suggestedRooms;
  }
}

export default new RoomService(); 