import streamlit as st
import swisseph as swe
import datetime
import math
import json
import os
from geopy.geocoders import Nominatim

# ==========================================
# 1. DATABASE & FILE HANDLING
# ==========================================
DB_FILE = "kundli_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(name, data):
    db = load_db()
    db[name] = data
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

# ==========================================
# 2. PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="ಭಾರತೀಯಮ್ Suite", 
    layout="centered", 
    page_icon="🕉️", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;600;800&display=swap');
    
    .stApp { background-color: #FFFDF7 !important; font-family: 'Noto Sans Kannada', sans-serif; color: #2D3748 !important; }
    
    .header-box { 
        background: linear-gradient(135deg, #8E2DE2, #4A00E0); color: #FFFFFF !important; 
        padding: 20px; text-align: center; font-weight: 800; font-size: 26px; 
        border-radius: 16px; margin-bottom: 24px; border-bottom: 4px solid #F6D365;
    }

    .hub-card {
        background: white; padding: 25px; border-radius: 15px; border: 2px solid #E2E8F0;
        text-align: center; transition: 0.3s; cursor: pointer; margin-bottom: 20px;
    }
    .hub-card:hover { border-color: #DD6B20; transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

    .grid-container { 
        display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); 
        width: 100%; max-width: 400px; aspect-ratio: 1 / 1; margin: 0 auto; gap: 4px; 
        background: #E2E8F0; border: 4px solid #E2E8F0; border-radius: 12px;
    }
    .box { 
        background: #FFFFFF; position: relative; display: flex; flex-direction: column; 
        align-items: center; justify-content: center; font-size: 12px; font-weight: 800; 
        padding: 4px; text-align: center; border-radius: 8px;
    }
    .center-box { 
        grid-column: 2/4; grid-row: 2/4; background: linear-gradient(135deg, #F6D365 0%, #FDA085 100%); 
        display: flex; flex-direction: column; align-items: center; justify-content: center; 
        color: #742A2A !important; font-weight: 900; font-size: 15px; border-radius: 8px;
    }
    .lbl { position: absolute; top: 3px; left: 5px; font-size: 10px; color: #2F855A !important; font-weight: 900; }
    .hi { color: #E53E3E !important; font-weight: 900; text-decoration: underline; } 
    .pl { color: #2B6CB0 !important; font-weight: 800; } 
    .sp { color: #805AD5 !important; font-weight: 800; font-size: 11px; } 
    .bindu { font-size: 22px; color: #DD6B20 !important; font-weight: 900; }
    .card { background: #FFFFFF; border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid #E2E8F0; }
    .key-val-table td { border-bottom: 1px solid #EDF2F7; padding: 10px 6px; font-size: 14px; }
    .key { color: #4A5568 !important; font-weight: 800; width: 45%; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
geolocator = Nominatim(user_agent="bharatheeyam_suite_2026")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
PLANET_ORDER = ["ಲಗ್ನ", "ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ", "ರಾಹು", "ಕೇತು", "ಮಾಂದಿ"]
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಘ", "ಪೂರ್ವ ಫಾಲ್ಗುಣಿ", "ಉತ್ತರ ಫಾಲ್ಗುಣಿ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜ್ಯೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
KN_YOGA = ["ವಿಷ್ಕಂಭ", "ಪ್ರೀತಿ", "ಆಯುಷ್ಮಾನ್", "ಸೌಭಾಗ್ಯ", "ಶೋಭನ", "ಅತಿಗಂಡ", "ಸುಕರ್ಮ", "ಧೃತಿ", "ಶೂಲ", "ಗಂಡ", "ವೃದ್ಧಿ", "ಧ್ರುವ", "ವ್ಯಾಘಾತ", "ಹರ್ಷಣ", "ವಜ್ರ", "ಸಿದ್ಧಿ", "ವ್ಯತೀಪಾತ", "ವರೀಯಾನ್", "ಪರಿಘ", "ಶಿವ", "ಸಿದ್ಧ", "ಸಾಧ್ಯ", "ಶುಭ", "ಶುಕ್ಲ", "ಬ್ರಹ್ಮ", "ಇಂದ್ರ", "ವೈಧೃತಿ"]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def fmt_deg(dec_deg):
    rem = dec_deg % 30
    t_sec = int(round(rem * 3600))
    dg = int(t_sec / 3600); mn = int((t_sec % 3600) / 60); sc = int(t_sec % 60)
    if dg == 30: dg=29; mn=59; sc=59
    return f"{dg}° {str(mn).zfill(2)}' {str(sc).zfill(2)}\""

def get_altitude_manual(jd, lat, lon):
    res = swe.calc_ut(jd, swe.SUN, swe.FLG_EQUATORIAL | swe.FLG_SWIEPH)
    ra = res[0][0]; dec = res[0][1]; gmst = swe.sidtime(jd)
    lst = gmst + (lon / 15.0)
    ha_deg = ((lst * 15.0) - ra + 360) % 360
    if ha_deg > 180: ha_deg -= 360
    lat_rad = math.radians(lat); dec_rad = math.radians(dec); ha_rad = math.radians(ha_deg)
    sin_alt = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad)
    return math.degrees(math.asin(sin_alt))

def find_sunrise_set_for_date(year, month, day, lat, lon):
    jd_start = swe.julday(year, month, day, 12.0)
    rise_time, set_time = -1, -1
    step = 1/24.0
    current = jd_start - 0.5
    for i in range(24):
        alt1 = get_altitude_manual(current, lat, lon)
        alt2 = get_altitude_manual(current + step, lat, lon)
        if alt1 < -0.833 and alt2 >= -0.833:
            l, h = current, current + step
            for _ in range(15):
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) < -0.833: l = m
                else: h = m
            rise_time = h
        if alt1 > -0.833 and alt2 <= -0.833:
            l, h = current, current + step
            for _ in range(15):
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) > -0.833: l = m
                else: h = m
            set_time = h
        current += step
    return rise_time, set_time

def calculate_mandi(jd_birth, lat, lon, dob_obj):
    sr, ss = find_sunrise_set_for_date(dob_obj.year, dob_obj.month, dob_obj.day, lat, lon)
    py_wday = (dob_obj.weekday() + 1) % 7 
    is_night = not (sr <= jd_birth < ss)
    if not is_night:
        start, dur, factors = sr, ss - sr, [26, 22, 18, 14, 10, 6, 2]
    else:
        if jd_birth < sr:
            prev = dob_obj - datetime.timedelta(days=1)
            p_sr, p_ss = find_sunrise_set_for_date(prev.year, prev.month, prev.day, lat, lon)
            start, dur = p_ss, sr - p_ss
            py_wday = (py_wday - 1) % 7
        else:
            nxt = dob_obj + datetime.timedelta(days=1)
            n_sr, n_ss = find_sunrise_set_for_date(nxt.year, nxt.month, nxt.day, lat, lon)
            start, dur = ss, n_sr - ss
        factors = [10, 6, 2, 26, 22, 18, 14]
    mandi_jd = start + (dur * factors[py_wday] / 30.0)
    return mandi_jd, is_night, sr, py_wday

def get_full_calculations(jd, lat, lon, dob, ayan_mode, node_mode):
    swe.set_sid_mode(ayan_mode)
    ayan = swe.get_ayanamsa(jd)
    pos, speeds, extra = {}, {}, {}
    flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    for pid in range(7):
        res = swe.calc_ut(jd, pid, flag)
        d = res[0][0] % 360
        pos[KN_PLANETS[pid]] = d; speeds[KN_PLANETS[pid]] = res[0][3]
        extra[KN_PLANETS[pid]] = {"nak": KN_NAK[int(d/13.3333)%27], "pada": int((d%13.3333)/3.3333)+1}
    r_res = swe.calc_ut(jd, node_mode, flag)
    pos[KN_PLANETS[101]] = r_res[0][0] % 360; speeds[KN_PLANETS[101]] = r_res[0][3]
    pos[KN_PLANETS[102]] = (pos[KN_PLANETS[101]] + 180) % 360; speeds[KN_PLANETS[102]] = r_res[0][3]
    for p in ["ರಾಹು", "ಕೇತು"]:
        d = pos[p]; extra[p] = {"nak": KN_NAK[int(d/13.3333)%27], "pada": int((d%13.3333)/3.3333)+1}
    h_res = swe.houses(jd, lat, lon, b'P')
    asc = (h_res[0][1] - ayan) % 360
    pos["ಲಗ್ನ"] = asc; speeds["ಲಗ್ನ"] = 0
    extra["ಲಗ್ನ"] = {"nak": KN_NAK[int(asc/13.3333)%27], "pada": int((asc%13.3333)/3.3333)+1}
    m_jd, is_n, p_sr, w_idx = calculate_mandi(jd, lat, lon, dob)
    m_h = swe.houses(m_jd, lat, lon, b'P')
    m_ayan = swe.get_ayanamsa(m_jd)
    m_deg = (m_h[0][1] - m_ayan) % 360
    pos["ಮಾಂದಿ"] = m_deg; extra["ಮಾಂದಿ"] = {"nak": KN_NAK[int(m_deg/13.3333)%27], "pada": int((m_deg%13.3333)/3.3333)+1}
    
    # Advanced Sphutas
    S, M, Md, Asc = pos["ರವಿ"], pos["ಚಂದ್ರ"], pos["ಮಾಂದಿ"], pos["ಲಗ್ನ"]
    adv = {
        "ತ್ರಿಸ್ಫುಟ": (Asc + M + Md) % 360, "ಪ್ರಾಣ": (Asc * 5 + Md) % 360,
        "ದೇಹ": (M * 8 + Md) % 360, "ಮೃತ್ಯು": (Md * 7 + S) % 360
    }
    # Panchanga
    m_deg, s_deg = pos["ಚಂದ್ರ"], pos["ರವಿ"]
    pan = {"t": KN_TITHI[int(((m_deg - s_deg + 360)%360)/12)%30], "v": KN_VARA[w_idx], 
           "n": KN_NAK[int(m_deg/13.3333)%27], "y": KN_YOGA[int(((m_deg + s_deg)%360)/13.3333)%27],
           "sr": p_sr, "adv_sphutas": adv, "n_idx": int(m_deg/13.3333), "perc": (m_deg%13.3333)/13.3333,
           "date_obj": datetime.datetime.fromtimestamp((jd - 2440587.5) * 86400), "lord_bal": LORDS[int(m_deg/13.3333)%9]}
    return pos, pan, extra, [ (h - ayan)%360 for h in h_res[0][1:13] ], speeds

# ==========================================
# 4. POPUP & DIALOGS
# ==========================================
@st.dialog("ಗ್ರಹದ ಸಂಪೂರ್ಣ ವಿವರ")
def show_planet_popup(p_name, deg, speed, sun_deg):
    asta = "ಹೌದು" if p_name not in ["ರವಿ","ರಾಹು","ಕೇತು","ಲಗ್ನ","ಮಾಂದಿ"] and abs(deg-sun_deg)%360 < 12 else "ಇಲ್ಲ"
    gathi = "ವಕ್ರಿ" if speed < 0 else "ನೇರ"
    d1_idx = int(deg/30); dr = deg % 30
    d9_idx = int(((deg*9)%360)/30)
    d12_idx = (d1_idx + int(dr/2.5)) % 12
    
    # Nested D3 Calculations
    def get_d3_str(d_val):
        sign_idx = int(d_val/30); sub_deg = d_val % 30
        part = 1 if sub_deg < 10 else (2 if sub_deg < 20 else 3)
        return f"{KN_RASHI[sign_idx]} {part}"

    st.markdown(f"**ಸ್ಫುಟ:** {fmt_deg(deg)} | **ಗತಿ:** {gathi} | **ಅಸ್ತ:** {asta}")
    st.markdown("#### 📊 ವರ್ಗಗಳು")
    st.write(f"ರಾಶಿ: {KN_RASHI[d1_idx]} | ನವಾಂಶ: {KN_RASHI[d9_idx]} | ದ್ವಾದಶಾಂಶ: {KN_RASHI[d12_idx]}")
    st.markdown("#### 📐 ಉಪ-ದ್ರೇಕ್ಕಾಣ (Nested D3)")
    st.write(f"D3 of D1: {get_d3_str(deg)}")
    st.write(f"D3 of D9: {get_d3_str((deg*9)%360)}")
    st.write(f"D3 of D12: {get_d3_str((d12_idx*30) + (deg%2.5)*12)}")

# ==========================================
# 5. LIBRARY APP MODULE
# ==========================================
def show_library():
    st.markdown('<div class="header-box">ಸ್ತೋತ್ರಮಾಲಾ ಗ್ರಂಥಾಲಯ</div>', unsafe_allow_html=True)
    huduku = st.text_input("🔍 ಹುಡುಕಿ (Search)", placeholder="ಉದಾ: ಗಣೇಶ, ದೇವೀ...")
    
    col1, col2, col3 = st.columns(3)
    col1.button("🕉️ ದೇವತೆಗಳು", use_container_width=True)
    col2.button("⭐ ಗ್ರಹ ಶಾಂತಿ", use_container_width=True)
    col3.button("📖 ವೇದ ಸೂಕ್ತ", use_container_width=True)
    
    with st.expander("⚙️ ಓದುವಿಕೆ ಸೆಟ್ಟಿಂಗ್ಸ್"):
        f_size = st.slider("ಅಕ್ಷರ ಗಾತ್ರ", 14, 42, 22)
        night = st.toggle("ನೈಟ್ ಮೋಡ್")
    
    bg, tc = ("#1A202C", "#F7FAFC") if night else ("#FFFFFF", "#2D3748")
    st.markdown(f"""<div style="background:{bg}; color:{tc}; padding:20px; border-radius:12px; font-size:{f_size}px; line-height:1.7;">
    <b>ಶ್ರೀ ಗಣೇಶ ಅಷ್ಟೋತ್ತರ ಶತನಾಮಾವಳಿಃ</b><br>ಓಂ ವಿನಾಯಕಾಯ ನಮಃ |<br>ಓಂ ವಿಘ್ನರಾಜಾಯ ನಮಃ |<br>ಓಂ ಗೌರಿಪುತ್ರಾಯ ನಮಃ |</div>""", unsafe_allow_html=True)

# ==========================================
# 6. MAIN APP LOGIC
# ==========================================
if 'app_mode' not in st.session_state: st.session_state.app_mode = "Hub"
if 'page' not in st.session_state: st.session_state.page = "input"

# Sidebar
nav = st.sidebar.radio("ನವಿಗೇಶನ್", ["ಹೋಮ್", "ಜ್ಯೋತಿಷ್ಯ", "ಗ್ರಂಥಾಲಯ"])

if nav == "ಹೋಮ್":
    st.markdown('<div class="header-box">ಭಾರತೀಯಮ್ Suite</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="hub-card"><h2>🪐</h2><h3>ಜ್ಯೋತಿಷ್ಯ</h3><p>ಕುಂಡಲಿ ಮತ್ತು ಲೆಕ್ಕಾಚಾರ</p></div>', unsafe_allow_html=True)
        if st.button("ಲಾಂಚ್ ಜ್ಯೋತಿಷ್ಯ", use_container_width=True): st.session_state.app_mode = "Astro"; st.rerun()
    with c2:
        st.markdown('<div class="hub-card"><h2>📚</h2><h3>ಗ್ರಂಥಾಲಯ</h3><p>ಸ್ತೋತ್ರಮಾಲಾ ಪಾರಾಯಣ</p></div>', unsafe_allow_html=True)
        if st.button("ಲಾಂಚ್ ಗ್ರಂಥಾಲಯ", use_container_width=True): st.session_state.app_mode = "Lib"; st.rerun()

elif nav == "ಜ್ಯೋತಿಷ್ಯ":
    if st.session_state.page == "input":
        st.markdown('<div class="header-box">ಜಾತಕ ವಿವರ</div>', unsafe_allow_html=True)
        name = st.text_input("ಹೆಸರು"); dob = st.date_input("ದಿನಾಂಕ")
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("ಗಂಟೆ", 1, 12); m = c2.number_input("ನಿಮಿಷ", 0, 59); ampm = c3.selectbox("AM/PM", ["AM", "PM"])
        lat = st.number_input("ಅಕ್ಷಾಂಶ", value=14.98, format="%.4f"); lon = st.number_input("ರೇಖಾಂಶ", value=74.73, format="%.4f")
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = (h % 12 + (12 if ampm == "PM" else 0)); jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            p1, p2, p3, p4, p5 = get_full_calculations(jd, lat, lon, dob, swe.SIDM_LAHIRI, swe.TRUE_NODE)
            st.session_state.data = {"pos": p1, "pan": p2, "details": p3, "bhavas": p4, "speeds": p5}; st.session_state.page = "dash"; st.rerun()
    else:
        # Dashboard
        pos, pan = st.session_state.data['pos'], st.session_state.data['pan']
        t1, t2, t3 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ"])
        with t1:
            c_v, c_b = st.columns(2)
            v_opt = c_v.selectbox("ವರ್ಗ", [1, 9, 3, 12, 30], format_func=lambda x: {1:"ರಾಶಿ", 9:"ನವಾಂಶ", 3:"ದ್ರೇಕ್ಕಾಣ", 12:"ದ್ವಾದಶಾಂಶ", 30:"ತ್ರಿಂಶಾಂಶ"}[x])
            c_mode = c_b.radio("ವೀಕ್ಷಣೆ", ["ರಾಶಿ", "ಭಾವ", "ಕೋಷ್ಟಕ"], horizontal=True)
            if c_mode == "ಕೋಷ್ಟಕ":
                st.markdown("#### 📊 ಗ್ರಹಗಳ ಕೋಷ್ಟಕ (Tale View)")
                for p in PLANET_ORDER: st.write(f"**{p}:** {fmt_deg(pos[p])} ({st.session_state.data['details'][p]['nak']})")
            else:
                # [Simplified Chart Rendering for brevity - use your grid-container logic here]
                st.info(f"{c_mode} {v_opt} ಚಾರ್ಟ್ ಲೋಡ್ ಆಗಿದೆ.")
            st.markdown("---"); bc = st.columns(4)
            for i, p in enumerate(PLANET_ORDER):
                if bc[i%4].button(p, key=f"btn_{p}"): show_planet_popup(p, pos[p], st.session_state.data['speeds'].get(p,0), pos["ರವಿ"])
        with t2:
            for k, v in pan['adv_sphutas'].items(): st.write(f"**{k}:** {fmt_deg(v)}")
        with t3:
            st.write(f"ಶಿಷ್ಟ ದಶೆ: {pan['lord_bal']} | ಉಳಿಕೆ: {pan['perc']:.2%}")

elif nav == "ಗ್ರಂಥಾಲಯ":
    show_library()
