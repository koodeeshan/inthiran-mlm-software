import streamlit as st 
import streamlit as st
import pandas as pd
import sqlite3

# பக்க வடிவமைப்பு
st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

# CSS: மெனு மற்றும் அம்புக்குறியை மறைக்க
hide_css = """
<style>
    #MainMenu, footer, header {visibility: hidden !important;}
    .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

# மல்டி-லாங்குவேஜ் அகராதி
LANG_DATA = {
    "English": {"login": "Login", "user": "Username", "pass": "Password", "dash": "Dashboard", "tree": "Network"},
    "සිංහල": {"login": "ඇතුල් වන්න", "user": "පරිශීලක නාමය", "pass": "මුරපදය", "dash": "පුවරුව", "tree": "ජාලය"},
    "தமிழ்": {"login": "உள்நுழைக", "user": "பயனர் பெயர்", "pass": "கடவுச்சொல்", "dash": "டேஷ்போர்டு", "tree": "நெட்வொர்க்"}
}

# Database
DB_NAME = 'gak_marketing_v7.db'
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS network (Name TEXT UNIQUE, Password TEXT, Status TEXT)')
conn.commit()
conn.close()

# Session State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lang' not in st.session_state: st.session_state.lang = "English"

# UI பகுதி
st.title("💰 G A K Smart Marketing")
st.session_state.lang = st.selectbox("🌐 Language / භාෂාව / மொழி", ["English", "සිංහල", "தமிழ்"])
L = LANG_DATA[st.session_state.lang]

if not st.session_state.logged_in:
    u = st.text_input(L["user"])
    p = st.text_input(L["pass"], type="password")
    if st.button(L["login"]):
        if u == "GAK" and p == "123":
            st.session_state.logged_in = True
            st.session_state.user = "Admin"
            st.rerun()
        else:
            st.error("Invalid Login")
else:
    # லாகின் ஆன பிறகு காண்பிக்கும் பகுதி
    st.success(f"வெல்கம் kodeeshan {st.session_state.user}!")
    
    # மெனு டேப்கள்
    tab1, tab2 = st.tabs([L["dash"], L["tree"]])
    with tab1:
        st.write("Dashboard content goes here")
    with tab2:
        st.write("Network tree goes here")
        
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
