from datetime import datetime, date, time, timedelta

class Holiday:
    def is_holiday(self, check_date: date):
        raise NotImplementedError("Subclasses should implement this method.")

class SingleHoliday(Holiday):
    def __init__(self, day, month, year):
        self.holiday_date = date(year, month, day)

    def is_holiday(self, check_date: date):
        return self.holiday_date == check_date
    
class RecurringHoliday(Holiday):
    def __init__(self, month: int, day: int):
        self.month = month
        self.day = day

    def is_holiday(self, check_date: date):
        return check_date.month == self.month and check_date.day == self.day

class WorkdayCalendar:
    """
        Assumptions:
        - Workdays never go over midnight
    """
    def __init__(self, start_datetime: datetime, workday_start = time(8, 0), workday_end = time(16, 0)):
        self.holidays = []
        self.workday_start = workday_start  # Default start 8:00
        self.workday_end = workday_end      # Default end 16:00
        self.start_datetime = start_datetime

        dummy_date = date(2000, 1, 1)
        wd_start = datetime.combine(dummy_date, self.workday_start)
        wd_end = datetime.combine(dummy_date, self.workday_end)
        
        self.workday_duration = wd_end - wd_start 

    def set_single_holiday(self, day, month, year):
        holiday = SingleHoliday(day, month, year)
        if holiday not in self.holidays:
            self.holidays.append(holiday)

    def set_recurring_holiday(self, month, day):
        holiday = RecurringHoliday(month, day)
        if holiday not in self.holidays:
            self.holidays.append(holiday)

    def is_workday(self, check_date: date) -> bool:
        if check_date.weekday() >= 5:  # Saturday or Sunday
            return False
        for holiday in self.holidays:
            if holiday.is_holiday(check_date):
                return False
        return True
    
    def _get_datetime_on_boundary(self, dt: datetime, direction: int) -> datetime:
        check_date = dt.date()
        check_time = dt.time()
        
        wd_start = self.workday_start
        wd_end = self.workday_end

        if self.is_workday(check_date) and wd_start <= check_time < wd_end:
            return dt
        
        if self.is_workday(check_date) and check_time == wd_end:
            if direction < 0:
                return dt
        
        current_dt = dt
        
        if direction > 0:
            if check_time < wd_start:
                current_dt = datetime.combine(check_date, wd_start)
            elif check_time >= wd_end:
                current_dt = datetime.combine(check_date + timedelta(days=1), wd_start)
        else: 
            if check_time > wd_end:
                current_dt = datetime.combine(check_date, wd_end)
            elif check_time <= wd_start:
                current_dt = datetime.combine(check_date - timedelta(days=1), wd_end)

        while not self.is_workday(current_dt.date()):
            current_dt += timedelta(days=direction) 
            current_time = wd_start if direction > 0 else wd_end
            current_dt = datetime.combine(current_dt.date(), current_time)
            
        return current_dt
    
    def calculate_workday_offset(self, offset_days: float) -> datetime:
        if offset_days == 0:
            return self.start_datetime

        direction = 1 if offset_days > 0 else -1

        seconds_needed = abs(offset_days * self.workday_duration.total_seconds())
        time_remaining = timedelta(seconds=seconds_needed)

        current_dt = self._get_datetime_on_boundary(self.start_datetime, direction)

        while time_remaining.total_seconds() > 1e-6:
            if direction > 0:
                wd_end = datetime.combine(current_dt.date(), self.workday_end)
                available_time = wd_end - current_dt
            else:
                wd_start = datetime.combine(current_dt.date(), self.workday_start)
                available_time = current_dt - wd_start
            if available_time.total_seconds() >= time_remaining.total_seconds():
                current_dt += (time_remaining * direction)
                return current_dt
            
            time_remaining -= available_time
            current_dt += timedelta(days=direction)
            
            while not self.is_workday(current_dt.date()):
                current_dt += timedelta(days=direction)
            
            new_time = self.workday_start if direction > 0 else self.workday_end
            current_dt = datetime.combine(current_dt.date(), new_time)

        return current_dt 

