import streamlit as st
import swisseph as swe
import datetime
import math
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & THEME
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered", page_icon="🕉️", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    .stApp { background-color: #FFFBF0 !important; font-family: 'Noto Sans Kannada', sans-serif; color: #1F1F1F !important; }
    .header-box { background: linear-gradient(135deg, #6A040F, #9D0208); color: #FFFFFF !important; padding: 16px; text-align: center; font-weight: 900; font-size: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(106, 4, 15, 0.3); border-bottom: 4px solid #FAA307; }
    div[data-testid="stInput"] { background-color: white; border-radius: 8px; border: 1px solid #E0E0E0; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #9D0208 !important; color: white !important; font-weight: bold; border: none; padding: 12px; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #D00000 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    button[kind="secondary"] { background-color: #FFFFFF !important; color: #9D0208 !important; border: 2px solid #9D0208 !important; }
    div[data-testid="stTabs"] button { background-color: transparent !important; }
    div[data-testid="stTabs"] button[aria-selected="false"] p { color: #5D4037 !important; font-weight: 700 !important; font-size: 14px !important; }
    div[data-testid="stTabs"] button[aria-selected="true"] p { color: #9D0208 !important; font-weight: 900 !important; font-size: 15px !important; }
    div[data-testid="stTabs"] button[aria-selected="true"] { border-bottom: 4px solid #9D0208 !important; }
    .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 100%; max-width: 380px; aspect-ratio: 1 / 1; margin: 0 auto; gap: 2px; background: #370617; border: 4px solid #6A040F; border-radius: 4px; }
    .box { background: #FFFFFF; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; padding: 2px; text-align: center; color: #000000 !important; }
    .center-box { grid-column: 2/4; grid-row: 2/4; background: linear-gradient(135deg, #FFBA08, #FAA307); display: flex; flex-direction: column; align-items: center; justify-content: center; color: #370617 !important; font-weight: 900; text-align: center; font-size: 13px; }
    .lbl { position: absolute; top: 2px; left: 3px; font-size: 9px; color: #DC2F02 !important; font-weight: 900; }
    .hi { color: #D00000 !important; text-decoration: underline; font-weight: 900; }
    .pl { color: #03071E !important; font-weight: bold; }
    .card { background: #FFFFFF; border-radius: 12px; padding: 15px; margin-bottom: 12px; border: 1px solid #F0F0F0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .key { color: #9D0208 !important; font-weight: 900; width: 40%; }
    .key-val-table td { border-bottom: 1px solid #f0f0f0; padding: 10px 4px; color: #333 !important; }
    details { margin-bottom: 6px; border: 1px solid #eee; border-radius: 8px; overflow: hidden; background: white; }
    summary { padding: 12px; font-size: 14px; border-bottom: 1px solid #f5f5f5; color: #000 !important; }
    .md-node { background: #6A040F !important; color: #FFFFFF !important; font-weight: 900; }
    .md-node span { color: white !important; }
    .ad-node { background: #FFEFD5 !important; color: #9D0208 !important; font-weight: 700; border-left: 6px solid #FAA307; }
    .ad-node span { color: #9D0208 !important; }
    .pd-node { background: #F1F8E9 !important; color: #1B5E20 !important; font-weight: 700; border-left: 6px solid #558B2F; }
    .pd-node span { color: #1B5E20 !important; }
    .sd-node { background: #F5F9FF !important; color: #0D47A1 !important; font-size: 11px; margin-left: 10px; border-left: 3px solid #2196F3; padding: 8px; }
    .sd-node span { color: #0D47A1 !important; }
    .date-label { font-size: 11px; opacity: 0.9; float: right; font-weight: normal; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v7_bulletproof")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಘ", "ಪೂರ್ವ ಫಾಲ್ಗುಣಿ", "ಉತ್ತರ ಫಾಲ್ಗುಣಿ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜ್ಯೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
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

def jd_to_time_str(jd):
    dt = datetime.datetime.fromtimestamp((jd - 2440587.5) * 86400.0)
    return dt.strftime("%I:%M:%S %p")

# ==========================================
# 3. CALCULATIONS
# ==========================================
def calculate_mandi(jd_birth, lat, lon, dob_obj):
    sr_civil, ss_civil = find_sunrise_set_for_date(dob_obj.year, dob_obj.month, dob_obj.day, lat, lon)
    py_weekday = dob_obj.weekday()
    civil_weekday_idx = (py_weekday + 1) % 7 
    
    is_night = False
    if jd_birth >= sr_civil and jd_birth < ss_civil: is_night = False
    else: is_night = True
        
    start_base = 0.0; duration = 0.0; vedic_wday = 0; panch_sr = 0.0
    
    if not is_night:
        vedic_wday = civil_weekday_idx
        panch_sr = sr_civil
        start_base = sr_civil
        duration = ss_civil - sr_civil
    else:
        if jd_birth < sr_civil:
            vedic_wday = (civil_weekday_idx - 1) % 7
            prev_date = dob_obj - datetime.timedelta(days=1)
            prev_sr, prev_ss = find_sunrise_set_for_date(prev_date.year, prev_date.month, prev_date.day, lat, lon)
            start_base = prev_ss
            duration = sr_civil - prev_ss
            panch_sr = prev_sr
        else:
            vedic_wday = civil_weekday_idx
            next_date = dob_obj + datetime.timedelta(days=1)
            next_sr, _ = find_sunrise_set_for_date(next_date.year, next_date.month, next_date.day, lat, lon)
            start_base = ss_civil
            duration = next_sr - ss_civil
            panch_sr = sr_civil

    if not is_night: factors = [26, 22, 18, 14, 10, 6, 2] 
    else: factors = [10, 6, 2, 26, 22, 18, 14] 
    factor = factors[vedic_wday]
    mandi_jd = start_base + (duration * factor / 30.0)
    
    return mandi_jd, is_night, panch_sr, vedic_wday, start_base

def get_full_calculations(jd_birth, lat, lon, dob_obj):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd_birth)
    positions = {}
    extra_details = {}
    
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        deg = (swe.calc_ut(jd_birth, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
        positions[KN_PLANETS[pid]] = deg
        nak_idx = int(deg / 13.333333333)
        pada = int((deg % 13.333333333) / 3.333333333) + 1
        extra_details[KN_PLANETS[pid]] = {"nak": KN_NAK[nak_idx % 27], "pada": pada}

    rahu = (swe.calc_ut(jd_birth, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]], positions[KN_PLANETS[102]] = rahu, (rahu + 180) % 360
    
    for p, d in [(KN_PLANETS[101], rahu), (KN_PLANETS[102], (rahu + 180)%360)]:
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
    extra_details[KN_PLANETS["Lagna"]] = {"nak": KN_NAK[nak_idx % 27], "pada": pada}

    mandi_time_jd, is_night, panch_sr, w_idx, debug_base = calculate_mandi(jd_birth, lat, lon, dob_obj)
    mandi_deg = (swe.houses(mandi_time_jd, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mandi_time_jd)) % 360
    positions[KN_PLANETS["Ma"]] = mandi_deg
    
    nak_idx = int(mandi_deg / 13.333333333)
    pada = int((mandi_deg % 13.333333333) / 3.333333333) + 1
    extra_details[KN_PLANETS["Ma"]] = {"nak": KN_NAK[nak_idx % 27], "pada": pada}

    m_deg, s_deg = positions["ಚಂದ್ರ"], positions["ರವಿ"]
    t_idx = int(((m_deg - s_deg + 360) % 360) / 12)
    n_idx = int(m_deg / 13.333333333)
    js = find_nak_limit(jd_birth, n_idx * 13.333333333); je = find_nak_limit(jd_birth, (n_idx + 1) * 13.333333333)
    perc = (m_deg % 13.333333333) / 13.333333333
    bal = YEARS[n_idx % 9] * (1 - perc)
    
    pan = {
        "t": KN_TITHI[min(t_idx, 29)], 
        "v": KN_VARA[w_idx], 
        "n": KN_NAK[n_idx % 27],
        "sr": panch_sr, 
        "udayadi": fmt_ghati((jd_birth - panch_sr) * 60), 
        "gata": fmt_ghati((jd_birth - js) * 60), 
        "parama": fmt_ghati((je - js) * 60), 
        "rem": fmt_ghati((je - jd_birth) * 60),
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(bal)}ವ {int((bal%1)*12)}ತಿ",
        "n_idx": n_idx, "perc": perc, "date_obj": datetime.datetime.fromtimestamp((jd_birth - 2440587.5) * 86400.0),
        "m_period": "Night" if is_night else "Day",
        "m_time": jd_to_time_str(mandi_time_jd),
        "m_base": jd_to_time_str(debug_base)
    }
    return positions, pan, extra_details, bhava_sphutas

# ==========================================
# 4. SESSION STATE & UI
# ==========================================
if 'page' not in st.session_state: st.session_state.page = "input"
if 'data' not in st.session_state: st.session_state.data = {}
if 'notes' not in st.session_state: st.session_state.notes = ""
if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lon = 14.98, 74.73

st.markdown('<div class="header-box">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)

if st.session_state.page == "input":
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.info("ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ (Enter Details)")
        name = st.text_input("ಹೆಸರು", "ಬಳಕೆದಾರ")
        dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
        c1, c2, c3 = st.columns(3)
        h, m, ampm = c1.number_input("ಗಂಟೆ", 1, 12, 2), c2.number_input("ನಿಮಿಷ", 0, 59, 43), c3.selectbox("M", ["AM", "PM"], index=0)
        place_q = st.text_input("ಊರು ಹುಡುಕಿ", "Yellapur")
        if st.button("ಹುಡುಕಿ"):
            try:
                loc = geolocator.geocode(place_q)
                if loc: st.session_state.lat, st.session_state.lon = loc.latitude, loc.longitude; st.success(f"📍 {loc.address}")
            except: st.error("Error")
        lat = st.number_input("Lat", value=st.session_state.lat, format="%.4f"); lon = st.number_input("Lon", value=st.session_state.lon, format="%.4f")
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0); h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            pos, pan, details, bhavas = get_full_calculations(jd, lat, lon, dob)
            st.session_state.data = {"pos": pos, "pan": pan, "details": details, "bhavas": bhavas}; st.session_state.page = "dashboard"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    pos = st.session_state.data['pos']
    pan = st.session_state.data['pan']
    details = st.session_state.data['details'] 
    bhavas = st.session_state.data['bhavas']   
    
    if st.button("⬅️ ಹಿಂದಕ್ಕೆ"): st.session_state.page = "input"; st.rerun()
    t1, t2, t3, t4, t5, t6 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಭಾವ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        c_v, c_b = st.columns([2, 1])
        v_opt = c_v.selectbox("ವರ್ಗ", [1, 3, 9, 12, 30], format_func=lambda x: f"D{x}")
        b_opt = c_b.checkbox("ಭಾವ", value=False)
        bxs = {i: "" for i in range(12)}; 
        ld = pos[KN_PLANETS["Lagna"]] 
        for n, d in pos.items():
            if v_opt == 1: ri = int(d/30) if not b_opt else (int(ld/30) + int(((d - ld + 360) % 360 + 15) / 30)) % 12
            elif v_opt == 30: 
                r = int(d/30); dr = d%30; is_odd = (int(d/30) % 2 == 0)
                ri = (0 if dr<5 else 10 if dr<10 else 8 if dr<18 else 2 if dr<25 else 6) if is_odd else (5 if dr<5 else 2 if dr<12 else 8 if dr<20 else 10 if dr<25 else 0)
            else:
                if v_opt == 9: block = int(d/30)%4; start = [0, 9, 6, 3][block]; steps = int((d%30)/3.33333); ri = (start + steps) % 12
                elif v_opt == 3: ri = (int(d/30) + (int((d%30)/10)*4)) % 12
                elif v_opt == 12: ri = (int(d/30) + int((d%30)/2.5)) % 12
                else: ri = int(d/30)
            cls = "hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl"
            bxs[ri] += f'<div class="{cls}">{n}</div>'
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for idx in grid:
            if idx is None:
                if html.count("center-box") == 0: html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v_opt}</div>'
            else: html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)
    
    with t2:
        # BULLETPROOF HTML CONSTRUCTION (No f-string concatenation issues)
        html_lines = ["<div class='card'><table class='key-val-table'><tr><th>ಗ್ರಹ</th><th>ರಾಶಿ</th><th style='text-align:right'>ಅಂಶ</th><th style='text-align:right'>ನಕ್ಷತ್ರ</th></tr>"]
        for p, d in pos.items():
            r_name = KN_RASHI[int(d/30)]
            deg_fmt = f"{int(d%30)}° {int((d%30*60)%60)}'"
            nak_name = details[p]["nak"]
            pada_num = details[p]["pada"]
            row_html = "<tr><td><b>" + p + "</b></td><td>" + r_name + "</td><td style='text-align:right'>" + deg_fmt + "</td><td style='text-align:right'>" + nak_name + "-" + str(pada_num) + "</td></tr>"
            html_lines.append(row_html)
        html_lines.append("</table></div>")
        st.markdown("".join(html_lines), unsafe_allow_html=True)
        
    with t3:
        st.markdown(f"<div class='card' style='color:#6A040F; font-weight:bold;'>ಶಿಷ್ಟ ದಶೆ: {pan['d_bal']}</div>", unsafe_allow_html=True)
        dh = ""; cur_d = pan['date_obj']; si = pan['n_idx'] % 9
        for i in range(9):
            im = (si + i) % 9; md_dur = YEARS[im] * ((1 - pan['perc']) if i==0 else 1); md_end = cur_d + datetime.timedelta(days=md_dur*365.25)
            dh += f"<details><summary class='md-node'><span>{LORDS[im]}</span><span class='date-label'>{md_end.strftime('%d-%m-%y')}</span></summary>"
            cad = cur_d
            for j in range(9):
                ia = (im + j) % 9; ad_y = (YEARS[im] * YEARS[ia] / 120.0)
                if i == 0: ad_y *= (1 - pan['perc'])
                ae = cad + datetime.timedelta(days=ad_y*365.25); dh += f"<details><summary class='ad-node'><span>{LORDS[ia]}</span><span class='date-label'>{ae.strftime('%d-%m-%y')}</span></summary>"; cpd = cad
                for k in range(9):
                    ip = (ia + k) % 9; pd_y = (ad_y * YEARS[ip] / 120.0); pe = cpd + datetime.timedelta(days=pd_y*365.25)
                    dh += f"<div class='pd-node' style='padding:8px 15px; border-bottom:1px solid #eee; display:flex; justify-content:space-between'><span>{LORDS[ip]}</span><span>{pe.strftime('%d-%m-%y')}</span></div>"; cpd = pe
                dh += "</details>"; cad = ae
            dh += "</details>"; cur_d = md_end
        st.markdown(dh, unsafe_allow_html=True)
    
    with t4:
        # BULLETPROOF PANCHANGA HTML CONSTRUCTION
        panch_data = [
            ("ವಾರ", str(pan['v'])),
            ("ತಿಥಿ", str(pan['t'])),
            ("ನಕ್ಷತ್ರ", str(pan['n'])),
            ("ಉದಯಾದಿ", str(pan['udayadi']) + " ಘಟಿ"),
            ("ಗತ", str(pan['gata']) + " ಘಟಿ"),
            ("ಪರಮ", str(pan['parama']) + " ಘಟಿ"),
            ("ಶೇಷ", str(pan['rem']) + " ಘಟಿ"),
            ("ಮಾಂದಿ ಕಾಲ", str(pan['m_period']) + " (" + str(pan['m_time']) + ")"),
            ("ಆಧಾರ ಸಮಯ", str(pan['m_base']))
        ]
        
        p_lines = ["<div class='card'><table class='key-val-table'>"]
        for key, val in panch_data:
            p_lines.append("<tr><td class='key'>" + key + "</td><td>" + val + "</td></tr>")
        p_lines.append("</table></div>")
        st.markdown("".join(p_lines), unsafe_allow_html=True)
            
    with t5:
        # BULLETPROOF BHAVA HTML CONSTRUCTION
        b_lines = ["<div class='card'><table class='key-va