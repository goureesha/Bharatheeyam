import datetime

def calculate_mandi(birth_datetime, sunrise_time, sunset_time, next_sunrise_time):
    """
    Calculates the exact time Mandi rises based on birth time, handling
    Day vs Night logic automatically.
    """
    
    # 1. Determine Weekday (0=Mon, 6=Sun)
    # CRITICAL: If birth is between 00:00 and Sunrise, it belongs to the PREVIOUS astrological day.
    # We use the sunrise date to determine the astrological weekday.
    
    # Convert input times to full datetime objects for comparison
    # Assuming sunrise/sunset are passed as time objects, we attach them to the birth date
    birth_date = birth_datetime.date()
    
    sunrise_dt = datetime.datetime.combine(birth_date, sunrise_time)
    sunset_dt = datetime.datetime.combine(birth_date, sunset_time)
    next_sunrise_dt = datetime.datetime.combine(birth_date + datetime.timedelta(days=1), next_sunrise_time)

    # Handle post-midnight birth (before sunrise)
    # If birth is 2 AM on Tuesday, astrologically it is still Monday night.
    if birth_datetime < sunrise_dt:
        # Shift back to previous day for logic
        astrological_weekday_idx = (birth_datetime.weekday() - 1) % 7
        is_day_birth = False
        
        # We need the previous day's sunset for calculation
        # For simplicity in this standalone snippet, we assume sunset/sunrise don't change drastically 
        # over 24h, but ideally you'd pass the specific previous sunset.
        # Here we approximate previous sunset as 24h before today's sunset
        current_period_start = sunset_dt - datetime.timedelta(days=1)
        current_period_end = sunrise_dt
        
    elif birth_datetime >= sunrise_dt and birth_datetime < sunset_dt:
        # Day Birth
        astrological_weekday_idx = birth_datetime.weekday()
        is_day_birth = True
        current_period_start = sunrise_dt
        current_period_end = sunset_dt
        
    else:
        # Night Birth (After sunset, before midnight)
        astrological_weekday_idx = birth_datetime.weekday()
        is_day_birth = False
        current_period_start = sunset_dt
        current_period_end = next_sunrise_dt

    # 2. Weekday Names for Display
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    astro_day_name = weekdays[astrological_weekday_idx]

    # 3. Define Mandi Ratios (The "Magic Numbers")
    # These represent the *End* of the Saturn portion in a 30-Ghati day.
    # Format: {Weekday_Index: (Day_Value, Night_Value)}
    # Monday=0, ... Sunday=6
    mandi_lookup = {
        6: (26, 10), # Sunday
        0: (22, 6),  # Monday
        1: (18, 2),  # Tuesday
        2: (14, 26), # Wednesday
        3: (10, 22), # Thursday
        4: (6, 18),  # Friday
        5: (2, 14)   # Saturday
    }

    # Get the specific value (Ghatis out of 30)
    day_val, night_val = mandi_lookup[astrological_weekday_idx]
    target_ghati = day_val if is_day_birth else night_val

    # 4. Calculate Duration of Day or Night
    total_duration = current_period_end - current_period_start
    total_seconds = total_duration.total_seconds()

    # 5. Apply the Formula
    # Formula: (Target_Ghati / 30) * Duration_in_Seconds
    mandi_seconds_from_start = (target_ghati / 30.0) * total_seconds
    
    # 6. Add offset to the Start Time (Sunrise for Day, Sunset for Night)
    mandi_rise_time = current_period_start + datetime.timedelta(seconds=mandi_seconds_from_start)

    # Output
    period_type = "Day" if is_day_birth else "Night"
    return {
        "Astrological Day": astro_day_name,
        "Birth Period": period_type,
        "Period Duration": str(total_duration),
        "Mandi Rise Time": mandi_rise_time.strftime('%Y-%m-%d %H:%M:%S')
    }

# ==========================================
# TEST CASE: USER SETTINGS
# ==========================================

# Example: A birth on Wednesday Night (Technically Thursday morning 2 AM)
# Date: 2025-11-20, Time: 02:00:00 (AM)
# Sunrise: 06:30, Sunset: 17:30 (5:30 PM)

b_date = datetime.date(2025, 11, 20)
b_time = datetime.time(2, 0, 0) # 2 AM
birth_dt = datetime.combine(b_date, b_time)

# Define Sunrise/Sunset for the location
sr = datetime.time(6, 30, 0) 
ss = datetime.time(17, 30, 0)

# Run Calculation
result = calculate_mandi(birth_dt, sr, ss, sr)

print("--- Mandi Calculation Result ---")
for k, v in result.items():
    print(f"{k}: {v}")
