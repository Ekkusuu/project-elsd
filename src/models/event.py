import json
import os
from typing import Dict
from .timeline_component import TimelineComponent
from .date import Date

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
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        # Create full path for the file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2) 