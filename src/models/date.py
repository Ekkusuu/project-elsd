from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Date:
    year: int
    month: Optional[int] = None
    day: Optional[int] = None

    def __init__(self, date_dict: Dict):
        if 'year' not in date_dict:
            raise ValueError("Year is required")
        
        self.year = date_dict.get('year')
        self.month = date_dict.get('month')
        self.day = date_dict.get('day')

        if not isinstance(self.year, int):
            raise ValueError("Year must be an integer")

        if self.month is not None:
            if not isinstance(self.month, int):
                raise ValueError("Month must be an integer")
            if not 1 <= self.month <= 12:
                raise ValueError("Month must be between 1 and 12")

        if self.day is not None:
            if not isinstance(self.day, int):
                raise ValueError("Day must be an integer")
            if self.month is None:
                raise ValueError("Cannot specify day without month")

            days_in_month = self._days_in_month(self.year, self.month)
            if not 1 <= self.day <= days_in_month:
                raise ValueError(f"Day must be between 1 and {days_in_month} for month {self.month}")

    def _days_in_month(self, year: int, month: int) -> int:
        days_per_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if month == 2 and self._is_leap_year(year):
            return 29
            
        return days_per_month[month]

    def _is_leap_year(self, year: int) -> bool:
        calc_year = year if year > 0 else abs(year) + 1
        
        # Leap year rules:
        # 1. Year must be divisible by 4
        # 2. If divisible by 100, must also be divisible by 400
        return calc_year % 4 == 0 and (calc_year % 100 != 0 or calc_year % 400 == 0)

    def __str__(self) -> str:
        parts = []

        if self.day is not None:
            parts.append(f"{self.day}")

        if self.month is not None:
            parts.append(f"{self.month}")

        year_str = f"{abs(self.year)}"
        if self.year < 0:
            year_str += " BCE"
        else:
            year_str += " CE"
        parts.append(year_str)
        
        return "-".join(parts)

    def __lt__(self, other):
        if not isinstance(other, Date):
            raise TypeError("Can only compare with another Date object")
        
        # Compare years first
        if self.year != other.year:
            return self.year < other.year
            
        # If months are available, compare them
        if self.month is not None and other.month is not None:
            if self.month != other.month:
                return self.month < other.month
        elif self.month is not None:
            # If this date has a month but other doesn't, this is more specific
            return False
        elif other.month is not None:
            # If other date has a month but this doesn't, other is more specific
            return True
                
        # If days are available, compare them
        if self.day is not None and other.day is not None:
            if self.day != other.day:
                return self.day < other.day
        elif self.day is not None:
            # If this date has a day but other doesn't, this is more specific
            return False
        elif other.day is not None:
            # If other date has a day but this doesn't, other is more specific
            return True
            
        return False

    def __eq__(self, other):
        if not isinstance(other, Date):
            return False
        return (self.year == other.year and 
                self.month == other.month and 
                self.day == other.day)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other 