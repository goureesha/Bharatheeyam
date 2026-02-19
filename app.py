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
    page_title="ಭಾರತೀಯಮ್", 
    layout="centered", 
    page_icon="🕉️", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    
    .stApp { 
        background-color: #FFFBF0 !important; 
        font-family: 'Noto Sans Kannada', sans-serif; 
        color: #1F1F1F !important; 
    }
    .header-box { 
        background: linear-gradient(135deg, #6A040F, #9D0208); 
        color: #FFFFFF !important; 
        padding: 16px; 
        text-align: center; 
        font-weight: 900; 
        font-size: 24px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 15px rgba(106, 4, 15, 0.3); 
        border-bottom: 4px solid #FAA307; 
    }
    div[data-testid="stInput"] { 
        background-color: white; 
        border-radius: 8px; 
        border: 1px solid #E0E0E0; 
    }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        background-color: #9D0208 !important; 
        color: white !important; 
        font-weight: bold; 
        border: none; 
        padding: 12px; 
        transition: all 0.3s ease; 
    }
    .stButton>button:hover { 
        background-color: #D00000 !important; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.2); 
    }
    button[kind="secondary"] { 
        background-color: #FFFFFF !important; 
        color: #9D0208 !important; 
        border: 2px solid #9D0208 !important; 
    }
    div[data-testid="stTabs"] button { 
        background-color: transparent !important; 
    }
    div[data-testid="stTabs"] button[aria-selected="false"] p { 
        color: #5D4037 !important; 
        font-weight: 700 !important; 
        font-size: 14px !important; 
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p { 
        color: #9D0208 !important; 
        font-weight: 900 !important; 
        font-size: 15px !important; 
    }
    div[data-testid="stTabs"] button[aria-selected="true"] { 
        border-bottom: 4px solid #9D0208 !important; 
    }
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(4, 1fr); 
        grid-template-rows: repeat(4, 1fr); 
        width: 100%; max-width: 380px; 
        aspect-ratio: 1 / 1; 
        margin: 0 auto; gap: 2px; 
        background: #370617; 
        border: 4px solid #6A040F; 
        border-radius: 4px; 
    }
    .box { 
        background: #FFFFFF; 
        position: relative; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        font-size: 11px; 
        font-weight: bold; 
        padding: 2px; 
        text-align: center; 
        color: #000000 !important; 
    }
    .center-box { 
        grid-column: 2/4; 
        grid-row: 2/4; 
        background: linear-gradient(135deg, #FFBA08, #FAA307); 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        color: #370617 !important; 
        font-weight: 900; 
        text-align: center; 
        font-size: 13px; 
    }
    .lbl { 
        position: absolute; top: 2px; left: 3px; 
        font-size: 9px; color: #DC2F02 !important; 
        font-weight: 900; 
    }
    .hi { color: #D00000 !important; text-decoration: underline; font-weight: 900; }
    .pl { color: #03071E !important; font-weight: bold; }
    .card { 
        background: #FFFFFF; border-radius: 12px; padding: 15px; 
        margin-bottom: 12px; border: 1px solid #F0F0F0; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
    }
    .key { color: #9D0208 !important; font-weight: 900; width: 40%; }
    .key-val-table td { 
        border-bottom: 1px solid #f0f0f0; 
        padding: 10px 4px; color: #333 !important; 
    }
    details { 
        margin-bottom: 6px; border: 1px solid #eee; 
        border-radius: 8px; overflow: hidden; background: white; 
    }
    summary { 
        padding: 12px; font-size: 14px; 
        border-bottom: 1px solid #f5f5f5; color: #000 !important; 
    }
    .md-node { background: #6A040F !important; color: #FFFFFF !important; font-weight: 900; }
    .md-node span { color: white !important; }
    .ad-node { 
        background: #FFEFD5 !important; color: #9D0208 !important; 
        font-weight: 700; border-left: 6px solid #FAA307; 
    }
    .ad-node span { color: #9D0208 !important; }
    .pd-node { 
        background: #F1F8E9 !important; color: #1B5E20 !important; 
        font-weight: 700; border-left: 6px solid #558B2F; 
    }
    .pd-node span { color: #1B5E20 !important; }
    .sd-node { 
        background: #F5F9FF !important; color: #0D47A1 !important; 
        font-size: 11px; margin-left: 10px; 
        border-left: 3px solid #2196F3; padding: 8px; 
    }
    .sd-node span { color: #0D47A1 !important; }
    .date-label { font-size: 11px; opacity: 0.9; float: right; font-weight: normal; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v21_ad_free")

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
# 4. CALCULATIONS
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
    extra_details = {}
    
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        deg = (swe.calc_ut(jd_birth, pid, flag)[0][0]) % 360
        positions[KN_PLANETS[pid]] = deg
        nak_idx = int(deg / 13.333333333)
        pada = int((deg % 13.333333333) / 3.333333333) + 1
        extra_details[KN_PLANETS[pid]] = {
            "nak": KN_NAK[nak_idx % 27], 
            "pada": pada
        }

    rahu_deg = swe.calc_ut(jd_birth, swe.TRUE_NODE, flag)[0][0]
    rahu = rahu_deg % 360
    positions[KN_PLANETS[101]] = rahu
    positions[KN_PLANETS[102]] = (rahu + 180) % 360
    
    nodes = [
        (KN_PLANETS[101], rahu), 
        (KN_PLANETS[102], (rahu + 180) % 360)
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
    
    nak_idx = int(mandi_deg / 13.333333333)
    pada = int((mandi_deg % 13.333333333) / 3.333333333) + 1
    extra_details[KN_PLANETS["Ma"]] = {
        "nak": KN_NAK[nak_idx % 27], 
        "pada": pada
    }

    # Panchanga details
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
    return positions, pan, extra_details, bhava_sphutas

# ==========================================
# 5. SESSION STATE & UI
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
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        saved_db = load_db()
        if len(saved_db) > 0:
            st.info("ಉಳಿಸಿದ ಜಾತಕ (Saved Profiles)")
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
                    
            st.markdown("<hr>", unsafe_allow_html=True)
        
        st.info("ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ (Enter Details)")
        
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
                st.error("Error")
                
        lat = st.number_input("Lat", key="lat", format="%.4f")
        lon = st.number_input("Lon", key="lon", format="%.4f")
        
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0)
            h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            
            p1, p2, p3, p4 = get_full_calculations(jd, lat, lon, dob)
            
            st.session_state.data = {
                "pos": p1, "pan": p2, "details": p3, "bhavas": p4
            }
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    pos = st.session_state.data['pos']
    pan = st.session_state.data['pan']
    details = st.session_state.data['details'] 
    bhavas = st.session_state.data['bhavas']   
    
    c_bk, c_sv = st.columns(2)
    
    if c_bk.button("⬅️ ಹಿಂದಕ್ಕೆ"): 
        st.session_state.page = "input"
        st.rerun()
        
    if c_sv.button("💾 ಉಳಿಸಿ (Save)"):
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
        c_v, c_b = st.columns([2, 1])
        opts = [1, 3, 9, 12, 30]
        v_opt = c_v.selectbox("ವರ್ಗ", opts, format_func=lambda x: "D" + str(x))
        b_opt = c_b.checkbox("ಭಾವ", value=False)
        
        bxs = {i: "" for i in range(12)}
        ld = pos[KN_PLANETS["Lagna"]] 
        
        for n, d in pos.items():
            if v_opt == 1: 
                if not b_opt:
                    ri = int(d/30)
                else:
                    ri = (int(ld/30) + int(((d - ld + 360)%360 + 15)/30)) % 12
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
                    g_txt = "<div class='center-box'>ಭಾರತೀಯಮ್<br>D"
                    g_txt += str(v_opt) + "</div>"
                    glines.append(g_txt)
                    c_count = 1
            else: 
                bx_str = "<div class='box'><span class='lbl'>" 
                bx_str += KN_RASHI[idx] + "</span>" + bxs[idx] + "</div>"
                glines.append(bx_str)
                
        glines.append("</div>")
        st.markdown("".join(glines), unsafe_allow_html=True)
    
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
        ht = "<div class='card' style='color:#6A040F; font-weight:bold;'>"
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
                    
                    p_div = "<div class='pd-node' style='padding:8px 15px; "
                    p_div += "border-bottom:1px solid #eee; display:flex; "
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
            ("ಉದಯಾದಿ", str(pan['udayadi']) + " ಘಟಿ"),
            ("ಗತ", str(pan['gata']) + " ಘಟಿ"),
            ("ಪರಮ", str(pan['parama']) + " ಘಟಿ"),
            ("ಶೇಷ", str(pan['rem']) + " ಘಟಿ")
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
        nlines.append("<tr><th>ಗ್ರಹ</th><th>D1 ಅಂಶ</th>")
        nlines.append("<th>D1-D3</th><th>D9-D3</th>")
        nlines.append("<th>D12-D3</th></tr>")
        
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
        st.markdown("### 🚫 ಜಾಹೀರಾತು-ಮುಕ್ತ (Ad-Free)")
        
        info_text = "ಜಾಹೀರಾತುಗಳಿಲ್ಲದೆ ನಿರಂತರವಾಗಿ ಆ್ಯಪ್ ಬಳಸಿ.<br>"
        info_text += "Enjoy a seamless, distraction-free calculation experience."
        st.markdown(info_text, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Remove Ads (₹99)", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with t9:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### ಭಾರತೀಯಮ್ (Bharatheeyam)")
        
        info = "**ಆವೃತ್ತಿ (Version): 1.0.0**<br><br>"
        info += "ನಿಖರವಾದ ವೈದಿಕ ಜ್ಯೋತಿಷ್ಯ ಲೆಕ್ಕಾಚಾರಗಳಿಗಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.<br>"
        info += "Designed for precise Vedic Astrology calculations, specifically tailored for accurate Dasha, Panchanga, and Nadi sub-divisional charts. Built to operate seamlessly offline for fast and private astrological consultations."
        st.markdown(info, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.link_button("</> Source Code", "https://github.com/your-username/bharatheeyam", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
