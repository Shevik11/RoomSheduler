export const API_BASE_URL = 'https://backend-roomsheduler.onrender.com';
// export const API_BASE_URL = 'http://localhost:8000'; // Для локальної розробки

export const DAYS_OF_WEEK = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота"];

export const PARA_TIMES = [
  null,
  '8:30-10:05',
  '10:25-12:00',
  '12:20-13:55',
  '14:15-15:50',
  '16:10-17:45',
  '18:05-19:40',
  '19:50-21:25',
  '21:35-23:10'
];

export const DEFAULT_FILTERS = {
  name_group: '',
  number_of_subgroup: null,
  day_of_week: null,
  nominator: null,
  namb_of_para: null,
  name_of_para: '',
  room: '',
  teacher: '',
  busy: null,
}; 