import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

DB_NAME = 'gak_marketing_v3.db'

# --- நிரந்தர டேட்டாபேஸ் சிஸ்டம் (Updated for Withdrawals) ---
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    # நெட்வொர்க் அட்டவணை
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
    
    # வித்ரா கோரிக்கை அட்டவணை
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            ID TEXT PRIMARY KEY,
            Name TEXT,
            Amount REAL,
            Method TEXT,
            Status TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003'))
        conn.commit()
    conn.close()

# டேட்டாபேஸை தயார் செய்தல்
init_db()

def get_network_df():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

def get_withdrawals_df(username):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT Amount, Method, Status FROM withdrawals WHERE Name = ?", conn, params=(username,))
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

# ஆரம்ப தரவை எடுத்தல்
df_net = get_network_df()

# கமிஷன் விநியோக முறை
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE network SET Sales = Sales + ?, Earnings = Earnings + ? WHERE Name = ?", (amount, amount, sales_person))
    
    current_person = sales_person
    level = 1
    commission_rates = {1: 0.50, 2: 0.30}
    
    while True:
        cursor.execute("SELECT Sponsor FROM network WHERE Name = ?", (current_person,))
        res = cursor.fetchone()
        if not res:
            break
            
        sponsor_name = res[0]
        if sponsor_name == "None" or sponsor_name is None:
            break
            
        if level in commission_rates:
            commission_amount = amount * commission_rates[level]
            cursor.execute("UPDATE network SET Earnings = Earnings + ? WHERE Name = ?", (commission_amount, sponsor_name))
        else:
            if sponsor_name == "Inthiran":
                cursor.execute("UPDATE network SET Earnings = Earnings + ? WHERE Name = ?", (amount * 0.20, sponsor_name))
                
        current_person = sponsor_name
        level += 1
        
    conn.commit()
    conn.close()

# புதிய நபர் பதிவு
def register_new_member(username, password, sponsor_name):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM network WHERE Name = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "⚠️ இந்த பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!"
    
    short_id = "GAK" + str(uuid.uuid4().int)[:4]
    cursor.execute("INSERT
