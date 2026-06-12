import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

# 1. பக்கத்தின் வடிவமைப்பு
st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

# 2. CSS: அம்புக்குறி, மெனு, மற்றும் பிழைத்திருத்தங்கள் முழுமையாக மறைக்க
hide_streamlit_style = """
<style>
    #MainMenu, footer, header {visibility: hidden !important;}
    .stAppDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

DB_NAME = 'gak_marketing_v7.db'
UPLOAD_DIR = 'uploaded_receipts'
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

# 3. Database Functions
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS network (Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT, Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT, Language TEXT, Package REAL, Status TEXT, Bank_Account TEXT, ID_Passport TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals (ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Status TEXT)''')
    conn.commit()
    # Default Admin Creation
    cursor.execute("SELECT COUNT(*) FROM network WHERE Name='AdminGAK'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network (Name, Password, Status) VALUES (?, ?, ?)", ('AdminGAK', '0771057786', 'Admin'))
        conn.commit()
    conn.close()

init_db()

# 4. Session States
if 'user' not in st.session_state: st.session_state.user = None
if 'is_admin' not in st.session_state: st.session_state.is_admin = False

# 5. UI Logic
if st.session_state.user is None and not st.session_state.is_admin:
    st.title("💰 G A K Smart Marketing")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("🚀 Login"):
        if u == "AdminGAK" and p == "0771057786":
            st.session_state.is_admin = True
            st.rerun()
        else:
            conn = sqlite3.connect(DB_NAME)
            df = pd.read_sql_query("SELECT * FROM network WHERE Name=? AND Password=?", conn, params=(u, p))
            conn.close()
            if not df.empty:
                st.session_state.user = u
                st.rerun()
            else: st.error("❌ தவறான பெயர் அல்லது கடவுச்சொல்!")

elif st.session_state.is_admin:
    st.title("👑 Admin Center")
    if st.button("🚪 Logout"): st.session_state.is_admin = False; st.rerun()
    st.subheader("👥 அனைத்து பயனர்கள்")
    conn = sqlite3.connect(DB_NAME)
    st.dataframe(pd.read_sql_query("SELECT * FROM network", conn))
    conn.close()

else:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM network WHERE Name=?", conn, params=(st.session_state.user,))
    conn.close()
    
    if not df.empty:
        user = df.iloc[0]
        st.title(f"👋 வணக்கம், {user['Name']}!")
        st.info(f"⚡ நிலை: {user['Status']}")
        st.text_input("🔗 ரெஃபரல் லிங்க்:", f"https://dyqq3.streamlit.app/?ref={user['Name']}")
        
        tab1, tab2, tab3 = st.tabs(["📊 டேஷ்போர்டு", "💰 வித்ரா", "🌲 நெட்வொர்க்"])
        with tab1:
            st.metric("📈 சொந்த விற்பனை", f"${user['Sales']}")
            st.metric("💰 மொத்த வருமானம்", f"${user['Earnings']}")
        with tab2:
            st.write("### 💵 பணம் வித்ரா கோரிக்கை")
            amt = st.number_input("தொகை ($)", min_value=10.0)
            if st.button("🚀 கோரிக்கை அனுப்பு"): st.success("கோரிக்கை அட்மினுக்கு அனுப்பப்பட்டது!")
        with tab3:
            st.write("### 🌲 உங்கள் நெட்வொர்க்")
            st.info("உறுப்பினர்கள் யாரும் இல்லை.")
            
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.rerun()
