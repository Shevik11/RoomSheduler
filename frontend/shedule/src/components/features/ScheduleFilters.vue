<template>
  <div class="filters-container">
    <h3>Фільтри розкладу</h3>
    <div class="filters">
      <!-- Фільтр за групою -->
      <div class="filter-item">
        <label for="name_group">Група:</label>
        <div class="autocomplete-container">
          <input 
            id="name_group"
            v-model="filters.name_group" 
            @input="handleGroupInputWrapper" 
            placeholder="Введіть назву групи"
            class="filter-input"
            @focus="showGroupSuggestions = true"
            @blur="handleGroupBlur"
            autocomplete="off"
          />
          <div v-if="showGroupSuggestions" class="suggestions-list">
            <div v-if="isFetchingGroups" class="suggestion-item loading">
              Завантаження...
            </div>
            <template v-else>
              <div v-if="filteredGroups.length === 0" class="suggestion-item no-results">
                Немає відповідних груп
              </div>
              <div 
                v-for="group in filteredGroups" 
                :key="group"
                class="suggestion-item"
                @mousedown.prevent="selectGroup(group)"
              >
                {{ group }}
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Фільтр за підгрупою -->
      <div class="filter-item">
        <label for="number_of_subgroup">Підгрупа:</label>
        <select 
          id="number_of_subgroup"
          v-model="filters.number_of_subgroup" 
          class="filter-select"
        >
          <option :value="null">Всі підгрупи</option>
          <option :value="1">1</option>
          <option :value="2">2</option>
        </select>
      </div>

      <!-- Фільтр за днем тижня -->
      <div class="filter-item">
        <label for="day_of_week">День тижня:</label>
        <select 
          id="day_of_week"
          v-model="filters.day_of_week" 
          class="filter-select"
        >
          <option :value="null">Всі дні</option>
          <option v-for="day in DAYS_OF_WEEK" :key="day" :value="day">{{ day }}</option>
        </select>
      </div>

      <!-- Фільтр за чисельником/знаменником -->
      <div class="filter-item">
        <label for="nominator">Тип тижня:</label>
        <select 
          id="nominator"
          v-model="filters.nominator" 
          class="filter-select"
        >
          <option :value="null">Будь-який</option>
          <option value="Чисельник">Чисельник</option>
          <option value="Знаменник">Знаменник</option>
        </select>
      </div>

      <!-- Фільтр за номером пари -->
      <div class="filter-item">
        <label for="namb_of_para">Номер пари:</label>
        <select 
          id="namb_of_para"
          v-model="filters.namb_of_para" 
          class="filter-select"
        >
          <option :value="null">Всі пари</option>
          <option v-for="n in 8" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <!-- Фільтр за назвою предмета -->
      <div class="filter-item">
        <label for="name_of_para">Назва предмета:</label>
        <div class="autocomplete-container">
          <input 
            id="name_of_para"
            v-model="filters.name_of_para" 
            @input="handleSubjectInputWrapper" 
            placeholder="Введіть назву предмета"
            class="filter-input"
            @focus="showSubjectSuggestions = true"
            @blur="handleSubjectBlur"
            autocomplete="off"
          />
          <div v-if="showSubjectSuggestions" class="suggestions-list">
            <div v-if="isFetchingSubjects" class="suggestion-item loading">
              Завантаження...
            </div>
            <template v-else>
              <div v-if="filteredSubjects.length === 0" class="suggestion-item no-results">
                Немає відповідних предметів
              </div>
              <div 
                v-for="subject in filteredSubjects" 
                :key="subject"
                class="suggestion-item"
                @mousedown.prevent="selectSubject(subject)"
              >
                {{ subject }}
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Фільтр за аудиторією -->
      <div class="filter-item">
        <label for="room">Аудиторія:</label>
        <div class="autocomplete-container">
          <input 
            id="room"
            v-model="filters.room" 
            @input="handleRoomInputWrapper" 
            placeholder="Введіть номер аудиторії"
            class="filter-input"
            @focus="showRoomSuggestions = true"
            @blur="handleRoomBlur"
            autocomplete="off"
          />
          <div v-if="showRoomSuggestions" class="suggestions-list">
            <div v-if="isFetchingRooms" class="suggestion-item loading">
              Завантаження...
            </div>
            <template v-else>
              <div v-if="filteredRooms.length === 0" class="suggestion-item no-results">
                {{ (filters.name_group) 
                  ? `Немає вільних аудиторій для групи ${filters.name_group}` 
                  : 'Немає відповідних аудиторій' }}
              </div>
              <div 
                v-for="room in filteredRooms" 
                :key="room"
                class="suggestion-item"
                @mousedown.prevent="selectRoom(room)"
              >
                {{ room }}
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Фільтр за викладачем -->
      <div class="filter-item">
        <label for="teacher">Викладач:</label>
        <div class="autocomplete-container">
          <input 
            id="teacher"
            v-model="filters.teacher" 
            @input="handleTeacherInputWrapper" 
            placeholder="Введіть ім'я викладача"
            class="filter-input"
            @focus="showTeacherSuggestions = true"
            @blur="handleTeacherBlur"
            autocomplete="off"
          />
          <div v-if="showTeacherSuggestions" class="suggestions-list">
            <div v-if="isFetchingTeachers" class="suggestion-item loading">
              Завантаження...
            </div>
            <template v-else>
              <div v-if="filteredTeachers.length === 0" class="suggestion-item no-results">
                Немає відповідних викладачів
              </div>
              <div 
                v-for="teacher in filteredTeachers" 
                :key="teacher"
                class="suggestion-item"
                @mousedown.prevent="selectTeacher(teacher)"
              >
                {{ teacher }}
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Фільтр за статусом зайнятості -->
      <div class="filter-item">
        <label for="busy">Статус:</label>
        <select 
          id="busy"
          v-model="filters.busy" 
          class="filter-select"
          @change="handleBusyChange"
        >
          <option :value="null">Всі</option>
          <option :value="true">Зайняті</option>
          <option :value="false">Вільні</option>
        </select>
      </div>

      <!-- Кнопка скидання фільтрів -->
      <div class="filter-buttons">
        <button @click="resetFilters" class="reset-button">Скинути фільтри</button>
        <button @click="applyFilters" class="apply-button">Застосувати</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { DAYS_OF_WEEK, DEFAULT_FILTERS } from '../../constants/schedule';
