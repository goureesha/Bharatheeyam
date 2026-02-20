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
# 2. PAGE CONFIG & MULTI-COLOR THEME
# ==========================================
st.set_page_config(
    page_title="ಭಾರತೀಯಮ್", 
    layout="centered", 
    page_icon="🕉️", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;600;800&display=swap');
    
    .stApp { 
        background-color: #FFFDF7 !important; 
        font-family: 'Noto Sans Kannada', sans-serif; 
        color: #2D3748 !important; 
    }
    
    .header-box { 
        background: linear-gradient(135deg, #8E2DE2, #4A00E0); 
        color: #FFFFFF !important; 
        padding: 20px; 
        text-align: center; 
        font-weight: 800; 
        font-size: 26px; 
        border-radius: 16px; 
        margin-bottom: 24px; 
        box-shadow: 0 4px 15px rgba(74, 0, 224, 0.3); 
        border-bottom: 4px solid #F6D365; 
        letter-spacing: 1px;
    }
    
    div[data-testid="stInput"] { 
        background-color: #FFFFFF; 
        border-radius: 10px; 
    }
    
    .stButton>button[kind="primary"] { 
        background: linear-gradient(135deg, #DD6B20, #C05621) !important;
        color: white !important; 
        font-weight: 800; 
        border-radius: 12px; 
        border: none; 
        padding: 12px; 
        box-shadow: 0 4px 10px rgba(221, 107, 32, 0.3);
    }
    
    .stButton>button[kind="secondary"] { 
        background-color: #E6FFFA !important; 
        color: #319795 !important; 
        font-weight: 800; 
        border: 2px solid #319795 !important; 
        border-radius: 12px; 
    }
    
    div[data-testid="stTabs"] button[aria-selected="false"] p { 
        color: #718096 !important; 
        font-weight: 600 !important; 
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p { 
        color: #047857 !important; 
        font-weight: 800 !important; 
    }
    div[data-testid="stTabs"] button[aria-selected="true"] { 
        border-bottom: 3px solid #047857 !important; 
    }
    
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(4, 1fr); 
        grid-template-rows: repeat(4, 1fr); 
        width: 100%; max-width: 400px; 
        aspect-ratio: 1 / 1; 
        margin: 0 auto; gap: 4px; 
        background: #E2E8F0; 
        border: 4px solid #E2E8F0; 
        border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .box { 
        background: #FFFFFF; 
        position: relative; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: flex-start; 
        font-size: 14px; 
        font-weight: 800; 
        padding: 15px 2px 2px 2px; 
        text-align: center; 
        border-radius: 8px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.02);
        overflow-y: auto; 
    }
    
    .box::-webkit-scrollbar { width: 3px; }
    .box::-webkit-scrollbar-track { background: transparent; }
    .box::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 10px; }
    
    .center-box { 
        grid-column: 2/4; 
        grid-row: 2/4; 
        background: linear-gradient(135deg, #F6D365 0%, #FDA085 100%); 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        color: #742A2A !important; 
        font-weight: 900; 
        text-align: center; 
        font-size: 16px; 
        border-radius: 8px;
        border: 2px solid #FFFFFF;
    }
    
    .lbl { 
        position: absolute; top: 3px; left: 5px; 
        font-size: 10px; color: #2F855A !important; 
        font-weight: 900; 
    }
    
    .hi { color: #E53E3E !important; font-weight: 900; text-decoration: underline; white-space: nowrap; font-size: 15px; } 
    .pl { color: #2B6CB0 !important; font-weight: 800; white-space: nowrap; font-size: 15px; } 
    .sp { color: #805AD5 !important; font-weight: 800; white-space: nowrap; font-size: 13px; } 
    .bindu { font-size: 22px; color: #DD6B20 !important; font-weight: 900; }
    
    .card { 
        background: #FFFFFF; border-radius: 16px; padding: 20px; 
        margin-bottom: 16px; border: 1px solid #E2E8F0; 
        box-shadow: 0 4px 16px rgba(0,0,0,0.03); 
    }
    .key { color: #4A5568 !important; font-weight: 800; width: 45%; }
    .key-val-table td { 
        border-bottom: 1px solid #EDF2F7; 
        padding: 12px 6px; color: #2D3748 !important; 
        font-size: 14px;
    }
    
    .bav-table th {
        background-color: #EDF2F7;
        color: #2D3748;
        padding: 6px 2px;
        font-size: 11px;
    }
    .bav-table td {
        padding: 8px 2px;
        font-size: 12px;
        border-bottom: 1px solid #EDF2F7;
    }
    
    details { 
        margin-bottom: 8px; border: 1px solid #EDF2F7; 
        border-radius: 10px; overflow: hidden; background: #FFFFFF; 
    }
    summary { 
        padding: 14px; font-size: 14px; 
        border-bottom: 1px solid #EDF2F7; color: #2D3748 !important; 
        cursor: pointer;
    }
    
    .md-node { 
        background: linear-gradient(135deg, #FF9933, #DD6B20) !important; 
        color: #FFFFFF !important; 
        font-weight: 800; 
    }
    .md-node span { color: white !important; }
    .ad-node { 
        background: #FFFDF7 !important; color: #C05621 !important; 
        font-weight: 800; border-left: 4px solid #FF9933; 
    }
    .ad-node span { color: #C05621 !important; }
    .pd-node { 
        background: #FFFFFF !important; color: #319795 !important; 
        font-weight: 700; border-left: 4px solid #81E6D9; 
    }
    .pd-node span { color: #319795 !important; }
    .date-label { font-size: 12px; opacity: 0.9; float: right; font-weight: normal; }

    @media (max-width: 600px) {
        .grid-container { gap: 2px; border-width: 2px; }
        .box { padding: 14px 2px 2px 2px; font-size: 12px; }
        .center-box { font-size: 14px; }
        .lbl { font-size: 9px; top: 1px; left: 2px; }
        .hi, .pl { font-size: 13px; line-height: 1.3; letter-spacing: 0px; }
        .sp { font-size: 12px; line-height: 1.3; letter-spacing: 0px; font-weight: 800;}
        .header-box { font-size: 20px; padding: 15px; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
geolocator = Nominatim(user_agent="bharatheeyam_app_final")

KN_PLANETS = {
    0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 
    5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", 
    "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"
}

PLANET_ORDER = ["ಲಗ್ನ", "ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ", "ರಾಹು", "ಕೇತು", "ಮಾಂದಿ"]

KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = [
    "ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ",
    "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", 
    "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", 
    "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"
]
KN_NAK = [
    "ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಘ", "ಪೂರ್ವ ಫಾಲ್ಗುಣಿ",
    "ಉತ್ತರ ಫಾಲ್ಗುಣಿ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜ್ಯೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ",
    "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"
]
KN_YOGA = [
    "ವಿಷ್ಕಂಭ", "ಪ್ರೀತಿ", "ಆಯುಷ್ಮಾನ್", "ಸೌಭಾಗ್ಯ", "ಶೋಭನ", "ಅತಿಗಂಡ", "ಸುಕರ್ಮ", "ಧೃತಿ", "ಶೂಲ", "ಗಂಡ",
    "ವೃದ್ಧಿ", "ಧ್ರುವ", "ವ್ಯಾಘಾತ", "ಹರ್ಷಣ", "ವಜ್ರ", "ಸಿದ್ಧಿ", "ವ್ಯತೀಪಾತ", "ವರೀಯಾನ್", "ಪರಿಘ", "ಶಿವ",
    "ಸಿದ್ಧ", "ಸಾಧ್ಯ", "ಶುಭ", "ಶುಕ್ಲ", "ಬ್ರಹ್ಮ", "ಇಂದ್ರ", "ವೈಧೃತಿ"
]
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

def find_sunrise_set_for_date(year, month, day, lat, lon):
    jd_start = swe.julday(year, month, day, 0.0) 
    rise_time, set_time = -1, -1
    step = 1/24.0
    current = jd_start - 0.3 
    for i in range(30): 
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

def find_nak_limit(jd, target_deg):
    low, high = jd - 1.2, jd + 1.2
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
    if v == 60: g, v = g + 1, 0
    return str(g) + "." + str(v).zfill(2)

def fmt_deg(dec_deg):
    rem = dec_deg % 30
    t_sec = int(round(rem * 3600))
    dg, mn, sc = int(t_sec / 3600), int((t_sec % 3600) / 60), int(t_sec % 60)
    if dg == 30: dg, mn, sc = 29, 59, 59
    return f"{dg}° {str(mn).zfill(2)}' {str(sc).zfill(2)}\""

def calculate_ashtakavarga(positions):
    P_KEYS = ["ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ", "ಲಗ್ನ"]
    r_idx = {k: int(positions[k] / 30) for k in P_KEYS}
    sav = [0] * 12
    bav = {p: [0]*12 for p in ["ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ"]}
    BAV_RULES = {
        "ರವಿ": [[1,2,4,7,8,9,10,11], [3,6,10,11], [1,2,4,7,8,9,10,11], [3,5,6,9,10,11,12], [5,6,9,11], [6,7,12], [1,2,4,7,8,9,10,11], [3,4,6,10,11,12]],
        "ಚಂದ್ರ": [[3,6,7,8,10,11], [1,3,6,7,10,11], [2,3,5,6,9,10,11], [1,3,4,5,7,8,10,11], [1,4,7,8,10,11,12], [3,4,5,7,9,10,11], [3,5,6,11], [3,6,10,11]],
        "ಕುಜ": [[3,5,6,10,11], [3,6,11], [1,2,4,7,8,10,11], [3,5,6,11], [6,10,11,12], [6,8,11,12], [1,4,7,8,9,10,11], [1,3,6,10,11]],
        "ಬುಧ": [[5,6,9,11,12], [2,4,6,8,10,11], [1,2,4,7,8,9,10,11], [1,3,5,6,9,10,11,12], [6,8,11,12], [1,2,3,4,5,8,9,11], [1,2,4,7,8,9,10,11], [1,2,4,6,8,10,11]],
        "ಗುರು": [[1,2,3,4,7,8,9,10,11], [2,5,7,9,11], [1,2,4,7,8,10,11], [1,2,4,5,6,9,10,11], [1,2,3,4,7,8,10,11], [2,5,6,9,10,11], [3,5,6,12], [1,2,4,5,6,9,10,11]],
        "ಶುಕ್ರ": [[8,11,12], [1,2,3,4,5,8,9,11,12], [3,5,6,9,11,12], [3,5,6,9,11], [5,8,9,10,11], [1,2,3,4,5,8,9,10,11], [3,4,5,8,9,10,11], [1,2,3,4,5,8,9,11]],
        "ಶನಿ": [[1,2,4,7,8,10,11], [3,6,11], [3,5,6,10,11,12], [6,8,9,10,11,12], [5,6,11,12], [6,11,12], [3,5,6,11], [1,3,4,6,10,11]]
    }
    for target in ["ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ"]:
        rules = BAV_RULES[target]
        for ref_idx, ref_planet in enumerate(P_KEYS):
            for h in rules[ref_idx]:
                sign_idx = (r_idx[ref_planet] + h - 1) % 12
                bav[target][sign_idx] += 1
                sav[sign_idx] += 1
    return sav, bav

def calculate_mandi(jd_birth, lat, lon, dob_obj):
    sr_civil, ss_civil = find_sunrise_set_for_date(dob_obj.year, dob_obj.month, dob_obj.day, lat, lon)
    civil_weekday_idx = (dob_obj.weekday() + 1) % 7 
    is_night = not (jd_birth >= sr_civil and jd_birth < ss_civil)
        
    if not is_night:
        vedic_wday, panch_sr, start_base, duration = civil_weekday_idx, sr_civil, sr_civil, ss_civil - sr_civil
    else:
        if jd_birth < sr_civil:
            vedic_wday = (civil_weekday_idx - 1) % 7
            prev_d = dob_obj - datetime.timedelta(days=1)
            p_sr, p_ss = find_sunrise_set_for_date(prev_d.year, prev_d.month, prev_d.day, lat, lon)
            start_base, duration, panch_sr = p_ss, sr_civil - p_ss, p_sr
        else:
            vedic_wday = civil_weekday_idx
            next_d = dob_obj + datetime.timedelta(days=1)
            n_sr, n_ss = find_sunrise_set_for_date(next_d.year, next_d.month, next_d.day, lat, lon)
            start_base, duration, panch_sr = ss_civil, n_sr - ss_civil, sr_civil

    factors = [10, 6, 2, 26, 22, 18, 14] if is_night else [26, 22, 18, 14, 10, 6, 2]
    mandi_jd = start_base + (duration * factors[vedic_wday] / 30.0)
    return mandi_jd, is_night, panch_sr, vedic_wday, start_base

def get_full_calculations(jd_birth, lat, lon, dob_obj, ayan_mode, node_mode):
    swe.set_sid_mode(ayan_mode)
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd_birth)
    positions, speeds, extra_details = {}, {}, {}
    
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        res = swe.calc_ut(jd_birth, pid, flag)
        deg = res[0][0] % 360
        positions[KN_PLANETS[pid]], speeds[KN_PLANETS[pid]] = deg, res[0][3]
        extra_details[KN_PLANETS[pid]] = {"nak": KN_NAK[int(deg / 13.333333333) % 27], "pada": int((deg % 13.333333333) / 3.333333333) + 1}

    rahu_res = swe.calc_ut(jd_birth, node_mode, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
    rahu_deg = rahu_res[0][0] % 360
    positions[KN_PLANETS[101]], speeds[KN_PLANETS[101]] = rahu_deg, rahu_res[0][3]
    positions[KN_PLANETS[102]], speeds[KN_PLANETS[102]] = (rahu_deg + 180) % 360, rahu_res[0][3]
    
    for p, d in [(KN_PLANETS[101], rahu_deg), (KN_PLANETS[102], (rahu_deg + 180) % 360)]:
        extra_details[p] = {"nak": KN_NAK[int(d / 13.333333333) % 27], "pada": int((d % 13.333333333) / 3.333333333) + 1}

    cusps = swe.houses(jd_birth, float(lat), float(lon), b'P')[0]
    bhava_sphutas = [(cusps[i] - ayan) % 360 for i in range(1, 13)] if len(cusps) == 13 else [(cusps[i] - ayan) % 360 for i in range(0, 12)]
    asc_deg = bhava_sphutas[0]

    positions[KN_PLANETS["Lagna"]], speeds[KN_PLANETS["Lagna"]] = asc_deg, 0
    extra_details[KN_PLANETS["Lagna"]] = {"nak": KN_NAK[int(asc_deg / 13.333333333) % 27], "pada": int((asc_deg % 13.333333333) / 3.333333333) + 1}

    mandi_time_jd, _, panch_sr, w_idx, _ = calculate_mandi(jd_birth, lat, lon, dob_obj)
    mandi_deg = (swe.houses(mandi_time_jd, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mandi_time_jd)) % 360
    positions[KN_PLANETS["Ma"]], speeds[KN_PLANETS["Ma"]] = mandi_deg, 0
    extra_details[KN_PLANETS["Ma"]] = {"nak": KN_NAK[int(mandi_deg / 13.333333333) % 27], "pada": int((mandi_deg % 13.333333333) / 3.333333333) + 1}

    sun_deg, moon_deg, jup_deg, ven_deg, mars_deg, rahu_deg = positions["ರವಿ"], positions["ಚಂದ್ರ"], positions["ಗುರು"], positions["ಶುಕ್ರ"], positions["ಕುಜ"], positions[KN_PLANETS[101]]
    
    dhooma = (sun_deg + 133.333333) % 360
    vyatipata = (360 - dhooma) % 360
    parivesha = (vyatipata + 180) % 360
    indrachapa = (360 - parivesha) % 360
    upaketu = (indrachapa + 16.666667) % 360
    
    trisphuta = (asc_deg + moon_deg + mandi_deg) % 360
    chatusphuta = (trisphuta + sun_deg) % 360
    prana_sphuta = ((asc_deg * 5) + mandi_deg) % 360
    deha_sphuta = ((moon_deg * 8) + mandi_deg) % 360
    mrityu_sphuta = ((mandi_deg * 7) + sun_deg) % 360

    adv_sphutas = {
        "ಧೂಮ": dhooma, "ವ್ಯತೀಪಾತ": vyatipata, "ಪರಿವೇಷ": parivesha, "ಇಂದ್ರಚಾಪ": indrachapa, "ಉಪಕೇತು": upaketu,
        "ಭೃಗು ಬಿ.": (moon_deg + rahu_deg) / 2, "ಬೀಜ": (sun_deg + ven_deg + jup_deg) % 360, "ಕ್ಷೇತ್ರ": (moon_deg + mars_deg + jup_deg) % 360,
        "ಯೋಗಿ": (sun_deg + moon_deg + 93.333333) % 360, "ತ್ರಿಸ್ಫುಟ": trisphuta, "ಚತುಃಸ್ಫುಟ": chatusphuta, 
        "ಪಂಚಸ್ಫುಟ": (chatusphuta + rahu_deg) % 360, "ಪ್ರಾಣ": prana_sphuta, "ದೇಹ": deha_sphuta, "ಮೃತ್ಯು": mrityu_sphuta, 
        "ಸೂಕ್ಷ್ಮ ತ್ರಿ.": (prana_sphuta + deha_sphuta + mrityu_sphuta) % 360
    }

    t_idx = int(((moon_deg - sun_deg + 360) % 360) / 12)
    n_idx = int(moon_deg / 13.333333333)
    k_idx = int(((moon_deg - sun_deg + 360) % 360) / 6)
    k_name = "ಕಿಂಸ್ತುಘ್ನ" if k_idx == 0 else ("ಶಕುನಿ" if k_idx == 57 else ("ಚತುಷ್ಪಾದ" if k_idx == 58 else ("ನಾಗ" if k_idx == 59 else ["ಬವ", "ಬಾಲವ", "ಕೌಲವ", "ತೈತಿಲ", "ಗರ", "ವಣಿಜ", "ಭದ್ರಾ (ವಿಷ್ಟಿ)"][(k_idx - 1) % 7])))
        
    js = find_nak_limit(jd_birth, n_idx * 13.333333333)
    je = find_nak_limit(jd_birth, (n_idx + 1) * 13.333333333)
    perc = (moon_deg % 13.333333333) / 13.333333333
    sav_bindus, bav_bindus = calculate_ashtakavarga(positions)
    
    pan = {
        "t": KN_TITHI[min(t_idx, 29)], "v": KN_VARA[w_idx], "n": KN_NAK[n_idx % 27],
        "y": KN_YOGA[int(((moon_deg + sun_deg) % 360) / 13.333333333)], "k": k_name, "r": KN_RASHI[int(moon_deg / 30)],
        "udayadi": fmt_ghati((jd_birth - panch_sr) * 60), "gata": fmt_ghati((jd_birth - js) * 60), 
        "parama": fmt_ghati((je - js) * 60), "rem": fmt_ghati((je - jd_birth) * 60),
        "d_bal": f"{int(YEARS[n_idx % 9] * (1 - perc))}ವ {int(((YEARS[n_idx % 9] * (1 - perc))%1)*12)}ತಿ",
        "n_idx": n_idx, "perc": perc, "date_obj": datetime.datetime.fromtimestamp((jd_birth - 2440587.5) * 86400),
        "lord_bal": LORDS[n_idx%9], "sav_bindus": sav_bindus, "bav_bindus": bav_bindus, "adv_sphutas": adv_sphutas
    }
    return positions, pan, extra_details, bhava_sphutas, speeds

# ==========================================
# 5. DIALOG UI FOR PLANET POPUP
# ==========================================
@st.dialog("ಗ್ರಹದ ಸಂಪೂರ್ಣ ವಿವರ")
def show_planet_popup(p_name, deg, speed, sun_deg):
    is_asta = False
    gathi_str = "ಅನ್ವಯಿಸುವುದಿಲ್ಲ"
    
    if p_name not in ["ರವಿ", "ರಾಹು", "ಕೇತು", "ಲಗ್ನ", "ಮಾಂದಿ"]:
        diff = abs(deg - sun_deg)
        if diff > 180: diff = 360 - diff
        if diff <= {"ಚಂದ್ರ": 12, "ಕುಜ": 17, "ಬುಧ": 14, "ಗುರು": 11, "ಶುಕ್ರ": 10, "ಶನಿ": 15}.get(p_name, 0): is_asta = True
        gathi_str = "ನೇರ" if p_name == "ಚಂದ್ರ" or speed >= 0 else "ವಕ್ರಿ"
    elif p_name in ["ರಾಹು", "ಕೇತು"]: gathi_str = "ವಕ್ರಿ"
    elif p_name == "ರವಿ": gathi_str = "ನೇರ"
        
    asta_text = "ಹೌದು" if is_asta else "ಇಲ್ಲ"
    if p_name in ["ರವಿ", "ರಾಹು", "ಕೇತು", "ಲಗ್ನ", "ಮಾಂದಿ"]: asta_text = "ಅನ್ವಯಿಸುವುದಿಲ್ಲ"
        
    # --- FLOAT SAFE MATH FOR UPA DREKKANA ---
    c_deg = round(deg, 6)
    d1_idx = int(c_deg / 30)
    dr_val = c_deg % 30
    is_odd = ((d1_idx) % 2 == 0)
    d2_idx = (4 if dr_val < 15 else 3) if is_odd else (3 if dr_val < 15 else 4)
    
    d30_idx = (0 if dr_val < 5 else (10 if dr_val < 10 else (8 if dr_val < 18 else (2 if dr_val < 25 else 6)))) if is_odd else (5 if dr_val < 5 else (2 if dr_val < 12 else (8 if dr_val < 20 else (10 if dr_val < 25 else 0))))
    
    # 1. Rashi Drekkana (D3 of D1)
    rashi_drek_num = int(dr_val / 10) + 1
    if rashi_drek_num > 3: rashi_drek_num = 3
    true_d3_idx = (d1_idx + (rashi_drek_num - 1) * 4) % 12
    
    # 2. Navamsha Drekkana (D3 of D9)
    d9_exact = round((c_deg * 9) % 360, 6)
    d9_idx = int(d9_exact / 30)
    d9_rem = d9_exact % 30
    nav_drek_num = int(d9_rem / 10) + 1
    if nav_drek_num > 3: nav_drek_num = 3
    nav_drek_idx = (d9_idx + (nav_drek_num - 1) * 4) % 12
    
    # 3. Dwadashamsha Drekkana (D3 of D12) - FLOAT SAFE
    d12_part = int(dr_val / 2.5)
    if d12_part > 11: d12_part = 11
    d12_idx = (d1_idx + d12_part) % 12
    
    slice_rem = round(dr_val - (d12_part * 2.5), 6)
    d12_deg = round(slice_rem * 12, 6)
    dwa_drek_num = int(d12_deg / 10) + 1
    if dwa_drek_num > 3: dwa_drek_num = 3
    dwa_drek_idx = (d12_idx + (dwa_drek_num - 1) * 4) % 12

    h_arr = [
        "<div class='card'><table class='key-val-table'>",
        f"<tr><td class='key'>ಸ್ಫುಟ</td><td>{fmt_deg(deg)}</td></tr>",
        f"<tr><td class='key'>ಗತಿ</td><td><b>{gathi_str}</b></td></tr>",
        f"<tr><td class='key'>ಅಸ್ತ</td><td><b>{asta_text}</b></td></tr></table></div>"
    ]
    st.markdown("".join(h_arr), unsafe_allow_html=True)
    
    st.markdown("#### 📊 ವರ್ಗಗಳು")
    v_arr = [
        "<div class='card'><table class='key-val-table'>",
        f"<tr><td class='key'>ರಾಶಿ</td><td>{KN_RASHI[d1_idx]}</td></tr>",
        f"<tr><td class='key'>ಹೋರಾ</td><td>{KN_RASHI[d2_idx]}</td></tr>",
        f"<tr><td class='key'>ದ್ರೇಕ್ಕಾಣ</td><td>{KN_RASHI[true_d3_idx]}</td></tr>",
        f"<tr><td class='key'>ನವಾಂಶ</td><td>{KN_RASHI[d9_idx]}</td></tr>",
        f"<tr><td class='key'>ದ್ವಾದಶಾಂಶ</td><td>{KN_RASHI[d12_idx]}</td></tr>",
        f"<tr><td class='key'>ತ್ರಿಂಶಾಂಶ</td><td>{KN_RASHI[d30_idx]}</td></tr></table></div>"
    ]
    st.markdown("".join(v_arr), unsafe_allow_html=True)

    st.markdown("#### 📊 ಉಪ ದ್ರೇಕ್ಕಾಣ")
    upa_arr = [
        "<div class='card'><table class='key-val-table'>",
        f"<tr><td class='key'>ರಾಶಿ ದ್ರೇಕ್ಕಾಣ</td><td>{KN_RASHI[true_d3_idx]} ({rashi_drek_num})</td></tr>",
        f"<tr><td class='key'>ನವಾಂಶ ದ್ರೇಕ್ಕಾಣ</td><td>{KN_RASHI[nav_drek_idx]} ({nav_drek_num})</td></tr>",
        f"<tr><td class='key'>ದ್ವಾದಶಾಂಶ ದ್ರೇಕ್ಕಾಣ</td><td>{KN_RASHI[dwa_drek_idx]} ({dwa_drek_num})</td></tr></table></div>"
    ]
    st.markdown("".join(upa_arr), unsafe_allow_html=True)

# ==========================================
# 6. SESSION STATE & UI
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "input"
if 'data' not in st.session_state: st.session_state.data = {}
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'name_input' not in st.session_state: st.session_state.name_input = ""
if 'place_input' not in st.session_state: st.session_state.place_input = "Yellapur"
if 'lat' not in st.session_state: st.session_state.lat = 14.98
if 'lon' not in st.session_state: st.session_state.lon = 74.73
if 'aroodhas' not in st.session_state: st.session_state.aroodhas = {} 

if 'dob_input' not in st.session_state:
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    st.session_state.dob_input = now.date()
    st.session_state.h_input = 12 if now.hour % 12 == 0 else now.hour % 12
    st.session_state.m_input = now.minute
    st.session_state.ampm_input = "AM" if now.hour < 12 else "PM"

st.markdown('<div class="header-box">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

if st.session_state.page == "input":
    with st.container():
        saved_db = load_db()
        if len(saved_db) > 0:
            st.markdown("<div class='card'>#### 📂 ಉಳಿಸಿದ ಜಾತಕ</div>", unsafe_allow_html=True)
            c_sel, c_btn = st.columns([3, 1])
            sel_n = c_sel.selectbox("ಆಯ್ಕೆಮಾಡಿ", [""] + list(saved_db.keys()), label_visibility="collapsed")
            if c_btn.button("ತೆಗೆಯಿರಿ", use_container_width=True) and sel_n != "":
                prof = saved_db[sel_n]
                st.session_state.update({
                    "name_input": sel_n, "dob_input": datetime.datetime.strptime(prof['d'], "%Y-%m-%d").date(),
                    "h_input": prof['h'], "m_input": prof['m'], "ampm_input": prof['ampm'],
                    "lat": prof['lat'], "lon": prof['lon'], "place_input": prof['p']
                })
                st.rerun()
        
        st.markdown("<div class='card'>#### ✨ ಹೊಸ ಜಾತಕ</div>", unsafe_allow_html=True)
        name = st.text_input("ಹೆಸರು", key="name_input")
        dob = st.date_input("ದಿನಾಂಕ", key="dob_input", min_value=datetime.date(1800, 1, 1), max_value=datetime.date(2100, 12, 31))
        
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("ಗಂಟೆ", 1, 12, key="h_input")
        m = c2.number_input("ನಿಮಿಷ", 0, 59, key="m_input")
        ampm = c3.selectbox("ಬೆಳಿಗ್ಗೆ/ಮಧ್ಯಾಹ್ನ", ["AM", "PM"], key="ampm_input")
        
        place_q = st.text_input("ಊರು ಹುಡುಕಿ", key="place_input")
        if st.button("ಹುಡುಕಿ"):
            try:
                loc = geolocator.geocode(place_q)
                if loc: 
                    st.session_state.lat, st.session_state.lon = loc.latitude, loc.longitude
                    st.success("📍 " + loc.address)
            except: st.error("ಲೋಪ: ಸ್ಥಳ ಕಂಡುಬಂದಿಲ್ಲ.")
                
        lat = st.number_input("ಅಕ್ಷಾಂಶ", key="lat", format="%.4f")
        lon = st.number_input("ರೇಖಾಂಶ", key="lon", format="%.4f")
        
        with st.expander("⚙️ ಸುಧಾರಿತ ಆಯ್ಕೆಗಳು"):
            ca, cn = st.columns(2)
            ayan_sel = ca.selectbox("ಅಯನಾಂಶ", ["ಲಾಹಿರಿ", "ರಾಮನ್", "ಕೆ.ಪಿ"])
            node_sel = cn.selectbox("ರಾಹು ಗಣನೆ", ["ನಿಜ ರಾಹು", "ಸರಾಸರಿ ರಾಹು"])
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0)
            h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            
            ayan_mode = {"ಲಾಹಿರಿ": swe.SIDM_LAHIRI, "ರಾಮನ್": swe.SIDM_RAMAN, "ಕೆ.ಪಿ": swe.SIDM_KRISHNAMURTI}[ayan_sel]
            node_mode = swe.TRUE_NODE if node_sel == "ನಿಜ ರಾಹು" else swe.MEAN_NODE
            
            p1, p2, p3, p4, p5 = get_full_calculations(jd, lat, lon, dob, ayan_mode, node_mode)
            st.session_state.data = {"pos": p1, "pan": p2, "details": p3, "bhavas": p4, "speeds": p5}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    pos, pan, details, bhavas, speeds = st.session_state.data['pos'], st.session_state.data['pan'], st.session_state.data['details'], st.session_state.data['bhavas'], st.session_state.data['speeds']
    
    c_bk, c_sv = st.columns(2)
    if c_bk.button("⬅️ ಹಿಂದಕ್ಕೆ"): 
        st.session_state.page = "input"
        st.rerun()
    if c_sv.button("💾 ಉಳಿಸಿ"):
        d_str = st.session_state.dob_input.strftime("%Y-%m-%d")
        prof_data = {"d": d_str, "h": st.session_state.h_input, "m": st.session_state.m_input, "ampm": st.session_state.ampm_input, "lat": st.session_state.lat, "lon": st.session_state.lon, "p": st.session_state.place_input}
        save_db(st.session_state.name_input if st.session_state.name_input != "" else "ಅಜ್ಞಾತ_" + d_str, prof_data)
        st.success("ಉಳಿಸಲಾಗಿದೆ!")
    
    tabs = ["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ಆರೂಢ", "ದಶ", "ಪಂಚಾಂಗ", "ಭಾವ", "ಅಷ್ಟಕವರ್ಗ", "ಟಿಪ್ಪಣಿ", "ಚಂದಾದಾರಿಕೆ", "ಬಗ್ಗೆ"]
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs(tabs)
    
    with t1:
        c_v, c_b = st.columns(2)
        d_names = {1: "ರಾಶಿ", 2: "ಹೋರಾ", 3: "ದ್ರೇಕ್ಕಾಣ", 9: "ನವಾಂಶ", 12: "ದ್ವಾದಶಾಂಶ", 30: "ತ್ರಿಂಶಾಂಶ"}
        
        with c_v:
            st.markdown("<div style='color:#2B6CB0; font-weight:800; font-size:15px; margin-bottom:5px;'>ವರ್ಗ</div>", unsafe_allow_html=True)
            v_opt_base = st.selectbox("ವರ್ಗ", [1, 2, 3, 9, 12, 30], format_func=lambda x: d_names[x], label_visibility="collapsed")
            
        with c_b:
            st.markdown("<div style='color:#2B6CB0; font-weight:800; font-size:15px; margin-bottom:5px;'>ಚಾರ್ಟ್ ವಿಧ</div>", unsafe_allow_html=True)
            c_mode = st.radio("ಚಾರ್ಟ್ ವಿಧ", ["ರಾಶಿ", "ಭಾವ", "ನವಾಂಶ"], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<hr style='margin: 10px 0px; border-color: #E2E8F0;'>", unsafe_allow_html=True)
        
        c_tog_txt, c_tog_btn = st.columns([3, 1])
        with c_tog_txt:
            st.markdown("<div style='color:#2B6CB0; font-weight:800; font-size:15px; margin-top:8px;'>ಸ್ಫುಟಗಳನ್ನು ಕುಂಡಲಿಯಲ್ಲಿ ತೋರಿಸಿ</div>", unsafe_allow_html=True)
        with c_tog_btn:
            show_sphutas = st.toggle("Sphutas", value=False, label_visibility="collapsed")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        v_opt = 1 if c_mode == "ಭಾವ" else (9 if c_mode == "ನವಾಂಶ" else v_opt_base)
        b_opt = True if c_mode == "ಭಾವ" else False
        
        bxs_list = {i: [] for i in range(12)}
        ld = pos[KN_PLANETS["Lagna"]] 
        
        render_items = list(PLANET_ORDER)
        render_pos = dict(pos)
        
        if show_sphutas:
            for k, v in pan['adv_sphutas'].items():
                render_items.append(k)
                render_pos[k] = v
        
        for n in render_items:
            d = render_pos[n]
            if v_opt == 1: ri = (int(ld/30) + int(((d - ld + 360)%360 + 15)/30)) % 12 if b_opt else int(d/30)
            elif v_opt == 2: ri = (4 if d % 30 < 15 else 3) if int(d/30) % 2 == 0 else (3 if d % 30 < 15 else 4)
            elif v_opt == 30: 
                dr = d%30
                if int(d/30) % 2 == 0: ri = 0 if dr < 5 else (10 if dr < 10 else (8 if dr < 18 else (2 if dr < 25 else 6)))
                else: ri = 5 if dr < 5 else (2 if dr < 12 else (8 if dr < 20 else (10 if dr < 25 else 0)))
            elif v_opt == 9: ri = ([0, 9, 6, 3][int(d/30)%4] + int((d%30)/3.33333)) % 12
            elif v_opt == 3: ri = (int(d/30) + (int((d%30)/10)*4)) % 12
            elif v_opt == 12: ri = (int(d/30) + int((d%30)/2.5)) % 12
            else: ri = int(d/30)
                
            cls = "hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else ("sp" if n in pan['adv_sphutas'] else "pl")
            
            bxs_list[ri].append((render_items.index(n), f"<div class='{cls}'>{n}</div>"))
            
        bxs = {i: "".join([item[1] for item in sorted(bxs_list[i], key=lambda x: x[0])]) for i in range(12)}
        
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        glines = ["<div class='grid-container'>"]
        c_count = 0
        for idx in grid:
            if idx is None:
                if c_count == 0: 
                    g_txt = ("ಭಾವ" if c_mode == "ಭಾವ" else ("ನವಾಂಶ" if c_mode == "ನವಾಂಶ" else d_names[v_opt]))
                    glines.append(f"<div class='center-box'>ಭಾರತೀಯಮ್<br>{g_txt}</div>")
                    c_count = 1
            else: 
                glines.append(f"<div class='box'><span class='lbl'>{KN_RASHI[idx]}</span>{bxs[idx]}</div>")
        glines.append("</div>")
        st.markdown("".join(glines), unsafe_allow_html=True)
        
        st.markdown("<br><h4 style='text-align:center; color:#2B6CB0;'>🔍 ಗ್ರಹಗಳ ವಿಸ್ತೃತ ವಿವರ</h4>", unsafe_allow_html=True)
        btn_cols = st.columns(4)
        for i, p_n in enumerate(PLANET_ORDER):
            if btn_cols[i % 4].button(p_n, key="pop_" + p_n, use_container_width=True):
                show_planet_popup(p_n, pos[p_n], speeds.get(p_n, 0), pos["ರವಿ"])
    
    with t2:
        slines = [
            "<div class='card'><table class='key-val-table'>",
            "<tr><th>ಸ್ಫುಟ ಬಿಂದು</th><th>ರಾಶಿ</th><th style='text-align:right'>ಅಂಶ</th><th style='text-align:right'>ನಕ್ಷತ್ರ</th></tr>"
        ]
        
        sphuta_order = [
            "ಧೂಮ", "ವ್ಯತೀಪಾತ", "ಪರಿವೇಷ", "ಇಂದ್ರಚಾಪ", "ಉಪಕೇತು",
            "ಭೃಗು ಬಿ.", "ಬೀಜ", "ಕ್ಷೇತ್ರ", "ಯೋಗಿ",
            "ತ್ರಿಸ್ಫುಟ", "ಚತುಃಸ್ಫುಟ", "ಪಂಚಸ್ಫುಟ",
            "ಪ್ರಾಣ", "ದೇಹ", "ಮೃತ್ಯು", "ಸೂಕ್ಷ್ಮ ತ್ರಿ."
        ]
        for sp in sphuta_order:
            d = pan['adv_sphutas'][sp]
            slines.append(f"<tr><td><b>{sp}</b></td><td>{KN_RASHI[int(d/30)]}</td><td style='text-align:right'>{fmt_deg(d)}</td><td style='text-align:right'>{KN_NAK[int(d / 13.333333333) % 27]}-{int((d % 13.333333333) / 3.333333333) + 1}</td></tr>")
        slines.append("</table></div>")
        st.markdown("".join(slines), unsafe_allow_html=True)

    with t3:
        st.markdown("#### ಆರೂಢ ಚಕ್ರ")
        
        c_aro1, c_aro2, c_aro3 = st.columns([2, 2, 1])
        aro_options = ["ಆರೂಢ", "ಉದಯ", "ಲಗ್ನಾಂಶ", "ಛತ್ರ", "ಸ್ಪೃಷ್ಟಾಂಗ", "ಚಂದ್ರ", "ತಾಂಬೂಲ"]
        
        selected_aro = c_aro1.selectbox("ಆರೂಢ ಆಯ್ಕೆಮಾಡಿ", aro_options, label_visibility="collapsed")
        selected_rashi = c_aro2.selectbox("ರಾಶಿ ಆಯ್ಕೆಮಾಡಿ", KN_RASHI, label_visibility="collapsed")
        
        st.markdown("""<style>div[data-testid="column"]:nth-of-type(3) { display: flex; align-items: flex-end; padding-bottom: 2px; }</style>""", unsafe_allow_html=True)
        if c_aro3.button("ಸೇರಿಸಿ", use_container_width=True):
            st.session_state.aroodhas[selected_aro] = KN_RASHI.index(selected_rashi)
            st.rerun()

        if len(st.session_state.aroodhas) > 0:
            if st.button("ತೆರವುಗೊಳಿಸಿ", key="clear_aro"):
                st.session_state.aroodhas = {}
                st.rerun()

        bxs_aro = {i: "" for i in range(12)}
        for a_name, r_idx in st.session_state.aroodhas.items():
            bxs_aro[r_idx] += f"<div class='hi'>{a_name}</div>"

        grid_aro = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        alines = ["<div class='grid-container' style='margin-top:20px;'>"]
        c_count_a = 0
        for idx in grid_aro:
            if idx is None:
                if c_count_a == 0: 
                    alines.append("<div class='center-box'>ಆರೂಢ<br>ಚಕ್ರ</div>")
                    c_count_a = 1
            else: 
                alines.append(f"<div class='box'><span class='lbl'>{KN_RASHI[idx]}</span>{bxs_aro[idx]}</div>")
        alines.append("</div>")
        st.markdown("".join(alines), unsafe_allow_html=True)
        
    with t4:
        st.markdown(f"<div class='card' style='color:#DD6B20; font-weight:900;'>ಶಿಷ್ಟ ದಶೆ: {pan['lord_bal']} ಉಳಿಕೆ: {pan['d_bal']}</div>", unsafe_allow_html=True)
        dlines, cur_d, si = [], pan['date_obj'], pan['n_idx'] % 9
        for i in range(9):
            im = (si + i) % 9
            md_end = cur_d + datetime.timedelta(days=(YEARS[im] * ((1 - pan['perc']) if i == 0 else 1))*365.25)
            dlines.append(f"<details><summary class='md-node'><span>{LORDS[im]}</span><span class='date-label'>{md_end.strftime('%d-%m-%y')}</span></summary>")
            cad = cur_d
            for j in range(9):
                ia = (im + j) % 9
                ad_y = (YEARS[im] * YEARS[ia] / 120.0) * ((1 - pan['perc']) if i == 0 else 1)
                ae = cad + datetime.timedelta(days=ad_y*365.25)
                dlines.append(f"<details><summary class='ad-node'><span>{LORDS[ia]}</span><span class='date-label'>{ae.strftime('%d-%m-%y')}</span></summary>")
                cpd = cad
                for k in range(9):
                    ip = (ia + k) % 9
                    pe = cpd + datetime.timedelta(days=(ad_y * YEARS[ip] / 120.0)*365.25)
                    dlines.append(f"<div class='pd-node' style='padding:10px 15px; border-bottom:1px solid #EDF2F7; display:flex; justify-content:space-between'><span>{LORDS[ip]}</span><span>{pe.strftime('%d-%m-%y')}</span></div>")
                    cpd = pe
                dlines.append("</details>")
                cad = ae
            dlines.append("</details>")
            cur_d = md_end
        st.markdown("".join(dlines), unsafe_allow_html=True)
    
    with t5:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#2B6CB0; font-weight:800; margin:0;'>ಸ್ಥಳ: <span style='color:#2D3748;'>{st.session_state.place_input}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#2B6CB0; font-weight:800; margin:0;'>ದಿನಾಂಕ: <span style='color:#2D3748;'>{st.session_state.dob_input.strftime('%d-%m-%Y')}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#2B6CB0; font-weight:800; margin:0;'>ಸಮಯ: <span style='color:#2D3748;'>{st.session_state.h_input}:{str(st.session_state.m_input).zfill(2)} {st.session_state.ampm_input}</span></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        p_lines = ["<div class='card'><table class='key-val-table'>"]
        for k, v in [("ವಾರ", str(pan['v'])), ("ತಿಥಿ", str(pan['t'])), ("ನಕ್ಷತ್ರ", str(pan['n'])), ("ಯೋಗ", str(pan['y'])), ("ಕರಣ", str(pan['k'])), ("ಚಂದ್ರ ರಾಶಿ", str(pan['r'])), ("ಉದಯಾದಿ ಘಟಿ", str(pan['udayadi'])), ("ಗತ ಘಟಿ", str(pan['gata'])), ("ಪರಮ ಘಟಿ", str(pan['parama'])), ("ಶೇಷ ಘಟಿ", str(pan['rem']))]:
            p_lines.append(f"<tr><td class='key'>{k}</td><td>{v}</td></tr>")
        p_lines.append("</table></div>")
        st.markdown("".join(p_lines), unsafe_allow_html=True)
            
    with t6:
        blines = ["<div class='card'><table class='key-val-table'><tr><th>ಭಾವ</th><th>ಮಧ್ಯ (Sphuta)</th><th>ರಾಶಿ</th></tr>"]
        for i, deg in enumerate(bhavas):
            blines.append(f"<tr><td><b>{str(i + 1)}</b></td><td>{fmt_deg(deg)}</td><td>{KN_RASHI[int(deg/30)]}</td></tr>")
        blines.append("</table></div>")
        st.markdown("".join(blines), unsafe_allow_html=True)
        
    with t7:
        st.markdown("<h4 style='text-align:center; color:#DD6B20;'>ಸರ್ವಾಷ್ಟಕವರ್ಗ (SAV)</h4>", unsafe_allow_html=True)
        slines, c_count = ["<div class='grid-container'>"], 0
        for idx in [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]:
            if idx is None:
                if c_count == 0: 
                    slines.append("<div class='center-box'>ಒಟ್ಟು ಬಿಂದು<br><span style='font-size:20px; color:#E53E3E;'>337</span></div>")
                    c_count = 1
            else: 
                slines.append(f"<div class='box'><span class='lbl'>{KN_RASHI[idx]}</span><div class='bindu'>{pan['sav_bindus'][idx]}</div></div>")
        slines.append("</div>")
        st.markdown("".join(slines), unsafe_allow_html=True)
        
        st.markdown("<br><h4 style='text-align:center; color:#2B6CB0;'>📝 ಬಿನ್ನಾಷ್ಟಕವರ್ಗ (BAV Detail)</h4>", unsafe_allow_html=True)
        t_arr = ["<div class='card' style='overflow-x:auto;'><table class='bav-table' style='width:100%; text-align:center;'><tr><th>ರಾಶಿ</th><th>ರವಿ</th><th>ಚಂ</th><th>ಕು</th><th>ಬು</th><th>ಗು</th><th>ಶು</th><th>ಶ</th><th>ಒಟ್ಟು</th></tr>"]
        for i in range(12):
            tr = f"<tr><td><b>{KN_RASHI[i]}</b></td>"
            for p in ["ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ"]: tr += f"<td>{pan['bav_bindus'][p][i]}</td>"
            tr += f"<td style='color:#E53E3E; font-weight:bold;'>{pan['sav_bindus'][i]}</td></tr>"
            t_arr.append(tr)
        t_arr.append("</table></div>")
        st.markdown("".join(t_arr), unsafe_allow_html=True)

    with t8: st.session_state.notes = st.text_area("ಟಿಪ್ಪಣಿಗಳು", value=st.session_state.notes, height=300)

    with t9:
        st.markdown("<div class='card' style='text-align:center;'>### 🚫 ಜಾಹೀರಾತು-ಮುಕ್ತ<p style='color:#718096; font-weight:600;'>ಜಾಹೀರಾತುಗಳಿಲ್ಲದೆ ನಿರಂತರವಾಗಿ ಆ್ಯಪ್ ಬಳಸಿ.<br></p><br></div>", unsafe_allow_html=True)
        st.button("ಜಾಹೀರಾತು ತೆಗೆಯಿರಿ", type="primary", use_container_width=True)

    with t10:
        st.markdown("<div class='card'>#### ಭಾರತೀಯಮ್<p style='color:#4A5568; font-size:14px; line-height:1.6;'><b>ಆವೃತ್ತಿ: 1.0.0</b><br><br>ನಿಖರವಾದ ವೈದಿಕ ಜ್ಯೋತಿಷ್ಯ ಲೆಕ್ಕಾಚಾರಗಳಿಗಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.</p><br></div>", unsafe_allow_html=True)
        st.link_button("</> ಮೂಲ ಕೋಡ್", "https://github.com/your-username/bharatheeyam", use_container_width=True)
