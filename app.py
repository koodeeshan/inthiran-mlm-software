import streamlit as st
import pandas as pd
import uuid

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல் (புதிய பெயர் மாற்றத்துடன்)
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

# 2. தரவுகளைச் சேமிப்பதற்கான சிஸ்டம் (Session State & Local Storage Simulation)
if 'network_data' not in st.session_state:
    # ஆரம்பக்கட்ட உறுப்பினர்கள் விவரம்
    initial_data = [
        {"Name": "Inthiran", "Password": "123", "Sponsor": "None", "Sales": 0.0, "Earnings": 0.0, "Unique_ID": "GAK001"},
        {"Name": "Anand", "Password": "123", "Sponsor": "Inthiran", "Sales": 0.0, "Earnings": 0.0, "Unique_ID": "GAK002"},
        {"Name": "Bala", "Password": "123", "Sponsor": "Anand", "Sales": 0.0, "Earnings": 0.0, "Unique_ID": "GAK003"}
    ]
    st.session_state.network_data = pd.DataFrame(initial_data)

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

df_net = st.session_state.network_data

# 3. புதிய销售 மற்றும் கமிஷன் பிரிப்பு ஃபங்க்ஷன்
def add_sale_and_distribute(sales_person, amount):
    df = st.session_state.network_data.copy()
    
    # விற்பனை செய்தவருக்குத் தொகை சேருதல்
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
            # லெவல் 2-க்கு மேல் மெயின் பாஸ் (Inthiran)-க்கு செல்லும் 20% ராயல்டி
            if sponsor_name == "Inthiran":
                df.loc[df['Name'] == sponsor_name, 'Earnings'] += (amount * 0.20)
                
        current_person = sponsor_name
        level += 1
        
    st.session_state.network_data = df

# 4. ரெஃபரல் மூலம் புதிய நபரைப் பதிவு செய்யும் ஃபங்க்ஷன்
def register_new_member(username, password, sponsor_name):
    df = st.session_state.network_data.copy()
    if username in df['Name'].values:
        return False, "⚠️ இந்த பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!"
    
    # தனித்துவமான புதிய ரெஃபரல் ஐடி (Unique ID - GAK என்று தொடங்கும்)
    short_id = "GAK" + str(uuid.uuid4().int)[:4]
    
    new_row = {
        "Name": username,
        "Password": password,
        "Sponsor": sponsor_name,
        "Sales": 0.0,
        "Earnings": 0.0,
        "Unique_ID": short_id
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.network_data = df
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
    
    # மெம்பரின் தனிப்பட்ட டேஷ்போர்டு (யாரும் இதை மாற்ற முடியாது - Sun Locked)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🆔 உங்கள் ரெஃபரல் ஐடி", value=str(user_info['Unique_ID']))
    with col2:
        st.metric(label="📈 உங்கள் சொந்த விற்பனை", value=f"Rs.{user_info['Sales']:,.1f}")
    with col3:
        st.metric(label="💰 மொத்த வருமானம் (Earnings)", value=f"Rs.{user_info['Earnings']:,.1f}")
        
    st.write("---")
    
    # புதிய விற்பனை பதிவு செய்யும் பகுதி (அவரவர் கணக்கில் இருந்து அவர்களே விற்பனை போடலாம்)
    st.header("🛒 புதிய விற்பனைப் பதிவு")
    sale_amount = st.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)
    
    if st.button("விற்பனையை உறுதிசெய் (கமிஷன் பிரி)"):
        add_sale_and_distribute(current_user, sale_amount)
        st.success(f"🔥 Rs.{sale_amount} க்கான விற்பனைப் பதிவு செய்யப்பட்டது! கமிஷன் தானாகவே பிரித்தளிக்கப்பட்டது.")
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
