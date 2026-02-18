import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & CSS (THEME)
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered", page_icon="🕉️")

# Exact CSS from your Colab code adapted for Streamlit
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    
    /* Main Background */
    .stApp { background-color: #fff8e1; font-family: 'Noto Sans Kannada', sans-serif; }
    
    /* Header */
    .header-box { background: #b71c1c; color: white; padding: 15px; text-align: center; font-weight: 900; font-size: 24px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    
    /* Grid System for Kundali */
    .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 340px; height: 340px; margin: 0 auto; gap: 2px; background: #333; border: 3px solid #b71c1c; }
    .box { background: white; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; min-height: 80px; padding: 2px; text-align: center; }
    .lbl { position: absolute; top: 1px; left: 2px; font-size: 9px; color: #999; font-weight: 900; }
    .hi { color: #d50000; text-decoration: underline; font-weight: 900; }
    .pl { color: #000; font-weight: bold; }
    .center-box { grid-column: 2/4; grid-row: 2/4; background: #ffe0b2; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #b71c1c; font-weight: 900; font-size: 12px; text-align: center; }
    
    /* Tables & Cards */
    .card { background: white; border-radius: 8px; padding: 15px; margin-bottom: 10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .key-val-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .key-val-table td { border-bottom: 1px solid #eee; padding: 8px; color: #000; }
    .key { color: #b71c1c; font-weight: 900; width: 40%; }
    
    /* Dasha Tree Styling (Pure HTML) */
    details { margin-bottom: 5px; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; background: white; }
    summary { cursor: pointer; padding: 10px; font-size: 14px; list-style: none; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; }
    .md-node { background: #b71c1c !important; color: white !important; font-weight: 900; }
    .ad-node { background: #fffde7 !important; color: #b71c1c !important; font-weight: 700; margin-left: 10px; border-left: 5px solid #ffd600; }
    .pd-node { background: #f1f8e9 !important; color: #1b5e20 !important; font-weight: 700; margin-left: 15px; border-left: 5px solid #4caf50; }
    .sd-node { background: #e3f2fd !important; color: #0d47a1 !important; font-size: 12px; font-weight: 900; margin-left: 20px; border-left: 5px solid #2196f3; padding: 8px; border-bottom: 1px solid #eee; }
    .date-label { font-size: 11px; opacity: 0.9; float: right; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE LOGIC (Your "Nuclear" Math)
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_app")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಘ", "ಪೂರ್ವ ಫಾಲ್ಗುಣಿ", "ಉತ್ತರ ಫಾಲ್ಗುಣಿ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜ್ಯೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_altitude_manual(jd, lat, lon):
    # Manual calculation to bypass library errors
    res = swe.calc_ut(jd, swe.SUN, swe.FLG_EQUATORIAL | swe.FLG_SWIEPH)
    ra, dec = res[0][0], res[0][1]
    gmst = swe.sidtime(jd)
    lst = gmst + (lon / 15.0)
    ha_deg = ((lst * 15.0) - ra + 360) % 360
    if ha_deg > 180: ha_deg -= 360
    lat_rad, dec_rad, ha_rad = math.radians(lat), math.radians(dec), math.radians(ha_deg)
    sin_alt = (math.sin(lat_rad) * math.sin(dec_rad)) + (math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad))
    return math.degrees(math.asin(sin_alt))

def find_sunrise_set(jd_noon, lat, lon):
    # Binary search for exact -0.833 altitude (Sunrise/Sunset)
    start_jd = jd_noon - 0.5
    rise_time, set_time = -1, -1
    step = 1/24.0
    current = start_jd
    for i in range(24):
        alt1 = get_altitude_manual(current, lat, lon)
        alt2 = get_altitude_manual(current + step, lat, lon)
        # Sunrise Cross
        if alt1 < -0.833 and alt2 >= -0.833:
            l, h = current, current + step
            for _ in range(20): # Precision loop
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) < -0.833: l = m
                else: h = m
            rise_time = h
        # Sunset Cross
        if alt1 > -0.833 and alt2 <= -0.833:
            l, h = current, current + step
            for _ in range(20): # Precision loop
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) > -0.833: l = m
                else: h = m
            set_time = h
        current += step
    return rise_time, set_time

def find_nak_limit(jd, target_deg):
    low = jd - 1.2; high = jd + 1.2
    for _ in range(20):
        mid = (low + high) / 2
        ayan = swe.get_ayanamsa(mid)
        m_deg = (swe.calc_ut(mid, swe.MOON)[0][0] - ayan) % 360
        diff = (m_deg - target_deg + 180) % 360 - 180
        if diff < 0: low = mid
        else: high = mid
    return mid

def fmt_ghati(decimal_val):
    g = int(decimal_val)
    rem = decimal_val - g
    v = int(round(rem * 60))
    if v == 60: g += 1; v = 0
    return f"{g}.{v:02d}"

def get_full_calculations(jd, lat, lon):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd)
    positions = {}
    
    # Planets
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        deg = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
        positions[KN_PLANETS[pid]] = deg
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]] = rahu
    positions[KN_PLANETS[102]] = (rahu + 180) % 360
    
    # Lagna
    lagna = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    positions[KN_PLANETS["Lagna"]] = lagna
    
    # Mandi Logic (Using Manual Sunrise)
    sr, ss = find_sunrise_set(jd, lat, lon)
    
    # Fallback if binary search missed (polar circles etc, unlikely in India)
    if sr == -1 or ss == -1: 
        sr = jd - 0.25; ss = jd + 0.25 

    # Check previous day if current time is before sunrise
    day_sr = sr if jd >= sr else find_sunrise_set(jd - 1.0, lat, lon)[0]
    
    w_idx = int(day_sr + 0.5 + 1.5) % 7
    
    # Mandi Factors
    yf_day = [26, 22, 18, 14, 10, 6, 2]
    yf_night = [10, 6, 2, 26, 22, 18, 14]
    
    if jd >= sr and jd < ss: # Day
        dur = ss - sr
        yf = yf_day[w_idx]
        mtime = sr + (dur * yf / 30.0)
    else: # Night
        if jd >= ss:
            next_sr = find_sunrise_set(jd + 1.0, lat, lon)[0]
            dur = next_sr - ss
            yf = yf_night[w_idx]
            mtime = ss + (dur * yf / 30.0)
        else: # Before sunrise
            prev_ss = find_sunrise_set(jd - 1.0, lat, lon)[1]
            # Previous day logic for night before sunrise
            prev_w_idx = (w_idx - 1) % 7
            dur = sr - prev_ss
            yf = yf_night[prev_w_idx]
            mtime = prev_ss + (dur * yf / 30.0)

    mandi_deg = (swe.houses(mtime, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mtime)) % 360
    positions[KN_PLANETS["Ma"]] = mandi_deg

    # Panchanga & Dasha
    moon_deg, sun_deg = positions["ಚಂದ್ರ"], positions["ರವಿ"]
    t_idx = int(((moon_deg - sun_deg + 360) % 360) / 12)
    n_idx = int(moon_deg / 13.333333333)
    
    # Limits for Ghati
    js = find_nak_limit(jd, n_idx * 13.333333333)
    je = find_nak_limit(jd, (n_idx + 1) * 13.333333333)
    
    perc = (moon_deg % 13.333333333) / 13.333333333
    bal = YEARS[n_idx % 9] * (1 - perc)

    pan = {
        "t": KN_TITHI[min(t_idx, 29)], "v": KN_VARA[w_idx], "n": KN_NAK[n_idx % 27],
        "sr": day_sr, "ss": ss,
        "udayadi": fmt_ghati((jd - day_sr) * 60), 
        "gata": fmt_ghati((jd - js) * 60),
        "parama": fmt_ghati((je - js) * 60), 
        "rem": fmt_ghati((je - jd) * 60),
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(bal)}ವ {int((bal%1)*12)}ತಿ {int((bal*12%1)*30)}ದಿ",
        "n_idx": n_idx, "perc": perc, "jd_birth": jd
    }
    return positions, pan

# ==========================================
# 3. SESSION STATE
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "input"
if 'data' not in st.session_state: st.session_state.data = {}
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'lat' not in st.session_state: st.session_state.lat = 14.98
if 'lon' not in st.session_state: st.session_state.lon = 74.73

# ==========================================
# 4. APP INTERFACE
# ==========================================
st.markdown('<div class="header-box">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

if st.session_state.page == "input":
    # --- INPUT PAGE ---
    with st.container():
        st.subheader("ಜಾತಕ ವಿವರಗಳು")
        name = st.text_input("ಹೆಸರು", "ಬಳಕೆದಾರ")
        dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
        
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("ಗಂಟೆ", 1, 12, 2)
        m = c2.number_input("ನಿಮಿಷ", 0, 59, 43)
        ampm = c3.selectbox("AM/PM", ["AM", "PM"], index=1)
        
        st.subheader("ಸ್ಥಳ")
        place_q = st.text_input("ಊರು ಹುಡುಕಿ (ಉದಾ: Bangalore)", "Yellapur")
        if st.button("ಹುಡುಕಿ"):
            try:
                loc = geolocator.geocode(place_q)
                if loc:
                    st.session_state.lat = loc.latitude
                    st.session_state.lon = loc.longitude
                    st.success(f"ಸಿಕ್ಕಿದೆ: {loc.address}")
            except: st.error("ಸಂಪರ್ಕ ದೋಷ")
            
        lat = st.number_input("ಅಕ್ಷಾಂಶ (Lat)", value=st.session_state.lat, format="%.4f")
        lon = st.number_input("ರೇಖಾಂಶ (Lon)", value=st.session_state.lon, format="%.4f")
        
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary", use_container_width=True):
            # Calculate JD
            h24 = h + (12 if ampm == "PM" and h != 12 else 0)
            h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            
            # Run Calculations
            pos, pan = get_full_calculations(jd, lat, lon)
            
            # Store in Session
            st.session_state.data = {"pos": pos, "pan": pan, "date": dob}
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    # --- DASHBOARD PAGE ---
    pos = st.session_state.data['pos']
    pan = st.session_state.data['pan']
    
    # Navigation
    c1, c2 = st.columns([1, 4])
    if c1.button("⬅️ ಹಿಂದಕ್ಕೆ"):
        st.session_state.page = "input"
        st.rerun()
    
    # Tabs
    t1, t2, t3, t4, t5 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        # KUNDALI
        c_v, c_b = st.columns(2)
        v_opt = c_v.selectbox("ವರ್ಗ", [1, 3, 9, 12, 30], format_func=lambda x: f"D{x}")
        b_opt = c_b.radio("View", ["ರಾಶಿ", "ಭಾವ"], horizontal=True)
        
        # Grid Logic
        bxs = {i: "" for i in range(12)}
        ld = pos["ಲಗ್ನ"]
        
        for n, d in pos.items():
            if v_opt == 1:
                # D1 Logic
                if b_opt == "ರಾಶಿ": 
                    ri = int(d/30)
                else: 
                    # Bhava Logic: 1st House centered on Lagna
                    ri = (int(ld/30) + int(((d - ld + 360) % 360 + 15) / 30)) % 12
            elif v_opt == 30:
                # Trimshamsha Logic
                r = int(d/30); dr = d%30; is_odd = (r%2==0) # 0 is Aries (Odd in 0-idx?) No, 0=Aries=Odd
                # Note: Index 0 is Aries (Odd). 1 is Taurus (Even).
                is_odd_sign = (int(d/30) % 2 == 0) # 0, 2, 4... are Odd Signs (Aries, Gemini...)
                if is_odd_sign: 
                    ri = 0 if dr<5 else 10 if dr<10 else 8 if dr<18 else 2 if dr<25 else 6
                else: 
                    ri = 5 if dr<5 else 2 if dr<12 else 8 if dr<20 else 10 if dr<25 else 0
            else:
                # Standard Division Logic (D9, D3, D12)
                if v_opt == 9: # Navamsha
                    block = int(d/30)%4 # Fire,Earth,Air,Water
                    start = [0, 9, 6, 3][block] # Aries, Capricorn, Libra, Cancer
                    steps = int((d%30)/3.33333)
                    ri = (start + steps) % 12
                elif v_opt == 3: # Drekkana
                    ri = (int(d/30) + (int((d%30)/10)*4)) % 12
                elif v_opt == 12: # Dwadashamsha
                    ri = (int(d/30) + int((d%30)/2.5)) % 12
                else:
                    ri = int(d/30) # Fallback

            cls = "hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl"
            bxs[ri] += f'<div class="{cls}">{n}</div>'

        # Render HTML Grid
        grid_order = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for idx in grid_order:
            if idx is None:
                if html.count("center-box") == 0:
                    html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v_opt}<br>{b_opt}</div>'
            else:
                html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with t2:
        # SPHUTA
        data = []
        for p, d in pos.items():
            r_name = KN_RASHI[int(d/30)]
            deg_str = f"{int(d%30)}° {int((d%30*60)%60)}'"
            data.append({"ಗ್ರಹ": p, "ರಾಶಿ": r_name, "ಅಂಶ": deg_str})
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.table(pd.DataFrame(data))
        st.markdown("</div>", unsafe_allow_html=True)

    with t3:
        # DASHA (The 4-Level HTML Generator)
        st.markdown(f"<div class='card'><b>ಶಿಷ್ಟ ದಶೆ:</b> {pan['d_bal']}</div>", unsafe_allow_html=True)
        
        dh = ""
        birth_date = datetime.datetime.combine(st.session_state.data['date'], datetime.time(0,0)) # Approx start for display math
        # Actually use JD for accurate math
        jd_start = pan['jd_birth']
        
        si = pan['n_idx'] % 9
        # Calculate start date of current MD
        # This is complex to display perfectly in static HTML without JS, 
        # so we display the tree structure assuming standard flow from birth.
        
        current_date = birth_date
        
        for i in range(9):
            im = (si + i) % 9
            # MD Duration (Adjust first MD for balance)
            md_dur_yrs = YEARS[im] * ((1 - pan['perc']) if i==0 else 1)
            md_end = current_date + datetime.timedelta(days=md_dur_yrs*365.25)
            
            dh += f"<details><summary class='md-node'><span>{LORDS[im]} ಮಹಾದಶ</span><span class='date-label'>ಮುಕ್ತಾಯ: {md_end.strftime('%d-%m-%Y')}</span></summary>"
            
            cad = current_date
            for j in range(9):
                ia = (im + j) % 9
                # AD Duration (MD * AD / 120) * balance_factor
                # Note: Dasha logic in Colab was simplified for display. 
                # Preserving the logic: Standard Proportions applied to the Remaining Time.
                
                ad_years = (YEARS[im] * YEARS[ia] / 120.0)
                if i==0: ad_years = ad_years * (1 - pan['perc']) # Scale first ADs? 
                # Actually, standard practice for Balance is:
                # The sub-periods run normally, but we start at a specific sub-period.
                # For this UI, we will list the proportional breakdown of the *remaining* time for the first block.
                
                ae = cad + datetime.timedelta(days=ad_years*365.25)
                
                dh += f"<details><summary class='ad-node'><span>{LORDS[ia]} ಭುಕ್ತಿ</span><span class='date-label'>{ae.strftime('%d-%m-%Y')}</span></summary>"
                
                cpd = cad
                for k in range(9):
                    ip = (ia + k) % 9
                    pd_years = (ad_years * YEARS[ip] / 120.0) # Relative to adjusted AD
                    pe = cpd + datetime.timedelta(days=pd_years*365.25)
                    
                    dh += f"<details><summary class='pd-node'><span>{LORDS[ip]}</span><span class='date-label'>{pe.strftime('%d-%m-%Y')}</span></summary>"
                    
                    csd = cpd
                    for l in range(9):
                        iss = (ip + l) % 9
                        sd_years = (pd_years * YEARS[iss] / 120.0)
                        se = csd + datetime.timedelta(days=sd_years*365.25)
                        
                        dh += f"<div class='sd-node'>&bull; {LORDS[iss]} ಸೂಕ್ಷ್ಮ: {se.strftime('%d-%m-%Y')}</div>"
                        csd = se
                    
                    dh += "</details>"
                    cpd = pe
                
                dh += "</details>"
                cad = ae
                
            dh += "</details>"
            current_date = md_end

        st.markdown(dh, unsafe_allow_html=True)

    with t4:
        # PANCHANGA
        st.markdown(f"""
        <div class='card'>
            <table class='key-val-table'>
                <tr><td class='key'>ತಿಥಿ</td><td>{pan['t']}</td></tr>
                <tr><td class='key'>ವಾರ</td><td>{pan['v']}</td></tr>
                <tr><td class='key'>ನಕ್ಷತ್ರ</td><td>{pan['n']}</td></tr>
                <tr><td class='key'>ಉದಯಾದಿ</td><td>{pan['udayadi']} ಘಟಿ</td></tr>
                <tr><td class='key'>ಗತ</td><td>{pan['gata']} ಘಟಿ</td></tr>
                <tr><td class='key'>ಶೇಷ</td><td>{pan['rem']} ಘಟಿ</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with t5:
        # NOTES
        st.session_state.notes = st.text_area("ಟಿಪ್ಪಣಿಗಳು", value=st.session_state.notes, height=300)
        if st.button("ಉಳಿಸಿ (Save Note)"):
            st.success("ಟಿಪ್ಪಣಿ ಉಳಿಸಲಾಗಿದೆ")
