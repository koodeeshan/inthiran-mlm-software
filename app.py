import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

st.set_page_config(page_title="G A K Smart Marketing", layout="centered")

# CSS மறைத்தல்
hide_style = """
<style>
#MainMenu, footer, header {visibility: hidden;}
.stAppDeployButton {display:none;}
[data-testid="stToolbar"] {visibility: hidden !important;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

DB_NAME = 'gak_marketing_v7.db'
UPLOAD_DIR = 'uploaded_receipts'
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

# --- DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS network (
        Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT,
        Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT,
        Language TEXT DEFAULT 'தமிழ்', Package REAL DEFAULT 0, 
        Status TEXT DEFAULT 'Free Account', Bank_Account TEXT, ID_Passport TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS withdrawals (
        ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Method TEXT, Status TEXT)''')
    conn.commit()
    # Initial Admin
    cursor.execute("SELECT COUNT(*) FROM network WHERE Name='Inthiran'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                       ('Inthiran', 'inthiran@gak.com', '0771112223', '123', 'None', 0.0, 0.0, 'GAK001', 'Tamil', 1000, 'Active', 'BOC 123456', 'NIC99001122'))
        conn.commit()
    conn.close()

init_db()

# --- LOGIC ---
if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None

def get_user_data(username):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM network WHERE Name = ?", conn, params=(username,))
    conn.close()
    return df

# --- UI START ---
if st.session_state.logged_in_user is None:
    st.title("💰 G A K Smart Marketing")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("🚀 Login"):
        df_user = get_user_data(user)
        if not df_user.empty and str(df_user.iloc[0]['Password']) == str(pwd):
            st.session_state.logged_in_user = user
            st.rerun()
        else:
            st.error("❌ Invalid Login")
else:
    # SUCCESS AREA
    df_user = get_user_data(st.session_state.logged_in_user)
    if df_user.empty:
        st.error("User data error!")
    else:
        user_info = df_user.iloc[0]
        st.title(f"👋 வணக்கம், {user_info['Name']}!")
        st.info(f"⚡ நிலை: {user_info['Status']}")
        st.success(f"🔗 உங்கள் லிங்க்: https://dyqq3.streamlit.app/?ref={user_info['Name']}")
        
        col1, col2 = st.columns(2)
        col1.metric("ID", user_info['Unique_ID'])
        col2.metric("Sales", f"${user_info['Sales']}")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in_user = None
            st.rerun()
