<template>
  <!-- Секція фільтрів -->
  <div class="filters-container">
    <h3>Фільтри розкладу</h3>
    <div class="filters">
      <!-- Фільтр за групою -->
      <div class="filter-item">
        <label for="name_group">Група:</label>
        <input 
          id="name_group"
          v-model="filters.name_group" 
          @input="debounceFetch" 
          placeholder="Введіть назву групи"
          class="filter-input"
        />
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
          <option v-for="day in daysOfWeek" :key="day" :value="day">{{ day }}</option>
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

      <!-- Фільтрt за назвою предмета -->
      <div class="filter-item">
        <label for="name_of_para">Назва предмета:</label>
        <input 
          id="name_of_para"
          v-model="filters.name_of_para" 
          @input="debounceFetch" 
          placeholder="Введіть назву предмета"
          class="filter-input"
        />
      </div>

      <!-- Фільтр за аудиторією -->
      <div class="filter-item">
        <label for="room">Аудиторія:</label>
        <div class="autocomplete-container">
          <input 
            id="room"
            v-model="filters.room" 
            @input="handleRoomInput" 
            placeholder="Введіть номер аудиторії"
            class="filter-input"
            @focus="showSuggestions = true"
            @blur="handleBlur"
            type="text"
            autocomplete="off"
          />
          <div v-if="showSuggestions" class="suggestions-list">
            <div v-if="isFetchingRooms" class="suggestion-item loading">
              Завантаження...
            </div>
            <template v-else>
              <div v-if="filteredRooms.length === 0" class="suggestion-item no-results">
                {{ filters.value.name_group 
                  ? `Немає вільних аудиторій для групи ${filters.value.name_group}` 
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
        <input 
          id="teacher"
          v-model="filters.teacher" 
          @input="debounceFetch" 
          placeholder="Введіть ім'я викладача"
          class="filter-input"
        />
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
        <button @click="fetchData" class="apply-button">Застосувати</button>
      </div>
    </div>
  </div>

  <!-- Індикатор завантаження -->
  <div v-if="loading" class="loading">
    <div class="spinner"></div>
    <p>Завантаження даних...</p>
  </div>
  
  <!-- Повідомлення про помилку -->
  <div v-if="error" class="error">
    <i class="error-icon">⚠️</i>
    <p>{{ error }}</p>
  </div>
  
  <!-- Повідомлення про відсутність даних -->
  <div v-if="!loading && !error && !hasData" class="no-data">
    <i class="no-data-icon">📭</i>
    <p>Немає даних, що відповідають заданим фільтрам</p>
  </div>

  <!-- Відображення розкладу -->
  <div v-if="!loading && !error && hasData" class="schedule-container">
    <h3>Знайдено записів: {{ groupedScheduleData.length }}</h3>
    
    <!-- Групування по дням тижня -->
    <div v-for="day in daysOfWeek" :key="day" class="day-group">
      <h4 v-if="hasDayInSchedule(day)" class="day-title">{{ day }}</h4>
      
      <!-- Звичайний режим відображення -->
      <div v-if="!showFreeScheduleGrid" class="schedule">
        <div 
          v-for="item in filterByDay(day)" 
          :key="`${item.key}`" 
          :class="['schedule-item', {'busy': item.busy}]"
        >
          <div class="item-header">
            <span class="item-group">{{ item.groups.join(', ') }}</span>
            <span v-if="item.number_of_subgroup" class="item-subgroup">(підгрупа {{ item.number_of_subgroup }})</span>
          </div>
          
          <div class="item-details">
            <div class="item-para">
              <span class="para-number">Пара {{ item.namb_of_para }}</span>
              <span class="para-time">{{ item.time_of_para }}</span>
            </div>
            
            <div class="item-subject">{{ item.name_of_para }}</div>
            
            <div class="item-location">
              <span v-if="item.room" class="item-room">Аудиторія: {{ item.room }}</span>
            </div>
            
            <div class="item-teacher" v-if="item.teacher">
              <span>Викладач: {{ item.teacher }}</span>
            </div>
            
            <div class="item-nominator" v-if="item.nominator">
              <span>{{ item.nominator }}</span>
            </div>
            
            <div class="item-status">
              <span :class="item.busy ? 'status-busy' : 'status-free'">
                {{ item.busy ? 'Зайнято' : 'Вільно' }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Сітка вільних пар -->
      <div v-if="showFreeScheduleGrid" class="free-schedule-grid">
        <div class="grid-header">
          <div class="grid-cell">Пара</div>
          <div class="grid-cell">Час</div>
          <div class="grid-cell">Статус</div>
        </div>
        <div 
          v-for="para in 8" 
          :key="para" 
          class="grid-row"
          :class="{'free-para': isParaFree(day, para)}"
        >
          <div class="grid-cell">{{ para }}</div>
          <div class="grid-cell">{{ getParaTime(para) }}</div>
          <div class="grid-cell">
            <span v-if="isParaFree(day, para)" class="status-free">Вільно</span>
            <span v-else class="status-busy">Зайнято</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Блок для відображення розкладу аудиторії -->
  <div v-if="!loading && !error && roomScheduleData" class="room-schedule">
    <h3>Розклад аудиторії {{ filters.room }}</h3>
    
    <div v-for="(day, dayName) in roomScheduleData" :key="dayName" class="day-schedule">
      <h4>{{ dayName }}</h4>
      
      <div v-for="para in day" :key="para.para" class="para-item" :class="{'free': para.status === 'Вільно'}">
        <div class="para-header">
          <span class="para-number">{{ para.para }} пара</span>
          <span class="para-time">{{ para.time }}</span>
          <span class="para-status" :class="{'free': para.status === 'Вільно', 'busy': para.status === 'Зайнято'}">
            {{ para.status }}
          </span>
        </div>
        
        <div v-if="para.status === 'Зайнято'" class="para-details">
          <div>Групи: {{ Array.isArray(para.group) ? para.group.join(', ') : para.group }}</div>
          <div>Предмет: {{ para.subject }}</div>
          <div v-if="para.teacher">Викладач: {{ para.teacher }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup type="module">
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'

// Стани
const loading = ref(true)
const error = ref(null)
const scheduleData = ref([])
const showFreeScheduleGrid = ref(false)
const roomScheduleData = ref(null)

// Обчислене властивість для згрупованих даних розкладу
const groupedScheduleData = computed(() => {
  const groups = {};
  scheduleData.value.forEach(item => {
    const key = `${item.day_of_week}-${item.namb_of_para}-${item.name_of_para}-${item.room}-${item.teacher}-${item.number_of_subgroup}-${item.nominator}`;
    if (!groups[key]) {
      groups[key] = {
        ...item,
        key,
        groups: [item.name_group]
      };
    } else {
      groups[key].groups.push(item.name_group);
    }
  });
  return Object.values(groups);
});

// Перевіряємо наявність даних
const hasData = computed(() => {
  return groupedScheduleData.value.length > 0 || (roomScheduleData.value && Object.keys(roomScheduleData.value).length > 0);
});

// Функція для завантаження розкладу аудиторії
const fetchRoomSchedule = async () => {
  try {
    loading.value = true;
    error.value = null;
    const encodedRoom = encodeURIComponent(filters.value.room);
    const response = await axios.get(`http://room_schedule/?room=${encodedRoom}`);
    // const response = await axios.get(`https://backend-roomsheduler.onrender.com/room_schedule/?room=${encodedRoom}`);
    const processedData = {};
    for (const day in response.data) {
      processedData[day] = [];
      const paraGroups = {};
      response.data[day].forEach(para => {
        const key = `${para.para}-${para.subject}-${para.teacher}`;
        if (para.status === 'Зайнято') {
          if (!paraGroups[key]) {
            paraGroups[key] = { ...para, group: [para.group] };
          } else {
            paraGroups[key].group.push(para.group);
          }
        } else {
          paraGroups[key] = para;
        }
      });
      processedData[day] = Object.values(paraGroups);
    }
    roomScheduleData.value = processedData;
    scheduleData.value = [];
    showFreeScheduleGrid.value = false;
  } catch (err) {
    error.value = `Помилка: ${err.response?.data?.detail || err.message}`;
    roomScheduleData.value = null;
  } finally {
    loading.value = false;
  }
};

// Дні тижня
const daysOfWeek = ref(['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Пятниця', 'Субота'])

// Час пар
const paraTimes = ref([
  null, '8:30-10:05', '10:25-12:00', '12:20-13:55', '14:15-15:50', '16:10-17:45', '18:05-19:40', '19:50-21:25', '21:35-23:10'
])

// Додаємо цей масив після paraTimes
const roomSuggestions = ref([
  "128/Т", "122/Т", "5/Б", "6/Т", "3/Т", "406/Т", "422/Т", "313/Т",
  "2/Б", "6(хім.факульт.)", "118/Б", "408/Б", "4/Т", "412/Т", "214/Б", "213/Т",
  "9/Б", "416/Б", "405/Б", "1/Б", "123/Т", "424/Т", "10/Б", "223/Т", " 406/Т",
  "206/Т", "4/Б", "2/Т", "409/Б", "414/Т", "106/Б", "324/Т", "312/Т", "002/Т",
  "210/Т", "129а/Т", "423/Т", "403/Б", " 128/Т", "7/Т", "115/Б", "413/Т", "1/Т",
  "130/Т", "122/T", " 129/Т", "11/Б", "3/Б", "407/Т", "8/Б", " 1/Б", "401/Б",
  "12/Т", "129/Т"
]);

// Фільтри
const filters = ref({
  name_group: '',
  number_of_subgroup: null,
  day_of_week: null,
  nominator: null,
  namb_of_para: null,
  name_of_para: '',
  room: '',
  teacher: '',
  busy: null
})

// Обробник зміни статусу зайнятості
const handleBusyChange = () => {
  if (filters.value.busy === false) {
    showFreeScheduleGrid.value = true;
    filters.value.namb_of_para = null;
    if (filters.value.room) {
      fetchData();
    }
  } else {
    showFreeScheduleGrid.value = false;
    roomScheduleData.value = null;
  }
}

// Перевіряємо, чи є записи для дня
const hasDayInSchedule = (day) => {
  if (showFreeScheduleGrid.value) return daysOfWeek.value.includes(day);
  return groupedScheduleData.value.some(item => item.day_of_week === day);
}

// Фільтруємо розклад для дня
const filterByDay = (day) => groupedScheduleData.value.filter(item => item.day_of_week === day);

// Отримуємо час пари
const getParaTime = (paraNumber) => paraTimes.value[paraNumber] || 'Невідомо';

// Перевіряємо, чи пара вільна
const isParaFree = (day, paraNumber) => {
  const busyItems = scheduleData.value.filter(item => 
    item.day_of_week === day && item.namb_of_para === paraNumber && item.busy === true
  );
  return busyItems.length === 0;
}

// Debounce для фільтрів
let debounceTimer = null
const debounceFetch = () => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(fetchData, 300);
}

// Завантаження даних
const fetchData = async () => {
  try {
    loading.value = true;
    error.value = null;
    if (filters.value.busy === false && filters.value.room) {
      await fetchRoomSchedule();
      return;
    } else if (filters.value.busy === false && filters.value.name_group) {
      // const response = await axios.get('https://backend-roomsheduler.onrender.com/free_slots/', 
      const response = await axios.get('http://localhost:8000/free_slots/', 

      {
        params: { name_group: filters.value.name_group }
      });
      scheduleData.value = response.data;
      showFreeScheduleGrid.value = true;
    } else {
      const params = {};
      Object.entries(filters.value).forEach(([key, value]) => {
        if (value !== null && value !== '') params[key] = value;
      });
      const response = await axios.get('http://localhost:8000/days/', { params });
      // const response = await axios.get('https://backend-roomsheduler.onrender.com/days/', { params });
      scheduleData.value = response.data;
      showFreeScheduleGrid.value = false;
    }
  } catch (err) {
    error.value = `Помилка: ${err.response?.data?.detail || err.message}`;
    scheduleData.value = [];
    roomScheduleData.value = null;
  } finally {
    loading.value = false;
  }
}

// Слідкуємо за змінами room
watch(() => filters.value.room, (newVal) => {
  if (newVal && filters.value.busy === false) fetchData();
});

// Скидання фільтрів
const resetFilters = () => {
  filters.value = {
    name_group: '',
    number_of_subgroup: null,
    day_of_week: null,
    nominator: null,
    time_of_para: '',
    namb_of_para: null,
    name_of_para: '',
    room: '',
    teacher: '',
    busy: null
  };
  showFreeScheduleGrid.value = false;
  roomScheduleData.value = null;
}

// Завантажуємо дані при старті
onMounted(fetchData)

// Add these after roomSuggestions ref
const showSuggestions = ref(false)
const filteredRooms = ref([])
const isFetchingRooms = ref(false)

const handleRoomInput = async (event) => {
  const input = event.target.value
  filters.value.room = input
  showSuggestions.value = true
  
  try {
    isFetchingRooms.value = true
    // Create params object with all current filters
    const params = {
      query: input,
      ...Object.fromEntries(
        Object.entries(filters.value)
          .filter(([key, value]) => 
            value !== null && 
            value !== '' && 
            key !== 'room' // Exclude the room filter itself
          )
          .map(([key, value]) => {
            // Map frontend parameter names to backend parameter names
            const paramMap = {
              'namb_of_para': 'number_of_para',
              'name_of_para': 'name_of_para',
              'name_group': 'name_group',
              'number_of_subgroup': 'number_of_subgroup',
              'day_of_week': 'day_of_week',
              'nominator': 'nominator',
              'teacher': 'teacher',
              'busy': 'busy'
            }
            return [paramMap[key] || key, value]
          })
      )
    }
    
    // If we have a group selected, ensure we're only getting rooms for that group
    if (filters.value.name_group) {
      params.name_group = filters.value.name_group
    }
    
    console.log('Fetching room suggestions with params:', params) // Debug log
    const response = await axios.get('http://localhost:8000/rooms/suggestions/', { params })
    // const response = await axios.get('https://backend-roomsheduler.onrender.com/rooms/suggestions/', { params })
    console.log('Received room suggestions:', response.data) // Debug log
    
    // Ensure we have an array of suggestions
    filteredRooms.value = Array.isArray(response.data) ? response.data : []
    
    // If no suggestions and we have input, don't fall back to local filtering
    // as it won't respect the group filter
    if (filteredRooms.value.length === 0) {
      filteredRooms.value = []
    }
  } catch (err) {
    console.error('Error fetching room suggestions:', err)
    filteredRooms.value = []
  } finally {
    isFetchingRooms.value = false
  }
}

const selectRoom = (room) => {
  filters.value.room = room
  showSuggestions.value = false
  debounceFetch() // Fetch schedule data after selecting a room
}

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}
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

.loading, .error, .no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px; /* Reduced padding to minimize empty space */
  text-align: center;
  min-height: 100px; /* Ensure minimum height for visibility */
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(74, 144, 226, 0.2);
  border-radius: 50%;
  border-top-color: #4a90e2;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #e74c3c;
}

.error-icon, .no-data-icon {
  font-size: 32px;
  margin-bottom: 15px;
}

.schedule-container {
  padding: 15px;
  margin-bottom: 0; /* Remove bottom margin */
}

.day-group {
  margin-bottom: 15px; /* Reduced margin to minimize empty space */
}

.day-title {
  padding: 10px 15px;
  background-color: #f0f4f8;
  border-radius: 6px;
  margin-bottom: 10px; /* Reduced margin */
  color: #2c3e50;
  font-weight: 600;
}

.schedule {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.schedule-item {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.schedule-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.schedule-item.busy {
  border-left: 4px solid #e74c3c;
}

.item-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.item-group {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
}

.item-subgroup {
  margin-left: 5px;
  font-size: 14px;
  color: #7f8c8d;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-para {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.para-number {
  font-weight: 500;
  color: #34495e;
}

.para-time {
  font-size: 14px;
  color: #7f8c8d;
}

.item-subject {
  font-weight: 600;
  font-size: 16px;
  color: #2c3e50;
  margin: 5px 0;
}

.item-location, .item-teacher, .item-nominator {
  font-size: 14px;
  color: #7f8c8d;
}

.item-status {
  margin-top: 8px;
  font-size: 14px;
}

.status-busy {
  color: #e74c3c;
  font-weight: 500;
}

.status-free {
  color: #27ae60;
  font-weight: 500;
}

/* Стилі для сітки вільних пар */
.free-schedule-grid {
  display: grid;
  grid-template-columns: 80px 150px 1fr;
  gap: 1px;
  background-color: #e0e0e0;
  border: 1px solid #e0e0e0;
  margin-bottom: 0; /* Remove bottom margin */
}

.grid-header {
  display: contents;
}

.grid-header .grid-cell {
  background-color: #4a90e2;
  color: white;
  padding: 10px;
  font-weight: 500;
  text-align: center;
}

.grid-row {
  display: contents;
}

.grid-row:nth-child(odd) .grid-cell {
  background-color: #f8f9fa;
}

.grid-row:nth-child(even) .grid-cell {
  background-color: #ffffff;
}

.grid-cell {
  padding: 10px;
  text-align: center;
}

.free-para .grid-cell {
  background-color: #e8f5e9 !important;
}

.free-para:hover .grid-cell {
  background-color: #d0e9d1 !important;
}

.room-schedule {
  padding: 15px; /* Reduced padding */
  margin-bottom: 0; /* Remove bottom margin */
  background-color: #f8f9fa;
  border-radius: 8px;
}

.day-schedule {
  margin-bottom: 15px; /* Reduced margin */
}

.para-item {
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  background-color: #fff;
  border-left: 4px solid #e74c3c;
}

.para-item.free {
  border-left-color: #27ae60;
}

.para-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-weight: 500;
}

.para-number {
  font-weight: 600;
}

.para-status.free {
  color: #27ae60;
}

.para-status.busy {
  color: #e74c3c;
}

.para-details {
  font-size: 14px;
  color: #555;
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