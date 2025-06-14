import json
from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from collections import defaultdict
from .timeline_component import TimelineComponent
from .event import Event
from .period import Period
from .relationship import Relationship
from .date import Date
import os
from io import BytesIO

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

        # Separate components by type and create lookup maps
        events_and_periods = []
        relationships = []
        component_map = {}

        # First pass: collect all events and periods
        for component in self.components:
            if isinstance(component, (Event, Period)):
                events_and_periods.append(component)
                component_map[component.id] = component
            elif isinstance(component, Relationship):
                relationships.append(component)

        # Second pass: update relationship references and validate
        for rel in relationships:
            # Check if both components exist in the timeline
            from_comp = component_map.get(rel.from_component.id)
            to_comp = component_map.get(rel.to_component.id)

            if not from_comp:
                raise ValueError(f"Relationship {rel.id}: 'from' component '{rel.from_component.id}' is not in the timeline")
            if not to_comp:
                raise ValueError(f"Relationship {rel.id}: 'to' component '{rel.to_component.id}' is not in the timeline")

            # Update relationship with actual component references
            rel.from_component = from_comp
            rel.to_component = to_comp

            # Validate temporal constraints based on relationship type
            if rel.type == "CAUSE_EFFECT":
                # For cause-effect, 'from' must be chronologically earlier than 'to'
                if isinstance(from_comp, Event) and isinstance(to_comp, Event):
                    if not (from_comp.date < to_comp.date):
                        raise ValueError(f"Relationship {rel.id}: In a cause-effect relationship, the cause ({from_comp.id}) must be earlier than the effect ({to_comp.id})")
                elif isinstance(from_comp, Period) and isinstance(to_comp, (Event, Period)):
                    if isinstance(to_comp, Event):
                        if not (from_comp.start < to_comp.date):
                            raise ValueError(f"Relationship {rel.id}: In a cause-effect relationship, the cause period ({from_comp.id}) must start before the effect ({to_comp.id})")
                    else:  # to_comp is Period
                        if not (from_comp.start < to_comp.start):
                            raise ValueError(f"Relationship {rel.id}: In a cause-effect relationship, the cause period ({from_comp.id}) must start before the effect period ({to_comp.id})")
                elif isinstance(from_comp, Event) and isinstance(to_comp, Period):
                    if not (from_comp.date < to_comp.end):
                        raise ValueError(f"Relationship {rel.id}: In a cause-effect relationship, the cause ({from_comp.id}) must be earlier than the end of the effect period ({to_comp.id})")

            elif rel.type == "PRECEDES":
                # For precedes, 'from' must end before 'to' starts
                from_date = from_comp.date if isinstance(from_comp, Event) else from_comp.end
                to_date = to_comp.date if isinstance(to_comp, Event) else to_comp.start
                if not (from_date < to_date):
                    raise ValueError(f"Relationship {rel.id}: In a precedes relationship, {from_comp.id} must be before {to_comp.id}")

            elif rel.type == "FOLLOWS":
                # For follows, 'to' must end before 'from' starts
                from_date = from_comp.date if isinstance(from_comp, Event) else from_comp.start
                to_date = to_comp.date if isinstance(to_comp, Event) else to_comp.end
                if not (to_date < from_date):
                    raise ValueError(f"Relationship {rel.id}: In a follows relationship, {to_comp.id} must be before {from_comp.id}")

            elif rel.type == "CONTEMPORANEOUS":
                # For contemporaneous, components must overlap in time
                if isinstance(from_comp, Event) and isinstance(to_comp, Event):
                    if from_comp.date != to_comp.date:
                        raise ValueError(f"Relationship {rel.id}: In a contemporaneous relationship between events, {from_comp.id} and {to_comp.id} must occur at the same time")
                elif isinstance(from_comp, Period) and isinstance(to_comp, Period):
                    if not (from_comp.start <= to_comp.end and to_comp.start <= from_comp.end):
                        raise ValueError(f"Relationship {rel.id}: In a contemporaneous relationship between periods, {from_comp.id} and {to_comp.id} must overlap")
                else:  # One is Event, one is Period
                    event = from_comp if isinstance(from_comp, Event) else to_comp
                    period = to_comp if isinstance(to_comp, Period) else from_comp
                    if not (period.start <= event.date <= period.end):
                        raise ValueError(f"Relationship {rel.id}: In a contemporaneous relationship, event {event.id} must occur during period {period.id}")

            elif rel.type == "INCLUDES":
                # Already validated in Relationship class that 'from' is a Period
                if isinstance(to_comp, Event):
                    if not (from_comp.start <= to_comp.date <= from_comp.end):
                        raise ValueError(f"Relationship {rel.id}: In an includes relationship, event {to_comp.id} must occur within period {from_comp.id}")
                else:  # to_comp is Period
                    if not (from_comp.start <= to_comp.start and to_comp.end <= from_comp.end):
                        raise ValueError(f"Relationship {rel.id}: In an includes relationship, period {to_comp.id} must be entirely within period {from_comp.id}")

            elif rel.type == "EXCLUDES":
                if isinstance(from_comp, Period) and isinstance(to_comp, Period):
                    if from_comp.start <= to_comp.end and to_comp.start <= from_comp.end:
                        raise ValueError(f"Relationship {rel.id}: In an excludes relationship, periods {from_comp.id} and {to_comp.id} must not overlap")
                elif isinstance(from_comp, Period):
                    if from_comp.start <= to_comp.date <= from_comp.end:
                        raise ValueError(f"Relationship {rel.id}: In an excludes relationship, event {to_comp.id} must not occur during period {from_comp.id}")
                elif isinstance(to_comp, Period):
                    if to_comp.start <= from_comp.date <= to_comp.end:
                        raise ValueError(f"Relationship {rel.id}: In an excludes relationship, event {from_comp.id} must not occur during period {to_comp.id}")
                else:  # Both are events
                    if from_comp.date == to_comp.date:
                        raise ValueError(f"Relationship {rel.id}: In an excludes relationship, events {from_comp.id} and {to_comp.id} must not occur at the same time") 

    def _date_to_decimal(self, date):
        """Convert a Date object to a decimal year for precise positioning"""
        year = date.year
        if date.month is not None:
            year += (date.month - 1) / 12
            if date.day is not None:
                days_in_month = date._days_in_month(date.year, date.month)
                year += (date.day - 1) / (days_in_month * 12)
        return year

    def _get_date_range(self):
        dates = []
        for comp in self.components:
            if isinstance(comp, Event):
                dates.append(comp.date)
            elif isinstance(comp, Period):
                dates.extend([comp.start, comp.end])
        return min(dates), max(dates)

    def _calculate_tick_interval(self, min_date, max_date):
        """Calculate appropriate tick interval based on date range"""
        total_span = self._date_to_decimal(max_date) - self._date_to_decimal(min_date)
        
        # Calculate desired number of ticks based on timeline width
        # Aim for roughly one tick every 100 pixels (assuming default figure width of 15 inches * 100 DPI)
        target_ticks = 15 * 100 / 100  # 15 inches * 100 DPI / 100 pixels per tick
        
        if total_span <= 1/12:  # Less than a month
            if total_span <= 1/24:  # Less than 15 days
                return "days_dense"  # Show every day
            return "days"  # Show every other day
        elif total_span <= 1:  # Less than a year
            if total_span <= 1/4:  # Less than 3 months
                return "weeks"  # Show weeks
            return "months"  # Show months
        elif total_span <= 5:  # 1-5 years
            if total_span <= 2:  # 1-2 years
                return "months_dense"  # Show all months
            return "months_selective"  # Show quarterly
        elif total_span <= 20:  # 5-20 years
            if total_span <= 10:  # 5-10 years
                return "years_dense"  # Show all years
            return "years"  # Show every other year
        elif total_span <= 100:  # 20-100 years
            return "years_5"  # Show every 5 years
        else:
            return "years_10"  # Show every 10 years

    def _get_date_range_with_margin(self, min_date, max_date, interval_type):
        """Calculate the extended date range to ensure ticks before and after components"""
        min_decimal = self._date_to_decimal(min_date)
        max_decimal = self._date_to_decimal(max_date)
        span = max_decimal - min_decimal

        # Calculate base margin based on interval type
        if interval_type in ["days", "days_dense"]:
            step = 1 if interval_type == "days_dense" else 2
            margin = step / 365  # Convert days to years
        elif interval_type == "weeks":
            margin = 7 / 365  # One week margin
        elif interval_type in ["months", "months_dense", "months_selective"]:
            margin = 1/12  # One month margin
        elif interval_type == "years_dense":
            margin = 1
        elif interval_type == "years":
            margin = 2
        elif interval_type == "years_5":
            margin = 5
        else:  # years_10
            margin = 10

        # Scale down the margin for larger spans to avoid excessive padding
        if span > 100:
            margin *= 0.5
        elif span > 50:
            margin *= 0.6
        elif span > 20:
            margin *= 0.7
        elif span > 10:
            margin *= 0.8
        elif span > 5:
            margin *= 0.9

        # Ensure margin is between 2% and 5% of the span
        if span != 0:
            min_margin = span * 0.02
            max_margin = span * 0.06
            margin = max(min_margin, min(margin, max_margin))
        
        return min_decimal - margin, max_decimal + margin

    def _generate_ticks(self, min_date, max_date, interval_type):
        """Generate tick positions and labels based on interval type"""
        start_year = self._date_to_decimal(min_date)
        end_year = self._date_to_decimal(max_date)
        ticks = []
        
        if interval_type in ["days", "days_dense"]:
            # Generate daily ticks
            # Calculate the first tick before min_date
            step = 1 if interval_type == "days_dense" else 2
            current = Date({"year": min_date.year, "month": min_date.month, "day": min_date.day})
            
            # Move back to find the previous tick
            for _ in range(step):
                if current.day > 1:
                    current = Date({"year": current.year, "month": current.month, "day": current.day - 1})
                else:
                    if current.month == 1:
                        current = Date({"year": current.year - 1, "month": 12, "day": 31})
                    else:
                        prev_month = current.month - 1
                        days_in_prev_month = current._days_in_month(current.year, prev_month)
                        current = Date({"year": current.year, "month": prev_month, "day": days_in_prev_month})
            
            # Generate ticks including one before and after
            while current <= max_date or self._date_to_decimal(current) <= end_year + step/365:
                pos = self._date_to_decimal(current)
                # Show month/day on first day of month or if dense
                if current.day == 1 or interval_type == "days_dense":
                    label = f"{current.month}/{current.day}"
                else:
                    label = f"{current.day}"
                ticks.append((pos, label))
                
                # Move to next day(s)
                for _ in range(step):
                    if current.day < current._days_in_month(current.year, current.month):
                        current = Date({"year": current.year, "month": current.month, "day": current.day + 1})
                    else:
                        if current.month == 12:
                            current = Date({"year": current.year + 1, "month": 1, "day": 1})
                        else:
                            current = Date({"year": current.year, "month": current.month + 1, "day": 1})
                            
        elif interval_type == "weeks":
            # Generate weekly ticks
            # Start from a week before
            current = Date({"year": min_date.year, "month": min_date.month, "day": min_date.day})
            for _ in range(7):  # Go back one week
                if current.day > 1:
                    current = Date({"year": current.year, "month": current.month, "day": current.day - 1})
                else:
                    if current.month == 1:
                        current = Date({"year": current.year - 1, "month": 12, "day": 31})
                    else:
                        prev_month = current.month - 1
                        days_in_prev_month = current._days_in_month(current.year, prev_month)
                        current = Date({"year": current.year, "month": prev_month, "day": days_in_prev_month})
            
            # Generate ticks including one before and after
            while current <= max_date or self._date_to_decimal(current) <= end_year + 7/365:
                pos = self._date_to_decimal(current)
                label = f"{current.month}/{current.day}"
                ticks.append((pos, label))
                
                # Move to next week
                for _ in range(7):
                    if current.day < current._days_in_month(current.year, current.month):
                        current = Date({"year": current.year, "month": current.month, "day": current.day + 1})
                    else:
                        if current.month == 12:
                            current = Date({"year": current.year + 1, "month": 1, "day": 1})
                        else:
                            current = Date({"year": current.year, "month": current.month + 1, "day": 1})
                            
        elif interval_type in ["months", "months_dense", "months_selective"]:
            # Calculate the first tick before min_date
            current = Date({"year": min_date.year, "month": min_date.month})
            if current.month == 1:
                current = Date({"year": current.year - 1, "month": 12})
            else:
                current = Date({"year": current.year, "month": current.month - 1})
            
            # Generate ticks including one before and after
            while current <= max_date or (current.month == max_date.month + 1 and current.year == max_date.year):
                pos = self._date_to_decimal(current)
                show_tick = (
                    interval_type == "months_dense" or
                    interval_type == "months" or
                    (interval_type == "months_selective" and current.month in [1, 4, 7, 10])
                )
                
                if show_tick:
                    if current.month == 1:
                        label = f"{current.year}"
                    else:
                        label = f"{current.month}/{current.year}"
                    ticks.append((pos, label))
                
                # Move to next month
                if current.month == 12:
                    current = Date({"year": current.year + 1, "month": 1})
                else:
                    current = Date({"year": current.year, "month": current.month + 1})
                    
        elif interval_type in ["years", "years_dense", "years_5", "years_10"]:
            # Determine step size
            if interval_type == "years_dense":
                step = 1
            elif interval_type == "years":
                step = 2
            elif interval_type == "years_5":
                step = 5
            else:  # years_10
                step = 10
                
            # Calculate the first tick before min_date
            start_year = min_date.year - (min_date.year % step) - step
            # Calculate the last tick after max_date
            end_year = max_date.year + (step - (max_date.year % step)) + step
            
            # Generate ticks
            for year in range(start_year, end_year + 1, step):
                pos = year
                label = f"{abs(year)} {'BCE' if year < 0 else 'CE'}"
                ticks.append((pos, label))
                
        return ticks

    def _calculate_levels(self, components):
        # Filter out relationships, only handle events and periods
        event_period_comps = [comp for comp in components if isinstance(comp, (Event, Period))]
        
        # Sort components by date
        sorted_comps = sorted(
            event_period_comps,
            key=lambda x: (x.date.year if isinstance(x, Event) else x.start.year,
                         x.date.month if isinstance(x, Event) and x.date.month else 0,
                         x.date.day if isinstance(x, Event) and x.date.day else 0)
        )

        # Initialize levels dictionary
        levels = {}
        
        # Constants for layout
        EVENT_LABEL_WIDTH = 2  # Approximate width of event label in years
        PERIOD_LABEL_WIDTH = 3  # Approximate width of period label in years
        MIN_GAP = 1  # Minimum gap between labels in years
        
        # Helper function to check overlap between any two labels
        def has_overlap(pos1, width1, pos2, width2, level1, level2):
            if abs(level1 - level2) > 0.75:  # If levels are far apart, no overlap
                return False
            # Check for overlap considering widths
            return not (pos1 + width1/2 + MIN_GAP < pos2 - width2/2 or 
                       pos2 + width2/2 + MIN_GAP < pos1 - width1/2)

        # Helper function to check if a position overlaps with existing labels
        def check_position_overlap(pos, width, level, existing_positions):
            return any(has_overlap(pos, width, 
                                 other_pos, other_width,
                                 level, other_level) 
                     for other_pos, other_width, other_level in existing_positions)

        # Keep track of all label positions (pos, width, level)
        label_positions = []

        # First pass: assign levels for events and store periods
        periods = []
        for comp in sorted_comps:
            if isinstance(comp, Event):
                # Start with level 1 (above timeline)
                current_level = 1
                pos = comp.date.year
                
                # Check for overlaps with existing labels
                while check_position_overlap(pos, EVENT_LABEL_WIDTH, current_level, label_positions):
                    # If current level is positive, try negative
                    if current_level > 0:
                        current_level = -current_level
                    # If current level is negative, try next positive
                    else:
                        current_level = -current_level + 1
                
                # Adjust level based on importance
                importance_factor = {
                    "HIGH": 1.2,
                    "MEDIUM": 1.0,
                    "LOW": 0.8
                }
                final_level = current_level * importance_factor[comp.importance]
                levels[comp] = final_level
                
                # Add to label positions
                label_positions.append((pos, EVENT_LABEL_WIDTH, final_level))
            else:
                periods.append(comp)
                levels[comp] = 0  # Periods stay at baseline

        # Second pass: assign levels for period labels
        for period in periods:
            mid_year = (period.start.year + period.end.year) / 2
            
            # Start with level -1 (below timeline)
            current_level = -1
            
            # Check overlaps with all existing labels
            while check_position_overlap(mid_year, PERIOD_LABEL_WIDTH, current_level, label_positions):
                current_level -= 0.1
            
            # Add period label position to the list
            label_positions.append((mid_year, PERIOD_LABEL_WIDTH, current_level))
            levels[period] = current_level

        return levels

    def _calculate_period_positions(self, periods):
        # Sort periods by start date
        sorted_periods = sorted(periods, key=lambda p: (p.start.year, p.end.year))
        
        # Track period vertical positions
        period_positions = {}
        period_height = 0.15  # Height of each period bar
        
        # Helper function to check if periods overlap horizontally
        def periods_overlap(p1, p2):
            return not (p1.end.year < p2.start.year or p2.end.year < p1.start.year)
        
        # For each period, find the lowest available vertical position
        for period in sorted_periods:
            position = period_height/2  # Start just above the baseline
            
            # Check each position until we find one with no overlaps
            while any(periods_overlap(period, other) and pos == position 
                     for other, pos in period_positions.items()):
                position += period_height  # Stack directly on top
            
            period_positions[period] = position
            
        return period_positions

    def generate_png_bytes(self) -> bytes:
        """Generate the timeline visualization and return it as bytes."""
        # Create figure with extra space at bottom for legend
        fig, ax = plt.subplots(figsize=(15, 10), layout='constrained')
        
        # Get date range and convert to decimal years for precise positioning
        min_date, max_date = self._get_date_range()
        
        # Calculate tick interval based on the actual data range
        interval_type = self._calculate_tick_interval(min_date, max_date)
        
        # Get extended range with margins for consistent ticks
        xlim_min, xlim_max = self._get_date_range_with_margin(min_date, max_date, interval_type)
        if xlim_max != xlim_min:
            ax.set_xlim(xlim_min, xlim_max)

        # Separate components by type
        events_and_periods = [comp for comp in self.components if isinstance(comp, (Event, Period))]
        relationships = [comp for comp in self.components if isinstance(comp, Relationship)]

        # Calculate levels for events and periods
        levels = self._calculate_levels(events_and_periods)
        min_y, max_y = min(levels.values()), max(levels.values())
        ax.set_ylim(min(-3, min_y), max(3, max_y))
        # Get periods and calculate their positions
        periods = [comp for comp in events_and_periods if isinstance(comp, Period)]
        period_positions = self._calculate_period_positions(periods)

        # Draw main axis with arrowhead
        ax.axhline(0, color='black', linewidth=1.5, zorder=1)
        
        # Add arrowhead to the right
        arrow_props = dict(
            facecolor='black',
            edgecolor='black',
            arrowstyle='-|>',
            shrinkA=0,
            shrinkB=0,
            mutation_scale=15,
            linewidth=1.5
        )
        ax.annotate('', xy=(xlim_max, 0), xytext=(xlim_max - (xlim_max - xlim_min) * 0.02, 0),
                   arrowprops=arrow_props, zorder=2)

        # Create temporary Date objects for the extended range
        extended_min_date = Date({"year": int(xlim_min), "month": 1, "day": 1})
        extended_max_date = Date({"year": int(xlim_max + 1), "month": 12, "day": 31})
        
        # Generate and add tick marks with the extended range
        ticks = self._generate_ticks(extended_min_date, extended_max_date, interval_type)
        
        # Calculate tick height as percentage of axis length
        axis_length = xlim_max - xlim_min
        tick_height = 0.09  # this seems to look good

        # Add tick marks and labels
        for pos, label in ticks:
            if xlim_min <= pos <= xlim_max:
                # Draw tick mark
                ax.plot([pos, pos], [-tick_height, tick_height], color='black', linewidth=1, zorder=1)
                
                # Add label
                ax.annotate(label, 
                          xy=(pos, 0),
                          xytext=(0, -15),
                          textcoords='offset points',
                          ha='center',
                          va='top',
                          fontsize=9,
                          rotation=45 if interval_type in ["months", "months_selective", "days"] else 0,
                          zorder=1)

        # Sort components for drawing
        sorted_components = sorted(
            events_and_periods,
            key=lambda x: (
                self._date_to_decimal(x.date if isinstance(x, Event) else x.start),
                -["HIGH", "MEDIUM", "LOW"].index(x.importance)
            )
        )

        # Group components by importance
        importance_groups = {
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }
        for comp in sorted_components:
            importance_groups[comp.importance].append(comp)

        # Color management
        color_indices = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        color_sets = {"HIGH": self.HIGH_COLORS, "MEDIUM": self.MEDIUM_COLORS, "LOW": self.LOW_COLORS}
        component_colors = {}  # Store assigned colors

        # Assign colors to ensure maximum difference between consecutive items
        for importance, components in importance_groups.items():
            if not components:  # Skip if no components of this importance
                continue
                
            color_list = color_sets[importance]
            n_colors = len(color_list)
            n_components = len(components)
            
            # Calculate step size to spread colors evenly
            step = max(1, n_colors // max(1, n_components))
            
            for i, comp in enumerate(components):
                # Use modulo to wrap around the color list
                color_idx = (i * step) % n_colors
                component_colors[comp] = color_list[color_idx]

        legend_entries = []

        # Draw components
        for component in sorted_components:
            color = component_colors[component]

            if isinstance(component, Event):
                level = levels[component]
                # Convert date to decimal for precise positioning
                pos = self._date_to_decimal(component.date)
                
                # Draw vertical line (stem)
                ax.vlines(pos, 0, level, color=color, linewidth=1.5, zorder=2)
                
                # Draw marker on baseline
                ax.plot(pos, 0, 'o', color=color, 
                       markersize=8, markeredgecolor='black', zorder=3)
                
                # Add label
                ax.annotate(
                    component.title,
                    xy=(pos, level),
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

                # Format date for legend
                date_str = str(component.date)
                legend_entries.append((
                    patches.Circle((0, 0), fc=color, ec='black'),
                    f"{component.title} ({date_str})"
                ))

            elif isinstance(component, Period):
                # Get period vertical position
                y_pos = period_positions[component]
                period_height = 0.15
                
                # Convert dates to decimal for precise positioning
                start_pos = self._date_to_decimal(component.start)
                end_pos = self._date_to_decimal(component.end)
                
                # Draw period bar above the axis
                rect = patches.Rectangle(
                    (start_pos, y_pos - period_height/2),
                    end_pos - start_pos,
                    period_height,
                    facecolor=color,
                    alpha=0.7,
                    zorder=2
                )
                ax.add_patch(rect)

                # Add period label
                mid_pos = (start_pos + end_pos) / 2
                label_level = levels[component]
                
                # Draw connecting line from period to label
                ax.vlines(mid_pos, y_pos, label_level,
                         color=color, linestyle='--', linewidth=1, alpha=0.5, zorder=2)
                
                ax.annotate(
                    component.title,
                    xy=(mid_pos, label_level),
                    xytext=(0, -5),
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

                # Format dates for legend
                start_str = str(component.start)
                end_str = str(component.end)
                legend_entries.append((
                    patches.Rectangle((0, 0), 1, 1, fc=color, alpha=0.7),
                    f"{component.title} ({start_str} → {end_str})"
                ))

        # Draw relationships
        for rel in relationships:
            # Get positions for the relationship line
            if isinstance(rel.from_component, Event):
                from_pos = self._date_to_decimal(rel.from_component.date)
                from_y = levels[rel.from_component]
            else:  # Period
                # Use the middle of the period for the x-position
                start_pos = self._date_to_decimal(rel.from_component.start)
                end_pos = self._date_to_decimal(rel.from_component.end)
                from_pos = (start_pos + end_pos) / 2
                from_y = levels[rel.from_component]

            if isinstance(rel.to_component, Event):
                to_pos = self._date_to_decimal(rel.to_component.date)
                to_y = levels[rel.to_component]
            else:  # Period
                # Use the middle of the period for the x-position
                start_pos = self._date_to_decimal(rel.to_component.start)
                end_pos = self._date_to_decimal(rel.to_component.end)
                to_pos = (start_pos + end_pos) / 2
                to_y = levels[rel.to_component]

            # Draw relationship line with arrow
            arrow_style = {
                "CAUSE_EFFECT": "->",
                "PRECEDES": "-|>",
                "FOLLOWS": "<|-",
                "CONTEMPORANEOUS": "<->",
                "INCLUDES": "->",
                "EXCLUDES": "-/"
            }.get(rel.type, "->")

            # Calculate midpoint for label
            mid_x = (from_pos + to_pos) / 2
            mid_y = (from_y + to_y) / 2
            
            # Calculate angle of the line for label rotation
            angle = np.degrees(np.arctan2(to_y - from_y, to_pos - from_pos))
            # Keep angle between -90 and 90 degrees for readability
            if angle > 90:
                angle -= 180
            elif angle < -90:
                angle += 180

            # Draw the arrow with a curved path
            # Adjust curvature based on vertical distance
            rad = 0.2 + abs(to_y - from_y) * 0.05  # More curve for larger vertical distances
            rad = min(rad, 0.4)  # Cap the maximum curvature

            # Calculate the actual midpoint on the curve using the control point
            # The control point of the quadratic bezier curve is perpendicular to the midpoint
            # at a distance determined by the rad parameter
            dx = to_pos - from_pos
            dy = to_y - from_y
            control_x = mid_x + dy * rad  # Control point x
            control_y = mid_y - dx * rad  # Control point y
            
            # The point at t=0.5 on a quadratic bezier curve is the actual midpoint
            curve_mid_x = 0.25 * from_pos + 0.5 * control_x + 0.25 * to_pos
            curve_mid_y = 0.25 * from_y + 0.5 * control_y + 0.25 * to_y
            
            ax.annotate("",
                       xy=(to_pos, to_y),
                       xytext=(from_pos, from_y),
                       arrowprops=dict(arrowstyle=arrow_style,
                                     color='gray',
                                     alpha=0.6,
                                     connectionstyle=f"arc3,rad={rad}"),
                       zorder=1)

            # Add relationship label at the curve midpoint
            # Convert relationship type to a more readable format
            rel_label = rel.type.replace('_', '-').title()
            ax.annotate(rel_label,
                       xy=(curve_mid_x, curve_mid_y),  # Use the curve midpoint
                       xytext=(0, 3),  # Small offset above the line
                       textcoords='offset points',
                       ha='center',
                       va='center',
                       rotation=angle,
                       fontsize=8,
                       color='gray',
                       alpha=0.8,
                       bbox=dict(
                           boxstyle='round,pad=0.2',
                           fc='white',
                           ec='none',
                           alpha=0.8
                       ),
                       zorder=1)

        # Configure axes
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)  # Hide the original x-axis
        ax.spines[['left', 'top', 'right', 'bottom']].set_visible(False)
        
        # Set title
        ax.set_title(self.title, fontsize=14, fontweight='bold', pad=20)

        # Add legend at the bottom
        if legend_entries:
            # Calculate number of columns based on number of entries
            ncol = min(2, len(legend_entries))  # Maximum 2 columns
            ax.legend(
                *zip(*legend_entries),
                loc='upper center',
                bbox_to_anchor=(0.5, -0.1),
                fontsize=10,
                frameon=True,
                framealpha=0.8,
                ncol=ncol
            )

        # Save to bytes buffer instead of file
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf.getvalue()

    def generate_json(self) -> str:
        """Generate the timeline data as a JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def export_png(self, filename: str = None):
        """Export the timeline visualization to a PNG file."""
        if filename is None:
            filename = f"{self.id}.png"
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        # Create full path for the file
        filepath = os.path.join(output_dir, filename)
        # Generate and save PNG
        png_data = self.generate_png_bytes()
        with open(filepath, 'wb') as f:
            f.write(png_data)

    def export_json(self, filename: str = None):
        """Export the timeline data to a JSON file."""
        if filename is None:
            filename = f"{self.id}.json"
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        # Create full path for the file
        filepath = os.path.join(output_dir, filename)
        # Generate and save JSON
        json_data = self.generate_json()
        with open(filepath, 'w') as f:
            f.write(json_data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "components": [comp.to_dict() for comp in self.components]
        } 