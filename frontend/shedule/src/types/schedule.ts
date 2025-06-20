export interface ScheduleFilters {
  name_group: string;
  number_of_subgroup: number | null;
  day_of_week: string | null;
  nominator: string | null;
  namb_of_para: number | null;
  name_of_para: string;
  room: string;
  teacher: string;
  busy: boolean | null;
}

export interface ScheduleItem {
  day_of_week: string;
  namb_of_para: number;
  time_of_para: string;
  name_of_para: string;
  room: string;
  teacher: string;
  number_of_subgroup: number | null;
  nominator: string | null;
  busy: boolean;
  name_group: string;
  key: string;
  groups: string[];
}

export interface RoomSchedule {
  [day: string]: {
    para: number;
    time: string;
    status: string;
  }[];
} 