import { useFilters } from '../../composables/useFilters';
import type { ScheduleFilters } from '../../types/schedule';

const props = defineProps<{
  modelValue: ScheduleFilters;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: ScheduleFilters): void;
  (e: 'apply'): void;
}>();

const filters = ref<ScheduleFilters>({ ...props.modelValue });

const {
  showGroupSuggestions,
  filteredGroups,
  isFetchingGroups,
  showSubjectSuggestions,
  filteredSubjects,
  isFetchingSubjects,
  showRoomSuggestions,
  filteredRooms,
  isFetchingRooms,
  showTeacherSuggestions,
  filteredTeachers,
  isFetchingTeachers,
  handleGroupInput,
  handleSubjectInput,
  handleRoomInput,
  handleTeacherInput
} = useFilters();

// Обробники введення
const handleGroupInputWrapper = (event: Event) => {
  const input = (event.target as HTMLInputElement).value;
  filters.value.name_group = input;
  handleGroupInput(input, filters.value);
  showGroupSuggestions.value = true;
};

const handleSubjectInputWrapper = (event: Event) => {
  const input = (event.target as HTMLInputElement).value;
  filters.value.name_of_para = input;
  handleSubjectInput(input, filters.value);
  showSubjectSuggestions.value = true;
};

const handleRoomInputWrapper = (event: Event) => {
  const input = (event.target as HTMLInputElement).value;
  filters.value.room = input;
  handleRoomInput(input, filters.value);
  showRoomSuggestions.value = true;
};

const handleTeacherInputWrapper = (event: Event) => {
  const input = (event.target as HTMLInputElement).value;
  filters.value.teacher = input;
  handleTeacherInput(input, filters.value);
  showTeacherSuggestions.value = true;
};

// Обробники вибору
const selectGroup = (group: string) => {
  filters.value.name_group = group;
  showGroupSuggestions.value = false;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectSubject = (subject: string) => {
  filters.value.name_of_para = subject;
  showSubjectSuggestions.value = false;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectRoom = (room: string) => {
  filters.value.room = room;
  showRoomSuggestions.value = false;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

const selectTeacher = (teacher: string) => {
  filters.value.teacher = teacher;
  showTeacherSuggestions.value = false;
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Обробники blur
const handleGroupBlur = () => {
  setTimeout(() => {
    showGroupSuggestions.value = false;
  }, 200);
};

const handleSubjectBlur = () => {
  setTimeout(() => {
    showSubjectSuggestions.value = false;
  }, 200);
};

const handleRoomBlur = () => {
  setTimeout(() => {
    showRoomSuggestions.value = false;
  }, 200);
};

const handleTeacherBlur = () => {
  setTimeout(() => {
    showTeacherSuggestions.value = false;
  }, 200);
};

// Обробник зміни статусу зайнятості
const handleBusyChange = () => {
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Скидання фільтрів
const resetFilters = () => {
  filters.value = { ...DEFAULT_FILTERS };
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Застосування фільтрів
const applyFilters = () => {
  emit('update:modelValue', { ...filters.value });
  emit('apply');
};

// Слідкуємо за змінами з батьківського компонента
watch(() => props.modelValue, (newValue) => {
  filters.value = { ...newValue };
}, { deep: true });
</script>

<style scoped>
.filters-container {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  align-items: flex-start;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
  padding: 0 8px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 14px;
  color: #505050;
}

.filter-input, .filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.filter-input:focus, .filter-select:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: stretch;
  padding: 0 8px;
}

.reset-button, .apply-button {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: background-color 0.2s;
  width: 100%;
}

.reset-button {
  background-color: #e0e0e0;
  color: #505050;
}

.apply-button {
  background-color: #4a90e2;
  color: white;
}

.reset-button:hover {
  background-color: #d0d0d0;
}

.apply-button:hover {
  background-color: #3a80d2;
}

.autocomplete-container {
  position: relative;
  width: 100%;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.suggestion-item:hover {
  background-color: #f0f4f8;
}

.suggestion-item.loading {
  color: #666;
  font-style: italic;
  cursor: default;
}

.suggestion-item.loading:hover {
  background-color: transparent;
}

.suggestion-item.no-results {
  color: #666;
  font-style: italic;
  cursor: default;
}

.suggestion-item.no-results:hover {
  background-color: transparent;
}
</style> 