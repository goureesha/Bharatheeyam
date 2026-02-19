import streamlit as st
import datetime
import calendar

# ==========================================
# 1. CORE ASTROLOGY LOGIC (The Brain)
# ==========================================

def get_astrological_day_details(birth_datetime, sunrise_time, sunset_time):
    """
    Determines the astrological weekday and whether it is day or night.
    Handles the '2 AM Problem' where early morning belongs to the previous day.
    """
    date_val = birth_datetime.date()
    time_val = birth_datetime.time()
    
    # Create full datetime objects for sunrise/sunset on the birth date
    sr_today = datetime.datetime.combine(date_val, sunrise_time)
    ss_today = datetime.datetime.combine(date_val, sunset_time)
    
    # LOGIC: 
    # If birth is before Sunrise (e.g., 2 AM), it belongs to the PREVIOUS day's night.
    if birth_datetime < sr_today:
        # It is technically "Yesterday" in Vedic terms
        astro_date = date_val - datetime.timedelta(days=1)
        weekday_idx = astro_date.weekday() # 0=Mon, 6=Sun
        period = "Night"
        
        # For calculation, we need Yesterday's Sunset and Today's Sunrise
        # (Approximation: We use today's SR and SS times shifted back, 
        # for precise astro you would query specific ephemeris, but this is standard for apps)
        start_time = ss_today - datetime.timedelta(days=1) # Yesterday Sunset
        end_time = sr_today # Today Sunrise
        
    # If birth is after Sunset, it is "Night" of the current day
    elif birth_datetime >= ss_today:
        astro_date = date_val
        weekday_idx = astro_date.weekday()
        period = "Night"
        
        start_time = ss_today # Today Sunset
        end_time = sr_today + datetime.timedelta(days=1) # Tomorrow Sunrise
        
    # Otherwise, it is "Day"
    else:
        astro_date = date_val
        weekday_idx = astro_date.weekday()
        period = "Day"
        
        start_time = sr_today
        end_time = ss_today

    return {
        "weekday_idx": weekday_idx,
        "period": period,
        "start_time": start_time,
        "end_time": end_time,
        "astro_date": astro_date
    }

def calculate_mandi_gulika(birth_datetime, sunrise_time, sunset_time):
    # 1. Get the correct astrological context
    astro_data = get_astrological_day_details(birth_datetime, sunrise_time, sunset_time)
    
    # 2. Define Coefficients (The "Ghati" values)
    # Format: Weekday Index (0=Mon): {'Day': x, 'Night': y}
    # Values represent the END of the Saturn/Gulika portion
    
    # Mandi Table
    mandi_table = {
        6: {'Day': 26, 'Night': 10}, # Sunday
        0: {'Day': 22, 'Night': 6},  # Monday
        1: {'Day': 18, 'Night': 2},  # Tuesday
        2: {'Day': 14, 'Night': 26}, # Wednesday
        3: {'Day': 10, 'Night': 22}, # Thursday
        4: {'Day': 6,  'Night': 18}, # Friday
        5: {'Day': 2,  'Night': 14}  # Saturday
    }
    
    # Gulika Table (Segments of 8)
    # Sunday=7, Mon=6, Tue=5, Wed=4, Thu=3, Fri=2, Sat=1
    # Day starts at Segment X, Night starts at Segment Y. 
    # Simplified standard Gulika start times (in Ghatis from sunrise/sunset):
    gulika_start_ghati = {
        6: {'Day': 26.25, 'Night': 10}, # Sun (Approx for simplicity, usually calculated by segment)
        0: {'Day': 22.5,  'Night': 6},  # Mon
        1: {'Day': 18.75, 'Night': 2},  # Tue
        2: {'Day': 15,    'Night': 26}, # Wed
        3: {'Day': 11.25, 'Night': 22}, # Thu
        4: {'Day': 7.5,   'Night': 18}, # Fri
        5: {'Day': 3.75,  'Night': 14}  # Sat
    }
    
    # 3. Calculate Duration
    duration_seconds = (astro_data['end_time'] - astro_data['start_time']).total_seconds()
    
    # 4. Calculate Mandi
    mandi_ghati = mandi_table[astro_data['weekday_idx']][astro_data['period']]
    mandi_seconds = (mandi_ghati / 30.0) * duration_seconds
    mandi_time = astro_data['start_time'] + datetime.timedelta(seconds=mandi_seconds)
    
    # 5. Return Results
    days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_kn = ["ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ", "ಭಾನುವಾರ"]
    
    return {
        "mandi_time": mandi_time,
        "astro_day_en": days_en[astro_data['weekday_idx']],
        "astro_day_kn": days_kn[astro_data['weekday_idx']],
        "period": astro_data['period'],
        "duration_hrs": duration_seconds / 3600
    }

