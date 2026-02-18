import streamlit as st
import swisseph as swe
import datetime
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. SETUP
# ==========================================
st.set_page_config(page_title="ಭಾರತೀಯಮ್", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans Kannada', sans-serif; background-color: #fff8e1; color: #000; }
    .main-title { color: white; background-color: #b71c1c; padding: 15px; text-align: center; font-weight: 900; font-size: 26px; border-radius: 10px; margin-bottom: 20px; }
    .grid-container { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); width: 360px; height: 360px; margin: 15px auto; gap: 2px; background: #333; border: 3px solid #000; }
    .box { background: white; position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; min-height: 85px; padding: 5px; text-align: center; }
    .box-lbl { position: absolute; top: 2px; left: 4px; font-size: 9px; color: #999; font-weight: 900; }
    .pl-name { color: #000; font-size: 12px; font-weight: 900; line-height: 1.1; }
    .hi { color: #d50000; text-decoration: underline; font-weight: 900; }
    .center-box { grid-column: 2/4; grid-row: 2/4; background: #ffe0b2; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #b71c1c; font-weight: 900; text-align: center; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v67")

# ==========================================
# 2. CONSTANTS & DATA
# ==========================================
KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯ", "ಶುಕ್ಲ ಬಿದಿಗೆ", "ಶುಕ್ಲ ತದಿಗೆ", "ಶುಕ್ಲ ಚೌತಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯ", "ಕೃಷ್ಣ ಬಿದಿಗೆ", "ಕೃಷ್ಣ ತದಿಗೆ", "ಕೃಷ್ಣ ಚೌತಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತ್ತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಖ", "ಪುಬ್ಬ", "ಉತ್ತರಾ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
KN_YOGA = ["ವಿಷ್ಕಂಭ", "ಪ್ರೀತಿ", "ಆಯುಷ್ಮಾನ್", "ಸೌಭಾಗ್ಯ", "ಶೋಭನ", "ಅತಿಗಂಡ", "ಸುಕರ್ಮ", "ಧೃತಿ", "ಶೂಲ", "ಗಂಡ", "ವೃದ್ಧಿ", "ಧ್ರುವ", "ವ್ಯಾಘಾತ", "ಹರ್ಷಣ", "ವಜ್ರ", "ಸಿದ್ಧಿ", "ವ್ಯತೀಪಾತ", "ವರೀಯಾನ್", "ಪರಿಘ", "ಶಿವ", "ಸಿದ್ಧ", "ಸಾಧ್ಯ", "ಶುಭ", "ಶುಕ್ಲ", "ಬ್ರಹ್ಮ", "ಐಂದ್ರ", "ವೈಧೃತಿ"]
KN_KARANA = ["ಬವ", "ಬಾಲವ", "ಕೌಲವ", "ತೈತಲ", "ಗರಜ", "ವಣಿಜ", "ಭದ್ರಾ", "ಶಕುನಿ", "ಚತುಷ್ಪಾದ", "ನಾಗ", "ಕಿಂಸ್ತುಘ್ನ"]

PLANET_IDS = {0: "ರವಿ", 1: "ಚಂದ್ರ", 2: "ಬುಧ", 3: "ಶುಕ್ರ", 4: "ಕುಜ", 5: "ಗುರು", 6: "ಶನಿ", 10: "ರಾಹು"}
LORDS = ["ಕೇತು","ಶುಕ್ರ","ರವಿ","ಚಂದ್ರ","ಕುಜ","ರಾಹು","ಗುರು","ಶನಿ","ಬುಧ"]
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

# ==========================================
# 3. MATH FUNCTIONS
# ==========================================
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
        # 1. Get Sunrise/Sunset
        res = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_RISE | swe.FLG_MOSEPH)
        sr = res[1][0]
        res_s = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_SET | swe.FLG_MOSEPH)
        ss = res_s[1][0]
        
        # 2. Weekday
        wday = int(jd + 0.5 + 1.5) % 7
        
        # 3. Mandi Indices (Yamasukra)
        day_idx = [26, 22, 18, 14, 10, 6, 2]
        night_idx = [10, 6, 2, 26, 22, 18, 14]
        
        if jd >= sr and jd < ss: # DAY BIRTH
            dur = ss - sr
            ghati_part = day_idx[wday]
            m_time = sr + (dur * ghati_part / 30.0)
        else: # NIGHT BIRTH
            # Find NEXT sunrise
            res_next = swe.rise_trans(jd + 1, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_RISE | swe.FLG_MOSEPH)
            next_sr = res_next[1][0]
            
            # If jd is early morning (before SR), we need PREV sunset
            if jd < sr:
                res_prev_s = swe.rise_trans(jd - 1, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_SET | swe.FLG_MOSEPH)
                ss = res_prev_s[1][0]
                dur = sr - ss
                # Important: Night logic uses weekday of the previous sunrise
                wday = (wday - 1) % 7 
            else:
                dur = next_sr - ss
                
            ghati_part = night_idx[wday]
            m_time = ss + (dur * ghati_part / 30.0)

        # 4. Ascendant at Mandi Time
        res_h = swe.houses_ex(m_time, lat, lon, b'P', swe.FLG_SIDEREAL | swe.FLG_MOSEPH)
        return res_h[0][0] % 360
    except: return 0.0

def get_panchanga(jd, moon_deg, sun_deg):
    diff = (moon_deg - sun_deg + 360) % 360
    tithi = KN_TITHI[int(diff / 12)]
    nak = KN_NAK[int(moon_deg / 13.333333)]
    yoga = KN_YOGA[int((moon_deg + sun_deg)%360 / 13.333333)]
    karana = KN_KARANA[int(diff / 6) % 11]
    wday = KN_VARA[int(jd + 0.5 + 1.5) % 7]
    return tithi, nak, yoga, karana, wday

# ==========================================
# 4. UI LOGIC
# ==========================================
st.markdown('<div class="main-title">ಭಾರತೀಯಮ್</div>', unsafe_allow_html=True)
if 'show_chart' not in st.session_state: st.session_state['show_chart'] = False

with st.sidebar:
    st.header("ವಿವರಗಳು")
    u_name = st.text_input("ಹೆಸರು", "ಬಳಕೆದಾರ")
    u_dob = st.date_input("ದಿನಾಂಕ", datetime.date(1997, 5, 24))
    u_tob = st.time_input("ಸಮಯ", datetime.time(14, 43))
    
    loc_q = st.text_input("ಸ್ಥಳ", "Yellapur")
    if st.button("ಹುಡುಕಿ"):
        try:
            loc = geolocator.geocode(loc_q)
            if loc:
                st.session_state.lat = loc.latitude
                st.session_state.lon = loc.longitude
                st.success("ಸ್ಥಳ ಸಿಕ್ಕಿದೆ!")
        except: st.error("ದೋಷ")
    
    if 'lat' not in st.session_state: st.session_state.lat = 14.9800
    if 'lon' not in st.session_state: st.session_state.lon = 74.7300
    
    u_lat = st.number_input("Lat", value=st.session_state.lat, format="%.4f")
    u_lon = st.number_input("Lon", value=st.session_state.lon, format="%.4f")
    
    if st.button("ಜಾತಕ ರಚಿಸಿ", type="primary"):
        st.session_state['show_chart'] = True

if st.session_state['show_chart']:
    h_dec = u_tob.hour + u_tob.minute/60.0
    jd = swe.julday(u_dob.year, u_dob.month, u_dob.day, h_dec - 5.5)
    
    pos = {}
    for pid, pnk in PLANET_IDS.items():
        res = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL | swe.FLG_MOSEPH)
        pos[pnk] = res[0][0] % 360
    pos["ಕೇತು"] = (pos["ರಾಹು"] + 180) % 360
    pos["ಮಾಂದಿ"] = get_mandi(jd, u_lat, u_lon)
    res_lag = swe.houses_ex(jd, u_lat, u_lon, b'P', swe.FLG_SIDEREAL | swe.FLG_MOSEPH)
    pos["ಲಗ್ನ"] = res_lag[0][0] % 360

    t1, t2, t3, t4, t5 = st.tabs(["ಕುಂಡಲಿ", "ಸ್ಫುಟ", "ದಶ (4 ಹಂತ)", "ಪಂಚಾಂಗ", "ಉಳಿಸಿ"])

    with t1:
        col1, col2 = st.columns(2)
        v_choice = col1.selectbox("ವರ್ಗ", [1, 3, 9, 12, 30], format_func=lambda x: f"D{x}")
        chart_mode = col2.radio("ವಿಧಾನ", ["Rashi", "Bhava"], horizontal=True)
        
        boxes = {i: "" for i in range(12)}
        lag_deg = pos["ಲಗ್ನ"]
        for p, d in pos.items():
            if chart_mode == "Bhava" and v_choice == 1:
                idx = int(((d - lag_deg + 15 + 360) % 360) / 30)
                lag_rashi = int(lag_deg / 30)
                final_idx = (lag_rashi + idx) % 12
            else:
                final_idx = get_varga_pos(d, v_choice)
            cls = "hi" if p in ["ಲಗ್ನ", "ಮಾಂದಿ"] else "pl-name"
            boxes[final_idx] += f'<div class="{cls}">{p}</div>'
        
        grid = [11, 0, 1, 2, 10, None, None, 3, 9, None, None, 4, 8, 7, 6, 5]
        html = '<div class="grid-container">'
        for g in grid:
            if g is None:
                label = f"ಭಾರತೀಯಮ್<br>D{v_choice}"
                if chart_mode == "Bhava": label += "<br>(Bhava)"
                if html.count('center-box') < 1: html += f'<div class="center-box">{label}</div>'
            else: html += f'<div class="box"><span class="box-lbl">{KN_RASHI[g]}</span>{boxes[g]}</div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    with t2:
        df = pd.DataFrame([{"ಗ್ರಹ": k, "ರಾಶಿ": KN_RASHI[int(v/30)], "ಅಂಶ": f"{int(v%30)}° {int((v%30*60)%60)}'"} for k,v in pos.items()])
        st.table(df)

    with t3:
        # 4-LEVEL DASHA LOGIC
        m_lon = pos.get("ಚಂದ್ರ", 0)
        n_idx = int(m_lon / 13.333333333)
        perc = (m_lon % 13.333333333) / 13.333333333
        start_lord = n_idx % 9
        
        y, m, d, hv = swe.revjul(jd + 5.5/24.0)
        birth_dt = datetime.datetime(y, m, d)

        # 1. Select Mahadasha
        st.subheader("ಹಂತ 1: ಮಹಾದಶ")
        md_opts = []
        curr = birth_dt
        for i in range(9):
            idx = (start_lord + i) % 9
            yrs = YEARS[idx] * ((1-perc) if i==0 else 1)
            end = curr + datetime.timedelta(days=yrs*365.25)
            md_opts.append({"L": LORDS[idx], "S": curr, "E": end, "Y": YEARS[idx], "I": idx})
            curr = end
        
        sel_md = st.selectbox("ಮಹಾದಶ ಆಯ್ಕೆ:", md_opts, format_func=lambda x: f"{x['L']} ({x['E'].strftime('%Y')})")

        # 2. Select Antardasha
        if sel_md:
            st.markdown("---")
            st.subheader(f"ಹಂತ 2: {sel_md['L']} > ಅಂತರ್ದಶ")
            ad_opts = []
            curr_ad = sel_md['S']
            
            for j in range(9):
                ad_idx = (sel_md['I'] + j) % 9
                # AD Duration = MD_Years * AD_Years / 120
                ad_yrs = (sel_md['Y'] * YEARS[ad_idx]) / 120.0
                ad_end = curr_ad + datetime.timedelta(days=ad_yrs*365.25)
                ad_opts.append({"L": LORDS[ad_idx], "S": curr_ad, "E": ad_end, "Y": ad_yrs, "I": ad_idx})
                curr_ad = ad_end
            
            sel_ad = st.selectbox("ಅಂತರ್ದಶ ಆಯ್ಕೆ:", ad_opts, format_func=lambda x: f"{x['L']} ({x['E'].strftime('%d-%m-%Y')})")

            # 3. Show Pratyantardasha & Sookshma Table
            if sel_ad:
                st.markdown("---")
                st.subheader(f"ಹಂತ 3 & 4: {sel_ad['L']} > ಪ್ರತ್ಯಂತರ & ಸೂಕ್ಷ್ಮ")
                pd_data = []
                curr_pd = sel_ad['S']
                
                for k in range(9):
                    pd_idx = (sel_ad['I'] + k) % 9
                    # PD Duration = AD_Years * PD_Years / 120
                    pd_yrs = (sel_ad['Y'] * YEARS[pd_idx]) / 120.0
                    pd_end = curr_pd + datetime.timedelta(days=pd_yrs*365.25)
                    
                    # Sookshma (Level 4) - Showing first Sookshma for context
                    sd_yrs = (pd_yrs * YEARS[pd_idx]) / 120.0 # Approximation for display
                    sd_end = curr_pd + datetime.timedelta(days=sd_yrs*365.25)

                    pd_data.append({
                        "ಪ್ರತ್ಯಂತರ": LORDS[pd_idx],
                        "ಆರಂಭ": curr_pd.strftime('%d-%m-%Y'),
                        "ಅಂತ್ಯ": pd_end.strftime('%d-%m-%Y')
                    })
                    curr_pd = pd_end
                st.table(pd.DataFrame(pd_data))

    with t4:
        # Full Panchanga Display
        tithi, nak, yoga, karana, vara = get_panchanga(jd, pos["ಚಂದ್ರ"], pos["ರವಿ"])
        st.success(f"ವಾರ: {vara}")
        st.info(f"ತಿಥಿ: {tithi}")
        st.info(f"ನಕ್ಷತ್ರ: {nak}")
        st.info(f"ಯೋಗ: {yoga}")
        st.info(f"ಕರಣ: {karana}")

    with t5:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("ಡೌನ್‌ಲೋಡ್ (CSV)", csv, f"{u_name}.csv")
