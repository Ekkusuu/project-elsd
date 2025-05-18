import json
from typing import Dict
from .timeline_component import TimelineComponent
from .date import Date

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