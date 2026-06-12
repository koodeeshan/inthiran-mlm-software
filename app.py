import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

# CSS: அனைத்தும் மறைக்க
hide_css = """
<style>
    #MainMenu, footer, header {visibility: hidden !important;}
    .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

# மல்டி-லாங்குவேஜ் அகராதி
LANG_DATA = {
    "தமிழ்": {"login": "உள்நுழைக", "user": "பயனர் பெயர்", "pass": "கடவுச்சொல்", "lang": "தமிழ்"},
    "සිංහල": {"login": "ඇතුල් වන්න", "user": "පරිශීලක නාමය", "pass": "මුරපදය", "lang": "සිංහල"},
    "English": {"login": "Login", "user": "Username", "pass": "Password", "lang": "English"}
}

# Database setup
DB_NAME = 'gak_marketing_v7.db'
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS network (Name TEXT UNIQUE, Password TEXT, Status TEXT)''')
    cursor.execute("SELECT COUNT(*) FROM network WHERE Name='AdminGAK'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network (Name, Password, Status) VALUES (?, ?, ?)", ('AdminGAK', '0771057786', 'Admin'))
        conn.commit()
    conn.close()
init_db()

# Session State
if 'lang' not in st.session_state: st.session_state.lang = "English"

# UI
st.title("💰 G A K Smart Marketing")
st.session_state.lang = st.selectbox("🌐 Select Language / භාෂාව තෝරන්න / மொழியைத் தேர்ந்தெடுக்கவும்", ["English", "සිංහල", "தமிழ்"])

L = LANG_DATA[st.session_state.lang]

u = st.text_input(L["user"])
p = st.text_input(L["pass"], type="password")

if st.button(L["login"]):
    if u == "AdminGAK" and p == "0771057786":
        st.success("Admin Access Granted")
    else:
        st.error("Login Failed")
