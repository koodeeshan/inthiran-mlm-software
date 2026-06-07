import streamlit as st
import pandas as pd
import uuid

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="A K G Smart Commission Marketing Pvt Ltd", page_icon="💰", layout="centered")

# 2. கூகுள் சீட் CSV முகவரி (தரவுகளைப் படிக்க மட்டும்)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1uu7CfjOA4ISDSQKxPVQCLDZufJummYbkMsFnjwWvvWc/export?format=csv"

# 3. தரவுகளை லோடு செய்யும் ஃபங்க்ஷன்
def load_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # புதிய சிஸ்டத்திற்குத் தேவையான தூண்கள் (Columns) உள்ளனவா எனச் சரிபார்த்தல்
        required_cols = ['Name', 'Password', 'Sponsor', 'Sales', 'Earnings', 'Unique_ID']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0 if col in ['Sales', 'Earnings'] else "None"
        return df
    except Exception:
        # ஆன்லைனில் படிக்க முடியாவிட்டால் காட்டப்படும் ஆரம்பக்கட்ட பாதுகாப்பான தரவு
        initial_data = [
            {"Name": "Inthiran", "Password": "123", "Sponsor": "None", "Sales": 0, "Earnings": 0, "Unique_ID": "AKG001"},
            {"Name": "Anand", "Password": "123", "Sponsor": "Inthiran", "Sales": 0, "Earnings": 0, "Unique_ID": "AKG002"},
            {"Name": "Bala", "Password": "123", "Sponsor": "Anand", "Sales": 0, "Earnings": 0, "Unique_ID": "AKG003"}
        ]
        return pd.DataFrame(initial_data)

# செஷன் ஸ்டேட்டில் தரவைச் சேமித்தல்
if 'network' not in st.session_state:
    st.session_state.network = load_data()

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = st.session_state.network

# 4. புதிய விற்பனை மற்றும் கமிஷன் தானாகப் பிரியும் ஃபங்க்ஷன்
def add_sale_and_distribute(sales_person, amount):
    df = st.session_state.network.copy()
    
    # விற்பனை செய்தவருக்கு கூட்டுதல்
    df.loc[df['Name'] == sales_person, 'Sales'] += amount
    df.loc[df['Name'] == sales_person, 'Earnings'] += amount
    
    current_person = sales_person
    level = 1
    commission_rates = {1: 0.50, 2: 0.30} # லெவல் 1: 50%, லெவல் 2: 30%
    
    while True:
        sponsor_row = df[df['Name'] == current_person]
        if sponsor_row.empty:
            break
            
        sponsor_name = sponsor_row.iloc[0]['Sponsor']
        if sponsor_name == "None" or pd.isna(sponsor_name):
            break
            
        if level in commission_rates:
            commission_amount = amount * commission_rates[level]
            df.loc[df['Name'] == sponsor_name, 'Earnings'] += commission_amount
        else:
            # மெயின் பாஸ் (Inthiran)-க்கு செல்லும் ராயல்டி கமிஷன்
            if sponsor_name == "Inthiran":
                df.loc[df['Name'] == sponsor_name, 'Earnings'] += (amount * 0.20)
                
        current_person = sponsor_name
        level += 1
        
    st.session_state.network = df

