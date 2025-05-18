from TimelineParserListener import TimelineParserListener
import re
import matplotlib.pyplot as plt
import json
import os
import matplotlib.patches as mpatches
from collections import defaultdict
import math
import calendar

class TimelineInterpreter(TimelineParserListener):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.relationships = {}
        self.already_exported = set()
        self.validation_errors = []
        self.enabled_stack = [True]

    def parse_year_literal(self, raw):
        """
        Parses strings in these formats:
        - '753' → 753
        - '753-BCE' → -753
        - '3-753-BCE' → 753 BCE in March (month=3)
        - '21-3-753-BCE' → full date
        Returns a dictionary like:
        {
            "year": int,
            "month": optional int,
            "day": optional int
        }
        """
        # First check for BCE/CE suffix
        is_bce = "-BCE" in raw
        is_ce = "-CE" in raw
        
        # Remove era suffix for parsing
        clean_raw = raw.replace("-BCE", "").replace("-CE", "")
        
        # Match full date: day-month-year
        full_date_match = re.match(r"(\d+)-(\d+)-(\d+)", clean_raw)
        if full_date_match:
            day = int(full_date_match.group(1))
            month = int(full_date_match.group(2))
            year = int(full_date_match.group(3))
            if is_bce:
                year = -year
            return {"year": year, "month": month, "day": day}

        # Match month-year: month-year
        month_year_match = re.match(r"(\d+)-(\d+)", clean_raw)
        if month_year_match:
            month = int(month_year_match.group(1))
            year = int(month_year_match.group(2))
            if is_bce:
                year = -year
            return {"year": year, "month": month}

        # Match year only
        year_match = re.match(r"(\d+)", clean_raw)
        if year_match:
            year = int(year_match.group(1))
            if is_bce:
                year = -year
            return {"year": year}

        return None

    def validate_string_literal(self, text, field_name):
        """Validate a string literal is properly formatted"""
        if not text.startswith('"') or not text.endswith('"'):
            self.validation_errors.append(f"Invalid {field_name}: Must be enclosed in double quotes")
            return False
        # Check if it's just empty quotes
        if text == '""':
            self.validation_errors.append(f"Invalid {field_name}: Cannot be empty")
            return False
        # Check if it contains only numbers
        inner_text = text.strip('"')
        if inner_text.isdigit():
            self.validation_errors.append(f"Invalid {field_name}: Cannot be just a number")
            return False
        return True

    def validate_date(self, date_dict):
        """Validate a date dictionary"""
        if not isinstance(date_dict, dict):
            self.validation_errors.append("Invalid date format")
            return False
        
        if 'year' not in date_dict:
            self.validation_errors.append("Date must include a year")
            return False
            
        year = date_dict['year']
        if not isinstance(year, int):
            self.validation_errors.append("Year must be an integer")
            return False
            
        if 'month' in date_dict:
            month = date_dict['month']
            if not isinstance(month, int) or month < 1 or month > 12:
                self.validation_errors.append("Month must be between 1 and 12")
                return False
                
        if 'day' in date_dict:
            day = date_dict['day']
            month = date_dict.get('month', 1)
            if not isinstance(day, int) or day < 1 or day > 31:
                self.validation_errors.append("Day must be between 1 and 31")
                return False
            # Validate days per month
            days_in_month = {
                1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
            }
            if day > days_in_month[month]:
                self.validation_errors.append(f"Invalid day {day} for month {month}")
                return False
                
        return True

    def validate_period_dates(self, start_date, end_date):
        """Validate that start date is before end date"""
        if not (isinstance(start_date, dict) and isinstance(end_date, dict)):
            return False
            
        start_year = start_date.get('year')
        end_year = end_date.get('year')
        
        if start_year > end_year:
            self.validation_errors.append(f"Period start year ({start_year}) cannot be after end year ({end_year})")
            return False
            
        if start_year == end_year:
            start_month = start_date.get('month', 1)
            end_month = end_date.get('month', 1)
            
            if start_month > end_month:
                self.validation_errors.append(f"Period start month ({start_month}) cannot be after end month ({end_month}) in the same year")
                return False
                
            if start_month == end_month:
                start_day = start_date.get('day', 1)
                end_day = end_date.get('day', 1)
                
                if start_day > end_day:
                    self.validation_errors.append(f"Period start day ({start_day}) cannot be after end day ({end_day}) in the same month")
                    return False
                    
        return True

    def validate_relationship(self, from_id, to_id, rel_type):
        """Validate relationship between components"""
        if from_id not in self.events and from_id not in self.periods:
            self.validation_errors.append(f"Relationship 'from' component '{from_id}' does not exist")
            return False
            
        if to_id not in self.events and to_id not in self.periods:
            self.validation_errors.append(f"Relationship 'to' component '{to_id}' does not exist")
            return False
            
        # Validate specific relationship type constraints
        if rel_type == 'includes':
            if from_id in self.events:
                self.validation_errors.append("'includes' relationship must have a period as the 'from' component")
                return False
                
        return True

    def enterEventDecl(self, ctx):
        event_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        
        # Validate title
        if not self.validate_string_literal(title, "event title"):
            return
            
        raw_date = ctx.dateExpr().getText()
        parsed_date = self.parse_year_literal(raw_date)
        
        # Validate date
        if not self.validate_date(parsed_date):
            return

        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()

        self.events[event_id] = {
            "title": title.strip('"'),
            "date": parsed_date,
            "importance": importance
        }

        print(f"Event parsed: {self.events[event_id]}")

    def enterPeriodDecl(self, ctx):
        period_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        
        # Validate title
        if not self.validate_string_literal(title, "period title"):
            return

        # Extract dates
        start_date = self.parse_year_literal(ctx.dateExpr(0).getText())
        end_date = self.parse_year_literal(ctx.dateExpr(1).getText())
        
        # Validate dates
        if not self.validate_date(start_date) or not self.validate_date(end_date):
            return
            
        # Validate period constraints
        if not self.validate_period_dates(start_date, end_date):
            return

        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()

        self.periods[period_id] = {
            "title": title.strip('"'),
            "start": start_date,
            "end": end_date,
            "importance": importance
        }

        print(f"Period parsed: {self.periods[period_id]}")

    def enterTimelineDecl(self, ctx):
        timeline_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        
        # Validate title
        if not self.validate_string_literal(title, "timeline title"):
            return

        # Extract component IDs from componentList
        id_list = []
        comp_ctx = ctx.componentList()
        if comp_ctx:
            ids = comp_ctx.ID()
            id_list = [id.getText() for id in ids]
            
            # Validate that all components exist
            for comp_id in id_list:
                if comp_id not in self.events and comp_id not in self.periods:
                    self.validation_errors.append(f"Timeline component '{comp_id}' does not exist")
                    return

        self.timelines[timeline_id] = {
            "title": title.strip('"'),
            "components": id_list
        }

        print(f"Timeline parsed: {self.timelines[timeline_id]}")

    def enterRelationshipDecl(self, ctx):
        relationship_id = ctx.ID()[0].getText()
        from_id = ctx.ID()[1].getText()
        to_id = ctx.ID()[2].getText()
        rel_type = ctx.relationshipType().getText()

        # Validate relationship
        if not self.validate_relationship(from_id, to_id, rel_type):
            return

        self.relationships[relationship_id] = {
            "from": from_id,
            "to": to_id,
            "type": rel_type
        }

        print(f"Relationship parsed: {self.relationships[relationship_id]}")

    def generate_visualization(self, timeline_id, save_path=None):
        timeline = self.timelines[timeline_id]
        components = timeline["components"]

        fig, ax = plt.subplots(figsize=(14, 7))
        renderer = fig.canvas.get_renderer()

        LOW_COLORS = ["#FFD700", "#FFC300", "#FFB000", "#FFA500", "#FF8C00", "#FF7F50", "#FF6F00", "#FF4500"]
        MEDIUM_COLORS = ["#00FF00", "#32CD32", "#3CB371", "#2ECC71", "#228B22", "#66FF66", "#7CFC00", "#20C997"]
        HIGH_COLORS = ["#1E90FF", "#007FFF", "#3399FF", "#0055FF", "#4682B4", "#4169E1", "#0000CD", "#0000FF"]

        color_sets = {"LOW": LOW_COLORS, "MEDIUM": MEDIUM_COLORS, "HIGH": HIGH_COLORS}
        color_indices = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        y_axis = 0

        # Store component positions for relationship arrows
        component_positions = {}

        all_years = []
        for comp_id in components:
            if comp_id in self.events:
                all_years.append(self.events[comp_id]["date"]["year"])  # Append the year value only
            elif comp_id in self.periods:
                all_years.append(self.periods[comp_id]["start"]["year"])  # Append the start year value only
                all_years.append(self.periods[comp_id]["end"]["year"])  # Append the end year value only

        if not all_years:
            print("[Error] No date data available.")
            return

        min_year = min(all_years)
        max_year = max(all_years)

        # Calculate the difference between the first and last year
        year_diff = max_year - min_year
        # Ensure that the timeline spans at least one year
        year_diff = max(year_diff, 1)

        # Determine 10% of the difference
        margin = year_diff * 0.10

        # Adjust the start and end years by +-10% of the difference
        timeline_start = min_year - margin
        timeline_end = max_year + margin

        range_years = timeline_end - timeline_start

        num_divisions = 12  # This determines how many ticks we want
        tick_step = range_years / num_divisions

        ticks = []
        ticks_set = set()

        # Check if tick_step is a float with decimals
        if isinstance(tick_step, float) and tick_step != int(tick_step):  # Has decimal part
            # Generate ticks in fractional years
            tick = timeline_start  # Start at the timeline_start year
            while tick <= timeline_end:
                year = math.floor(tick)  # Year part
                month_fraction = tick - year  # Decimal part of the tick step

                # Convert the decimal part to months (e.g., 0.5 years is 6 months)
                month = round(month_fraction * 12)

                # Handle the case where month == 12 (i.e., 1 full year)
                if month == 12:
                    month = 0
                    year += 1

                # Store the tick as a floating-point value
                ticks.append(year + month / 12)
                ticks_set.add(year + month / 12)

                # Move to the next tick based on tick_step
                tick += tick_step
        else:
            # If tick_step is a whole number, just use years
            ticks = list(range(int(timeline_start),int (timeline_end) + 1, int(tick_step)))
            ticks_set = set(ticks)

        print(f"Ticks: {ticks}")

        ax.annotate(
            '',
            xy=(timeline_end, y_axis),
            xytext=(timeline_start, y_axis),
            arrowprops=dict(arrowstyle='->', color='black', linewidth=2)
        )

        def get_month_name(month_number):
            """
            Convert a month number (1-12) to the full month name.
            For example: 1 -> "January", 2 -> "February", etc.
            """
            return calendar.month_name[month_number]

        # Draw tick marks
        for tick in ticks[1:-1]:
            ax.plot([tick, tick], [y_axis - 0.05, y_axis + 0.05], color='black', linewidth=1)

            # Convert tick into year.month format
            year = math.floor(tick)
            month = round((tick - year) * 12)+1

            month_name = get_month_name(month)  # Get the month name using the function
            if tick_step != int(tick_step):
                ax.text(tick, y_axis - 0.15, f"{year}.{month_name[:3]}", 
                    ha='center', 
                    va='top', 
                    fontsize=8,
                    fontfamily='sans-serif',
                    fontstyle='italic',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.5, pad=1)
                )
            else:
                ax.text(tick, y_axis - 0.15, f"{year}", 
                    ha='center', 
                    va='top', 
                    fontsize=8,
                    fontfamily='sans-serif',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.5, pad=1)
                )

        def get_next_color(importance):
            idx = color_indices[importance]
            color_list = color_sets[importance]
            color = color_list[idx % len(color_list)]
            color_indices[importance] += 1
            return color

        importance_order = ["HIGH", "MEDIUM", "LOW"]
        drawn_components = []

        # Initialize widths and text sizes based on importance
        importance_properties = {
            "HIGH": {
                "width": 10, 
                "size": 12, 
                "base_offset": 0.3,
                "font_weight": "bold",
                "font_family": "sans-serif",
                "alpha": 1.0,
                "bbox": dict(facecolor='white', edgecolor='none', alpha=0.7, pad=2)
            },
            "MEDIUM": {
                "width": 8, 
                "size": 10, 
                "base_offset": 0.2,
                "font_weight": "normal",
                "font_family": "sans-serif",
                "alpha": 0.9,
                "bbox": dict(facecolor='white', edgecolor='none', alpha=0.6, pad=1.5)
            },
            "LOW": {
                "width": 6, 
                "size": 8, 
                "base_offset": 0.1,
                "font_weight": "light",
                "font_family": "sans-serif",
                "alpha": 0.8,
                "bbox": dict(facecolor='white', edgecolor='none', alpha=0.5, pad=1)
            }
        }
        used_offsets = defaultdict(set)
        event_overlap = defaultdict(int)
        period_overlap = defaultdict(int)
        legend_entries = []
        used_labels = set()
        text_boxes = []  # Store positions and sizes of text boxes for collision detection

        def check_collision(proposed_box, buffer=0.1):  # Increased buffer
            for box in text_boxes:
                if (proposed_box['right'] + buffer > box['left'] and
                    proposed_box['left'] - buffer < box['right'] and
                    proposed_box['top'] + buffer > box['bottom'] and
                    proposed_box['bottom'] - buffer < box['top']):
                    return True
            return False

        def find_non_colliding_position(x_pos, text_width, text_height, importance):
            base_offset = importance_properties[importance]["base_offset"]
            y_offset = y_axis + base_offset
            step = 0.25  # Increased step size
            max_attempts = 100  # Increased max attempts
            attempts = 0

            while attempts < max_attempts:
                proposed_box = {
                    'left': x_pos - text_width / 2,
                    'right': x_pos + text_width / 2,
                    'bottom': y_offset - text_height,
                    'top': y_offset
                }

                if not check_collision(proposed_box):
                    return y_offset, proposed_box

                y_offset += step
                attempts += 1

            # If we couldn't find a non-colliding position, return the last attempted position
            return y_offset, proposed_box

        for importance in importance_order:
            for comp_id in components:
                if comp_id in drawn_components:
                    continue

                # Events
                if comp_id in self.events:
                    event = self.events[comp_id]
                    if event.get("importance", "MEDIUM").upper() != importance:
                        continue

                    date = event["date"]
                    date_tuple = (date["year"], date.get("month", 1), date.get("day", 1))
                    title = event["title"]
                    color = get_next_color(importance)

                    size = importance_properties[importance]["size"]
                    width = importance_properties[importance]["width"]

                    offset = event_overlap[date_tuple]
                    y_offset = y_axis + offset * 0.25

                    # Estimate text box dimensions using renderer
                    text_obj = ax.text(0, 0, title, fontsize=size)
                    bbox = text_obj.get_window_extent(renderer=renderer)
                    text_width = bbox.width / fig.dpi
                    text_height = bbox.height / fig.dpi
                    text_obj.remove()

                    x_pos = date["year"]
                    y_offset, proposed_box = find_non_colliding_position(x_pos, text_width, text_height, importance)
                    text_boxes.append(proposed_box)

                    # Draw the event
                    ax.scatter(date["year"], y_axis, s=width ** 2, color=color, edgecolors='black', zorder=3)
                    ax.text(
                        x_pos,
                        y_offset,
                        title,
                        rotation=0,
                        ha='center',
                        va='bottom',
                        fontsize=size,
                        fontweight=importance_properties[importance]["font_weight"],
                        fontfamily=importance_properties[importance]["font_family"],
                        alpha=importance_properties[importance]["alpha"],
                        bbox=importance_properties[importance]["bbox"],
                        zorder=4
                    )

                    # Draw vertical line connecting event to text
                    if y_offset > y_axis + 0.2:  # Only draw line if text is significantly above
                        ax.vlines(x_pos, y_axis + 0.1, y_offset - 0.05, 
                                colors='gray', linestyles='dotted', linewidth=1, zorder=2)

                    if date["year"] not in ticks_set:
                        ax.text(date["year"], y_axis - 0.25, f"{date['year']}", ha='center', va='top', fontsize=7)

                    label = f"{title} ({date['year']})"
                    if label not in used_labels:
                        legend_entries.append((mpatches.Patch(color=color), label))
                        used_labels.add(label)

                    drawn_components.append(comp_id)

                # Periods
                elif comp_id in self.periods:
                    period = self.periods[comp_id]
                    if period.get("importance", "MEDIUM").upper() != importance:
                        continue

                    start = period["start"]
                    end = period["end"]
                    title = period["title"]
                    color = get_next_color(importance)
                    width = importance_properties[importance]["width"]
                    size = importance_properties[importance]["size"]

                    # Estimate text box dimensions using renderer for periods
                    text_obj = ax.text(0, 0, title, fontsize=size)
                    bbox = text_obj.get_window_extent(renderer=renderer)
                    text_width = bbox.width / fig.dpi
                    text_height = bbox.height / fig.dpi
                    text_obj.remove()

                    x_pos = (start["year"] + end["year"]) / 2
                    y_offset, proposed_box = find_non_colliding_position(x_pos, text_width, text_height, importance)
                    text_boxes.append(proposed_box)

                    # Draw period line and text
                    ax.hlines(y_axis, start["year"], end["year"], linewidth=width, color=color, alpha=0.9, zorder=2)
                    ax.text(
                        x_pos, 
                        y_offset, 
                        title,
                        ha='center',
                        va='bottom',
                        fontsize=size,
                        fontweight=importance_properties[importance]["font_weight"],
                        fontfamily=importance_properties[importance]["font_family"],
                        alpha=importance_properties[importance]["alpha"],
                        bbox=importance_properties[importance]["bbox"],
                        zorder=3
                    )

                    # Draw vertical line connecting period to text
                    if y_offset > y_axis + 0.2:
                        ax.vlines(x_pos, y_axis + 0.1, y_offset - 0.05, 
                                colors='gray', linestyles='dotted', linewidth=1, zorder=2)

                    if start["year"] not in ticks_set:
                        ax.text(start["year"], y_axis - 0.25, f"{start['year']}", ha='center', va='top', fontsize=7)
                    if end["year"] not in ticks_set:
                        ax.text(end["year"], y_axis - 0.25, f"{end['year']}", ha='center', va='top', fontsize=7)

                    label = f"{title}  {start['year']} → {end['year']}"
                    if label not in used_labels:
                        legend_entries.append((mpatches.Patch(color=color, alpha=0.9), label))
                        used_labels.add(label)

                    drawn_components.append(comp_id)

        ax.set_xlim(timeline_start-1, timeline_end+1)
        ax.set_ylim(-1, max(event_overlap.values()) * 0.4 + 1)
        ax.set_yticks([])
        ax.set_xticks([])

        # After drawing components, draw relationships
        relationship_y_offset = -0.5  # Start relationships below the axis
        relationship_spacing = 0.3  # Vertical spacing between relationships
        min_relationship_y = float('inf')  # Track the lowest y-coordinate used by relationships

        # Define relationship styles
        relationship_colors = {
            'cause-effect': 'red',
            'precedes': 'blue',
            'contemporaneous': 'green',
            'includes': 'purple',
            'excludes': 'purple'
        }
        relationship_styles = {
            'cause-effect': '->', 
            'precedes': '->', 
            'contemporaneous': '<->', 
            'includes': '->', 
            'excludes': '->'
        }
        relationship_linestyles = {
            'cause-effect': 'solid',
            'precedes': 'dashed',
            'contemporaneous': 'solid',
            'includes': 'solid',
            'excludes': 'dotted'
        }
        
        # Group relationships by type for better organization
        relationships_by_type = defaultdict(list)
        for rel_id, rel in self.relationships.items():
            relationships_by_type[rel["type"]].append(rel)

        # Track used y positions to avoid overlaps
        used_y_positions = set()

        # Draw relationships and track the lowest y-coordinate
        for rel_type, rels in relationships_by_type.items():
            for rel in rels:
                from_id = rel["from"]
                to_id = rel["to"]
                
                # Get x-coordinates for the relationship endpoints
                from_x = None
                to_x = None
                
                # Find x positions based on events or periods
                if from_id in self.events:
                    from_x = self.events[from_id]["date"]["year"]
                elif from_id in self.periods:
                    from_x = (self.periods[from_id]["start"]["year"] + self.periods[from_id]["end"]["year"]) / 2
                    
                if to_id in self.events:
                    to_x = self.events[to_id]["date"]["year"]
                elif to_id in self.periods:
                    to_x = (self.periods[to_id]["start"]["year"] + self.periods[to_id]["end"]["year"]) / 2
                
                if from_x is not None and to_x is not None:
                    # Find a free y position
                    current_y = relationship_y_offset
                    while current_y in used_y_positions:
                        current_y -= relationship_spacing
                    used_y_positions.add(current_y)
                    min_relationship_y = min(min_relationship_y, current_y)
                    
                    # Draw the relationship arrow
                    color = relationship_colors.get(rel_type, 'gray')
                    style = relationship_styles.get(rel_type, '->')
                    linestyle = relationship_linestyles.get(rel_type, 'solid')
                    
                    # Draw curved arrow below the axis
                    ax.annotate('',
                        xy=(to_x, current_y),
                        xytext=(from_x, current_y),
                        arrowprops=dict(
                            arrowstyle=style,
                            color=color,
                            linestyle=linestyle,
                            connectionstyle='arc3,rad=0.1',
                            linewidth=2
                        )
                    )
                    
                    # Add relationship label
                    mid_x = (from_x + to_x) / 2
                    ax.text(mid_x, current_y - 0.1, rel_type, 
                           ha='center', va='top', 
                           color=color,
                           fontsize=8,
                           fontfamily='sans-serif',
                           fontstyle='italic',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.5, pad=1),
                           zorder=2
                    )

        # Adjust plot limits to show relationships
        current_ylim = ax.get_ylim()
        min_y = min(used_y_positions) - relationship_spacing if used_y_positions else -1

        # Calculate the maximum y position needed for text above axis
        max_y = 0
        for box in text_boxes:
            max_y = max(max_y, box['top'])

        # Add extra space for legend and text
        legend_height = 0.15 * len(legend_entries) if legend_entries else 0  # Space per legend entry
        top_margin = max(1.5, max_y + 0.5)  # At least 1.5 or text height + 0.5
        
        # Set axis limits with proper spacing
        ax.set_ylim(min_y, top_margin + legend_height)

       

        # Add legend in the upper right corner of axis box with proper spacing
        if legend_entries:
            handles, labels = zip(*legend_entries)
            legend = ax.legend(
                handles, 
                labels, 
                loc='upper right', 
                fontsize=9,
                frameon=True,
                framealpha=0.8,
                edgecolor='none',
                fancybox=True,
                bbox_to_anchor=(0.98, 0.98),  # Position in upper right
                bbox_transform=ax.transAxes,  # Use axis coordinates (0-1)
                borderaxespad=1.0,  # Increased padding
                labelspacing=0.5  # Add space between legend entries
            )
            # Ensure the legend background doesn't overlap with other elements
            legend.get_frame().set_alpha(0.8)

        ax.set_title(timeline["title"], 
            fontsize=14, 
            fontweight='bold', 
            fontfamily='sans-serif',
            pad=20
        )

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"[Exported] Timeline image saved to {save_path}")
            plt.close()
        else:
            plt.show()

    def enterIfStmt(self, ctx):
        result = self.evaluate_condition(ctx.condition())
        # push: only enabled if we were already enabled AND this condition is True
        self.enabled_stack.append(self.enabled_stack[-1] and result)

    def exitIfStmt(self, ctx):
        # pop back to previous enabled/disabled state
        self.enabled_stack.pop()

    # ===== FOR handling (always stays in the same enabled state) =====
    def enterForStmt(self, ctx):
        # Loops don’t change “enabled” status
        self.enabled_stack.append(self.enabled_stack[-1])
        # Now actually execute the loop body in our interpreter
        loopVar = ctx.ID(0).getText()
        iterable = ctx.ID(1).getText()
        items = self.timelines.get(iterable, {}).get("components", [])
        for item in items:
            # set loop variable if you need it
            setattr(self, loopVar, item)
            for stmt in ctx.statement():
                self.handleStatement(stmt)

    def exitForStmt(self, ctx):
        self.enabled_stack.pop()

    # ===== EXPORT handling (gated on enabled_stack) =====
    def enterExportStmt(self, ctx):
        # Determine the "export_id" by checking for loop‑bound variables first
        name = ctx.ID().getText()           # e.g. "comp"
        if hasattr(self, name):
            export_id = getattr(self, name) # e.g. "E1" or "E2"
        else:
            export_id = name                # a regular literal ID

        # Now you can gate on enabled_stack as before...
        if not self.enabled_stack[-1]:
            return

        print(f"Export requested for: {export_id}")

        # Prevent duplicate exports
        if export_id in self.already_exported:
            print(f"[Info] Skipping already exported: {export_id}")
            return
        self.already_exported.add(export_id)

        # … rest of your existing export logic goes here …
        if export_id in self.timelines:
            # timeline export
            timeline = self.timelines[export_id]
            png = f"{export_id}.png"
            jsonf = f"{export_id}.json"
            self.generate_visualization(export_id, save_path=png)
            export_data = {
                "timeline_id": export_id,
                "title": timeline["title"],
                "events": [], "periods": []
            }
            for cid in timeline["components"]:
                if cid in self.events:
                    export_data["events"].append({"id": cid, **self.events[cid]})
                elif cid in self.periods:
                    export_data["periods"].append({"id": cid, **self.periods[cid]})
            with open(jsonf, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4)
            print(f"[Exported] Timeline image saved to {png}")
            print(f"[Exported] Timeline '{export_id}' → {jsonf}")

        elif export_id in self.events:
            # event export
            jsonf = f"{export_id}.json"
            with open(jsonf, "w", encoding="utf-8") as f:
                json.dump({"id": export_id, **self.events[export_id]}, f, indent=4)
            print(f"[Exported] Event '{export_id}' → {jsonf}")

        elif export_id in self.periods:
            # period export
            jsonf = f"{export_id}.json"
            with open(jsonf, "w", encoding="utf-8") as f:
                json.dump({"id": export_id, **self.periods[export_id]}, f, indent=4)
            print(f"[Exported] Period '{export_id}' → {jsonf}")

        else:
            print(f"[Warning] ID '{export_id}' not found.")




    def handleStatement(self, ctx):
        # EXPORT
        if ctx.exportStmt():
            self.enterExportStmt(ctx.exportStmt())

        # IF
        elif ctx.ifStmt():
            if_ctx = ctx.ifStmt()
            # 1) evaluate and push
            result = self.evaluate_condition(if_ctx.condition())
            # combine with current stack top
            self.enabled_stack.append(self.enabled_stack[-1] and result)

            # 2) run the 'then' block
            for st in if_ctx.statement():
                self.handleStatement(st)

            # 3) pop back out of the if
            self.enabled_stack.pop()

            # 4) if there's an ELSE, evaluate that separately
            if if_ctx.ELSE():
                # ELSE block is child index 6…8 in your grammar, but easiest is:
                else_stmts = if_ctx.getChild(6).statement()
                # ELSE inherits the *negation* of the then‑condition
                self.enabled_stack.append(self.enabled_stack[-1] and not result)
                for st in else_stmts:
                    self.handleStatement(st)
                self.enabled_stack.pop()

        # FOR
        elif ctx.forStmt():
            for_ctx = ctx.forStmt()
            # push same enabled state
            self.enabled_stack.append(self.enabled_stack[-1])

            loop_var = for_ctx.ID(0).getText()
            iterable = for_ctx.ID(1).getText()
            items = self.timelines.get(iterable, {}).get("components", [])

            for item in items:
                # bind the loop variable (if you need it later)
                setattr(self, loop_var, item)
                for st in for_ctx.statement():
                    self.handleStatement(st)

            self.enabled_stack.pop()

        # MODIFY (if you have it)
        elif ctx.modifyStmt():
            self.enterModifyStmt(ctx.modifyStmt())

        # empty semicolon
        else:
            pass

    def enterMainBlock(self, ctx):
        for stmt in ctx.statement():
            self.handleStatement(stmt)



    def evaluate_condition(self, ctx):
        # comparison: expr OP expr
        if ctx.comparisonOp():
            left  = self.evaluate_expr(ctx.expr(0))
            right = self.evaluate_expr(ctx.expr(1))
            op    = ctx.comparisonOp().getText()
            return self.apply_comparison(left, right, op)

        # single‑ID: true if it names an existing event _or_ period
        elif ctx.ID():
            name = ctx.ID().getText()
            present = (name in self.events) or (name in self.periods)
            return bool(present)

        # literal true/false
        elif ctx.booleanLiteral():
            return ctx.booleanLiteral().getText().lower() == "true"

        # fallback: explicitly False
        return False

    def evaluate_expr(self, ctx):
        # 1) dateExpr → year only
        if ctx.dateExpr():
            raw    = ctx.dateExpr().getText()
            parsed = self.parse_year_literal(raw)
            if parsed and "year" in parsed:
                return parsed["year"]

        # 2) ID.property
        if ctx.ID() and ctx.property_():
            obj_id = ctx.ID().getText()
            prop   = ctx.property_().getText().lower()

            # look up the raw value
            if obj_id in self.events and prop in self.events[obj_id]:
                val = self.events[obj_id][prop]
            elif obj_id in self.periods and prop in self.periods[obj_id]:
                val = self.periods[obj_id][prop]
            else:
                val = None

            # if it’s a date‐dict, pull out the year
            if isinstance(val, dict) and "year" in val:
                return val["year"]
            return val

        # 3) STRING
        if ctx.STRING():
            return ctx.STRING().getText().strip('"')

        # 4) bare INT
        if ctx.INT():
            return int(ctx.INT().getText())

        # 5) importanceValue
        if ctx.importanceValue():
            return ctx.importanceValue().getText().upper()

        return None

    def apply_comparison(self, left, right, op):
        ops = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b
        }
        return ops.get(op, lambda a, b: False)(left, right)
