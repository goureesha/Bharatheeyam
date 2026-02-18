import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & HIGH-CONTRAST CSS
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered", page_icon="🕉️", initial_sidebar_state="expanded")

# CSS OVERHAUL FOR VISIBILITY
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    
    /* 1. FORCE LIGHT THEME & TEXT COLOR */
    /* This overrides system Dark Mode settings */
    .stApp { 
        background-color: #fff8e1 !important; 
        font-family: 'Noto Sans Kannada', sans-serif; 
        color: #2c0e0e !important; 
    }
    
    /* Force all standard text to be dark */
    p, label, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #2c0e0e !important;
    }

    /* 2. HEADER */
    .header-box { 
        background: #800000; 
        color: #fffbe6 !important; /* Force white text on maroon header */
        padding: 12px; 
        text-align: center; 
        font-weight: 900; 
        font-size: 22px; 
        border-radius: 8px; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.15); 
        border-bottom: 3px solid #d4af37;
    }
    .header-box * { color: #fffbe6 !important; } /* Ensure children are white */

    /* 3. TABS (The specific issue you faced) */
    /* Tab Labels (Unselected) */
    button[data-baseweb="tab"] div p {
        color: #5d4037 !important;
        font-weight: bold;
    }
    /* Tab Labels (Selected) */
    button[data-baseweb="tab"][aria-selected="true"] div p {
        color: #b71c1c !important;
        font-weight: 900;
    }
    /* Tab Highlight Bar */
    div[data-testid="stTabs"] span {
        background-color: #b71c1c !important;
    }

    /* 4. INPUTS & TOGGLES (Bhava Button Fix) */
    /* Radio/Checkbox Labels */
    div[data-testid="stCheckbox"] label p {
        color: #800000 !important;
        font-weight: bold;
        font-size: 14px;
    }
    /* Dropdown/Selectbox Text */
    div[data-baseweb="select"] div {
        color: #2c0e0e !important;
    }
    /* Input Box Labels */
    div[data-testid="stMarkdownContainer"] p {
        color: #3e2723 !important;
    }

    /* 5. KUNDALI GRID (unchanged but robust) */
    .grid-container { 
        display: grid; 
        grid-template-columns: repeat(4, 1fr); 
        grid-template-rows: repeat(4, 1fr); 
        width: 100%; max-width: 380px; 
        aspect-ratio: 1 / 1; 
        margin: 0 auto; gap: 2px; 
        background: #2c0e0e; 
        border: 4px solid #800000; 
    }
    .box { 
        background: #fffcf5; 
        position: relative; 
        display: flex; flex-direction: column; 
        align-items: center; justify-content: center; 
        font-size: 11px; font-weight: bold; 
        padding: 2px; text-align: center; 
        color: #3e2723 !important; 
    }
    .center-box { 
        grid-column: 2/4; grid-row: 2/4; 
        background: #F7E7CE; 
        display: flex; flex-direction: column; 
        align-items: center; justify-content: center; 
        color: #800000 !important; 
        font-weight: 900; text-align: center; 
        border: 2px solid #d4af37; font-size: 12px;
    }
    @media only screen and (max-width: 450px) {
        .box { font-size: 9px; line-height: 1.1; }
        .lbl { font-size: 7px; top: 1px; left: 1px; }
        .header-box { font-size: 18px; padding: 10px; }
        .center-box { font-size: 10px; }
    }
    .lbl { position: absolute; top: 2px; left: 3px; font-size: 9px; color: #8d6e63 !important; font-weight: 900; }
    .hi { color: #b71c1c !important; text-decoration: underline; font-weight: 900; }
    .pl { color: #1a0000 !important; font-weight: bold; }
    
    /* 6. DATA TABLES */
    .card { background: #fffcf5; border-radius: 8px; padding: 12px; margin-bottom: 8px; border: 1px solid #e6d5c3; }
    .key-val-table { width: 100%; border-collapse: collapse; font-size: 14px; }
    .key-val-table td { border-bottom: 1px solid #eee; padding: 8px 4px; color: #3e2723 !important; }
    .key { color: #800000 !important; font-weight: 900; width: 45%; }
    
    /* 7. ACCORDION (DASHA) */
    details { margin-bottom: 4px; border: 1px solid #e0c097; border-radius: 6px; overflow: hidden; background: white; }
    summary { cursor: pointer; padding: 10px; font-size: 13px; list-style: none; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; color: #000 !important; }
    
    /* Explicit Colors for Dasha Levels */
    .md-node { background: #800000 !important; color: #fffbe6 !important; font-weight: 900; }
    .md-node span { color: #fffbe6 !important; }
    
    .ad-node { background: #FFF9C4 !important; color: #5d4037 !important; font-weight: 700; margin-left: 0px; border-left: 5px solid #FBC02D; }
    .ad-node span { color: #5d4037 !important; }

    .pd-node { background: #E8F5E9 !important; color: #1B5E20 !important; font-weight: 700; margin-left: 5px; border-left: 4px solid #43A047; }
    .pd-node span { color: #1B5E20 !important; }

    .sd-node { background: #E3F2FD !important; color: #0D47A1 !important; font-size: 11px; margin-left: 10px; border-left: 3px solid #1E88E5; padding: 6px; border-bottom: 1px solid #eee; }
    .sd-node span { color: #0D47A1 !important; }
    
    .date-label { font-size: 10px; opacity: 0.85; text-align: right; }

    /* 8. BUTTONS */
    .stButton>button { width: 100%; border-radius: 8px; background-color: #800000 !important; color: white !important; font-weight: bold; border: none; }
    div[data-testid="stInput"] { border-radius: 8px; border: 1px solid #800000; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v85")

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
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        deg = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
        positions[KN_PLANETS[pid]] = deg
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]] = rahu
    positions[KN_PLANETS[102]] = (rahu + 180) % 360
    lagna = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    positions[KN_PLANETS["Lagna"]] = lagna
    
    sr, ss = find_sunrise_set(jd, lat, lon)
    if sr == -1 or ss == -1: sr = jd - 0.25; ss = jd + 0.25 
    day_sr = sr if jd >= sr else find_sunrise_set(jd - 1.0, lat, lon)[0]
    w_idx = int(day_sr + 0.5 + 1.5) % 7
    yf_day = [26, 22, 18, 14, 10, 6, 2]; yf_night = [10, 6, 2, 26, 22, 18, 14]
    
    if jd >= sr and jd < ss: 
        dur = ss - sr; yf = yf_day[w_idx]; mtime = sr + (dur * yf / 30.0)
    else:
        if jd >= ss: 
            next_sr = find_sunrise_set(jd + 1.0, lat, lon)[0]; dur = next_sr - ss; yf = yf_night[w_idx]; mtime = ss + (dur * yf / 30.0)
        else: 
            prev_ss = find_sunrise_set(jd - 1.0, lat, lon)[1]; prev_w_idx = (w_idx - 1) % 7; dur = sr - prev_ss; yf = yf_night[prev_w_idx]; mtime = prev_ss + (dur * yf / 30.0)
            
    mandi_deg = (swe.houses(mtime, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mtime)) % 360
    positions[KN_PLANETS["Ma"]] = mandi_deg

    moon_deg, sun_deg = positions["ಚಂದ್ರ"], positions["ರವಿ"]
    t_idx = int(((moon_deg - sun_deg + 360) % 360) / 12)
    n_idx = int(moon_deg / 13.333333333)
    js = find_nak_limit(jd, n_idx * 13.333333333); je = find_nak_limit(jd, (n_idx + 1) * 13.333333333)
    perc = (moon_deg % 13.333333333) / 13.333333333
    bal = YEARS[n_idx % 9] * (1 - perc)
    pan = {
        "t": KN_TITHI[min(t_idx, 29)], "v": KN_VARA[w_idx], "n": KN_NAK[n_idx % 27],
        "sr": day_sr, "ss": ss, "udayadi": fmt_ghati((jd - day_sr) * 60), 
        "gata": fmt_ghati((jd - js) * 60), "parama": fmt_ghati((je - js) * 60), "rem": fmt_ghati((je - jd) * 60),
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(bal)}ವ {int((bal%1)*12)}ತಿ {int((bal*12%1)*30)}ದಿ",
        "n_idx": n_idx, "perc": perc, "jd_birth": jd, "date_obj": datetime.datetime.fromtimestamp((jd - 2440587.5) * 86400.0)
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
    with st.container():
        st.info("ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ (Enter Details)")
        name = st.text_input("ಹೆಸರು (Name)", "ಬಳಕೆದಾರ")
        dob = st.date_input("ದಿನಾಂಕ (Date)", datetime.date(1997, 5, 24))
        
        st.write("ಜನನ ಸಮಯ (Time)")
        c1, c2, c3 = st.columns([1,1,1])
        h = c1.number_input("ಗಂಟೆ", 1, 12, 2)
        m = c2.number_input("ನಿಮಿಷ", 0, 59, 43)
        ampm = c3.selectbox("M", ["AM", "PM"], index=1, label_visibility="collapsed")
        
        st.write("ಸ್ಥಳ (Location)")
        place_q = st.text_input("ಊರು ಹುಡುಕಿ (Search Place)", "Yellapur")
        if st.button("ಹುಡುಕಿ (Search)", type="secondary"):
            try:
                loc = geolocator.geocode(place_q)
                if loc:
                    st.session_state.lat = loc.latitude; st.session_state.lon = loc.longitude
                    st.success(f"📍 {loc.address}")
            except: st.error("Offline / Error")
            
        c_lat, c_lon = st.columns(2)
        lat = c_lat.number_input("Lat", value=st.session_state.lat, format="%.4f")
        lon = c_lon.number_input("Lon", value=st.session_state.lon, format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ಜಾತಕ ರಚಿಸಿ (Generate)", type="primary"):
            h24 = h + (12 if ampm == "PM" and h != 12 else 0); h24 = 0 if ampm == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            pos, pan = get_full_calculations(jd, lat, lon)
            st.session_state.data = {"pos": pos, "pan": pan, "date": dob}
            st.session_state.page = "dashboard"
            st.rerun()

elif st.session_state.page == "dashboard":
    pos = st.session_state.data['pos']; pan = st.session_state.data['pan']
    
    if st.button("⬅️ ಹಿಂದಕ್ಕೆ (Back)", type="secondary"): st.session_state.page = "input"; st.rerun()
    
    t1, t2, t3, t4, t5 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        c_v, c_b = st.columns([2, 1])
        v_opt = c_v.selectbox("ವರ್ಗ", [1, 3, 9, 12, 30], format_func=lambda x: f"D{x}")
        b_opt = c_b.checkbox("ಭಾವ (Bhava)", value=False)
        
        bxs = {i: "" for i in range(12)}; ld = pos["ಲಗ್ನ"]
        for n, d in pos.items():
            if v_opt == 1: ri = int(d/30) if not b_opt else (int(ld/30) + int(((d - ld + 360) % 360 + 15) / 30)) % 12
            elif v_opt == 30: r = int(d/30); dr = d%30; is_odd = (int(d/30) % 2 == 0); ri = (0 if dr<5 else 10 if dr<10 else 8 if dr<18 else 2 if dr<25 else 6) if is_odd else (5 if dr<5 else 2 if dr<12 else 8 if dr<20 else 10 if dr<25 else 0)
            else:
                if v_opt == 9: block = int(d/30)%4; start = [0, 9, 6, 3][block]; steps = int((d%30)/3.33333); ri = (start + steps) % 12
                elif v_opt == 3: ri = (int(d/30) + (int((d%30)/10)*4)) % 12
                elif v_opt == 12: ri = (int(d/30) + int((d%30)/2.5)) % 12
                else: ri = int(d/30)
            cls = "hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl"
            bxs[ri] += f'<div class="{cls}">{n}</div>'
            
        grid_order = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        center_txt = "Bhava" if b_opt else "Rashi"
        for idx in grid_order:
            if idx is None:
                if html.count("center-box") == 0: html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v_opt}<br>{center_txt}</div>'
            else: html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        tbl_html = "<table class='key-val-table'><tr><th style='text-align:left; color:#800000'>ಗ್ರಹ</th><th style='text-align:left; color:#800000'>ರಾಶಿ</th><th style='text-align:right; color:#800000'>ಅಂಶ</th></tr>"
        for p, d in pos.items():
            r_name = KN_RASHI[int(d/30)]
            deg_str = f"{int(d%30)}° {int((d%30*60)%60)}'"
            tbl_html += f"<tr><td><b>{p}</b></td><td>{r_name}</td><td style='text-align:right'>{deg_str}</td></tr>"
        tbl_html += "</table></div>"
        st.markdown(tbl_html, unsafe_allow_html=True)

    with t3:
        st.markdown(f"<div class='card' style='color:#800000; font-weight:bold'>ಶಿಷ್ಟ ದಶೆ: {pan['d_bal']}</div>", unsafe_allow_html=True)
        dh = ""; current_date = pan['date_obj']; si = pan['n_idx'] % 9
        for i in range(9):
            im = (si + i) % 9; md_dur_yrs = YEARS[im] * ((1 - pan['perc']) if i==0 else 1)
            md_end = current_date + datetime.timedelta(days=md_dur_yrs*365.25)
            dh += f"<details><summary class='md-node'><span>{LORDS[im]}</span><span class='date-label'>{md_end.strftime('%d-%m-%y')}</span></summary>"
            cad = current_date
            for j in range(9):
                ia = (im + j) % 9; ad_years = (YEARS[im] * YEARS[ia] / 120.0); 
                if i==0: ad_years = ad_years * (1 - pan['perc'])
                ae = cad + datetime.timedelta(days=ad_years*365.25)
                dh += f"<details><summary class='ad-node'><span>{LORDS[ia]}</span><span class='date-label'>{ae.strftime('%d-%m-%y')}</span></summary>"; cpd = cad
                for k in range(9):
                    ip = (ia + k) % 9; pd_years = (ad_years * YEARS[ip] / 120.0); pe = cpd + datetime.timedelta(days=pd_years*365.25)
                    dh += f"<details><summary class='pd-node'><span>{LORDS[ip]}</span><span class='date-label'>{pe.strftime('%d-%m-%y')}</span></summary>"; csd = cpd
                    for l in range(9):
                        iss = (ip + l) % 9; sd_years = (pd_years * YEARS[iss] / 120.0); se = csd + datetime.timedelta(days=sd_years*365.25)
                        dh += f"<div class='sd-node'>{LORDS[iss]} <span style='float:right'>{se.strftime('%d-%m-%y')}</span></div>"; csd = se
                    dh += "</details>"; cpd = pe
                dh += "</details>"; cad = ae
            dh += "</details>"; current_date = md_end
        st.markdown(dh, unsafe_allow_html=True)

    with t4:
        st.markdown(f"""<div class='card'><table class='key-val-table'><tr><td class='key'>ತಿಥಿ</td><td>{pan['t']}</td></tr><tr><td class='key'>ವಾರ</td><td>{pan['v']}</td></tr><tr><td class='key'>ನಕ್ಷತ್ರ</td><td>{pan['n']}</td></tr><tr><td class='key'>ಉದಯಾದಿ</td><td>{pan['udayadi']} ಘಟಿ</td></tr><tr><td class='key'>ಗತ</td><td>{pan['gata']} ಘಟಿ</td></tr><tr><td class='key'>ಶೇಷ</td><td>{pan['rem']} ಘಟಿ</td></tr></table></div>""", unsafe_allow_html=True)

    with t5:
        st.session_state.notes = st.text_area("ಟಿಪ್ಪಣಿಗಳು", value=st.session_state.notes, height=300)
        if st.button("ಉಳಿಸಿ (Save)"): st.success("Saved!")
