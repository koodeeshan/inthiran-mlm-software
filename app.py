import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

# CSS - டூல்பார் மறைக்க
st.markdown("""<style>#MainMenu, footer, header {visibility: hidden;} .stAppDeployButton {display:none;}</style>""", unsafe_allow_html=True)

DB_NAME = 'gak_marketing_v7.db'
if not os.path.exists('uploaded_receipts'): os.makedirs('uploaded_receipts')

# DATABASE SETUP
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS network (Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT, Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT, Status TEXT, Package REAL, Bank_Account TEXT, ID_Passport TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals (ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Status TEXT)''')
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM network WHERE Name='Inthiran'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES ('Inthiran', 'inthiran@gak.com', '0771112223', '123', 'None', 0.0, 0.0, 'GAK001', 'Active', 1000, 'BOC', 'NIC')")
        conn.commit()
    conn.close()
init_db()

# SESSION STATE
if 'user' not in st.session_state: st.session_state.user = None

# UI
if st.session_state.user is None:
    st.title("💰 G A K Smart Marketing")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("🚀 Login"):
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM network WHERE Name=? AND Password=?", conn, params=(u, p))
        conn.close()
        if not df.empty:
            st.session_state.user = u
            st.rerun()
        else: st.error("❌ தவறு!")
else:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM network WHERE Name=?", conn, params=(st.session_state.user,))
    conn.close()
    
    if not df.empty:
        user = df.iloc[0]
        st.title(f"👋 வணக்கம், {user['Name']}!")
        st.info(f"⚡ நிலை: {user['Status']}")
        st.success(f"🔗 ரெஃபரல்: https://dyqq3.streamlit.app/?ref={user['Name']}")
        
        # Dashboard Tabs
        t1, t2, t3 = st.tabs(["📊 டேஷ்போர்டு", "💰 வித்ரா", "🌲 நெட்வொர்க்"])
        with t1:
            st.metric("விற்பனை", f"${user['Sales']}")
            st.metric("வருமானம்", f"${user['Earnings']}")
        with t2:
            st.write("வித்ரா கோரிக்கை...")
            amt = st.number_input("தொகை", min_value=10.0)
            if st.button("கோரிக்கை அனுப்பு"): st.success("அனுப்பப்பட்டது!")
        with t3:
            st.write("உங்கள் குழு உறுப்பினர்கள்...")
        
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()
