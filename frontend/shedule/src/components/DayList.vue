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
          <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <!-- Фільтр за часом пари -->
      <div class="filter-item">
        <label for="time_of_para">Час пари:</label>
        <input 
          id="time_of_para"
          v-model="filters.time_of_para" 
          @input="debounceFetch" 
          placeholder="Час (напр. 8:30-10:05)"
          class="filter-input"
        />
      </div>

      <!-- Фільтр за назвою предмета -->
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
        <input 
          id="room"
          v-model="filters.room" 
          @input="debounceFetch" 
          placeholder="Введіть номер аудиторії"
          class="filter-input"
        />
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
  <div v-if="!loading && !error && scheduleData.length === 0" class="no-data">
    <i class="no-data-icon">📭</i>
    <p>Немає даних, що відповідають заданим фільтрам</p>
  </div>

  <!-- Відображення розкладу -->
  <div v-if="!loading && !error && scheduleData.length > 0" class="schedule-container">
    <h3>Знайдено записів: {{ scheduleData.length }}</h3>
    
    <!-- Групування по дням тижня -->
    <div v-for="day in daysOfWeek" :key="day" class="day-group">
      <h4 v-if="hasDayInSchedule(day)" class="day-title">{{ day }}</h4>
      
      <div class="schedule">
        <div 
          v-for="item in filterByDay(day)" 
          :key="`${item.id}-${item.name_group}-${item.namb_of_para}`" 
          :class="['schedule-item', {'busy': item.busy}]"
        >
          <div class="item-header">
            <span class="item-group">{{ item.name_group }}</span>
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

// Стани
const loading = ref(true)
const error = ref(null)
const scheduleData = ref([])

// Дні тижня
const daysOfWeek = ref([
  'Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота'
])

// Фільтри
const filters = ref({
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
})

// Перевіряємо, чи є записи для конкретного дня тижня
const hasDayInSchedule = (day) => {
  return scheduleData.value.some(item => item.day_of_week === day);
}

// Фільтруємо розклад для конкретного дня тижня (для відображення)
const filterByDay = (day) => {
  return scheduleData.value.filter(item => item.day_of_week === day);
}

// Функція для debounce введення в полях фільтрів
const debounceFetch = () => {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(fetchData, 300);
}

// Завантаження даних з сервера
const fetchData = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Формуємо параметри запиту, видаляючи пусті значення
    const params = {}
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        params[key] = value
      }
    })
    
    console.log('Відправка запиту з параметрами:', params)
    
    // Використовуємо endpoint /days/ з фільтрами
    const response = await axios.get('http://localhost:8000/days/', { params })
    
    // Перевіряємо, що дані в правильному форматі
    if (!Array.isArray(response.data)) {
      throw new Error('Невірний формат даних від сервера')
    }
    
    scheduleData.value = response.data
    console.log('Отримані дані:', scheduleData.value)
    console.log('Кількість записів:', scheduleData.value.length)
  } catch (err) {
    console.error('Помилка завантаження:', err)
    error.value = `Помилка завантаження: ${err.message}`
    scheduleData.value = [] // Очищаємо дані при помилці
  } finally {
    loading.value = false
  }
}

// Слідкуємо за змінами фільтрів і оновлюємо дані
watch(filters, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchData, 300)
}, { deep: true })

let debounceTimer = null

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
  }
}

// Завантажуємо початкові дані при старті
onMounted(fetchData)
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
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
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
  gap: 10px;
  align-items: flex-end;
}

.reset-button, .apply-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
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
  padding: 40px 20px;
  text-align: center;
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
}

.day-group {
  margin-bottom: 30px;
}

.day-title {
  padding: 10px 15px;
  background-color: #f0f4f8;
  border-radius: 6px;
  margin-bottom: 15px;
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
</style>