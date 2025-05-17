from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import defaultdict


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
    HIGH_COLORS = ["#1E90FF", "#007FFF", "#3399FF", "#0055FF", "#4682B4", "#4169E1", "#0000CD", "#0000FF"]
    MEDIUM_COLORS = ["#00FF00", "#32CD32", "#3CB371", "#2ECC71", "#228B22", "#66FF66", "#7CFC00", "#20C997"]
    LOW_COLORS = ["#FFD700", "#FFC300", "#FFB000", "#FFA500", "#FF8C00", "#FF7F50", "#FF6F00", "#FF4500"]

    def __init__(self, id: str, title: str, components: List[TimelineComponent]):
        self.id = id
        self.title = title
        self.components = components
        self.validate_components()

    def validate_components(self):
        if not self.components:
            raise ValueError("Timeline must have at least one component")

    def _get_date_range(self):
        dates = []
        for comp in self.components:
            if isinstance(comp, Event):
                dates.append(comp.date)
            elif isinstance(comp, Period):
                dates.extend([comp.start, comp.end])
        return min(dates), max(dates)

    def _calculate_levels(self, components):
        sorted_comps = sorted(
            components,
            key=lambda x: x.date.year if isinstance(x, Event) else x.start.year
        )

        # Group components by year
        year_groups = defaultdict(list)
        for comp in sorted_comps:
            year = comp.date.year if isinstance(comp, Event) else comp.start.year
            year_groups[year].append(comp)

        # Calculate levels for each component
        levels = {}
        unique_years = sorted(year_groups.keys())
        
        for i, year in enumerate(unique_years):
            comps_in_year = year_groups[year]
            base_level = 1.0 if i % 2 == 0 else -1.0
            
            # Adjust level based on importance
            for j, comp in enumerate(comps_in_year):
                if len(comps_in_year) > 1:
                    # If multiple components in the same year, stack them
                    level = base_level * (1 + 0.5 * j)
                else:
                    level = base_level
                    
                # Adjust level based on importance
                importance_factor = {
                    "HIGH": 1.2,
                    "MEDIUM": 1.0,
                    "LOW": 0.8
                }
                level *= importance_factor[comp.importance]
                levels[comp] = level

        return levels

    def export_png(self, filename: str = None):
        if filename is None:
            filename = f"{self.id}.png"

        # Create figure
        fig, ax = plt.subplots(figsize=(15, 8), layout='constrained')
        
        # Get date range
        min_date, max_date = self._get_date_range()
        year_span = max_date.year - min_date.year
        margin = year_span * 0.05  # 5% margin
        ax.set_xlim(min_date.year - margin, max_date.year + margin)

        # Calculate levels for components
        levels = self._calculate_levels(self.components)

        # Draw baseline
        ax.axhline(0, color='black', linewidth=1.5, zorder=1)

        # Sort components for drawing
        sorted_components = sorted(
            self.components,
            key=lambda x: (
                x.date.year if isinstance(x, Event) else x.start.year,
                -["HIGH", "MEDIUM", "LOW"].index(x.importance)
            )
        )

        # Track used positions for periods
        period_positions = []
        legend_entries = []

        # Color management
        color_indices = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        color_sets = {"HIGH": self.HIGH_COLORS, "MEDIUM": self.MEDIUM_COLORS, "LOW": self.LOW_COLORS}

        def get_next_color(importance):
            idx = color_indices[importance]
            color_list = color_sets[importance]
            color = color_list[idx % len(color_list)]
            color_indices[importance] += 1
            return color

        # Draw components
        for component in sorted_components:
            color = get_next_color(component.importance)
            level = levels[component]

            if isinstance(component, Event):
                # Draw vertical line (stem)
                ax.vlines(component.date.year, 0, level, color=color, linewidth=1.5, zorder=2)
                
                # Draw marker on baseline
                ax.plot(component.date.year, 0, 'o', color=color, 
                       markersize=8, markeredgecolor='black', zorder=3)
                
                # Add label
                ax.annotate(
                    component.title,
                    xy=(component.date.year, level),
                    xytext=(0, np.sign(level) * 5),
                    textcoords='offset points',
                    ha='center',
                    va='bottom' if level > 0 else 'top',
                    fontsize=10,
                    fontweight='bold' if component.importance == "HIGH" else 'normal',
                    bbox=dict(
                        boxstyle='round,pad=0.5',
                        fc='white',
                        ec=color,
                        alpha=0.8,
                        lw=1
                    ),
                    zorder=4
                )

                # Add to legend
                legend_entries.append((
                    patches.Circle((0, 0), fc=color, ec='black'),
                    f"{component.title} ({component.date.year})"
                ))

            elif isinstance(component, Period):
                # Draw period bar
                period_height = 0.1
                rect = patches.Rectangle(
                    (component.start.year, -period_height/2),
                    component.end.year - component.start.year,
                    period_height,
                    facecolor=color,
                    alpha=0.7,
                    zorder=2
                )
                ax.add_patch(rect)

                # Add period label
                mid_year = (component.start.year + component.end.year) / 2
                ax.annotate(
                    component.title,
                    xy=(mid_year, -period_height),
                    xytext=(0, -15),
                    textcoords='offset points',
                    ha='center',
                    va='top',
                    fontsize=10,
                    fontweight='bold' if component.importance == "HIGH" else 'normal',
                    bbox=dict(
                        boxstyle='round,pad=0.5',
                        fc='white',
                        ec=color,
                        alpha=0.8,
                        lw=1
                    ),
                    zorder=4
                )

                # Add to legend
                legend_entries.append((
                    patches.Rectangle((0, 0), 1, 1, fc=color, alpha=0.7),
                    f"{component.title} ({component.start.year} → {component.end.year})"
                ))

        # Configure axes
        ax.yaxis.set_visible(False)
        ax.spines[['left', 'top', 'right']].set_visible(False)
        
        # Set title
        ax.set_title(self.title, fontsize=14, fontweight='bold', pad=20)

        # Add legend
        if legend_entries:
            ax.legend(
                *zip(*legend_entries),
                loc='center left',
                bbox_to_anchor=(1.05, 0.5),
                fontsize=10,
                frameon=True,
                framealpha=0.8,
                title="Timeline Components"
            )

        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

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
