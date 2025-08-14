import httpClient from "./httpClient";
import type { ScheduleFilters } from "../types/schedule";

class TeacherService {
  async getAllTeachers(): Promise<string[]> {
    const response = await httpClient.get("/teachers/suggestions/");
    return response.data;
  }

  async getTeacherSuggestions(
    query: string,
    filters: ScheduleFilters,
  ): Promise<string[]> {
    const params = {
      query,
      ...Object.fromEntries(
        Object.entries(filters).filter(
          ([key, value]) => value !== null && value !== "" && key !== "teacher",
        ),
      ),
    };
    console.log(
      "Teacher suggestions request params:",
      JSON.stringify(params, null, 2),
    );
    const response = await httpClient.get("/teachers/suggestions/", { params });
    console.log(
      "Teacher suggestions response:",
      JSON.stringify(response.data, null, 2),
    );
    return response.data;
  }
}

export default new TeacherService();
