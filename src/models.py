from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime
import json

@dataclass
class Date:
    year: int
    month: Optional[int] = None
    day: Optional[int] = None

    def __init__(self, date_dict: Dict):
        # Validate required year
        if 'year' not in date_dict:
            raise ValueError("Year is required")
        
        self.year = date_dict.get('year')
        self.month = date_dict.get('month')
        self.day = date_dict.get('day')
        
        # Validate year
        if not isinstance(self.year, int):
            raise ValueError("Year must be an integer")
        
        # Validate month if provided
        if self.month is not None:
            if not isinstance(self.month, int):
                raise ValueError("Month must be an integer")
            if not 1 <= self.month <= 12:
                raise ValueError("Month must be between 1 and 12")
                
        # Validate day if provided
        if self.day is not None:
            if not isinstance(self.day, int):
                raise ValueError("Day must be an integer")
            if self.month is None:
                raise ValueError("Cannot specify day without month")
            
            # Get days in month (accounting for leap years)
            days_in_month = self._days_in_month(self.year, self.month)
            if not 1 <= self.day <= days_in_month:
                raise ValueError(f"Day must be between 1 and {days_in_month} for month {self.month}")

    def _days_in_month(self, year: int, month: int) -> int:
        """Calculate the number of days in a given month of a year."""
        days_per_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if month == 2 and self._is_leap_year(year):
            return 29
            
        return days_per_month[month]

    def _is_leap_year(self, year: int) -> bool:
        """Determine if a year is a leap year."""        
        calc_year = year if year > 0 else abs(year) + 1
        
        # Leap year rules:
        # 1. Year must be divisible by 4
        # 2. If divisible by 100, must also be divisible by 400
        return calc_year % 4 == 0 and (calc_year % 100 != 0 or calc_year % 400 == 0)

    def __str__(self) -> str:
        """Return a human-readable string representation of the date."""
        parts = []
        
        # Add day if available
        if self.day is not None:
            parts.append(f"{self.day}")
            
        # Add month if available
        if self.month is not None:
            parts.append(f"{self.month}")
            
        # Add year with BCE/CE
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

class TimelineComponent:
    def __init__(self, id: str, title: str, importance: str = "MEDIUM"):
        self.id = id
        self.title = title
        self._importance = None
        self.importance = importance  # Using the setter

    @property
    def importance(self) -> str:
        return self._importance

    @importance.setter
    def importance(self, value: str):
        valid_importance = ["HIGH", "MEDIUM", "LOW"]
        if value.upper() not in valid_importance:
            raise ValueError(f"Importance must be one of {valid_importance}")
        self._importance = value.upper()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "importance": self.importance
        }


class Event(TimelineComponent):
    def __init__(self, id: str, title: str, date: Dict, importance: str = "MEDIUM"):
        super().__init__(id, title, importance)
        self.date = Date(date)

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict["date"] = {
            "year": self.date.year,
            "month": self.date.month,
            "day": self.date.day
        }
        return base_dict

    def export_json(self, filename: str = None):
        if filename is None:
            filename = f"{self.id}.json"
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class Period(TimelineComponent):
    def __init__(self, id: str, title: str, start: Dict, end: Dict, importance: str = "MEDIUM"):
        super().__init__(id, title, importance)
        self.start = Date(start)
        self.end = Date(end)
        self.validate_dates()

    def validate_dates(self):
        if self.end < self.start:
            raise ValueError(f"End date ({self.end}) cannot be before start date ({self.start})")

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "start": {
                "year": self.start.year,
                "month": self.start.month,
                "day": self.start.day
            },
            "end": {
                "year": self.end.year,
                "month": self.end.month,
                "day": self.end.day
            }
        })
        return base_dict

    def export_json(self, filename: str = None):
        if filename is None:
            filename = f"{self.id}.json"
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class Relationship:
    VALID_TYPES = {
        "CAUSE_EFFECT", "CONTEMPORANEOUS", "PRECEDES", 
        "FOLLOWS", "INCLUDES", "EXCLUDES"
    }

    def __init__(self, id: str, from_component: TimelineComponent, 
                 to_component: TimelineComponent, relationship_type: str):
        self.id = id
        self.from_component = from_component
        self.to_component = to_component
        self._type = None
        self.type = relationship_type  # Using the setter
        self.validate_relationship()

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        clean_value = value.upper().replace("-", "_")
        if clean_value not in self.VALID_TYPES:
            raise ValueError(f"Relationship type must be one of {self.VALID_TYPES}")
        self._type = clean_value

    def validate_relationship(self):
        # Add specific validation rules for each relationship type
        if self.type == "INCLUDES":
            if not isinstance(self.from_component, Period):
                raise ValueError("'INCLUDES' relationship requires a Period as the 'from' component")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "from": self.from_component.id,
            "to": self.to_component.id,
            "type": self.type
        }


class Timeline:
    def __init__(self, id: str, title: str, components: List[TimelineComponent]):
        self.id = id
        self.title = title
        self.components = components
        self.validate_components()

    def validate_components(self):
        if not self.components:
            raise ValueError("Timeline must have at least one component")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "components": [comp.to_dict() for comp in self.components]
        }

    def export_json(self, filename: str = None):
        if filename is None:
            filename = f"{self.id}.json"
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def export_png(self):
        pass
