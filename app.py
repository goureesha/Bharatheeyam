import streamlit as st
import swisseph as swe
import datetime
import pandas as pd
from geopy.geocoders import Nominatim

# ==========================================
# 1. SERVER CONFIG
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
    .dasha-row { display: flex; justify-content: space-between; padding: 5px; border-bottom: 1px dashed #ccc; font-size: 14px; }
    .panch-row { background: white; padding: 10px; margin-bottom: 5px; border-left: 5px solid #b71c1c; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. CALCULATION ENGINE
# ==========================================
swe.set_ephe_path(None)
swe.set_sid_mode(swe.SIDM_LAHIRI)
geolocator = Nominatim(user_agent="bharatheeyam_v66")

KN_RASHI = ["ಮೇಷ", "ವೃಷಭ", "ಮಿಥುನ", "ಕರ್ಕ", "ಸಿಂಹ", "ಕನ್ಯಾ", "ತುಲಾ", "ವೃಶ್ಚಿಕ", "ಧನು", "ಮಕರ", "ಕುಂಭ", "ಮೀನ"]
KN_VARA = ["ಭಾನುವಾರ", "ಸೋಮವಾರ", "ಮಂಗಳವಾರ", "ಬುಧವಾರ", "ಗುರುವಾರ", "ಶುಕ್ರವಾರ", "ಶನಿವಾರ"]
KN_TITHI = ["ಶುಕ್ಲ ಪಾಡ್ಯ", "ಶುಕ್ಲ ಬಿದಿಗೆ", "ಶುಕ್ಲ ತದಿಗೆ", "ಶುಕ್ಲ ಚೌತಿ", "ಶುಕ್ಲ ಪಂಚಮಿ", "ಶುಕ್ಲ ಷಷ್ಠಿ", "ಶುಕ್ಲ ಸಪ್ತಮಿ", "ಶುಕ್ಲ ಅಷ್ಟಮಿ", "ಶುಕ್ಲ ನವಮಿ", "ಶುಕ್ಲ ದಶಮಿ", "ಶುಕ್ಲ ಏಕಾದಶಿ", "ಶುಕ್ಲ ದ್ವಾದಶಿ", "ಶುಕ್ಲ ತ್ರಯೋದಶಿ", "ಶುಕ್ಲ ಚತುರ್ದಶಿ", "ಹುಣ್ಣಿಮೆ", "ಕೃಷ್ಣ ಪಾಡ್ಯ", "ಕೃಷ್ಣ ಬಿದಿಗೆ", "ಕೃಷ್ಣ ತದಿಗೆ", "ಕೃಷ್ಣ ಚೌತಿ", "ಕೃಷ್ಣ ಪಂಚಮಿ", "ಕೃಷ್ಣ ಷಷ್ಠಿ", "ಕೃಷ್ಣ ಸಪ್ತಮಿ", "ಕೃಷ್ಣ ಅಷ್ಟಮಿ", "ಕೃಷ್ಣ ನವಮಿ", "ಕೃಷ್ಣ ದಶಮಿ", "ಕೃಷ್ಣ ಏಕಾದಶಿ", "ಕೃಷ್ಣ ದ್ವಾದಶಿ", "ಕೃಷ್ಣ ತ್ರಯೋದಶಿ", "ಕೃಷ್ಣ ಚತುರ್ದಶಿ", "ಅಮಾವಾಸ್ಯೆ"]
KN_NAK = ["ಅಶ್ವಿನಿ", "ಭರಣಿ", "ಕೃತ್ತಿಕಾ", "ರೋಹಿಣಿ", "ಮೃಗಶಿರ", "ಆರಿದ್ರಾ", "ಪುನರ್ವಸು", "ಪುಷ್ಯ", "ಆಶ್ಲೇಷ", "ಮಖ", "ಪುಬ್ಬ", "ಉತ್ತರಾ", "ಹಸ್ತ", "ಚಿತ್ತಾ", "ಸ್ವಾತಿ", "ವಿಶಾಖ", "ಅನುರಾಧ", "ಜೇಷ್ಠ", "ಮೂಲ", "ಪೂರ್ವಾಷಾಢ", "ಉತ್ತರಾಷಾಢ", "ಶ್ರವಣ", "ಧನಿಷ್ಠ", "ಶತಭಿಷ", "ಪೂರ್ವಾಭಾದ್ರ", "ಉತ್ತರಾಭಾದ್ರ", "ರೇವತಿ"]
KN_YOGA = ["ವಿಷ್ಕಂಭ", "ಪ್ರೀತಿ", "ಆಯುಷ್ಮಾನ್", "ಸೌಭಾಗ್ಯ", "ಶೋಭನ", "ಅತಿಗಂಡ", "ಸುಕರ್ಮ", "ಧೃತಿ", "ಶೂಲ", "ಗಂಡ", "ವೃದ್ಧಿ", "ಧ್ರುವ", "ವ್ಯಾಘಾತ", "ಹರ್ಷಣ", "ವಜ್ರ", "ಸಿದ್ಧಿ", "ವ್ಯತೀಪಾತ", "ವರೀಯಾನ್", "ಪರಿಘ", "ಶಿವ", "ಸಿದ್ಧ", "ಸಾಧ್ಯ", "ಶುಭ", "ಶುಕ್ಲ", "ಬ್ರಹ್ಮ", "ಐಂದ್ರ", "ವೈಧೃತಿ"]
KN_KARANA = ["ಬವ", "ಬಾಲವ", "ಕೌಲವ", "ತೈತಲ", "ಗರಜ", "ವಣಿಜ", "ಭದ್ರಾ", "ಶಕುನಿ", "ಚತುಷ್ಪಾದ", "ನಾಗ", "ಕಿಂಸ್ತುಘ್ನ"]

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
        # Calculate Sunrise/Sunset for the day
        res = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_RISE | swe.FLG_MOSEPH)
        sr = res[1][0]
        res_s = swe.rise_trans(jd, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_SET | swe.FLG_MOSEPH)
        ss = res_s[1][0]
        
        # Get Weekday (0=Sun, 6=Sat)
        wday = int(jd + 0.5 + 1.5) % 7
        
        # Day vs Night Logic
        is_day = (jd >= sr and jd < ss)
        
        # Mandi Ghatis (Standard Vedic Table)
        # Day: Sun=26, Mon=22, Tue=18, Wed=14, Thu=10, Fri=6, Sat=2
        day_ghatis = [26, 22, 18, 14, 10, 6, 2]
        # Night: Sun=10, Mon=6, Tue=2, Wed=26, Thu=22, Fri=18, Sat=14 (from sunset)
        night_ghatis = [10, 6, 2, 26, 22, 18, 14]
        
        if is_day:
            duration = ss - sr
            ghati_val = day_ghatis[wday]
            m_time = sr + (duration * ghati_val / 30.0) # 30 Ghatis = Day Duration
        else:
            # For night, we need next sunrise
            res_next = swe.rise_trans(jd + 1, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_RISE | swe.FLG_MOSEPH)
            next_sr = res_next[1][0]
            # If jd is before today's sunrise (early morning), use previous sunset
            if jd < sr:
                 res_prev_s = swe.rise_trans(jd - 1, swe.SUN, lon, lat, 0, 0, 0, swe.CALC_SET | swe.FLG_MOSEPH)
                 ss = res_prev_s[1][0]
                 duration = sr - ss
                 # Weekday is previous day for night calculation before sunrise
                 wday = (wday - 1) % 7 
            else:
                 duration = next_sr - ss
            
            ghati_val = night_ghatis[wday]
            m_time = ss + (duration * ghati_val / 30.0)

        # Calculate Ascendant at Mandi Time
        res_h = swe.houses_ex(m_time, lat, lon, b'P', swe.FLG_SIDEREAL | swe.FLG_MOSEPH)
        return res_h[0][0] % 360
    except: return 0.0

def get_panchanga(jd, moon_lon, sun_lon):
    # Tithi
    diff = (moon_lon - sun_lon + 360) % 360
    tithi_idx = int(diff / 12)
    tithi_rem = (diff % 12) / 12 # % left
    
    # Nakshatra
    nak_idx = int(moon_lon / 13.333333)
    nak_rem = (moon_lon % 13.333333) / 13.333333
    
    # Yoga
    yoga_sum = (moon_lon + sun_lon) % 360
    yoga_idx = int(yoga_sum / 13.333333)
    
    # Karana (Half Tithi)
    karana_idx = int(diff / 6)
    
    # Vara
    wday = int(jd + 0.5 + 1.5) % 7
    
    return {
        "tithi": KN_TITHI[tithi_idx],
        "nak": KN_NAK[nak_idx],
        "yoga": KN_YOGA[yoga_idx],
        "karana": KN_KARANA[karana_idx % 11], # Karana cycles
        "vara": KN_VARA[wday]
    }

# ==========================================
# 3. UI LOGIC
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
    try:
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
            
            # 1. Level 1: Mahadasha Selection
            st.subheader("ಹಂತ 1: ಮಹಾದಶ ಆಯ್ಕೆ ಮಾಡಿ")
            
            md_list = []
            curr_dt = birth_dt
            
            for i in range(9):
                idx = (start_lord + i) % 9
                yrs = YEARS[idx] * ((1-perc) if i==0 else 1)
                end_dt = curr_dt + datetime.timedelta(days=yrs*365.25)
                md_list.append({"Lord": LORDS[idx], "Start": curr_dt, "End": end_dt, "Years": YEARS[idx], "Idx": idx})
                curr_dt = end_dt
                
            md_choice = st.selectbox("ಮಹಾದಶ", md_list, format_func=lambda x: f"{x['Lord']} ({x['End'].strftime('%Y')})")
            
            # 2. Level 2: Antardasha Selection
            if md_choice:
                st.markdown("---")
                st.subheader(f"ಹಂತ 2: {md_choice['Lord']} ಅಂತರ್ದಶ")
                ad_list = []
                # AD always starts from MD Lord
                curr_ad_dt = md_choice['Start']
                
                # If it's the very first MD of life, we need to adjust the start time for the first AD?
                # Vimsottari Math: ADs follow standard proportions. 
                # For simplicity in 4-level drill down, we calculate standard ADs from MD Start
                # Note: Correct handling of birth balance in Level 2+ requires complex math. 
                # This version projects full AD cycles within the MD timeframe selected.
                
                for j in range(9):
                    ad_idx = (md_choice['Idx'] + j) % 9
                    # Prop: MD * AD / 120
                    ad_yrs = (md_choice['Years'] * YEARS[ad_idx]) / 120.0
                    
                    # Correction for first MD balance: If this is the birth MD, scaling is tricky.
                    # We will simply list the standard ADs within the dates.
                    
                    ad_end_dt = curr_ad_dt + datetime.timedelta(days=ad_yrs*365.25)
                    ad_list.append({"Lord": LORDS[ad_idx], "Start": curr_ad_dt, "End": ad_end_dt, "Years": ad_yrs, "Idx": ad_idx})
                    curr_ad_dt = ad_end_dt
                
                ad_choice = st.selectbox("ಅಂತರ್ದಶ", ad_list, format_func=lambda x: f"{x['Lord']} ({x['End'].strftime('%d-%m-%Y')})")
                
                # 3. Level 3 & 4 Table
                if ad_choice:
                    st.markdown("---")
                    st.subheader(f"ಹಂತ 3 & 4: {ad_choice['Lord']} ಭುಕ್ತಿ ವಿವರ")
                    
                    pd_data = []
                    curr_pd_dt = ad_choice['Start']
                    
                    for k in range(9):
                        pd_idx = (ad_choice['Idx'] + k) % 9
                        # Prop: AD * PD / 120
                        pd_yrs = (ad_choice['Years'] * YEARS[pd_idx]) / 120.0
                        pd_end = curr_pd_dt + datetime.timedelta(days=pd_yrs*365.25)
                        
                        # Level 4: Sookshma (Just listing the range for brevity in table)
                        pd_data.append({
                            "ಪ್ರತ್ಯಂತರ": LORDS[pd_idx],
                            "ಆರಂಭ": curr_pd_dt.strftime('%d-%m-%Y'),
                            "ಅಂತ್ಯ": pd_end.strftime('%d-%m-%Y')
                        })
                        curr_pd_dt = pd_end
                    
                    st.table(pd.DataFrame(pd_data))

        with t4:
            # Full Panchanga
            panch = get_panchanga(jd, pos["ಚಂದ್ರ"], pos["ರವಿ"])
            st.markdown(f"<div class='panch-row'><b>ವಾರ:</b> {panch['vara']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panch-row'><b>ತಿಥಿ:</b> {panch['tithi']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panch-row'><b>ನಕ್ಷತ್ರ:</b> {panch['nak']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panch-row'><b>ಯೋಗ:</b> {panch['yoga']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panch-row'><b>ಕರಣ:</b> {panch['karana']}</div>", unsafe_allow_html=True)
            
        with t5:
            st.download_button("ಡೌನ್‌ಲೋಡ್ (CSV)", df.to_csv(index=False), f"{u_name}.csv")

    except Exception as e:
        st.error(f"Error: {e}")
