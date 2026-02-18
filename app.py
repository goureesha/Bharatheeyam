import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & THEME
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
    .key { color: #9D0208 !important; font-weight: 900; width: 45%; }
    .key-val-table td { border-bottom: 1px solid #f0f0f0; padding: 8px 4px; color: #333 !important; }
    details { margin-bottom: 4px; border: 1px solid #e0c097; border-radius: 6px; overflow: hidden; background: white; }
    summary { cursor: pointer; padding: 10px; font-size: 13px; list-style: none; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v103")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತ್ತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಖ", "ಪುಬ್ಬ", "ಉತ್ತರಾ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def find_sunrise_set(jd, lat, lon):
    res_sr = swe.rise_trans(jd, swe.SUN, lon, lat, swe.CALC_RISE | swe.FLG_MOSEPH)
    res_ss = swe.rise_trans(jd, swe.SUN, lon, lat, swe.CALC_SET | swe.FLG_MOSEPH)
    return res_sr[1][0], res_ss[1][0]

def fmt_ghati(decimal_val):
    g = int(decimal_val)
    v = int(round((decimal_val - g) * 60))
    if v == 60: g += 1; v = 0
    return f"{g}.{v:02d}"

def get_full_calculations(jd, lat, lon):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd)
    positions = {}
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        positions[KN_PLANETS[pid]] = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]], positions[KN_PLANETS[102]] = rahu, (rahu + 180) % 360
    positions[KN_PLANETS["Lagna"]] = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    
    sr_today, ss_today = find_sunrise_set(jd, lat, lon)
    jd_local = jd + (5.5/24.0)
    cal_wday = int(jd_local + 0.5 + 1.5) % 7 
    
    if jd < sr_today:
        _, prev_ss = find_sunrise_set(jd - 1.0, lat, lon)
        w_idx, is_night, start_base, dur, panch_sr = (cal_wday - 1) % 7, True, prev_ss, (sr_today - prev_ss), find_sunrise_set(jd - 1.0, lat, lon)[0]
    else:
        panch_sr = sr_today
        if jd >= ss_today:
            next_sr, _ = find_sunrise_set(jd + 1.0, lat, lon)
            w_idx, is_night, start_base, dur = cal_wday, True, ss_today, (next_sr - ss_today)
        else:
            w_idx, is_night, start_base, dur = cal_wday, False, sr_today, (ss_today - sr_today)

    factor = [10, 6, 2, 26, 22, 18, 14][w_idx] if is_night else [26, 22, 18, 14, 10, 6, 2][w_idx]
    mtime = start_base + (dur * factor / 30.0)
    positions[KN_PLANETS["Ma"]] = (swe.houses(mtime, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mtime)) % 360

    m_deg, s_deg = positions["ಚಂದ್ರ"], positions["ರವಿ"]
    t_idx = int(((m_deg - s_deg + 360) % 360) / 12)
    n_idx = int(m_deg / 13.333333333)
    perc = (m_deg % 13.333333333) / 13.333333333
    
    pan_dict = {
        "t": KN_TITHI[min(t_idx, 29)], "v": KN_VARA[w_idx], "n": KN_NAK[n_idx % 27],
        "sr": panch_sr, "udayadi": fmt_ghati((jd - panch_sr) * 60), 
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(YEARS[n_idx%9]*(1-perc))}ವ",
        "n_idx": n_idx, "perc": perc, "date_obj": datetime.datetime.fromtimestamp((jd - 2440587.5) * 86400.0)
    }
    return positions, pan_dict

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
        h, m, am = c1.number_input("ಗಂಟೆ", 1, 12, 2), c2.number_input("ನಿಮಿಷ", 0, 59, 43), c3.selectbox("AM/PM", ["AM", "PM"])
        lat, lon = st.number_input("Lat", value=14.98, format="%.4f"), st.number_input("Lon", value=74.73, format="%.4f")
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary", use_container_width=True):
            h24 = h + (12 if am == "PM" and h != 12 else 0); h24 = 0 if am == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            pos, pan = get_full_calculations(jd, lat, lon)
            st.session_state.data = {"pos": pos, "pan": pan}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    if 'data' not in st.session_state:
        st.session_state.page = "input"; st.rerun()
    
    pos, pan = st.session_state.data.get('pos', {}), st.session_state.data.get('pan', {})
    if st.button("⬅️ ಹಿಂದಕ್ಕೆ"): st.session_state.page = "input"; st.rerun()
    t1, t2, t3, t4, t5 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        v = st.selectbox("ವರ್ಗ", [1, 9, 3, 12], format_func=lambda x: f"D{x}")
        bxs = {i: "" for i in range(12)}; ld = pos.get("ಲಗ್ನ", 0)
        for n, d in pos.items():
            ri = int(d/30) if v == 1 else (([0,9,6,3][int(d/30)%4]) + int((d%30)/3.33333)) % 12 if v==9 else int(d/30)
            bxs[ri] += f'<div class="{"hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else ""}">{n}</div>'
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for idx in grid:
            if idx is None:
                if html.count("center-box") == 0: html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v}</div>'
            else: html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        data = [{"ಗ್ರಹ": k, "ರಾಶಿ": KN_RASHI[int(v/30)], "ಅಂಶ": f"{int(v%30)}°"} for k,v in pos.items()]
        st.table(pd.DataFrame(data)); st.markdown("</div>", unsafe_allow_html=True)

    with t3:
        b_dt = pan.get('date_obj', datetime.datetime.now())
        si, pc, dh = pan.get('n_idx', 0) % 9, pan.get('perc', 0), ""
        cur = b_dt
        for i in range(9):
            im = (si + i) % 9; md = YEARS[im] * ((1 - pc) if i==0 else 1); me = cur + datetime.timedelta(days=md*365.25)
            dh += f"<details><summary><b>{LORDS[im]}</b> <span>{me.strftime('%d-%m-%y')}</span></summary>"
            cad = cur
            for j in range(9):
                ia = (im + j) % 9; ad = (YEARS[im]*YEARS[ia]/120.0); ae = cad + datetime.timedelta(days=ad*365.25)
                dh += f"<div style='padding:5px 15px; border-bottom:1px solid #eee; display:flex; justify-content:space-between'><span>{LORDS[ia]}</span><span>{ae.strftime('%d-%m-%y')}</span></div>"; cad = ae
            dh += "</details>"; cur = me
        st.markdown(dh, unsafe_allow_html=True)

    with t4:
        st.markdown(f"""<div class='card'><table class='key-val-table'>
            <tr><td class='key'>ವಾರ</td><td>{pan.get('v', '-')}</td></tr>
            <tr><td class='key'>ತಿಥಿ</td><td>{pan.get('t', '-')}</td></tr>
            <tr><td class='key'>ನಕ್ಷತ್ರ</td><td>{pan.get('n', '-')}</td></tr>
            <tr><td class='key'>ಉದಯಾದಿ</td><td>{pan.get('udayadi', '-')} ಘಟಿ</td></tr>
            <tr><td class='key'>ಶಿಷ್ಟ ದಶೆ</td><td>{pan.get('d_bal', '-')}</td></tr>
        </table></div>""", unsafe_allow_html=True)

    with t5:
        st.text_area("ಟಿಪ್ಪಣಿಗಳು", height=300)
