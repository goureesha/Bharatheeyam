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
    
    div[data-testid="stRadio"] label p {
        font-weight: 800 !important;
        color: #2B6CB0 !important;
        font-size: 15px !important;
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
        justify-content: center; 
        font-size: 12px; 
        font-weight: 800; 
        padding: 4px; 
        text-align: center; 
        border-radius: 8px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.02);
    }
    
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
        font-size: 15px; 
        border-radius: 8px;
        border: 2px solid #FFFFFF;
    }
    
    .lbl { 
        position: absolute; top: 3px; left: 5px; 
        font-size: 10px; color: #2F855A !important; 
        font-weight: 900; 
    }
    .hi { color: #E53E3E !important; font-weight: 900; text-decoration: underline; } 
    .pl { color: #2B6CB0 !important; font-weight: 800; } 
    
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v29_popups")

KN_PLANETS = {
    0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 
    5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", 
    "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"
}

KN_RASHI = [
    "ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", 
    "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"
]

KN_VARA = [
    "ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", 
    "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"
]
KN_TITHI = [
    "ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ",
    "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ",
    "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ",
    "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ",
    "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ",
    "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ",
    "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ",
    "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"
]
KN_NAK = [
    "ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ",
    "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಘ", "ಪೂರ್ವ ಫಾಲ್ಗುಣಿ",
    "ಉತ್ತರ ಫಾಲ್ಗುಣಿ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ",
    "ಅನುರಾಧ", "ಜ್ಯೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ",
    "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ",
    "ರೇವತಿ"
]
KN_YOGA = [
    "ವಿಷ್ಕಂಭ", "ಪ್ರೀತಿ", "ಆಯುಷ್ಮಾನ್", "ಸೌಭಾಗ್ಯ", "ಶೋಭನ",
    "ಅತಿಗಂಡ", "ಸುಕರ್ಮ", "ಧೃತಿ", "ಶೂಲ", "ಗಂಡ",
    "ವೃದ್ಧಿ", "ಧ್ರುವ", "ವ್ಯಾಘಾತ", "ಹರ್ಷಣ", "ವಜ್ರ",
    "ಸಿದ್ಧಿ", "ವ್ಯತೀಪಾತ", "ವರೀಯಾನ್", "ಪರಿಘ", "ಶಿವ",
    "ಸಿದ್ಧ", "ಸಾಧ್ಯ", "ಶುಭ", "ಶುಕ್ಲ", "ಬ್ರಹ್ಮ",
    "ಇಂದ್ರ", "ವೈಧೃತಿ"
]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def get_altitude_manual(jd, lat, lon):
    res = swe.calc_ut(jd, swe.SUN, swe.FLG_EQUATORIAL | swe.FLG_SWIEPH)
    ra = res[0][0]
    dec = res[0][1]
    gmst = swe.sidtime(jd)
    lst = gmst + (lon / 15.0)
    ha_deg = ((lst * 15.0) - ra + 360) % 360
    if ha_deg > 180: 
        ha_deg -= 360
        
    lat_rad = math.radians(lat)
    dec_rad = math.radians(dec)
    ha_rad = math.radians(ha_deg)
    
    p1 = math.sin(lat_rad) * math.sin(dec_rad)
    p2 = math.cos(lat_rad) * math.cos(dec_rad) * math.cos(ha_rad)
    sin_alt = p1 + p2
    
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
                if get_altitude_manual(m, lat, lon) < -0.833: 
                    l = m
                else: 
                    h = m
            rise_time = h
        if alt1 > -0.833 and alt2 <= -0.833:
            l, h = current, current + step
            for _ in range(20): 
                m = (l + h) / 2
                if get_altitude_manual(m, lat, lon) > -0.833: 
                    l = m
                else: 
                    h = m
            set_time = h
        current += step
    return rise_time, set_time

def find_nak_limit(jd, target_deg):
    low = jd - 1.2
    high = jd + 1.2
    for _ in range(20):
        mid = (low + high) / 2
        ayan = swe.get_ayanamsa(mid)
        m_deg = (swe.calc_ut(mid, swe.MOON)[0][0] - ayan) % 360
        diff = (m_deg - target_deg + 180) % 360 - 180
        if diff < 0: 
            low = mid
        else: 
            high = mid
    return mid

def fmt_ghati(decimal_val):
    g = int(decimal_val)
    rem = decimal_val - g
    v = int(round(rem * 60))
    if v == 60: 
        g += 1
        v = 0
    return str(g) + "." + str(v).zfill(2)

# ==========================================
# 4. CALCULATIONS & SPEED LOGIC
# ==========================================
def calculate_mandi(jd_birth, lat, lon, dob_obj):
    y = dob_obj.year
    m = dob_obj.month
    d = dob_obj.day
    sr_civil, ss_civil = find_sunrise_set_for_date(y, m, d, lat, lon)
    
    py_weekday = dob_obj.weekday()
    civil_weekday_idx = (py_weekday + 1) % 7 
    
    is_night = False
    if jd_birth >= sr_civil and jd_birth < ss_civil: 
        is_night = False
    else: 
        is_night = True
        
    start_base = 0.0
    duration = 0.0
    vedic_wday = 0
    panch_sr = 0.0
    
    if not is_night:
        vedic_wday = civil_weekday_idx
        panch_sr = sr_civil
        start_base = sr_civil
        duration = ss_civil - sr_civil
    else:
        if jd_birth < sr_civil:
            vedic_wday = (civil_weekday_idx - 1) % 7
            prev_d = dob_obj - datetime.timedelta(days=1)
            p_y = prev_d.year
            p_m = prev_d.month
            p_d = prev_d.day
            p_sr, p_ss = find_sunrise_set_for_date(p_y, p_m, p_d, lat, lon)
            start_base = p_ss
            duration = sr_civil - p_ss
            panch_sr = p_sr
        else:
            vedic_wday = civil_weekday_idx
            next_d = dob_obj + datetime.timedelta(days=1)
            n_y = next_d.year
            n_m = next_d.month
            n_d = next_d.day
            n_sr, n_ss = find_sunrise_set_for_date(n_y, n_m, n_d, lat, lon)
            start_base = ss_civil
            duration = n_sr - ss_civil
            panch_sr = sr_civil

    if not is_night: 
        factors = [26, 22, 18, 14, 10, 6, 2] 
    else: 
        factors = [10, 6, 2, 26, 22, 18, 14] 
        
    factor = factors[vedic_wday]
    mandi_jd = start_base + (duration * factor / 30.0)
    
    return mandi_jd, is_night, panch_sr, vedic_wday, start_base

def get_full_calculations(jd_birth, lat, lon, dob_obj):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd_birth)
    positions = {}
    speeds = {} # Captures Planet Speed for Vakri
    extra_details = {}
    
    # CALCULATE MAIN PLANETS + SPEED
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        res = swe.calc_ut(jd_birth, pid, flag)
        deg = res[0][0] % 360
        speed = res[0][3]
        
        positions[KN_PLANETS[pid]] = deg
        speeds[KN_PLANETS[pid]] = speed
        
        nak_idx = int(deg / 13.333333333)
        pada = int((deg % 13.333333333) / 3.333333333) + 1
        extra_details[KN_PLANETS[pid]] = {
            "nak": KN_NAK[nak_idx % 27], 
            "pada": pada
        }

    # CALCULATE RAHU / KETU + SPEED
    rahu_res = swe.calc_ut(jd_birth, swe.TRUE_NODE, flag)
    rahu_deg = rahu_res[0][0] % 360
    rahu_speed = rahu_res[0][3]
    
    positions[KN_PLANETS[101]] = rahu_deg
    speeds[KN_PLANETS[101]] = rahu_speed
    
    positions[KN_PLANETS[102]] = (rahu_deg + 180) % 360
    speeds[KN_PLANETS[102]] = rahu_speed
    
    nodes = [
        (KN_PLANETS[101], rahu_deg), 
        (KN_PLANETS[102], (rahu_deg + 180) % 360)
    ]
    
    for p, d in nodes:
        nak_idx = int(d / 13.333333333)
        pada = int((d % 13.333333333) / 3.333333333) + 1
        extra_details[p] = {"nak": KN_NAK[nak_idx % 27], "pada": pada}

    houses_res = swe.houses(jd_birth, float(lat), float(lon), b'P')
    cusps = houses_res[0]
    
    if len(cusps) == 13:
        asc_deg = (cusps[1] - ayan) % 360
        bhava_sphutas = [(cusps[i] - ayan) % 360 for i in range(1, 13)]
    else:
        asc_deg = (cusps[0] - ayan) % 360
        bhava_sphutas = [(cusps[i] - ayan) % 360 for i in range(0, 12)]

    positions[KN_PLANETS["Lagna"]] = asc_deg
    speeds[KN_PLANETS["Lagna"]] = 0
    nak_idx = int(asc_deg / 13.333333333)
    pada = int((asc_deg % 13.333333333) / 3.333333333) + 1
    extra_details[KN_PLANETS["Lagna"]] = {
        "nak": KN_NAK[nak_idx % 27], 
        "pada": pada
    }

    res = calculate_mandi(jd_birth, lat, lon, dob_obj)
    mandi_time_jd = res[0]
    is_night = res[1]
    panch_sr = res[2]
    w_idx = res[3]
    debug_base = res[4]
    
    h_mandi = swe.houses(mandi_time_jd, float(lat), float(lon), b'P')
    a_mandi = swe.get_ayanamsa(mandi_time_jd)
    mandi_deg = (h_mandi[1][0] - a_mandi) % 360
    positions[KN_PLANETS["Ma"]] = mandi_deg
    speeds[KN_PLANETS["Ma"]] = 0
    
    nak_idx = int(mandi_deg / 13.333333333)
    pada = int((mandi_deg % 13.333333333) / 3.333333333) + 1
    extra_details[KN_PLANETS["Ma"]] = {
        "nak": KN_NAK[nak_idx % 27], 
        "pada": pada
    }

    m_deg = positions["ಚಂದ್ರ"]
    s_deg = positions["ರವಿ"]
    t_idx = int(((m_deg - s_deg + 360) % 360) / 12)
    n_idx = int(m_deg / 13.333333333)
    
    y_deg = (m_deg + s_deg) % 360
    y_idx = int(y_deg / 13.333333333)
    yoga_name = KN_YOGA[y_idx]
    
    k_idx = int(((m_deg - s_deg + 360) % 360) / 6)
    if k_idx == 0:
        k_name = "ಕಿಂಸ್ತುಘ್ನ"
    elif k_idx == 57:
        k_name = "ಶಕುನಿ"
    elif k_idx == 58:
        k_name = "ಚತುಷ್ಪಾದ"
    elif k_idx == 59:
        k_name = "ನಾಗ"
    else:
        k_arr = ["ಬವ", "ಬಾಲವ", "ಕೌಲವ", "ತೈತಿಲ", "ಗರ", "ವಣಿಜ", "ಭದ್ರಾ (ವಿಷ್ಟಿ)"]
        k_name = k_arr[(k_idx - 1) % 7]
        
    r_idx = int(m_deg / 30)
    rasi_name = KN_RASHI[r_idx]
    
    js = find_nak_limit(jd_birth, n_idx * 13.333333333)
    je = find_nak_limit(jd_birth, (n_idx + 1) * 13.333333333)
    
    perc = (m_deg % 13.333333333) / 13.333333333
    bal = YEARS[n_idx % 9] * (1 - perc)
    dt_birth = datetime.datetime.fromtimestamp((jd_birth - 2440587.5) * 86400)
    
    pan = {
        "t": KN_TITHI[min(t_idx, 29)], 
        "v": KN_VARA[w_idx], 
        "n": KN_NAK[n_idx % 27],
        "y": yoga_name,
        "k": k_name,
        "r": rasi_name,
        "sr": panch_sr, 
        "udayadi": fmt_ghati((jd_birth - panch_sr) * 60), 
        "gata": fmt_ghati((jd_birth - js) * 60), 
        "parama": fmt_ghati((je - js) * 60), 
        "rem": fmt_ghati((je - jd_birth) * 60),
        "d_bal": str(int(bal)) + "ವ " + str(int((bal%1)*12)) + "ತಿ",
        "n_idx": n_idx, 
        "perc": perc, 
        "date_obj": dt_birth,
        "lord_bal": LORDS[n_idx%9]
    }
    return positions, pan, extra_details, bhava_sphutas, speeds

# ==========================================
# 5. DIALOG UI FOR PLANET POPUP
# ==========================================
@st.dialog("ಗ್ರಹದ ಸಂಪೂರ್ಣ ವಿವರ (Planet Details)")
def show_planet_popup(p_name, deg, speed, sun_deg):
    d1_v1 = str(int(deg%30))
    d1_v2 = str(int((deg%30*60)%60))
    deg_fmt = d1_v1 + "° " + d1_v2 + "'"
    
    # Asta (Combust) Logic
    is_asta = False
    gathi_str = "N/A"
    
    if p_name not in ["ರವಿ", "ರಾಹು", "ಕೇತು", "ಲಗ್ನ", "ಮಾಂದಿ"]:
        diff = abs(deg - sun_deg)
        if diff > 180: diff = 360 - diff
        limits = {"ಚಂದ್ರ": 12, "ಕುಜ": 17, "ಬುಧ": 14, "ಗುರು": 11, "ಶುಕ್ರ": 10, "ಶನಿ": 15}
        if diff <= limits.get(p_name, 0):
            is_asta = True
            
        if p_name == "ಚಂದ್ರ": gathi_str = "ನೇರ (Direct)"
        elif speed < 0: gathi_str = "ವಕ್ರಿ (Retrograde)"
        else: gathi_str = "ನೇರ (Direct)"
        
    elif p_name in ["ರಾಹು", "ಕೇತು"]:
        gathi_str = "ವಕ್ರಿ (Retrograde)"
    elif p_name == "ರವಿ":
        gathi_str = "ನೇರ (Direct)"
    else:
        gathi_str = "ಅನ್ವಯಿಸುವುದಿಲ್ಲ (-)"
        
    asta_text = "ಹೌದು (Combust)" if is_asta else "ಇಲ್ಲ (No)"
    if p_name in ["ರವಿ", "ರಾಹು", "ಕೇತು", "ಲಗ್ನ", "ಮಾಂದಿ"]: 
        asta_text = "ಅನ್ವಯಿಸುವುದಿಲ್ಲ (-)"
        
    # Varga Math
    d1_idx = int(deg/30)
    
    r_val = int(deg/30)
    dr_val = deg % 30
    is_odd = (r_val % 2 == 0)
    if is_odd: d2_idx = 4 if dr_val < 15 else 3
    else: d2_idx = 3 if dr_val < 15 else 4
    
    if dr_val < 10: d3_idx = d1_idx
    elif dr_val < 20: d3_idx = (d1_idx + 4) % 12
    else: d3_idx = (d1_idx + 8) % 12
    
    d9_exact = (deg * 9) % 360
    d9_idx = int(d9_exact / 30)
    
    d12_exact = (deg * 12) % 360
    d12_idx = int(d12_exact / 30)
    
    if is_odd:
        if dr_val < 5: d30_idx = 0
        elif dr_val < 10: d30_idx = 10
        elif dr_val < 18: d30_idx = 8
        elif dr_val < 25: d30_idx = 2
        else: d30_idx = 6
    else:
        if dr_val < 5: d30_idx = 5
        elif dr_val < 12: d30_idx = 2
        elif dr_val < 20: d30_idx = 8
        elif dr_val < 25: d30_idx = 10
        else: d30_idx = 0
        
    d9_dr = d9_exact % 30
    if d9_dr < 10: d9_d3_idx = d9_idx; d9_part = " 1"
    elif d9_dr < 20: d9_d3_idx = (d9_idx + 4) % 12; d9_part = " 2"
    else: d9_d3_idx = (d9_idx + 8) % 12; d9_part = " 3"
    
    d12_dr = d12_exact % 30
    if d12_dr < 10: d12_d3_idx = d12_idx; d12_part = " 1"
    elif d12_dr < 20: d12_d3_idx = (d12_idx + 4) % 12; d12_part = " 2"
    else: d12_d3_idx = (d12_idx + 8) % 12; d12_part = " 3"
    
    h_arr = []
    h_arr.append("<div class='card'><table class='key-val-table'>")
    h_arr.append("<tr><td class='key'>ಸ್ಫುಟ (Sphuta)</td><td>" + deg_fmt + "</td></tr>")
    h_arr.append("<tr><td class='key'>ಗತಿ (Vakri/Nera)</td><td><b>" + gathi_str + "</b></td></tr>")
    h_arr.append("<tr><td class='key'>ಅಸ್ತ (Asta)</td><td><b>" + asta_text + "</b></td></tr>")
    h_arr.append("</table></div>")
    st.markdown("".join(h_arr), unsafe_allow_html=True)
    
    st.markdown("#### 📊 ವರ್ಗಗಳು (Vargas)")
    v_arr = []
    v_arr.append("<div class='card'><table class='key-val-table'>")
    v_arr.append("<tr><td class='key'>ರಾಶಿ</td><td>" + KN_RASHI[d1_idx] + "</td></tr>")
    v_arr.append("<tr><td class='key'>ಹೋರಾ</td><td>" + KN_RASHI[d2_idx] + "</td></tr>")
    v_arr.append("<tr><td class='key'>ದ್ರೇಕ್ಕಾಣ</td><td>" + KN_RASHI[d3_idx] + "</td></tr>")
    v_arr.append("<tr><td class='key'>ನವಾಂಶ</td><td>" + KN_RASHI[d9_idx] + "</td></tr>")
    v_arr.append("<tr><td class='key'>ದ್ವಾದಶಾಂಶ</td><td>" + KN_RASHI[d12_idx] + "</td></tr>")
    v_arr.append("<tr><td class='key'>ತ್ರಿಂಶಾಂಶ</td><td>" + KN_RASHI[d30_idx] + "</td></tr>")
    v_arr.append("</table></div>")
    st.markdown("".join(v_arr), unsafe_allow_html=True)
    
    st.markdown("#### 📐 ಉಪ-ದ್ರೇಕ್ಕಾಣ (Sub-Drekkanas)")
    sd_arr = []
    sd_arr.append("<div class='card'><table class='key-val-table'>")
    sd_arr.append("<tr><td class='key'>ರಾಶಿ ದ್ರೇಕ್ಕಾಣ</td><td>" + KN_RASHI[d3_idx] + "</td></tr>")
    sd_arr.append("<tr><td class='key'>ನವಾಂಶ ದ್ರೇಕ್ಕಾಣ</td><td>" + KN_RASHI[d9_d3_idx] + d9_part + "</td></tr>")
    sd_arr.append("<tr><td class='key'>ದ್ವಾದಶಾಂಶ ದ್ರೇಕ್ಕಾಣ</td><td>" + KN_RASHI[d12_d3_idx] + d12_part + "</td></tr>")
    sd_arr.append("</table></div>")
    st.markdown("".join(sd_arr), unsafe_allow_html=True)

# ==========================================
# 6. SESSION STATE & UI
# ==========================================
if 'page' not in st.session_state: 
    st.session_state.page = "input"
if 'data' not in st.session_state: 
    st.session_state.data = {}
if 'notes' not in st.session_state: 
    st.session_state.notes = ""
    
if 'name_input' not in st.session_state: 
    st.session_state.name_input = ""
if 'place_input' not in st.session_state: 
    st.session_state.place_input = "Yellapur"
if 'lat' not in st.session_state: 
    st.session_state.lat = 14.98
if 'lon' not in st.session_state: 
    st.session_state.lon = 74.73

if 'dob_input' not in st.session_state:
    tz_ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now = datetime.datetime.now(tz_ist)
    
    st.session_state.dob_input = now.date()
    
    h24 = now.hour
    h12 = h24 % 12
    if h12 == 0:
        h12 = 12
        
    st.session_state.h_input = h12
    st.session_state.m_input = now.minute
    
    if h24 < 12:
        st.session_state.ampm_input = "AM"
    else:
        st.session_state.ampm_input = "PM"

st.markdown('<div class="header-box">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

if st.session_state.page == "input":
    with st.container():
        
        saved_db = load_db()
        if len(saved_db) > 0:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("#### 📂 ಉಳಿಸಿದ ಜಾತಕ")
            c_sel, c_btn = st.columns([3, 1])
            k_list = [""] + list(saved_db.keys())
            
            sel_n = c_sel.selectbox("Select", k_list, label_visibility="collapsed")
            
            if c_btn.button("Open", use_container_width=True):
                if sel_n != "":
                    prof = saved_db[sel_n]
                    st.session_state.name_input = sel_n
                    
                    dt_obj = datetime.datetime.strptime(prof['d'], "%Y-%m-%d")
                    st.session_state.dob_input = dt_obj.date()
                    
                    st.session_state.h_input = prof['h']
                    st.session_state.m_input = prof['m']
                    st.session_state.ampm_input = prof['ampm']
                    st.session_state.lat = prof['lat']
                    st.session_state.lon = prof['lon']
                    st.session_state.place_input = prof['p']
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### ✨ ಹೊಸ ಜಾತಕ")
        
        name = st.text_input("ಹೆಸರು", key="name_input")
        
        d_min = datetime.date(1800, 1, 1)
        d_max = datetime.date(2100, 12, 31)
        
        dob = st.date_input(
            "ದಿನಾಂಕ", 
            key="dob_input", 
            min_value=d_min, 
            max_value=d_max
        )
        
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("ಗಂಟೆ", 1, 12, key="h_input")
        m = c2.number_input("ನಿಮಿಷ", 0, 59, key="m_input")
        ampm = c3.selectbox("M", ["AM", "PM"], key="ampm_input")
        
        place_q = st.text_input("ಊರು ಹುಡುಕಿ", key="place_input")
        if st.button("ಹುಡುಕಿ"):
            try:
                loc = geolocator.geocode(place_q)
                if loc: 
                    st.session_state.lat = loc.latitude
                    st.session_state.lon = loc.longitude
                    st.success("📍 " + loc.address)
            except: 
                st.error("Error connecting to location service.")
                
        lat = st.number_input("Latitude", key="lat", format="%.4f")
        lon = st.number_input("Longitude", key="lon", format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0)
            h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            
            p1, p2, p3, p4, p5 = get_full_calculations(jd, lat, lon, dob)
            
            st.session_state.data = {
                "pos": p1, "pan": p2, "details": p3, "bhavas": p4, "speeds": p5
            }
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    pos = st.session_state.data['pos']
    pan = st.session_state.data['pan']
    details = st.session_state.data['details'] 
    bhavas = st.session_state.data['bhavas']
    speeds = st.session_state.data['speeds']
    
    c_bk, c_sv = st.columns(2)
    
    if c_bk.button("⬅️ ಹಿಂದಕ್ಕೆ"): 
        st.session_state.page = "input"
        st.rerun()
        
    if c_sv.button("💾 ಉಳಿಸಿ"):
        d_str = st.session_state.dob_input.strftime("%Y-%m-%d")
        
        prof_data = {
            "d": d_str,
            "h": st.session_state.h_input,
            "m": st.session_state.m_input,
            "ampm": st.session_state.ampm_input,
            "lat": st.session_state.lat,
            "lon": st.session_state.lon,
            "p": st.session_state.place_input
        }
        
        n_val = st.session_state.name_input
        if n_val == "":
            n_val = "Unknown_" + d_str
            
        save_db(n_val, prof_data)
        st.success("ಉಳಿಸಲಾಗಿದೆ! (Saved successfully)")
    
    tabs = ["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಭಾವ", "ದ್ರೇಕ್ಕಾಣ", "ಟಿಪ್ಪಣಿ", "ಚಂದಾದಾರಿಕೆ", "ಬಗ್ಗೆ"]
    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs(tabs)
    
    with t1:
        c_v, c_b = st.columns(2)
        
        d_names = {
            1: "ರಾಶಿ", 
            2: "ಹೋರಾ",
            3: "ದ್ರೇಕ್ಕಾಣ", 
            9: "ನವಾಂಶ", 
            12: "ದ್ವಾದಶಾಂಶ", 
            30: "ತ್ರಿಂಶಾಂಶ"
        }
        
        opts = [1, 2, 3, 9, 12, 30]
        v_opt = c_v.selectbox("ವರ್ಗ", opts, format_func=lambda x: d_names[x])
        
        mode_opts = ["ರಾಶಿ", "ಭಾವ"]
        c_mode = c_b.radio("ಚಾರ್ಟ್ ವಿಧ", mode_opts, horizontal=True)
        b_opt = (c_mode == "ಭಾವ")
        
        bxs = {i: "" for i in range(12)}
        ld = pos[KN_PLANETS["Lagna"]] 
        
        for n, d in pos.items():
            if v_opt == 1: 
                if not b_opt:
                    ri = int(d/30)
                else:
                    ri = (int(ld/30) + int(((d - ld + 360)%360 + 15)/30)) % 12
            elif v_opt == 2:
                r = int(d/30)
                dr = d % 30
                is_odd_sign = (r % 2 == 0)
                if is_odd_sign:
                    if dr < 15: ri = 4 
                    else: ri = 3 
                else:
                    if dr < 15: ri = 3 
                    else: ri = 4 
            elif v_opt == 30: 
                r = int(d/30)
                dr = d%30
                is_odd = (r % 2 == 0)
                if is_odd:
                    if dr < 5: ri = 0
                    elif dr < 10: ri = 10
                    elif dr < 18: ri = 8
                    elif dr < 25: ri = 2
                    else: ri = 6
                else:
                    if dr < 5: ri = 5
                    elif dr < 12: ri = 2
                    elif dr < 20: ri = 8
                    elif dr < 25: ri = 10
                    else: ri = 0
            elif v_opt == 9: 
                block = int(d/30)%4
                start = [0, 9, 6, 3][block]
                steps = int((d%30)/3.33333)
                ri = (start + steps) % 12
            elif v_opt == 3: 
                ri = (int(d/30) + (int((d%30)/10)*4)) % 12
            elif v_opt == 12: 
                ri = (int(d/30) + int((d%30)/2.5)) % 12
            else: 
                ri = int(d/30)
                
            if n in ["ಲಗ್ನ", "ಮಾಂದಿ"]:
                cls = "hi"
            else:
                cls = "pl"
                
            bxs[ri] += "<div class='" + cls + "'>" + n + "</div>"
            
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        
        glines = []
        glines.append("<div class='grid-container'>")
        
        c_count = 0
        for idx in grid:
            if idx is None:
                if c_count == 0: 
                    g_txt = "<div class='center-box'>ಭಾರತೀಯಮ್<br>"
                    g_txt += d_names[v_opt] + "</div>"
                    glines.append(g_txt)
                    c_count = 1
            else: 
                bx_str = "<div class='box'><span class='lbl'>" 
                bx_str += KN_RASHI[idx] + "</span>" + bxs[idx] + "</div>"
                glines.append(bx_str)
                
        glines.append("</div>")
        st.markdown("".join(glines), unsafe_allow_html=True)
        
        # --- PLANET INSPECTOR BUTTONS (TRIGGERS POPUP) ---
        st.markdown("<br><h4 style='text-align:center; color:#2B6CB0;'>🔍 ಗ್ರಹಗಳ ವಿಸ್ತೃತ ವಿವರ (Click Planet)</h4>", unsafe_allow_html=True)
        btn_cols = st.columns(4)
        p_list = ["ಲಗ್ನ", "ರವಿ", "ಚಂದ್ರ", "ಕುಜ", "ಬುಧ", "ಗುರು", "ಶುಕ್ರ", "ಶನಿ", "ರಾಹು", "ಕೇತು", "ಮಾಂದಿ"]
        
        for i, p_n in enumerate(p_list):
            if btn_cols[i % 4].button(p_n, key="pop_" + p_n, use_container_width=True):
                show_planet_popup(p_n, pos[p_n], speeds.get(p_n, 0), pos["ರವಿ"])
    
    with t2:
        slines = []
        slines.append("<div class='card'><table class='key-val-table'>")
        slines.append("<tr><th>ಗ್ರಹ</th><th>ರಾಶಿ</th>")
        slines.append("<th style='text-align:right'>ಅಂಶ</th>")
        slines.append("<th style='text-align:right'>ನಕ್ಷತ್ರ</th></tr>")
        
        for p, d in pos.items():
            r_name = KN_RASHI[int(d/30)]
            d1 = str(int(d%30))
            d2 = str(int((d%30*60)%60))
            deg_fmt = d1 + "° " + d2 + "'"
            nak_name = details[p]["nak"]
            pada_num = str(details[p]["pada"])
            
            sr = "<tr><td><b>" + p + "</b></td><td>" + r_name + "</td>"
            sr += "<td style='text-align:right'>" + deg_fmt + "</td>"
            sr += "<td style='text-align:right'>" + nak_name + "-"
            sr += pada_num + "</td></tr>"
            slines.append(sr)
            
        slines.append("</table></div>")
        st.markdown("".join(slines), unsafe_allow_html=True)
        
    with t3:
        bal_txt = "ಶಿಷ್ಟ ದಶೆ: " + pan['lord_bal'] + " ಉಳಿಕೆ: " + pan['d_bal']
        ht = "<div class='card' style='color:#DD6B20; font-weight:900;'>"
        ht += bal_txt + "</div>"
        st.markdown(ht, unsafe_allow_html=True)
        
        dlines = []
        cur_d = pan['date_obj']
        si = pan['n_idx'] % 9
        
        for i in range(9):
            im = (si + i) % 9
            y_mul = (1 - pan['perc']) if i == 0 else 1
            md_dur = YEARS[im] * y_mul
            md_end = cur_d + datetime.timedelta(days=md_dur*365.25)
            
            dlines.append("<details><summary class='md-node'><span>")
            dlines.append(LORDS[im] + "</span><span class='date-label'>")
            dlines.append(md_end.strftime('%d-%m-%y') + "</span></summary>")
            
            cad = cur_d
            for j in range(9):
                ia = (im + j) % 9
                ad_y = (YEARS[im] * YEARS[ia] / 120.0)
                if i == 0: ad_y *= (1 - pan['perc'])
                ae = cad + datetime.timedelta(days=ad_y*365.25)
                
                dlines.append("<details><summary class='ad-node'><span>")
                dlines.append(LORDS[ia] + "</span><span class='date-label'>")
                dlines.append(ae.strftime('%d-%m-%y') + "</span></summary>")
                
                cpd = cad
                for k in range(9):
                    ip = (ia + k) % 9
                    pd_y = (ad_y * YEARS[ip] / 120.0)
                    pe = cpd + datetime.timedelta(days=pd_y*365.25)
                    
                    p_div = "<div class='pd-node' style='padding:10px 15px; "
                    p_div += "border-bottom:1px solid #EDF2F7; display:flex; "
                    p_div += "justify-content:space-between'><span>"
                    p_div += LORDS[ip] + "</span><span>" 
                    p_div += pe.strftime('%d-%m-%y') + "</span></div>"
                    
                    dlines.append(p_div)
                    cpd = pe
                dlines.append("</details>")
                cad = ae
            dlines.append("</details>")
            cur_d = md_end
            
        st.markdown("".join(dlines), unsafe_allow_html=True)
    
    with t4:
        p_lines = []
        p_lines.append("<div class='card'><table class='key-val-table'>")
        
        arr = [
            ("ವಾರ", str(pan['v'])),
            ("ತಿಥಿ", str(pan['t'])),
            ("ನಕ್ಷತ್ರ", str(pan['n'])),
            ("ಯೋಗ", str(pan['y'])),
            ("ಕರಣ", str(pan['k'])),
            ("ಚಂದ್ರ ರಾಶಿ", str(pan['r'])),
            ("ಉದಯಾದಿ ಘಟಿ", str(pan['udayadi'])),
            ("ಗತ ಘಟಿ", str(pan['gata'])),
            ("ಪರಮ ಘಟಿ", str(pan['parama'])),
            ("ಶೇಷ ಘಟಿ", str(pan['rem']))
        ]
        
        for k, v in arr:
            p_lines.append("<tr><td class='key'>" + k + "</td><td>")
            p_lines.append(v + "</td></tr>")
            
        p_lines.append("</table></div>")
        st.markdown("".join(p_lines), unsafe_allow_html=True)
            
    with t5:
        blines = []
        blines.append("<div class='card'><table class='key-val-table'>")
        blines.append("<tr><th>ಭಾವ</th><th>ಮಧ್ಯ (Sphuta)</th>")
        blines.append("<th>ರಾಶಿ</th></tr>")
        
        for i, deg in enumerate(bhavas):
            bhava_num = str(i + 1)
            r_name = KN_RASHI[int(deg/30)]
            d1 = str(int(deg%30))
            d2 = str(int((deg%30*60)%60))
            d_fmt = d1 + "° " + d2 + "'"
            
            br = "<tr><td><b>" + bhava_num + "</b></td><td>" + d_fmt
            br += "</td><td>" + r_name + "</td></tr>"
            blines.append(br)
            
        blines.append("</table></div>")
        st.markdown("".join(blines), unsafe_allow_html=True)
        
    with t6:
        nlines = []
        nlines.append("<div class='card'><table class='key-val-table'>")
        
        nlines.append("<tr><th>ಗ್ರಹ</th><th>ಅಂಶ</th>")
        nlines.append("<th>ರಾಶಿ ದ್ರೇಕ್ಕಾಣ</th><th>ನವಾಂಶ ದ್ರೇಕ್ಕಾಣ</th>")
        nlines.append("<th>ದ್ವಾದಶಾಂಶ ದ್ರೇಕ್ಕಾಣ</th></tr>")
        
        for p, d in pos.items():
            
            d1_v1 = str(int(d%30))
            d1_v2 = str(int((d%30*60)%60))
            deg_fmt = d1_v1 + "° " + d1_v2 + "'"
            
            d1_idx = int(d / 30)
            d1_name = KN_RASHI[d1_idx]
            deg_in_d1 = d % 30
            if deg_in_d1 < 10: p1_part = " 1"
            elif deg_in_d1 < 20: p1_part = " 2"
            else: p1_part = " 3"
            d3_d1_str = d1_name + p1_part
            
            d9_exact = (d * 9) % 360
            d9_idx = int(d9_exact / 30)
            d9_name = KN_RASHI[d9_idx]
            deg_in_d9 = d9_exact % 30
            if deg_in_d9 < 10: p9_part = " 1"
            elif deg_in_d9 < 20: p9_part = " 2"
            else: p9_part = " 3"
            d3_d9_str = d9_name + p9_part
            
            d12_exact = (d * 12) % 360
            d12_idx = int(d12_exact / 30)
            d12_name = KN_RASHI[d12_idx]
            deg_in_d12 = d12_exact % 30
            if deg_in_d12 < 10: p12_part = " 1"
            elif deg_in_d12 < 20: p12_part = " 2"
            else: p12_part = " 3"
            d3_d12_str = d12_name + p12_part
            
            nr = "<tr><td><b>" + p + "</b></td><td>" + deg_fmt
            nr += "</td><td>" + d3_d1_str + "</td><td>" 
            nr += d3_d9_str + "</td><td>" + d3_d12_str + "</td></tr>"
            
            nlines.append(nr)
            
        nlines.append("</table></div>")
        st.markdown("".join(nlines), unsafe_allow_html=True)

    with t7:
        val = st.session_state.notes
        st.session_state.notes = st.text_area("ಟಿಪ್ಪಣಿಗಳು", value=val, height=300)

    with t8:
        st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("### 🚫 ಜಾಹೀರಾತು-ಮುಕ್ತ")
        
        info_text = "<p style='color:#718096; font-weight:600;'>ಜಾಹೀರಾತುಗಳಿಲ್ಲದೆ ನಿರಂತರವಾಗಿ ಆ್ಯಪ್ ಬಳಸಿ.<br></p>"
        st.markdown(info_text, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Remove Ads (₹99)", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with t9:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### ಭಾರತೀಯಮ್")
        
        info = "<p style='color:#4A5568; font-size:14px; line-height:1.6;'>"
        info += "<b>ಆವೃತ್ತಿ: 1.0.0</b><br><br>"
        info += "ನಿಖರವಾದ ವೈದಿಕ ಜ್ಯೋತಿಷ್ಯ ಲೆಕ್ಕಾಚಾರಗಳಿಗಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.</p>"
        st.markdown(info, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.link_button("</> Source Code", "https://github.com/your-username/bharatheeyam", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