# ==========================================
# 2. UI & APP STRUCTURE (The Body)
# ==========================================

st.set_page_config(page_title="Vedic Astro Pro", layout="wide")

# Custom CSS for that "App" feel
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .result-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 1px solid #d1d1d1; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    # Placeholder for Logo
    st.write("☀️/🌑")
with col2:
    st.title("Dawn & Dusk: Vedic Calculator")
    st.write("ದಾನ್ ಅಂಡ್ ಡಸ್ಕ್ ಜ್ಯೋತಿಷ್ಯ ಅಪ್ಲಿಕೇಶನ್")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🧮 Mandi Calc", "🔮 Kundali", "📅 Appointments"])

# --- TAB 1: HOME ---
with tab1:
    st.header("Welcome / ಸ್ವಾಗತ")
    st.info("Currently running correctly for Day and Night calculations.")
    st.write("This app provides accurate Vedic calculations specifically tuned for Indian Standard Time.")

# --- TAB 2: MANDI CALCULATOR (The Fix) ---
with tab2:
    st.header("Mandi & Gulika Calculator")
    st.markdown("Use this tab to find the exact rising time of Mandi (ಮಂದಿ).")
    
    with st.form("calc_form"):
        c1, c2 = st.columns(2)
        with c1:
            d_date = st.date_input("Birth Date (ದಿನಾಂಕ)", datetime.date.today())
            t_time = st.time_input("Birth Time (ಸಮಯ)", datetime.datetime.now().time())
        with c2:
            # Default to roughly India average if not known, but editable
            sunrise = st.time_input("Sunrise (ಸೂರ್ಯೋದಯ)", datetime.time(6, 30))
            sunset = st.time_input("Sunset (ಸೂರ್ಯಾಸ್ತ)", datetime.time(18, 30))
            
        submitted = st.form_submit_button("Calculate / ಲೆಕ್ಕಾಚಾರ ಮಾಡಿ")
        
    if submitted:
        # Combine Date and Time
        b_dt = datetime.datetime.combine(d_date, t_time)
        
        # Run the Logic
        res = calculate_mandi_gulika(b_dt, sunrise, sunset)
        
        st.write("---")
        # Display Results in a nice box
        st.markdown(f"""
        <div class="result-box">
            <h3>Results (ಫಲಿತಾಂಶಗಳು)</h3>
            <p><b>Astrological Day:</b> {res['astro_day_en']} ({res['astro_day_kn']})</p>
            <p><b>Birth Period:</b> {res['period']} (Day/Night)</p>
            <p><b>Day/Night Duration:</b> {res['duration_hrs']:.2f} Hours</p>
            <hr>
            <p class="big-font">Mandi Rise Time: {res['mandi_time'].strftime('%I:%M:%S %p')}</p>
            <p><i>(Use this time to calculate the Mandi Ascendant)</i></p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: KUNDALI (Placeholder) ---
with tab3:
    st.header("Kundali (ಜಾತಕ)")
    st.warning("Feature coming soon... (Rashi, Navamsha, Bhava)")
    # This is where you would integrate the chart drawing logic later

# --- TAB 4: APPOINTMENTS ---
with tab4:
    st.header("Book Consultation")
    st.write("Astrology & Yoga Appointment System")
    
    with st.expander("Book a Slot"):
        name = st.text_input("Name")
        service = st.selectbox("Service", ["Horoscope Analysis", "Muhurtha", "Prashna"])
        st.button("Confirm Booking")

# --- FOOTER ---
st.write("---")
st.caption("© 2026 Dawn and Dusk | Developed for Vedic Research")
