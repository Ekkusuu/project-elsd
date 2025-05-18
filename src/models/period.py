import json
import os
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
            "type": "period",
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

    def to_json(self) -> str:
        """Generate the period data as a JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def export_json(self, filename: str = None):
        if filename is None:
            filename = f"{self.id}.json"
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        # Create full path for the file
        filepath = os.path.join(output_dir, filename)
        # Generate and save JSON
        json_data = self.to_json()
        with open(filepath, 'w') as f:
            f.write(json_data) 