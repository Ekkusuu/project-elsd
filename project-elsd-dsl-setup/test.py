import math

timeline_start = 10
timeline_end = 14

range_years = timeline_end - timeline_start

# Example tick calculation
num_divisions = 12  # This determines how many ticks we want
tick_step =  range_years / num_divisions

ticks = []
ticks_set = set()
print(tick_step)
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

        # Store the tick as a (year, month) tuple
        ticks.append((year, month))
        ticks_set.add((year, month))

        # Move to the next tick based on tick_step
        tick += tick_step

else:
    # If tick_step is a whole number, just use years
    ticks = list(range(timeline_start, timeline_end + 1, int(tick_step)))
    ticks_set = set(ticks)

# Print the ticks for verification
print(f"Ticks: {ticks}")
