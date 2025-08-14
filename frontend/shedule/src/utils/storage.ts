const STORAGE_PREFIX = "schedule_";

export const storage = {
  set<T>(key: string, value: T): void {
    try {
      const serializedValue = JSON.stringify(value);
      localStorage.setItem(`${STORAGE_PREFIX}${key}`, serializedValue);
    } catch (error) {
      console.error("Error saving to localStorage:", error);
    }
  },

  get<T>(key: string): T | null {
    try {
      const serializedValue = localStorage.getItem(`${STORAGE_PREFIX}${key}`);
      return serializedValue ? JSON.parse(serializedValue) : null;
    } catch (error) {
      console.error("Error reading from localStorage:", error);
      return null;
    }
  },

  remove(key: string): void {
    try {
      localStorage.removeItem(`${STORAGE_PREFIX}${key}`);
    } catch (error) {
      console.error("Error removing from localStorage:", error);
    }
  },

  clear(): void {
    try {
      Object.keys(localStorage)
        .filter((key) => key.startsWith(STORAGE_PREFIX))
        .forEach((key) => localStorage.removeItem(key));
    } catch (error) {
      console.error("Error clearing localStorage:", error);
    }
  },
};
