import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# --- நிரந்தர டேட்டாபேஸ் சிஸ்டம் (Updated Database Name for Reset) ---
def init_db():
    # முரண்பாடுகளைத் தவிர்க்க புதிய பெயரில் டேட்டாபேஸ் உருவாக்கப்படுகிறது
    conn = sqlite3.connect('gak_marketing_v2.db', check_same_thread=False)
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
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?)", ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003'))
        conn.commit()
    conn.close()

# டேட்டாபேஸை தயார் செய்தல்
init_db()

def get_network_df():
    conn = sqlite3.connect('gak_marketing_v2.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = get_network_df()

# கமிஷன் விநியோக முறை
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect('gak_marketing_v2.db', check_same_thread=False)
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
    conn = sqlite3.connect('gak_marketing_v2.db', check_same_thread=False)
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


# --- இணையதள வடிவமைப்பு ---

if st.session_state.logged_in_user is None:
    st.title("💰 G A K Smart Marketing")
    st.caption("Private Limited | MLM Business Portal")
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔐 லாகின் (Login)", "📝 புதிய பதிவு (Sign Up)"])
    
    with tab1:
        st.subheader("👋 நல்வரவு! உங்கள் கணக்கில் நுழையவும்")
        login_user = st.text_input("பயனர் பெயர் (Username):", key="l_user", placeholder="உங்கள் பெயர்...")
        login_pass = st.text_input("கடவுச்சொல் (Password):", type="password", key="l_pass", placeholder="உங்கள் கடவுச்சொல்...")
        
        st.write("")
        if st.button("🚀 உள்நுழைக (Login)", use_container_width=True):
            user_row = df_net[(df_net['Name'] == login_user) & (df_net['Password'].astype(str) == str(login_pass))]
            if not user_row.empty:
                st.session_state.logged_in_user = login_user
                st.success(f"🎉 வெற்றிகரமாக உள்நுழைந்துவிட்டீர்கள்!")
                st.rerun()
            else:
                st.error("❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!")
                
    with tab2:
        st.subheader("🤝 புதிய உறுப்பினரை இணைக்கவும்")
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

else:
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title(f"👋 வணக்கம், {current_user}!")
        st.caption("G A K Smart Marketing Private Limited")
    with col_logout:
        st.write("")
        if st.button("🚪 லாக்-அவுட்", type="secondary"):
            st.session_state.logged_in_user = None
            st.rerun()
        
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🆔 உங்கள் ரெஃபரல் ஐடி", value=str(user_info['Unique_ID']))
    with col2:
        st.metric(label="📈 உங்கள் சொந்த விற்பனை", value=f"Rs.{user_info['Sales']:,.1f}")
    with col3:
        st.metric(label="💰 மொத்த வருமானம் (Earnings)", value=f"Rs.{user_info['Earnings']:,.1f}")
        
    st.write("---")
    
    st.header("🛒 புதிய விற்பனைப் பதிவு")
    sale_amount = st.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)
    
    if st.button("🔥 விற்பனையை உறுதிசெய் (கமிஷன் பிரி)", use_container_width=True):
        add_sale_and_distribute(current_user, sale_amount)
        st.success(f"🎉 Rs.{sale_amount} க்கான விற்பனைப் பதிவு செய்யப்பட்டது!")
        st.rerun()
        
    st.write("---")
    
    st.header("👥 உங்கள் நெட்வொர்க் டீம் விபரங்கள்")
    st.write(f"🔹 **உங்களை அறிமுகப்படுத்தியவர் (Sponsor):** **{user_info['Sponsor']}**")
    
    st.write("**🗣️ உங்களுக்குக் கீழே உள்ள டீம் மெம்பர்கள் (Downlines):**")
    downlines = df_net[df_net['Sponsor'] == current_user]
    
    if downlines.empty:
        st.info("உங்களுக்குக் கீழே இன்னும் நபர்கள் இணையவில்லை நண்பா.")
    else:
        for idx, row in downlines.iterrows():
            with st.container(border=True):
                st.write(f"👤 **பெயர்:** {row['Name']} | 🆔 **ஐடி:** {row['Unique_ID']}")
                st.write(f"📊 **விற்பனை:** Rs.{row['Sales']:,} | 💰 **வருமானம்:** Rs.{row['Earnings']:,}")
    
