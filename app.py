import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

# 1. பக்கத்தின் வடிவமைப்பு மற்றும் டூல்பாரை மறைக்கும் CSS அமைப்புகள்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# ரகசிய CSS: மேல் பகுதி செட்டிங்ஸ் மற்றும் கீழ் பகுதி வாட்டர்மார்க்கை முற்றிலும் மறைக்கிறது
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppDeployButton {display:none;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

DB_NAME = 'gak_marketing_v7.db'
UPLOAD_DIR = 'uploaded_receipts'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- பன்மொழி அகராதி ---
LANG_DICT = {
    "தமிழ்": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | சர்வதேச MLM பிசினஸ் போர்ட்டல்",
        "tab_login": "🔐 லாகின் (Login)",
        "tab_signup": "📝 இலவசப் பதிவு (Free Sign Up)",
        "username": "பயனர் பெயர் / போன் / Email (Username):",
        "password": "கடவுச்சொல் (Password):",
        "btn_login": "🚀 உள்நுழைக",
        "login_err": "❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!",
        "reg_title": "🤝 புதிய கணக்கைத் துவங்குங்கள் (இலவசம்)",
        "reg_user_lbl": "பயனர் பெயர் (பெயர், போன் அல்லது Email பயன்படுத்தலாம்):",
        "reg_pass": "புதிய கடவுச்சொல் (Password):",
        "reg_sponsor": "அறிமுகப்படுத்துபவர் (Sponsor Name):",
        "btn_register": "🚀 கணக்கைத் துவங்கு (Open Account)",
        "logout": "🚪 லாக்-அவுட்",
        "welcome": "👋 வணக்கம், ",
        "menu_dash": "📊 டேஷாபோர்டு",
        "menu_with": "💰 பணம் வித்ரா",
        "menu_tree": "🌲 நெட்வொர்க்",
        "menu_search": "🔍 தேடல்",
        "ref_id": "🆔 ரெஃபரல் ஐடி",
        "my_sales": "📈 சொந்த விற்பனை",
        "my_earnings": "💰 மொத்த வருமானம்",
        "ref_link_lbl": "🔗 உங்கள் ரெஃபரல் லிங்க் (இதனைப் பகிருங்கள்):",
        "status_lbl": "⚡ கணக்கு நிலை (Account Status):"
    },
    "English": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | Global MLM Business Portal",
        "tab_login": "🔐 Login",
        "tab_signup": "📝 Free Sign Up",
        "username": "Username / Phone / Email:",
        "password": "Password:",
        "btn_login": "🚀 Login",
        "login_err": "❌ Invalid username or password!",
        "reg_title": "🤝 Create a Free Account",
        "reg_user_lbl": "Username (You can use Name, Phone or Email):",
        "reg_pass": "Create Password:",
        "reg_sponsor": "Sponsor Name:",
        "btn_register": "🚀 Open Account",
        "logout": "🚪 Logout",
        "welcome": "👋 Welcome, ",
        "menu_dash": "📊 Dashboard",
        "menu_with": "💰 Withdrawal",
        "menu_tree": "🌲 Network Tree",
        "menu_search": "🔍 Search",
        "ref_id": "Referral ID",
        "my_sales": "📈 Personal Sales",
        "my_earnings": "💰 Total Earnings",
        "ref_link_lbl": "🔗 Your Referral Link:",
        "status_lbl": "⚡ Account Status:"
    }
}

def get_package_commission_details(pkg_value):
    if pkg_value in [5, 10]: rate = 10
    elif pkg_value in [20, 40, 50]: rate = 12
    elif pkg_value in [80, 100, 150]: rate = 15
    elif pkg_value in [250, 500]: rate = 18
    elif pkg_value in [1000]: rate = 20
    else: rate = 0
    return rate, (pkg_value * rate) / 100

def init_db():
    conn = sqlite3.
            
