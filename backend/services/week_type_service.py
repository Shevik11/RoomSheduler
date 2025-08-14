from datetime import datetime, timedelta


class WeekTypeService:
    def __init__(self):
        # start date (1 september 2023) - can be changed to the desired one
        self.start_date = datetime(2023, 9, 1)
        self.week_types = ["Чисельник", "Знаменник"]

    def get_current_week_type(self) -> dict:
        """
        determine current week type (numerator/denominator)
        """
        current_date = datetime.now()

        # count number of weeks from start date
        weeks_passed = (current_date - self.start_date).days // 7

        # determine week type (0 - numerator, 1 - denominator)
        week_type_index = weeks_passed % 2
        current_week_type = self.week_types[week_type_index]

        # determine start date of current week
        current_week_start = current_date - timedelta(days=current_date.weekday())
        current_week_end = current_week_start + timedelta(days=6)

        return {
            "week_type": current_week_type,
            "week_start": current_week_start.strftime("%Y-%m-%d"),
            "week_end": current_week_end.strftime("%Y-%m-%d"),
            "current_date": current_date.strftime("%Y-%m-%d"),
        }

    def get_week_type_for_date_range(self, start_date: str, end_date: str) -> dict:
        # determine week type for given date range
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            # if range is greater than week, take first week
            if (end - start).days > 7:
                end = start + timedelta(days=6)

            # count number of weeks from start date
            weeks_passed = (start - self.start_date).days // 7

            # determine week type (0 - numerator, 1 - denominator)
            week_type_index = weeks_passed % 2
            week_type = self.week_types[week_type_index]

            # determine start date of week
            week_start = start - timedelta(days=start.weekday())
            week_end = week_start + timedelta(days=6)

            return {
                "week_type": week_type,
                "week_start": week_start.strftime("%Y-%m-%d"),
                "week_end": week_end.strftime("%Y-%m-%d"),
                "requested_start_date": start_date,
                "requested_end_date": end_date,
            }
        except ValueError:
            raise ValueError(
                "Неправильний формат дати. Використовуйте формат YYYY-MM-DD"
            )


week_type_service = WeekTypeService()
