import matplotlib.pyplot as plt
import json
import os
import matplotlib.patches as mpatches
from collections import defaultdict
import math
import calendar
import re
from src.TimelineParserVisitor import TimelineParserVisitor
from src.TimelineParser import TimelineParser


class TimelineInterpreter(TimelineParserVisitor):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.relationships = {}
        self.already_exported = set()
        self.validation_errors = []

    def visitYearLiteral(self, ctx:TimelineParser.YearLiteralContext):
        print(f"Visiting yearLiteral: {ctx.getText()}")
        year = int(ctx.INT().getText())
        if ctx.BCE():
            year = -year
        return {"year": year}

    def visitMonthYearLiteral(self, ctx:TimelineParser.MonthYearLiteralContext):
        print(f"Visiting monthYearLiteral: {ctx.getText()}")
        month = int(ctx.INT().getText())
        year = self.visit(ctx.yearLiteral())
        return {"year": year, "month": month}

    def visitFullDateLiteral(self, ctx:TimelineParser.FullDateLiteralContext):
        print(f"Visiting fullDateLiteral: {ctx.getText()}")
        day = int(ctx.INT().getText())
        month_year = self.visit(ctx.monthYearLiteral())
        return {"year": month_year["year"], "month": month_year["month"], "day": day}

    def visitDateExpr(self, ctx:TimelineParser.DateExprContext):
        # print(f"Visiting dateExpr: {ctx.getText()}")
        # Visit the first child which should be one of: yearLiteral, monthYearLiteral, fullDateLiteral, or dateCalculation
        for child in ctx.children:
            # print(f"Child type: {type(child)}")
            result = self.visit(child)
            if result is not None:
                return result
        # print("No matching date format found")
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

    def visitEventDecl(self, ctx:TimelineParser.EventDeclContext):
        event_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        print(title)
        # Validate title
        if not self.validate_string_literal(title, "event title"):
            return None
            
        # Get date using visitor pattern
        parsed_date = self.visit(ctx.dateExpr())
        print(parsed_date)
        # Validate date
        if not self.validate_date(parsed_date):
            return None

        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()

        self.events[event_id] = {
            "title": title.strip('"'),
            "date": parsed_date,
            "importance": importance
        }

        print(f"Event parsed: {self.events[event_id]}")
        return None

    def visitPeriodDecl(self, ctx:TimelineParser.PeriodDeclContext):
        period_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        
        # Validate title
        if not self.validate_string_literal(title, "period title"):
            return None

        # Extract dates using visitor pattern
        start_date = self.visit(ctx.dateExpr(0))
        end_date = self.visit(ctx.dateExpr(1))
        
        # Validate dates
        if not self.validate_date(start_date) or not self.validate_date(end_date):
            return None
            
        # Validate period constraints
        if not self.validate_period_dates(start_date, end_date):
            return None

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
        return None

    def visitTimelineDecl(self, ctx:TimelineParser.TimelineDeclContext):
        timeline_id = ctx.ID().getText()
        title = ctx.STRING().getText()
        
        # Validate title
        if not self.validate_string_literal(title, "timeline title"):
            return None

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
                    return None

        self.timelines[timeline_id] = {
            "title": title.strip('"'),
            "components": id_list
        }

        print(f"Timeline parsed: {self.timelines[timeline_id]}")
        return None

    def visitRelationshipDecl(self, ctx:TimelineParser.RelationshipDeclContext):
        relationship_id = ctx.ID()[0].getText()
        from_id = ctx.ID()[1].getText()
        to_id = ctx.ID()[2].getText()
        rel_type = ctx.relationshipType().getText()

        # Validate relationship
        if not self.validate_relationship(from_id, to_id, rel_type):
            return None

        self.relationships[relationship_id] = {
            "from": from_id,
            "to": to_id,
            "type": rel_type
        }

        print(f"Relationship parsed: {self.relationships[relationship_id]}")
        return None

    def visitExportStmt(self, ctx:TimelineParser.ExportStmtContext):
        export_id = ctx.ID().getText()
        print(f"Export requested for: {export_id}")
        print(self.validation_errors)
        # Prevent duplicate exports
        if export_id in self.already_exported:
            print(f"[Info] Skipping already exported: {export_id}")
            return None

        self.already_exported.add(export_id)

        # Export a timeline
        if export_id in self.timelines:
            timeline = self.timelines[export_id]
            filename_png = f"{export_id}.png"
            filename_json = f"{export_id}.json"

            # Generate visualization
            self.generate_visualization(export_id, save_path=filename_png)

            # Collect export data
            export_data = {
                "timeline_id": export_id,
                "title": timeline["title"],
                "events": [],
                "periods": []
            }

            for cid in timeline["components"]:
                if cid in self.events:
                    export_data["events"].append({"id": cid, **self.events[cid]})
                elif cid in self.periods:
                    export_data["periods"].append({"id": cid, **self.periods[cid]})

            with open(filename_json, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4)

            print(f"[Exported] Timeline image saved to {filename_png}")
            print(f"[Exported] Timeline '{export_id}' → {filename_json}")

        # Export an event
        elif export_id in self.events:
            filename = f"{export_id}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"id": export_id, **self.events[export_id]}, f, indent=4)
            print(f"[Exported] Event '{export_id}' → {filename}")

        # Export a period
        elif export_id in self.periods:
            filename = f"{export_id}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"id": export_id, **self.periods[export_id]}, f, indent=4)
            print(f"[Exported] Period '{export_id}' → {filename}")

        # Unknown ID
        else:
            print(f"[Warning] ID '{export_id}' not found.")

        return None

    def visitIfStmt(self, ctx:TimelineParser.IfStmtContext):
        result = self.evaluate_condition(ctx.condition())

        if result:
            for stmt in ctx.statement():
                self.visit(stmt)
        elif ctx.ELSE():
            else_block = ctx.getChild(6)  # The ELSE block is always the 7th child
            for stmt in else_block.statement():
                self.visit(stmt)
        return None

    def evaluate_condition(self, ctx):
        # Case: expr OP expr
        if ctx.comparisonOp():
            left = self.evaluate_expr(ctx.expr(0))
            right = self.evaluate_expr(ctx.expr(1))
            op = ctx.comparisonOp().getText()
            return self.apply_comparison(left, right, op)
        elif ctx.ID():
            return ctx.ID().getText() in self.events or self.periods
        elif ctx.booleanLiteral():
            return ctx.booleanLiteral().getText().lower() == "true"
        return False

    def evaluate_expr(self, ctx):
        if ctx.ID() and ctx.property_():
            obj_id = ctx.ID().getText()
            prop = ctx.property_().getText().lower()

            # Check events
            if obj_id in self.events and prop in self.events[obj_id]:
                return self.events[obj_id][prop]
            if obj_id in self.periods and prop in self.periods[obj_id]:
                return self.periods[obj_id][prop]
        elif ctx.STRING():
            return ctx.STRING().getText().strip('"')
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.importanceValue():
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
                all_years.append(self.events[comp_id]["date"]["year"])
            elif comp_id in self.periods:
                all_years.append(self.periods[comp_id]["start"]["year"])
                all_years.append(self.periods[comp_id]["end"]["year"])

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
            ticks = list(range(int(timeline_start), int(timeline_end) + 1, int(tick_step)))
            ticks_set = set(ticks)

        ax.annotate(
            '',
            xy=(timeline_end, y_axis),
            xytext=(timeline_start, y_axis),
            arrowprops=dict(arrowstyle='->', color='black', linewidth=2)
        )

        def get_month_name(month_number):
            """Convert a month number (1-12) to the full month name."""
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
