from TimelineParserListener import TimelineParserListener
import re
import matplotlib.pyplot as plt
import json
import os
import matplotlib.patches as mpatches
from collections import defaultdict

class TimelineInterpreter(TimelineParserListener):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.already_exported = set()

    def parse_year_literal(self, raw):
        # Match something like 753-BCE or 753-CE or just 753
        match = re.match(r"(\d+)(?:-(BCE|CE))?", raw)
        if match:
            year = int(match.group(1))
            era = match.group(2)
            if era == "BCE":
                year = -year
            return year
        return None

    def enterEventDecl(self, ctx):
        event_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        raw_date = ctx.dateExpr().getText()
        parsed_date = self.parse_year_literal(raw_date)

        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()

        self.events[event_id] = {
            "title": title,
            "date": parsed_date,
            "importance": importance
        }

        print(f"Event parsed: {self.events[event_id]}")

    def enterPeriodDecl(self, ctx):
        period_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')

        raw_start = ctx.START().getText()
        raw_end = ctx.END().getText()

        # Extract dates
        start_date = self.parse_year_literal(ctx.dateExpr(0).getText())
        end_date = self.parse_year_literal(ctx.dateExpr(1).getText())

        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()

        self.periods[period_id] = {
            "title": title,
            "start": start_date,
            "end": end_date,
            "importance": importance
        }

        print(f"Period parsed: {self.periods[period_id]}")

    def enterTimelineDecl(self, ctx):
        timeline_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')

        # Extract component IDs from componentList
        id_list = []
        comp_ctx = ctx.componentList()
        if comp_ctx:
            ids = comp_ctx.ID()
            id_list = [id.getText() for id in ids]

        self.timelines[timeline_id] = {
            "title": title,
            "components": id_list
        }

        print(f"Timeline parsed: {self.timelines[timeline_id]}")

    def generate_visualization(self, timeline_id, save_path=None):
        timeline = self.timelines[timeline_id]
        components = timeline["components"]

        fig, ax = plt.subplots(figsize=(14, 5))

        LOW_COLORS = ["#FFD700", "#FFC300", "#FFB000", "#FFA500", "#FF8C00", "#FF7F50", "#FF6F00", "#FF4500"]
        MEDIUM_COLORS = ["#00FF00", "#32CD32", "#3CB371", "#2ECC71", "#228B22", "#66FF66", "#7CFC00", "#20C997"]
        HIGH_COLORS = ["#1E90FF", "#007FFF", "#3399FF", "#0055FF", "#4682B4", "#4169E1", "#0000CD", "#0000FF"]

        color_sets = {"LOW": LOW_COLORS, "MEDIUM": MEDIUM_COLORS, "HIGH": HIGH_COLORS}
        color_indices = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        y_axis = 0

        all_years = []
        for comp_id in components:
            if comp_id in self.events:
                all_years.append(self.events[comp_id]["date"])
            elif comp_id in self.periods:
                all_years.extend([self.periods[comp_id]["start"], self.periods[comp_id]["end"]])

        if not all_years:
            print("[Error] No date data available.")
            return

        min_year = min(all_years)
        max_year = max(all_years)
        timeline_start = min_year - 20
        timeline_end = max_year + 20
        range_years = timeline_end - timeline_start

        num_divisions = max(10, range_years // 10)
        tick_step = max(1, range_years // num_divisions)
        ticks = list(range(timeline_start, timeline_end + 1, tick_step))
        ticks_set = set(ticks)

        ax.annotate(
            '',
            xy=(timeline_end, y_axis),
            xytext=(timeline_start, y_axis),
            arrowprops=dict(arrowstyle='->', color='black', linewidth=2)
        )

        for tick in ticks:
            ax.plot([tick, tick], [y_axis - 0.05, y_axis + 0.05], color='black', linewidth=1)
            ax.text(tick, y_axis - 0.15, str(tick), ha='center', va='top', fontsize=8)

        event_overlap = defaultdict(int)
        period_overlap = defaultdict(int)
        legend_entries = []
        used_labels = set()

        def get_next_color(importance):
            idx = color_indices[importance]
            color_list = color_sets[importance]
            color = color_list[idx % len(color_list)]
            color_indices[importance] += 1
            return color

        importance_order = ["HIGH", "MEDIUM", "LOW"]
        drawn_components = []

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
                    title = event["title"]
                    color = get_next_color(importance)
                    size = {"HIGH": 14, "MEDIUM": 10, "LOW": 8}[importance]

                    offset = event_overlap[date]
                    y_offset = y_axis + offset * 0.25
                    event_overlap[date] += 1

                    ax.scatter(date, y_offset, s=size ** 2, color=color, edgecolors='black', zorder=3)
                    ax.text(
                        date + 0.5 * (offset % 2 * 2 - 1),  # alternate left/right
                        y_offset + 0.15,
                        title,
                        rotation=45,
                        ha='center',
                        va='bottom',
                        fontsize=8,
                        zorder=4
                    )

                    if date not in ticks_set:
                        ax.text(date, y_axis - 0.25, f"{date}", ha='center', va='top', fontsize=7)

                    label = f"{title} = {date}"
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
                    width = {"HIGH": 8, "MEDIUM": 6, "LOW": 4}[importance]

                    key = (start, end)
                    offset = period_overlap[key]
                    y_offset = y_axis + offset * 0.25
                    period_overlap[key] += 1

                    ax.hlines(y_offset, start, end, linewidth=width, color=color, alpha=0.9, zorder=2)
                    ax.text((start + end) / 2, y_offset + 0.15, title, ha='center', va='bottom', fontsize=8, zorder=3)

                    if start not in ticks_set:
                        ax.text(start, y_axis - 0.25, f"{start}", ha='center', va='top', fontsize=7)
                    if end not in ticks_set:
                        ax.text(end, y_axis - 0.25, f"{end}", ha='center', va='top', fontsize=7)

                    label = f"{title} = {start} → {end}"
                    if label not in used_labels:
                        legend_entries.append((mpatches.Patch(color=color, alpha=0.9), label))
                        used_labels.add(label)

                    drawn_components.append(comp_id)

                else:
                    print(f"[Warning] Unknown component '{comp_id}'")

        ax.set_xlim(timeline_start, timeline_end)
        ax.set_ylim(-1, max(event_overlap.values()) * 0.4 + 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(timeline["title"])
        ax.set_xlabel("Year")

        if legend_entries:
            handles, labels = zip(*legend_entries)
            ax.legend(handles, labels, loc='upper right', fontsize=9, frameon=True, bbox_to_anchor=(1, 1))

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"[Exported] Timeline image saved to {save_path}")
            plt.close()
        else:
            plt.show()

    def enterExportStmt(self, ctx):
        export_id = ctx.ID().getText()
        print(f"Export requested for: {export_id}")

        # Prevent duplicate exports
        if hasattr(self, 'already_exported') is False:
            self.already_exported = set()

        if export_id in self.already_exported:
            print(f"[Info] Skipping already exported: {export_id}")
            return

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

    def enterIfStmt(self, ctx):
        result = self.evaluate_condition(ctx.condition())

        if result:
            for stmt in ctx.statement():
                self.handleStatement(stmt)
        elif ctx.ELSE():
            else_block = ctx.getChild(6)  # The ELSE block is always the 7th child
            for stmt in else_block.statement():
                self.handleStatement(stmt)

    def handleStatement(self, ctx):
        if ctx.exportStmt():
            self.enterExportStmt(ctx.exportStmt())
        elif ctx.ifStmt():
            self.enterIfStmt(ctx.ifStmt())
        elif ctx.modifyStmt():
            self.enterModifyStmt(ctx.modifyStmt())
        elif ctx.forStmt():
            self.enterForStmt(ctx.forStmt())

    def enterMainBlock(self, ctx):
        for stmt in ctx.statement():
            self.handleStatement(stmt)

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
