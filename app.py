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
    .md-node { background-color: #b71c1c; color: white; padding: 10px; border-radius: 5px; margin-top: 5px; font-weight: bold; display: flex; justify-content: space-between; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CALCULATION ENGINE (STABLE)
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v60")

KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
PLANET_IDS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 10: "ರಾಹು"}
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_varga_pos(deg, div):
    deg = deg % 360
    if div == 1: return int(deg/30)
    if div == 3: return (int(deg/30) + (int((deg%30)/10) * 4)) % 12
    if div == 9: return (([0,9,6,3][int(deg/30)%4]) + int((deg%30)/3.33333)) % 12
    if div == 12: return (int(deg/30) + int((deg%30)/2.5)) % 12
    if div == 30:
        r, dr = int(deg/30), deg%30
        if r%2 == 0: return 0 if dr<5 else 10 if dr<10 else 8 if dr<18 else 2 if dr<25 else 6
        else: return 5 if dr<5 else 2 if dr<12 else 8 if dr<20 else 10 if dr<25 else 0
    return int(deg/30)

def get_mandi(jd, lat, lon):
    try:
        res = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_RISE | swe.FLG_MOSEPH)
        sr = res[1][0]
        res_s = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_SET | swe.FLG_MOSEPH)
        ss = res_s[1][0]
        part = (ss - sr) / 8.0
        wday = int(jd + 0.5 + 1.5) % 7
        m_factors = [26, 22, 18, 14, 10, 6, 2]
        m_jd = sr + (part * m_factors[wday] / 30.0 * 3.75)
        return (swe.houses_ex(m_jd, swe.FLG_SIDEREAL | swe.FLG_MOSEPH, lat, lon, b'P')[0][0]) % 360
    except: return 0.0

# ==========================================
# 3. APP INTERFACE
# ==========================================
st.markdown('<div class="main-title">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ")
    u_name = st.text_input("ಹೆಸರು", "ಬಳಕೆದಾರ")
    u_dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
    u_tob = st.time_input("ಸಮಯ", datetime.time(14, 43))
    
    # Location Search Feature
    loc_query = st.text_input("ಸ್ಥಳ (Place)", "Yellapur")
    if st.button("ಸ್ಥಳ ಹುಡುಕಿ"):
        try:
            loc_data = geolocator.geocode(loc_query)
            if loc_data:
                st.session_state.lat, st.session_state.lon = loc_data.latitude, loc_data.longitude
                st.success(f"ಸಿಕ್ಕಿದೆ: {loc_data.address[:30]}...")
        except: st.error("ಸಂಪರ್ಕ ದೋಷ")
    
    u_lat = st.number_input("Lat", value=st.session_state.get('lat', 14.9800), format="%.4f")
    u_lon = st.number_input("Lon", value=st.session_state.get('lon', 74.7300), format="%.4f")
    
    st.markdown("---")
    run_main = st.button("ಜಾತಕ ರಚಿಸಿ", type="primary")

if run_main:
    try:
        h_dec = u_tob.hour + u_tob.minute/60.0
        jd = swe.julday(u_dob.year, u_dob.month, u_dob.day, h_dec - 5.5)
        
        # Calculate Data
        pos = {}
        for pid, pnk in PLANET_IDS.items():
            res = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_MOSEPH)
            pos[pnk] = res[0][0] % 360
        
        pos["ಕೇತು"] = (pos["ರಾಹು"] + 180) % 360
        pos["ಮಾಂದಿ"] = get_mandi(jd, u_lat, u_lon)
        res_h = swe.houses_ex(jd, swe.FLG_SIDEREAL | swe.FLG_MOSEPH, u_lat, u_lon, b'P')
        pos["ಲಗ್ನ"] = res_h[0][0] % 360

        t1, t2, t3, t4 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಉಳಿಸಿ"])

        with t1:
            v_choice = st.selectbox("ವರ್ಗ ಆಯ್ಕೆ ಮಾಡಿ", [1, 3, 9, 12, 30], format_func=lambda x: f"D{x} ವರ್ಗ")
            boxes = {i: "" for i in range(12)}
            for p, d in pos.items():
                idx = get_varga_pos(d, v_choice)
                cls = "hi" if p in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl-name"
                boxes[idx] += f'<div class="{cls}">{p}</div>'
            
            grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
            html = '<div class="grid-container">'
            for g in grid:
                if g is None:
                    if html.count('center-box') < 1: html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v_choice}</div>'
                else: html += f'<div class="box"><span class="box-lbl">{KN_RASHI[g]}</span>{boxes[g]}</div>'
            st.markdown(html + '</div>', unsafe_allow_html=True)

        with t2:
            st.subheader("ಗ್ರಹ ಸ್ಫುಟ ವಿವರ")
            df = pd.DataFrame([{"ಗ್ರಹ": k, "ರಾಶಿ": KN_RASHI[int(v/30)], "ಅಂಶ": f"{int(v%30)}° {int((v%30*60)%60)}'"} for k,v in pos.items()])
            st.table(df)

        with t3:
            m_lon = pos.get("ಚಂದ್ರ", 0)
            n_idx = int(m_lon / 13.333333333)
            perc = (m_lon % 13.333333333) / 13.333333333
            start_l = n_idx % 9
            y, m, d, hv = swe.revjul(jd + 5.5/24.0)
            dt = datetime.datetime(y, m, d)
            st.subheader(f"ವಿಂಶೋತ್ತರಿ ದಶ")
            for i in range(9):
                l_idx = (start_l + i) % 9
                dur = YEARS[l_idx] * ((1-perc) if i==0 else 1)
                dt += datetime.timedelta(days=dur*365.25)
                st.markdown(f"<div class='md-node'><span>{LORDS[l_idx]}</span> <span>{dt.strftime('%d-%m-%Y')} ರವರೆಗೆ</span></div>", unsafe_allow_html=True)

        with t4:
            st.success("ಜಾತಕ ಮಾಹಿತಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದು.")
            st.download_button("ಡೌನ್‌ಲೋಡ್ (CSV)", df.to_csv(index=False), f"{u_name}.csv")

    except Exception as e:
        st.error("Error: " + str(e))
