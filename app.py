import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

# 1. பக்க அமைப்பு மற்றும் பிழைகளை மறைக்கும் CSS
st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

hide_css = """
<style>
    #MainMenu, footer, header {visibility: hidden !important;}
    .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

DB_NAME = 'gak_marketing_v7.db'
UPLOAD_DIR = 'uploaded_receipts'
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

# 2. Database Functions
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS network (Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT, Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT, Language TEXT, Package REAL, Status TEXT, Bank_Account TEXT, ID_Passport TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals (ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. Logic & UI
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    st.title("💰 G A K Smart Marketing")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("🚀 Login"):
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM network WHERE Name=? AND Password=?", conn, params=(u, p))
        conn.close()
        if not df.empty:
            st.session_state.logged_in_user = u
            st.rerun()
        else: st.error("❌ தவறான பெயர் அல்லது கடவுச்சொல்!")
else:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM network WHERE Name=?", conn, params=(st.session_state.logged_in_user,))
    conn.close()
    
    if not df.empty:
        user = df.iloc[0]
        st.title(f"👋 வணக்கம், {user['Name']}!")
        st.info(f"⚡ நிலை: {user['Status']}")
        st.text_input("🔗 உங்கள் ரெஃபரல் லிங்க்:", f"https://dyqq3.streamlit.app/?ref={user['Name']}")
        
        tab1, tab2, tab3 = st.tabs(["📊 டேஷ்போர்டு", "💰 வித்ரா", "🌲 நெட்வொர்க்"])
        with tab1:
            st.metric("📈 சொந்த விற்பனை", f"${user['Sales']}")
            st.metric("💰 மொத்த வருமானம்", f"${user['Earnings']}")
        with tab2:
            st.write("### 💵 பணம் வித்ரா கோரிக்கை")
            amt = st.number_input("தொகை ($)", min_value=10.0)
            if st.button("🚀 கோரிக்கை அனுப்பு"): st.success("கோரிக்கை அட்மினுக்கு அனுப்பப்பட்டது!")
        with tab3:
            st.write("### 🌲 உங்கள் நெட்வொர்க் மரம்")
            st.info("உறுப்பினர்கள் யாரும் இல்லை.")
            
        if st.button("🚪 Logout"):
            st.session_state.logged_in_user = None
            st.rerun()
