import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# --- நிரந்தர டேட்டாபேஸ் உருவாக்கும் பகுதி (SQLite Local Storage Database) ---
# இது Streamlit சர்வரில் ஒரு நிரந்தர கோப்பாக (.db) விபரங்களைச் சேமிக்கும். தளம் மூடினாலும் அழியாது.
def init_db():
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    # மெம்பர்களின் விவரங்களைச் சேமிக்க அட்டவணை உருவாக்குதல்
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
    
    # ஆரம்பக்கட்ட லீடர்கள் இன்னும் உருவாக்கப்படவில்லை என்றால் மட்டும் சேர்த்தல்
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001')")
        cursor.execute("INSERT INTO network VALUES ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002')")
        cursor.execute("INSERT INTO network VALUES ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003')")
        conn.commit()
    conn.close()

# டேட்டாபேஸை தயார் செய்தல்
init_db()

# டேட்டாபேஸில் இருந்து தரவுகளைப் படிக்கும் ஃபங்க்ஷன்
def get_network_df():
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = get_network_df()

# 2. புதிய விற்பனை மற்றும் கமிஷன் பிரிப்பு ஃபங்க்ஷன் (நிரந்தர அப்டேட்)
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # விற்பனை செய்தவருக்குத் தொகை சேருதல்
    cursor.execute("UPDATE network SET Sales = Sales + ?, Earnings = Earnings + ? WHERE Name = ?", (amount, amount, sales_person))
    
    current_person = sales_person
    level = 1
    commission_rates = {1: 0.50, 2: 0.30} # லெவல் 1: 50%, லெவல் 2: 30%
    
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
            # லெவல் 2-க்கு மேல் மெயின் பாஸ் (Inthiran)-க்கு செல்லும் 20% ராயல்டி
            if sponsor_name == "Inthiran":
                cursor.execute("UPDATE network SET Earnings = Earnings + ? WHERE Name = ?", (amount * 0.20, sponsor_name))
                
        current_person = sponsor_name
        level += 1
        
    conn.commit()
    conn.close()

# 3. ரெஃபரல் மூலம் புதிய நபரை நிரந்தரமாகப் பதிவு செய்யும் ஃபங்க்ஷன்
def register_new_member(username, password, sponsor_name):
    conn = sqlite3.connect('gak_mlm_database.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Name FROM network WHERE Name = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, "⚠️ இந்த பெயர் ஏற்கனவே நெ트வொர்க்கில் உள்ளது நண்பா!"
    
    # தனித்துவமான புதிய ரெஃபரல் ஐடி (Unique ID - GAK)
    short_id = "GAK" + str(uuid.uuid4().int)[:4]
    
    cursor.execute("INSERT INTO network VALUES (?, ?, ?, 0.0, 0.0, ?)", (username, password, sponsor_name, short_id))
    conn.commit()
    conn.close()
    return True, f"🎉 பதிவு வெற்றி! உங்கள் ரெஃபரல் ஐடி: {short_id}"


# --- இணையதள வடிவமைப்பு (UI Design) ---

# லாகின் செய்யாத போது காட்டும் திரை
if st.session_state.logged_in_user is None:
    st.title("💰 G A K Smart Marketing Private Limited")
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔐 லாகின் (Login)", "📝 புதிய பதிவு (Sign Up)"])
    
    with tab1:
        st.subheader("உங்கள் கணக்கில் நுழையவும்")
        login_user = st.text_input("பயனர் பெயர் (Username):", key="l_user")
        login_pass = st.text_input("கடவுச்சொல் (Password):", type="password", key="l_pass")
        
        if st.button("உள்நுழைக (Login)"):
            user_row = df_net[(df_net['Name'] == login_user) & (df_net['Password'].astype(str) == str(login_pass))]
            if not user_row.empty:
                st.session_state.logged_in_user = login_user
                st.success(f"வரவேற்கிறோம் {login_user} நண்பா!")
                st.rerun()
            else:
                st.error("❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!")
                
    with tab2:
        st.subheader("புதிய உறுப்பினரை இணைக்கவும்")
        reg_user = st.text_input("புதிய நபர் பெயர் (Space இல்லாமல் டைப் செய்யவும்):", key="r_user")
        reg_pass = st.text_input("புதிய கடவுச்சொல் உருவாக்குங்கள்:", type="password", key="r_pass")
        
        # நெட்வொர்க்கில் உள்ள ஸ்பான்சர்களின் பட்டியல்
        all_sponsors = df_net['Name'].tolist()
        selected_sponsor = st.selectbox("அறிமுகப்படுத்துபவர் (Sponsor Name):", all_sponsors)
        
        if st.button("பதிவு செய்க (Register)"):
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

# லாகின் செய்த பின் காட்டும் பாதுகாப்பான மெம்பர் டேஷ்போர்டு (Sun-Locking)
else:
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    st.title(f"👋 வணக்கம், {current_user}!")
    st.subheader("G A K Smart Marketing Private Limited")
    
    if st.button("🚪 லாக்-அவுட் (Logout)"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.write("---")
    
    # மெம்பரின் தனிப்பட்ட டேஷ்போர்டு (Sun Locked)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🆔 உங்கள் ரெஃபரல் ஐடி", value=str(user_info['Unique_ID']))
    with col2:
        st.metric(label="📈 உங்கள் சொந்த விற்பனை", value=f"Rs.{user_info['Sales']:,.1f}")
    with col3:
        st.metric(label="💰 மொத்த வருமானம் (Earnings)", value=f"Rs.{user_info['Earnings']:,.1f}")
        
    st.write("---")
    
    # புதிய விற்பனை பதிவு செய்யும் பகுதி
    st.header("🛒 புதிய விற்பனைப் பதிவு")
    sale_amount = st.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)
    
    if st.button("விற்பனையை உறுதிசெய் (கமிஷன் பிரி)"):
        add_sale_and_distribute(current_user, sale_amount)
        st.success(f"🔥 Rs.{sale_amount} க்கக்கான விற்பனைப் பதிவு செய்யப்பட்டது! கமிஷன் தானாகவே பிரித்தளிக்கப்பட்டது.")
        st.rerun()
        
    st.write("---")
    
    # நெட்வொர்க் ட்ரீ (டீம் விபரங்கள் பார்க்கும் செக்யூரிட்டி சிஸ்டம்)
    st.header("👥 உங்கள் நெட்வொர்க் டீம் விபரங்கள்")
    st.write(f"**உங்களை அறிமுகப்படுத்தியவர் (Sponsor):** {user_info['Sponsor']}")
    
    st.write("**உங்களுக்குக் கீழே உள்ள டீம் மெம்பர்கள் (Downlines):**")
    downlines = df_net[df_net['Sponsor'] == current_user]
    
    if downlines.empty:
        st.info("உங்களுக்குக் கீழே இன்னும் நபர்கள் இணையவில்லை நண்பா. உங்கள் ரெஃபரல் ஐடியைக் கூறி புதிய நபர்களை இணைத்து டீமை உருவாக்குங்கள்!")
    else:
        for idx, row in downlines.iterrows():
            st.warning(f"👤 **{row['Name']}** | ஐடி: {row['Unique_ID']} | மொத்த விற்பனை: Rs.{row['Sales']} | வருமானம்: Rs.{row['Earnings']}")
            
