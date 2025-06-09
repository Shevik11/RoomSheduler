from datetime import datetime, timedelta

class WeekTypeService:
    def __init__(self):
        # Початкова дата (1 вересня 2023) - можна змінити на потрібну
        self.start_date = datetime(2023, 9, 1)
        self.week_types = ["Чисельник", "Знаменник"]

    def get_current_week_type(self) -> dict:
        """
        Визначає поточний тип тижня (чисельник/знаменник)
        """
        current_date = datetime.now()
        
        # Рахуємо кількість тижнів від початкової дати
        weeks_passed = (current_date - self.start_date).days // 7
        
        # Визначаємо тип тижня (0 - чисельник, 1 - знаменник)
        week_type_index = weeks_passed % 2
        current_week_type = self.week_types[week_type_index]
        
        # Визначаємо дату початку поточного тижня
        current_week_start = current_date - timedelta(days=current_date.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        
        return {
            "week_type": current_week_type,
            "week_start": current_week_start.strftime("%Y-%m-%d"),
            "week_end": current_week_end.strftime("%Y-%m-%d"),
            "current_date": current_date.strftime("%Y-%m-%d")
        }

week_type_service = WeekTypeService() 