import httpClient from "./httpClient";
import cache from "../utils/cache";
import { storage } from "../utils/storage";

const CACHE_KEYS = {
  ALL_GROUPS: "all_groups",
  GROUP_SUGGESTIONS: "group_suggestions_",
};

class GroupService {
  async getAllGroups(): Promise<string[]> {
    // Спочатку перевіряємо кеш
    const cachedData = cache.get<string[]>(CACHE_KEYS.ALL_GROUPS);
    if (cachedData) return cachedData;

    // Потім перевіряємо локальне сховище
    const storedData = storage.get<string[]>(CACHE_KEYS.ALL_GROUPS);
    if (storedData) {
      cache.set(CACHE_KEYS.ALL_GROUPS, storedData);
      return storedData;
    }

    // Якщо немає в кеші і сховищі, робимо запит
    const response = await httpClient.get("/groups/");
    const data = response.data;

    // Зберігаємо в кеш і сховище
    cache.set(CACHE_KEYS.ALL_GROUPS, data);
    storage.set(CACHE_KEYS.ALL_GROUPS, data);

    return data;
  }

  async getGroupSuggestions(query: string): Promise<string[]> {
    const cacheKey = `${CACHE_KEYS.GROUP_SUGGESTIONS}${query}`;

    // Перевіряємо кеш
    const cachedData = cache.get<string[]>(cacheKey);
    if (cachedData) return cachedData;

    // Робимо запит
    const response = await httpClient.get("/groups/suggestions/", {
      params: { query },
    });
    const data = response.data;

    // Зберігаємо в кеш
    cache.set(cacheKey, data);

    return data;
  }
}

export default new GroupService();
