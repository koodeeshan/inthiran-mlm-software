import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# --- நிரந்தர டேட்டாபேஸ் சிஸ்டம் ---
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
        cursor.execute("INSERT INTO network VALUES ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001')")
        cursor.execute("INSERT INTO network VALUES ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002')")
        cursor.execute("INSERT INTO network VALUES ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003')")
        conn.commit()
    conn.close()

init_db()

def get_network_df():
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = get_network_df()

# கமிஷன் விநியோகம்
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
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
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM network WHERE Name = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "⚠️ இந்த பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!"
    
    short_id = "GAK" + str(uuid.uuid4().int)[:4]
    cursor.execute("INSERT INTO network VALUES (?, ?, ?, 0.0, 0.0, ?)", (username, password, sponsor_name, short_id))
    conn.commit()
    conn.close()
    return True, f"🎉 பதிவு வெற்றி! உங்கள் ரெஃபரல் ஐடி: {short_id}"


# --- இணையதள வடிவமைப்பு (Colorful UI) ---

# லாகின் செய்யாத போது காட்டும் திரை
if st.session_state.logged_in_user is None:
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>💰 G A K Smart Marketing</h1>", unsafe_style_allowed=True)
    st.markdown("<p style='text-align: center; color: #666;'>Private Limited | MLM Business Portal</p>", unsafe_style_allowed=True)
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔐 லாகின் (Login)", "📝 புதிய பதிவு (Sign Up)"])
    
    with tab1:
        st.markdown("### 👋 நல்வரவு! உங்கள் கணக்கில் நுழையவும்")
        login_user = st.text_input("பயனர் பெயர் (Username):", key="l_user", placeholder="உங்கள் பெயர்...")
        login_pass = st.text_input("கடவுச்சொல் (Password):", type="password", key="l_pass", placeholder="உங்கள் கடவுச்சொல்...")
        
        st.write("")
        if st.button("🚀 உள்நுழைக (Login)", use_container_width=True):
            user_row = df_net[(df_net['Name'] == login_user) & (df_net['Password'].astype(str) == str(login_pass))]
            if not user_row.empty:
                st.session_state.logged_in_user = login_user
                st.success(f"வரவேற்கிறோம் {login_user} நண்பா!")
                st.rerun()
            else:
                st.error("❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!")
                
    with tab2:
        st.markdown("### 🤝 புதிய உறுப்பினரை இணைக்கவும்")
        reg_user = st.text_input("புதிய நபர் பெயர் (Space இல்லாமல்):", key="r_user", placeholder="உதாரணம்: Siva")
        reg_pass = st.text_input("புதிய கடவுச்சொல் உருவாக்குங்கள்:", type="password", key="r_pass", placeholder="பாதுகாப்பான கடவுச்சொல்...")
        
        all_sponsors = df_net['Name'].tolist()
        selected_sponsor = st.selectbox("அறிமுகப்படுத்துபவர் (Sponsor Name):", all_sponsors)
        
        st.write("")
        if st.button("✅ பதிவு செய்க (Register)", use_container_width=True):
            if reg_user.strip() != "" and reg_pass.strip() != "":
                success, msg = register_new_member(reg_user.strip(), reg_pass.strip(), selected_sponsor)
                if success:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("தயவுசெய்து அனைத்து விபரங்களையும் நிரப்பவும் நண்பா!")

# லாகின் செய்த பின் காட்டும் பாதுகாப்பான மெம்பர் டேஷ்போர்டு
else:
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    # மேல் பகுதி வடிவமைப்பு
    st.markdown(f"<h2 style='color: #00CC66;'>👋 வணக்கம், {current_user}!</h2>", unsafe_style_allowed=True)
    st.markdown("<p style='font-size:18px; color:#555;'><b>G A K Smart Marketing Private Limited</b></p>", unsafe_style_allowed=True)
    
    if st.button("🚪 லாக்-அவுட் (Logout)", type="secondary"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.write("---")
    
    # மெம்பரின் தனிப்பட்ட வண்ணமயமான டேஷ்போர்டு (Metrics Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='background-color:#F0F2F6; padding:15px; border-radius:10px; border-left: 5px solid #FF4B4B;'><b>🆔 ரெஃபரல் ஐடி</b><br><span style='font-size:22px; color:#FF4B4B; font-weight:bold;'>{user_info['Unique_ID']}</span></div>", unsafe_style_allowed=True)
    with col2:
        st.markdown(f"<div style='background-color:#F0F2F6; padding:15px; border-radius:10px; border-left: 5px solid #1E90FF;'><b>📈 சொந்த விற்பனை</b><br><span style='font-size:22px; color:#1E90FF; font-weight:bold;'>Rs.{user_info['Sales']:,.1f}</span></div>", unsafe_style_allowed=True)
    with col3:
        st.markdown(f"<div style='background-color:#EEF9F1; padding:15px; border-radius:10px; border-left: 5px solid #00CC66;'><b>💰 மொத்த வருமானம்</b><br><span style='font-size:22px; color:#00CC66; font-weight:bold;'>Rs.{user_info['Earnings']:,.1f}</span></div>", unsafe_style_allowed=True)
        
    st.write("---")
    
    # புதிய விற்பனை பதிவு செய்யும் பகுதி
    st.markdown("### 🛒 புதிய விற்பனைப் பதிவு")
    st.write("உங்களின் புதிய விற்பனைத் தொகையை இங்கே பதிவிடுங்கள்:")
    sale_amount = st.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0, label_visibility="collapsed")
    
    if st.button("🔥 விற்பனையை உறுதிசெய் (கமிஷன் பிரி)", use_container_width=True):
        add_sale_and_distribute(current_user, sale_amount)
        st.success(f"🎉 Rs.{sale_amount} க்கான விற்பனைப் பதிவு வெற்றிகரமாகச் சேர்க்கப்பட்டது!")
        st.rerun()
        
    st.write("---")
    
    # நெட்வொர்க் டீம் விபரங்கள் காட்டும் பகுதி
    st.markdown("### 👥 உங்கள் நெட்வொர்க் டீம் விபரங்கள்")
    st.markdown(f"🔹 **உங்களை அறிமுகப்படுத்தியவர் (Sponsor):** <span style='color:#FF4B4B; font-weight:bold;'>{user_info['Sponsor']}</span>", unsafe_style_allowed=True)
    st.write("")
    
    st.markdown("🗣️ **உங்களுக்குக் கீழே உள்ள டீம் மெம்பர்கள் (Downlines):**")
    downlines = df_net[df_net['Sponsor'] == current_user]
    
    if downlines.empty:
        st.info("உங்களுக்குக் கீழே இன்னும் நபர்கள் இணையவில்லை நண்பா. உங்கள் ரெஃபரல் ஐடியைக் கூறி புதிய நபர்களை இணைத்து டீமை உருவாக்குங்கள்!")
    else:
        for idx, row in downlines.iterrows():
            # ஒவ்வொரு மெம்பருக்கும் தனித்தனியாக அழகான கார்டு வடிவமைப்பு
            st.markdown(f"""
            <div style='background-color:#FFF; padding:12px; border-radius:8px; border:1px solid #E0E0E0; margin-bottom:10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);'>
                <span style='font-size:16px; color:#333;'>👤 <b>{row['Name']}</b> (ஐடி: {row['Unique_ID']})</span><br>
                <span style='font-size:14px; color:#666;'>📊 விற்பனை: Rs.{row['Sales']:,} | 💰 வருமானம்: Rs.{row['Earnings']:,}</span>
            </div>
            """, unsafe_style_allowed=True)