# 5. புதிய நபர் சைன்-அப் / ரெஃபரல் மூலம் இணையும் ஃபங்க்ஷன்
def register_new_member(username, password, sponsor_name):
    df = st.session_state.network.copy()
    if username in df['Name'].values:
        return False, "⚠️ இந்த பெயர் ஏற்கனவே உள்ளது நண்பா!"
    
    # தனித்துவமான ரெஃபரல் ஐடி உருவாக்குதல்
    short_id = "AKG" + str(uuid.uuid4().int)[:4]
    
    new_row = {
        "Name": username,
        "Password": password,
        "Sponsor": sponsor_name,
        "Sales": 0,
        "Earnings": 0,
        "Unique_ID": short_id
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.network = df
    return True, f"🎉 வெற்றி! உங்கள் ரெஃபரல் ஐடி: {short_id}"

# --- லாகின் ஸ்கிரீன் வடிவமைப்பு ---
if st.session_state.logged_in_user is None:
    st.title("💰 A K G Smart MLM Portal")
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔐 லாகின் (Login)", "📝 புதிய பதிவு (Sign Up)"])
    
    with tab1:
        st.subheader("உங்கள் கணக்கில் நுழையவும்")
        login_user = st.text_input("பயனர் பெயர் (Username):", key="login_u")
        login_pass = st.text_input("கடவுச்சொல் (Password):", type="password", key="login_p")
        
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
        reg_user = st.text_input("புதிய நபர் பெயர்:", key="reg_u")
        reg_pass = st.text_input("புதிய கடவுச்சொல் உருவாக்குங்கள்:", type="password", key="reg_p")
        
        # ரெஃபரல் கொடுப்பதற்காக ஏற்கனவே இருக்கும் மெம்பர்களின் பட்டியல்
        all_sponsors = df_net['Name'].tolist()
        selected_sponsor = st.selectbox("அறிமுகப்படுத்துபவர் (Sponsor Name):", all_sponsors)
        
        if st.button("பதிவு செய்க (Register)"):
            if reg_user.strip() != "" and reg_pass.strip() != "":
                success, msg = register_new_member(reg_user.strip(), reg_pass.strip(), selected_sponsor)
                if success:
                    st.success(msg)
                    st.balloons()
                else:
                    st.error(msg)
            else:
                st.warning("தயவுசெய்து அனைத்து விபரங்களையும் நிரப்பவும் நண்பா!")

# --- லாகின் செய்த பின் காட்டும் மெம்பர் டேஷ்போர்டு (Sun-Locking Dashboard) ---
else:
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    # ஹேடர் பகுதி
    st.title(f"👋 வணக்கம், {current_user}!")
    st.subheader("A K G Smart Commission Marketing Pvt Ltd")
    
    if st.button("🚪 லாக்-அவுட் (Logout)"):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.write("---")
    
    # மெம்பரின் தனிப்பட்ட டேஷ்போர்டு (யாரும் இதை மாற்ற முடியாது - Sun Locked)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🆔 உங்கள் ரெஃபரல் ஐடி", value=str(user_info['Unique_ID']))
    with col2:
        st.metric(label="📈 உங்கள் சொந்த விற்பனை", value=f"Rs.{user_info['Sales']:,}")
    with col3:
        st.metric(label="💰 மொத்த வருமானம் (Earnings)", value=f"Rs.{user_info['Earnings']:,}")
        
    st.write("---")
    
    # புதிய விற்பனை பதிவு செய்யும் பகுதி (அவரவர் கணக்கில் இருந்து அவர்களே விற்பனை போடலாம்)
    st.header("🛒 புதிய விற்பனைப் பதிவு")
    sale_amount = st.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)
    
    if st.button("விற்பனையை உறுதிசெய் (கமிஷன் பிரி)"):
        add_sale_and_distribute(current_user, sale_amount)
        st.success(f"🔥 Rs.{sale_amount} க்கான விற்பனைப் பதிவு செய்யப்பட்டது! கமிஷன் அப்லைனர்களுக்குப் பிரித்தளிக்கப்பட்டது.")
        st.rerun()
        
    st.write("---")
    
    # நெட்வொர்க் ட்ரீ (டீம் விபரங்கள் பார்க்கும் பகுதி)
    st.header("👥 உங்கள் நெட்வொர்க் டீம் விபரங்கள்")
    
    # லாகின் செய்த நபருக்குக் கீழே இருப்பவர்களை (Downlines) மட்டும் காட்டும் செக்யூரிட்டி சிஸ்டம்
    st.write(f"**உங்களை அறிமுகப்படுத்தியவர் (Sponsor):** {user_info['Sponsor']}")
    
    st.write("**உங்களுக்குக் கீழே உள்ள டீம் மெம்பர்கள்:**")
    downlines = df_net[df_net['Sponsor'] == current_user]
    
    if downlines.empty:
        st.info("உங்களுக்குக் கீழே இன்னும் நபர்கள் இணையவில்லை நண்பா. உங்கள் ரெஃபரல் ஐடியைப் பகிர்ந்து டீமை உருவாக்குங்கள்!")
    else:
        for idx, row in downlines.iterrows():
            st.warning(f"👤 **{row['Name']}** | ஐடி: {row['Unique_ID']} | விற்பனை: Rs.{row['Sales']} | வருமானம்: Rs.{row['Earnings']}")
