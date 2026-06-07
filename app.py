import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# --- நிரந்தர டேட்டாபேஸ் சிஸ்டம் (SQLite) ---
def init_db():
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    # மெம்பர்கள் அட்டவணை
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            Name TEXT UNIQUE,
            Password TEXT,
            Sponsor TEXT,
            Sales REAL,
            Earnings REAL,
            Unique_ID TEXT
        )
    ''')
    # வித்ரா கோரிக்கைகளுக்கான புதிய அட்டவணை
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Amount REAL,
            Bank_Details TEXT,
            Status TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001')")
        cursor.execute("INSERT INTO network VALUES ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002')")
        cursor.execute("INSERT INTO network VALUES ('Bala', '123', 'An