import streamlit as st
import swisseph as swe
import datetime
import math
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. PAGE CONFIG & THEME
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
    .key { color: #9D0208 !important; font-weight: 900; width: 45%; }
    .key-val-table td { border-bottom: 1px solid #f0f0f0; padding: 8px 4px; color: #333 !important; }
    details { margin-bottom: 4px; border: 1px solid #e0c097; border-radius: 6px; overflow: hidden; background: white; }
    summary { cursor: pointer; padding: 10px; font-size: 13px; list-style: none; display: flex; justify-content: space-between; border-bottom: 1px solid #eee; color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE MATH ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v103")

KN_PLANETS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 101: "ರಾಹು", 102: "ಕೇತು", "Ma": "ಮಾಂದಿ", "Lagna": "ಲಗ್ನ"}
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯಮಿ", "ಶುಕ್ಲ ದ್ವಿತೀಯ", "ಶುಕ್ಲ ತೃತೀಯ", "ಶುಕ್ಲ ಚತುರ್ಥಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯಮಿ", "ಕೃಷ್ಣ ದ್ವಿತೀಯ", "ಕೃಷ್ಣ ತೃತೀಯ", "ಕೃಷ್ಣ ಚತುರ್ಥಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತ್ತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಖ", "ಪುಬ್ಬ", "ಉತ್ತರಾ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def find_sunrise_set(jd, lat, lon):
    res_sr = swe.rise_trans(jd, swe.SUN, lon, lat, swe.CALC_RISE | swe.FLG_MOSEPH)
    res_ss = swe.rise_trans(jd, swe.SUN, lon, lat, swe.CALC_SET | swe.FLG_MOSEPH)
    return res_sr[1][0], res_ss[1][0]

def fmt_ghati(decimal_val):
    g = int(decimal_val)
    v = int(round((decimal_val - g) * 60))
    if v == 60: g += 1; v = 0
    return f"{g}.{v:02d}"

def get_full_calculations(jd, lat, lon):
    swe.set_topo(float(lon), float(lat), 0)
    ayan = swe.get_ayanamsa(jd)
    positions = {}
    for pid in [0, 1, 2, 3, 4, 5, 6]:
        positions[KN_PLANETS[pid]] = (swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    rahu = (swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]) % 360
    positions[KN_PLANETS[101]], positions[KN_PLANETS[102]] = rahu, (rahu + 180) % 360
    positions[KN_PLANETS["Lagna"]] = (swe.houses(jd, float(lat), float(lon), b'P')[1][0] - ayan) % 360
    
    sr_today, ss_today = find_sunrise_set(jd, lat, lon)
    jd_local = jd + (5.5/24.0)
    cal_wday = int(jd_local + 0.5 + 1.5) % 7 
    
    if jd < sr_today:
        _, prev_ss = find_sunrise_set(jd - 1.0, lat, lon)
        w_idx, is_night, start_base, dur, panch_sr = (cal_wday - 1) % 7, True, prev_ss, (sr_today - prev_ss), find_sunrise_set(jd - 1.0, lat, lon)[0]
    else:
        panch_sr = sr_today
        if jd >= ss_today:
            next_sr, _ = find_sunrise_set(jd + 1.0, lat, lon)
            w_idx, is_night, start_base, dur = cal_wday, True, ss_today, (next_sr - ss_today)
        else:
            w_idx, is_night, start_base, dur = cal_wday, False, sr_today, (ss_today - sr_today)

    factor = [10, 6, 2, 26, 22, 18, 14][w_idx] if is_night else [26, 22, 18, 14, 10, 6, 2][w_idx]
    mtime = start_base + (dur * factor / 30.0)
    positions[KN_PLANETS["Ma"]] = (swe.houses(mtime, float(lat), float(lon), b'P')[1][0] - swe.get_ayanamsa(mtime)) % 360

    m_deg, s_deg = positions["ಚಂದ್ರ"], positions["ರವಿ"]
    t_idx = int(((m_deg - s_deg + 360) % 360) / 12)
    n_idx = int(m_deg / 13.333333333)
    perc = (m_deg % 13.333333333) / 13.333333333
    
    pan_dict = {
        "t": KN_TITHI[min(t_idx, 29)], "v": KN_VARA[w_idx], "n": KN_NAK[n_idx % 27],
        "sr": panch_sr, "udayadi": fmt_ghati((jd - panch_sr) * 60), 
        "d_bal": f"{LORDS[n_idx%9]} ಉಳಿಕೆ: {int(YEARS[n_idx%9]*(1-perc))}ವ",
        "n_idx": n_idx, "perc": perc, "date_obj": datetime.datetime.fromtimestamp((jd - 2440587.5) * 86400.0)
    }
    return positions, pan_dict

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
        h, m, am = c1.number_input("ಗಂಟೆ", 1, 12, 2), c2.number_input("ನಿಮಿಷ", 0, 59, 43), c3.selectbox("AM/PM", ["AM", "PM"])
        lat, lon = st.number_input("Lat", value=14.98, format="%.4f"), st.number_input("Lon", value=74.73, format="%.4f")
        if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary", use_container_width=True):
            h24 = h + (12 if am == "PM" and h != 12 else 0); h24 = 0 if am == "AM" and h == 12 else h24
            jd = swe.julday(dob.year, dob.month, dob.day, h24 + m/60.0 - 5.5)
            pos, pan = get_full_calculations(jd, lat, lon)
            st.session_state.data = {"pos": pos, "pan": pan}
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    if 'data' not in st.session_state:
        st.session_state.page = "input"; st.rerun()
    
    pos, pan = st.session_state.data.get('pos', {}), st.session_state.data.get('pan', {})
    if st.button("⬅️ ಹಿಂದಕ್ಕೆ"): st.session_state.page = "input"; st.rerun()
    t1, t2, t3, t4, t5 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ", "ಪಂಚಾಂಗ", "ಟಿಪ್ಪಣಿ"])
    
    with t1:
        v = st.selectbox("ವರ್ಗ", [1, 9, 3, 12], format_func=lambda x: f"D{x}")
        bxs = {i: "" for i in range(12)}; ld = pos.get("ಲಗ್ನ", 0)
        for n, d in pos.items():
            ri = int(d/30) if v == 1 else (([0,9,6,3][int(d/30)%4]) + int((d%30)/3.33333)) % 12 if v==9 else int(d/30)
            bxs[ri] += f'<div class="{"hi" if n in ["ಲಗ್ನ", "ಮಾಂದಿ"] else ""}">{n}</div>'
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for idx in grid:
            if idx is None:
                if html.count("center-box") == 0: html += f'<div class="center-box">ಭಾರತೀಯಮ್<br>D{v}</div>'
            else: html += f'<div class="box"><span class="lbl">{KN_RASHI[idx]}</span>{bxs[idx]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        data = [{"ಗ್ರಹ": k, "ರಾಶಿ": KN_RASHI[int(v/30)], "ಅಂಶ": f"{int(v%30)}°"} for k,v in pos.items()]
        st.table(pd.DataFrame(data)); st.markdown("</div>", unsafe_allow_html=True)

    with t3:
        b_dt = pan.get('date_obj', datetime.datetime.now())
        si, pc, dh = pan.get('n_idx', 0) % 9, pan.get('perc', 0), ""
        cur = b_dt
        for i in range(9):
            im = (si + i) % 9; md = YEARS[im] * ((1 - pc) if i==0 else 1); me = cur + datetime.timedelta(days=md*365.25)
            dh += f"<details><summary><b>{LORDS[im]}</b> <span>{me.strftime('%d-%m-%y')}</span></summary>"
            cad = cur
            for j in range(9):
                ia = (im + j) % 9; ad = (YEARS[im]*YEARS[ia]/120.0); ae = cad + datetime.timedelta(days=ad*365.25)
                dh += f"<div style='padding:5px 15px; border-bottom:1px solid #eee; display:flex; justify-content:space-between'><span>{LORDS[ia]}</span><span>{ae.strftime('%d-%m-%y')}</span></div>"; cad = ae
            dh += "</details>"; cur = me
        st.markdown(dh, unsafe_allow_html=True)

    with t4:
        st.markdown(f"""<div class='card'><table class='key-val-table'>
            <tr><td class='key'>ವಾರ</td><td>{pan.get('v', '-')}</td></tr>
            <tr><td class='key'>ತಿಥಿ</td><td>{pan.get('t', '-')}</td></tr>
            <tr><td class='key'>ನಕ್ಷತ್ರ</td><td>{pan.get('n', '-')}</td></tr>
            <tr><td class='key'>ಉದಯಾದಿ</td><td>{pan.get('udayadi', '-')} ಘಟಿ</td></tr>
            <tr><td class='key'>ಶಿಷ್ಟ ದಶೆ</td><td>{pan.get('d_bal', '-')}</td></tr>
        </table></div>""", unsafe_allow_html=True)

    with t5:
        st.text_area("ಟಿಪ್ಪಣಿಗಳು", height=300)
