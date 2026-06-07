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
        "welcome": "
