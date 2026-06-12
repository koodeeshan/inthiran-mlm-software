import streamlit as st

# 1. பக்கத்தின் அமைப்பு
st.set_page_config(page_title="G A K Smart Marketing", layout="wide")

# 2. அந்த 'Manage app' அம்புக்குறியை மறைக்கும் குறியீடு
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stDecoration"] {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. ஹெடர் பகுதி
st.title("💰 G A K Smart Marketing")

# 4. மொழித் தேர்வு
lang = st.selectbox("🌐 Language / භාෂාව / மொழி", ["English", "Tamil", "Sinhala"])

# 5. உள்நுழைவு நிலை (வெற்றிகரமான லாகின் உதாரணம்)
st.success("Welcome Admin!")

# 6. டேஷ்போர்டு தாவல்கள் (Tabs)
tab1, tab2 = st.tabs(["📊 Dashboard", "🌐 Network"])

with tab1:
    st.subheader("Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Members", "1,250")
    col2.metric("Active Members", "980")
    col3.metric("Total Revenue", "$15,400")
    st.write("இங்கு உங்கள் மார்க்கெட்டிங் புள்ளிவிவரங்கள் அமையும்.")

with tab2:
    st.subheader("Network Structure")
    st.write("உங்கள் குழுவின் கட்டமைப்பு மற்றும் உறுப்பினர்களின் விபரங்கள் இங்கே இருக்கும்.")
    # உதாரணத்திற்கு ஒரு டேபிள்
    st.table({
        "Name": ["அருண்", "குமார்", "கவிதா"],
        "Level": ["Gold", "Silver", "Platinum"],
        "Earnings": ["$500", "$300", "$800"]
    })

# 7. லாக் அவுட் பட்டன்
if st.button("Logout"):
    st.warning("நீங்கள் வெளியேறிவிட்டீர்கள்.")
    
