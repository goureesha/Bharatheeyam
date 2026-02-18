import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. SERVER CONFIG & THEME
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans Kannada', sans-serif; background-color: #fff8e1; color: #000; }
    .main-title { color: white; background-color: #b71c1c; padding: 15px; text-align: center; font-weight: 900; font-size: 26px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 360px; height: 360px; margin: 15px auto; gap: 2px; background: #333; border: 3px solid #000; }
    .box { background: white; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; min-height: 85px; padding: 5px; text-align: center; }
    .box-lbl { position: absolute; top: 2px; left: 4px; font-size: 9px; color: #999; font-weight: 900; }
    .pl-name { color: #000; font-size: 12px; font-weight: 900; line-height: 1.1; }
    .hi { color: #d50000; text-decoration: underline; font-weight: 900; }
    .center-box { grid-column: 2/4; grid-row: 2/4; background: #ffe0b2; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #b71c1c; font-weight: 900; text-align: center; font-size: 14px; }
    .md-node { background-color: #b71c1c; color: white; padding: 10px; border-radius: 5px; margin-top: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CALCULATION ENGINE
# ==========================================
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_final_v57")

KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
# Unified keys for the dictionary
KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_varga_pos(deg, div):
    if div == 1: return int(deg/30)
    if div == 9: return (([0,9,6,3][int(deg/30)%4]) + int((deg%30)/3.33333)) % 12
    if div == 30:
        r = int(deg/30); dr = deg%30; is_odd = (r%2 == 0)
        if is_odd: return 0 if dr<5 else 10 if dr<10 else 8 if dr<18 else 2 if dr<25 else 6
        else: return 5 if dr<5 else 2 if dr<12 else 8 if dr<20 else 10 if dr<25 else 0
    return (int(deg/30) + int((deg%30)/(30/div))) % 12

def calculate_all(dob, tob, lat, lon):
    h_dec = tob.hour + tob.minute/60.0
    jd = swe.julday(dob.year, dob.month, dob.day, h_dec - 5.5)
    swe.set_topo(lon, lat, 0)
    ayan = swe.get_ayanamsa(jd)
    
    pos = {}
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        pos[KN_PLANETS[pid]] = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    pos[KN_PLANETS[101]], pos[KN_PLANETS[102]] = rahu, (rahu + 180) % 360
    pos["ಲಗ್ನ"] = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    
    y, m, d, h = swe.revjul(jd + 5.5/24.0)
    birth_dt = datetime.datetime(y, m, d, int(h), int((h % 1) * 60))
    return pos, jd, ayan, birth_dt

# ==========================================
# 3. WEB INTERFACE
# ==========================================
st.markdown('<div class="main-title">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("ವಿವರಗಳು")
    u_name = st.text_input("ಹೆಸರು", "ಬಳಕೆದಾರ")
    u_dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
    u_tob = st.time_input("ಸಮಯ", datetime.time(14, 43))
    loc_input = st.text_input("ಸ್ಥಳ", "Yellapur")
    u_lat = st.number_input("Lat", value=14.9800, format="%.4f")
    u_lon = st.number_input("Lon", value=74.7300, format="%.4f")
    run = st.button("ಜಾತಕ ರಚಿಸಿ", type="primary")

if run:
    pos, jd, ayan, birth_dt = calculate_all(u_dob, u_tob, u_lat, u_lon)
    t1, t2, t3, t4 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        col1, col2 = st.columns(2)
        v_div = col1.selectbox("ವರ್ಗ", options=[1, 2, 3, 9, 12, 30], format_func=lambda x: f"D{x}")
        mode = col2.radio("ಮೋಡ್", ["Rashi", "Bhava"], horizontal=True)
        
        boxes = {i: "" for i in range(12)}
        # Fix: Safely get Lagna degree
        lag_deg = pos.get("ಲಗ್ನ", 0)
        
        for p, d in pos.items():
            if mode == "Bhava" and v_div == 1:
                r_idx = (int(lag_deg/30) + int(((d-lag_deg+360)%360+15)/30))%12
            else:
                r_idx = get_varga_pos(d, v_div)
            
            cls = "hi" if p in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl-name"
            boxes[r_idx] += f'<div class="{cls}">{p}</div>'
            
        grid_map = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        h_grid = '<div class="grid-container">'
        for idx in grid_map:
            if idx is None:
                if h_grid.count('center-box') < 1: h_grid += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v_div}</div>'
            else:
                h_grid += f'<div class="box"><span class="box-lbl">{KN_RASHI[idx]}</span>{boxes[idx]}</div>'
        st.markdown(h_grid + '</div>', unsafe_allow_html=True)

    with t2:
        st.table(pd.DataFrame([{"ಗ್ರಹ": k, "ರಾಶಿ": KN_RASHI[int(v/30)], "ಅಂಶ": f"{int(v%30)}° {int((v%30*60)%60)}'"} for k,v in pos.items()]))

    with t3:
        m_lon = pos.get("ಚಂದ್ರ", 0)
        n_idx = int(m_lon / 13.333333333)
        perc = (m_lon % 13.333333333) / 13.333333333
        curr_dt = birth_dt
        start_idx = n_idx % 9
        for i in range(9):
            idx = (start_idx + i) % 9
            dur = YEARS[idx] * ((1-perc) if i==0 else 1)
            end_dt = curr_dt + datetime.timedelta(days=dur*365.25)
            st.markdown(f"<div class='md-node'>{LORDS[idx]} ಮಹಾದಶ (ಅಂತ್ಯ: {end_dt.strftime('%d-%m-%Y')})</div>", unsafe_allow_html=True)
            curr_dt = end_dt
