import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & ROYAL VEDIC THEME
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered", page_icon="🕉️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    .stApp { background-color: #FFFBF0 !important; font-family: 'Noto Sans Kannada', sans-serif; color: #1F1F1F !important; }
    .header-box { background: linear-gradient(135deg, #6A040F, #9D0208); color: #FFFFFF !important; padding: 16px; text-align: center; font-weight: 900; font-size: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(106, 4, 15, 0.3); border-bottom: 4px solid #FAA307; }
    div[data-testid="stTabs"] button[aria-selected="false"] p { color: #5D4037 !important; font-weight: 700 !important; }
    div[data-testid="stTabs"] button[aria-selected="true"] p { color: #9D0208 !important; font-weight: 900 !important; }
    .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 100%; max-width: 380px; aspect-ratio: 1 / 1; margin: 0 auto; gap: 2px; background: #370617; border: 4px solid #6A040F; border-radius: 4px; }
    .box { background: #FFFFFF; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; padding: 2px; text-align: center; color: #000 !important; }
    .center-box { grid-column: 2/4; grid-row: 2/4; background: linear-gradient(135deg, #FFBA08, #FAA307); display: flex; flex-direction: column; align-items: center; justify-content: center; color: #370617 !important; font-weight: 900; font-size: 13px; }
    .lbl { position: absolute; top: 2px; left: 3px; font-size: 9px; color: #DC2F02 !important; font-weight: 900; }
    .hi { color: #D00000 !important; text-decoration: underline; font-weight: 900; }
    .card { background: #FFFFFF; border-radius: 12px; padding: 15px; margin-bottom: 12px; border: 1px solid #F0F0F0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .key { color: #9D0208 !important; font-weight: 900; width: 40%; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v97")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
KN_RASHI = ["ಮೇಷ", "Vೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_altitude_manual(jd, lat, lon):
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
    start_jd = jd_noon - 0.5
    rise_time, set_time = -1, -1
    step = 1/24.0
    current = start_jd
    for i in range(24):
        alt1 = get_altitude_manual(current, lat, lon)
        alt2 = get_altitude_manual(current + step, lat, lon)
        if alt1 < -0.833 and alt2 >= -0.833:
            l, h = current, current + step
            for _ in range(20): 
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) < -0.833: l = m
                else: h = m
            rise_time = h
        if alt1 > -0.833 and alt2 <= -0.833:
            l, h = current, current + step
            for _ in range(20): 
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) > -0.833: l = m
                else: h = m
            set_time = h
        current += step
    return rise_time, set_time

def get_full_calculations(jd, lat, lon):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd)
    positions = {}
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        positions[KN_PLANETS[pid]] = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]], positions[KN_PLANETS[102]] = rahu, (rahu + 180) % 360
    positions[KN_PLANETS["Lagna"]] = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    
    # --- RIGOROUS MANDI LOGIC ---
    sr_today, ss_today = find_sunrise_set(jd, lat, lon)
    
    day_ghati = [26, 22, 18, 14, 10, 6, 2]
    night_ghati = [10, 6, 2, 26, 22, 18, 14]
    
    # 1. Determine Local Weekday (IST Correction)
    jd_local = jd + (5.5/24.0)
    cal_wday = int(jd_local + 0.5 + 1.5) % 7
    
    if jd < sr_today:
        # Case A: Born before sunrise today (Night of Yesterday)
        prev_sr, prev_ss = find_sunrise_set(jd - 1.0, lat, lon)
        w_idx = (cal_wday - 1) % 7
        start_base, dur = prev_ss, (sr_today - prev_ss)
        factor = night_ghati[w_idx]
        pan_sr = prev_sr
    elif jd >= ss_today:
        # Case B: Born after sunset today (Night of Today)
        next_sr, _ = find_sunrise_set(jd + 1.0, lat, lon)
        w_idx = cal_wday
        start_base, dur = ss_today, (next_sr - ss_today)
        factor = night_ghati[w_idx]
        pan_sr = sr_today
    else:
        # Case C: Day Birth
        w_idx = cal_wday
        start_base, dur = sr_today, (ss_today - sr_today)
        factor = day_ghati[w_idx]
        pan_sr = sr_today

    mtime = start_base + (dur * factor / 30.0)
    positions[KN_PLANETS["Ma"]] = (swe.houses(mtime, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mtime)) % 360

    # Panchanga
    diff = (positions["ಚಂದ್ರ"] - positions["ರವಿ"] + 360) % 360
    n_idx = int(positions["ಚಂದ್ರ"] / 13.333333333)
    perc = (positions["ಚಂದ್ರ"] % 13.333333333) / 13.333333333
    
    pan = {
        "v": KN_VARA[w_idx], "sr": pan_sr, 
        "udayadi": f"{int((jd - pan_sr)*60)} ಘಟಿ",
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(YEARS[n_idx%9]*(1-perc))}ವ",
        "n_idx": n_idx, "perc": perc, "jd_birth": jd
    }
    return positions, pan

# ==========================================
# 3. UI
# ==========================================
st.markdown('<div class="header-box">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)
if 'page' not in st.session_state: st.session_state.page = "input"

if st.session_state.page == "input":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("ಗಂಟೆ", 1, 12, 2)
        m = c2.number_input("ನಿಮಿಷ", 0, 59, 43)
        ampm = c3.selectbox("AM/PM", ["AM", "PM"], index=0) # Set to AM for your example
        lat = st.number_input("Lat", value=14.98, format="%.4f")
        lon = st.number_input("Lon", value=74.73, format="%.4f")
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0)
            h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            pos, pan = get_full_calculations(jd, lat, lon)
            st.session_state.data = {"pos": pos, "pan": pan, "date": dob}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    pos, pan = st.session_state.data['pos'], st.session_state.data['pan']
    if st.button("⬅️ ಹಿಂದಕ್ಕೆ"): st.session_state.page = "input"; st.rerun()
    t1, t2, t3, t4 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ"])
    with t1:
        v_opt = st.selectbox("ವರ್ಗ", [1, 9], format_func=lambda x: f"D{x}")
        bxs = {i: "" for i in range(12)}
        for n, d in pos.items():
            ri = int(d/30) if v_opt==1 else (([0,9,6,3][int(d/30)%4]) + int((d%30)/3.33333)) % 12
            bxs[ri] += f'<div class="{"hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else ""}" style="font-weight:900;">{n}</div>'
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for idx in grid:
            if idx is None:
                if html.count("center-box") == 0: html += f'<div class="center-box">D{v_opt}</div>'
            else: html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)
    with t2:
        st.table(pd.DataFrame([{"ಗ್ರಹ": k, "ಅಂಶ": f"{int(v/30)}R {int(v%30)}°"} for k,v in pos.items()]))
    with t4:
        st.markdown(f"<div class='card'><b>ವಾರ:</b> {pan['v']}<br><b>ಉದಯಾದಿ:</b> {pan['udayadi']}</div>", unsafe_allow_html=True)
