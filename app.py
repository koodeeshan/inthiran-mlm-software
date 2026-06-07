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
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        # எரர் வராதபடி மிகவும் பாதுகாப்பான முறையில் ஆரம்ப தரவுகளைச் சேர்த்தல்
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003'))
        conn.commit()
    conn.close()

# டேட்டாபேஸை தயார் செய்தல்
init_db()

def get_network_df():
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = get_network_df()

# கமிஷன் விநியோக முறை
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE network SET Sales = Sales + ?, Earnings = Earnings + ? WHERE Name = ?", (amount, amount, sales_person))
    
    current_person = sales_person
    level = 1
    commission_rates = {1: 0.50, 2: 0.30} #
