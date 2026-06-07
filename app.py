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
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT,
            Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT,
            Language TEXT DEFAULT 'தமிழ்', Package REAL DEFAULT 0, 
            Status TEXT DEFAULT 'Free Account', Bank_Account TEXT, ID_Passport TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Method TEXT, Status TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network WHERE Name='Inthiran'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                       ('Inthiran', 'inthiran@gak.com', '0771112223', '123', 'None', 0.0, 0.0, 'GAK001', 'English', 1000, 'Active', 'BOC 123456', 'NIC99001122'))
        conn.commit()
    conn.close()

init_db()

def get_network_df():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

def activate_user_business(username):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Sponsor, Package FROM network WHERE Name = ?", (username,))
    res = cursor.fetchone()
    if res:
        sponsor, package = res
        cursor.execute("UPDATE network SET Status = 'Active' WHERE Name = ?", (username,))
        
        if sponsor and sponsor != "None":
            _, comm_to_pay = get_package_commission_details(package)
            cursor.execute("UPDATE network SET Sales = Sales + ?, Earnings = Earnings + ? WHERE Name = ?", (package, comm_to_pay, sponsor))
            
        conn.commit()
    conn.close()

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
if 'current_lang' not in st.session_state: st.session_state.current_lang = "தமிழ்"
if 'is_admin_logged' not in st.session_state: st.session_state.is_admin_logged = False

query_params = st.query_params
url_ref = query_params.get("ref", "")

df_net = get_network_df()
L = LANG_DICT[st.session_state.current_lang]

# --- UI வடிவமைப்பு ---

if st.session_state.logged_in_user is None and not st.session_state.is_admin_logged:
    st.title(L["title"])
    st.caption(L["caption"])
    st.write("---")
    
    tab1, tab2 = st.tabs([L["tab_login"], L["tab_signup"]])
    
    with tab1:
        login_user = st.text_input(L["username"], key="l_user")
        login_pass = st.text_input(L["password"], type="password", key="l_pass")
        
        if st.button(L["btn_login"], use_container_width=True):
            if login_user.strip() == "gak smart marketing private limited" and login_pass.strip() == "0771057786":
                st.session_state.is_admin_logged = True
                st.rerun()
            else:
                user_row = df_net[(df_net['Name'] == login_user) & (df_net['Password'].astype(str) == str(login_pass))]
                if not user_row.empty:
                    st.session_state.logged_in_user = login_user
                    st.session_state.current_lang = user_row.iloc[0]['Language']
                    st.rerun()
                else:
                    st.error(L["login_err"])
                    
    with tab2:
        st.subheader(L["reg_title"])
        all_sponsors = df_net['Name'].tolist()
        default_sponsor_idx = 0
        if url_ref and url_ref in all_sponsors:
            default_sponsor_idx = all_sponsors.index(url_ref)
            st.success(f"🔗 Referred by: **{url_ref}**")
            
        r_user = st.text_input(L["reg_user_lbl"], placeholder="Siva / 0771234567")
        r_pass = st.text_input(L["reg_pass"], type="password", key="reg_p_field")
        r_sponsor = st.selectbox(L["reg_sponsor"], all_sponsors, index=default_sponsor_idx)
        
        if st.button(L["btn_register"], use_container_width=True):
            if r_user.strip() and r_pass.strip():
                conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute("SELECT Name FROM network WHERE Name = ?", (r_user.strip(),))
                if cursor.fetchone():
                    st.error("⚠️ இந்த பெயர் ஏற்கனவேப் பயன்பாட்டில் உள்ளது!")
                    conn.close()
                else:
                    short_id = "GAK" + str(uuid.uuid4().int)[:4]
                    cursor.execute("INSERT INTO network VALUES (?, '', '', ?, ?, 0.0, 0.0, ?, 'தமிழ்', 0, 'Free Account', '', '')",
                                   (r_user.strip(), r_pass.strip(), r_sponsor, short_id))
                    conn.commit()
                    conn.close()
                    st.success("🎉 கணக்கு துவங்கப்பட்டது நண்பா! இப்போது நீங்கள் லாகின் செய்யலாம்.")
            else:
                st.warning("⚠️ விபரங்களை நிரப்பவும் நண்பா!")

elif st.session_state.is_admin_logged:
    st.title("👑 GAK Admin Command Center")
    if st.sidebar.button("🚪 அட்மின் லாக்-அவுட்", type="primary"):
        st.session_state.is_admin_logged = False; st.rerun()
        
    st.write("---")
    adm_tab1, adm_tab2 = st.tabs(["📥 Pending verifications", "👥 Full Network DB"])
    
    with adm_tab1:
        st.subheader("Working நிலையில் உள்ள கணக்குகள்")
        df_working = df_net[df_net['Status'] == 'Working']
        
        if df_working.empty:
            st.info("தற்போது சரிபார்ப்பிற்கு எந்தவொரு கணக்கும் நிலுவையில் இல்லை நண்பா!")
        else:
            for _, w_row in df_working.iterrows():
                with st.container(border=True):
                    st.subheader(f"👤 பயனர் ஐடி: {w_row['Name']}")
                    st.write(f"📧 **Email:** {w_row['Email']} | 📞 **Phone:** {w_row['Phone']}")
                    st.write(f"🏦 **வங்கி கணக்கு:** {w_row['Bank_Account']}")
                    st.write(f"🆔 **ID/பாஸ்போர்ட் இலக்கம்:** {w_row['ID_Passport']}")
                    st.write(f"📦 **பேக்கேஜ்:** ${w_row['Package']} | 🔗 **Sponsor:** {w_row['Sponsor']}")
                    
                    receipt_filename = os.path.join(UPLOAD_DIR, f"{w_row['Name']}_receipt.png")
                    if os.path.exists(receipt_filename):
                        st.image(receipt_filename, caption="Slip", width=300)
                    
                    if st.button(f"✅ Approve & Make 'Active' ({w_row['Name']})", use_container_width=True):
                        activate_user_business(w_row['Name'])
                        st.success("🎉 கணக்கு Active செய்யப்பட்டது!")
                        st.rerun()

    with adm_tab2:
        st.subheader("மாஸ்டர் நெட்வொர்க்")
        st.dataframe(df_net, use_container_width=True)

else:
    df_net = get_network_df()
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    st.title(f"👋 {L['welcome']}{current_user}!")
    st.caption("G A K Smart Marketing Private Limited")
    
    if st.sidebar.button(L["logout"], type="secondary"):
        st.session_state.logged_in_user = None; st.rerun()
        
    st.write("---")
    
    status_colors = {"Free Account": "🔵 Free Account", "Working": "⚙️ Working", "Active": "🟢 Active"}
    st.markdown(f"### {L['status_lbl']} **{status_colors.get(user_info['Status'], user_info['Status'])}**")
    
    if user_info['Status'] == 'Free Account':
        st.warning("⚠️ கணக்கை ஆக்டிவேட் செய்ய விபரங்களை பூர்த்தி செய்யவும் நண்பா!")
        
        with st.form("activation_form"):
            f_email = st.text_input("மின்னஞ்சல் முகவரி (Email Address):")
            f_phone = st.text_input("தொலைபேசி இலக்கம் (Phone Number):")
            f_bank = st.text_input("பணம் வித்ரோல் பெறும் வங்கி கணக்கு:")
            f_id_passport = st.text_input("பாஸ்போர்ட் அல்லது அடையாள அட்டை இலக்கம்:")
            
            packages = [5, 10, 20, 40, 50, 80, 100, 150, 250, 500, 1000]
            f_pkg = st.selectbox("📦 வியாபாரத் தொகை ($):", packages)
            
            p_rate, p_comm = get_package_commission_details(f_pkg)
            st.info(f"📊 கமிஷன் வீதம்: {p_rate}% | கமிஷன் தொகை: ${p_comm}")
            
            f_slip = st.file_uploader("📸 ரசீது (Upload Slip):", type=["png", "jpg", "jpeg"])
            
            if st.form_submit_button("🔥 விபரங்களை சமர்ப்பி"):
                if f_email.strip() and f_phone.strip() and f_bank.strip() and f_id_passport.strip() and f_slip:
                    file_path = os.path.join(UPLOAD_DIR, f"{current_user}_receipt.png")
                    with open(file_path, "wb") as f:
                        f.write(f_slip.getbuffer())
                    
                    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE network 
                        SET Email=?, Phone=?, Bank_Account=?, ID_Passport=?, Package=?, Status='Working' 
                        WHERE Name=?
                    ''', (f_email.strip(), f_phone.strip(), f_bank.strip(), f_id_passport.strip(), f_pkg, current_user))
                    conn.commit()
                    conn.close()
                    st.success("🎉 விபரங்கள் சமர்ப்பிக்கப்பட்டது! அட்மின் ஒப்புதலுக்குப் பின் 'Active' ஆகும் நண்பா.")
                    st.rerun()
                else:
                    st.error("⚠️ விபரங்களை முழுமையாக நிரப்பவும்!")

    else:
        shareable_ref_link = f"https://dyqq3.streamlit.app/?ref={current_user}"
        st.info(f"{L['ref_link_lbl']} `{shareable_ref_link}`")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(L["ref_id"], str(user_info['Unique_ID']))
        with col2: st.metric(L["my_sales"], f"${user_info['Sales']:,.1f}")
        with col3: st.metric(L["my_earnings"], f"${user_info['Earnings']:,.1f}")
        
        menu_tab1, menu_tab2, menu_tab3 = st.tabs([L["menu_dash"], L["menu_with"], L["menu_tree"]])
        
        with menu_tab1:
            st.write("### 📊 உங்கள் கணக்கு விபரங்கள்")
            st.write(f"📧 **மின்னஞ்சல்:** {user_info['Email']}")
            st.write(f"📞 **தொலைபேசி:** {user_info['Phone']}")
            st.write(f"🏦 **வங்கி கணக்கு:** {user_info['Bank_Account']}")
            st.write(f"🆔 **ID/பாஸ்போர்ட்:** {user_info['ID_Passport']}")
            st.write(f"📦 **பேக்கேஜ்:** ${user_info['Package']}")
            
        with menu_tab2:
            st.header(L["menu_with"])
            st.write(f"💵 உங்கள் தற்போதைய வருமானம்: **${user_info['Earnings']:,.1f}**")
            with st.form("withdraw_form"):
                w_amount = st.number_input("வித்ரா தொகை ($):", min_value=10.0, value=50.0)
                if st.form_submit_button("🚀 வித்ரா கோரிக்கை அனுப்பு"):
                    if w_amount <= user_info['Earnings'] and user_info['Status'] == 'Active':
                        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                        cursor = conn.cursor()
                        req_id = "REQ" + str(uuid.uuid4().int)[:4]
                        cursor.execute("INSERT INTO withdrawals VALUES (?, ?, ?, 'Bank Transfer', 'Pending')", (req_id, current_user, w_amount))
                        conn.commit()
                        conn.close()
                        st.success("🎉 கோரிக்கை அனுப்பப்பட்டது!"); st.rerun()
                    elif user_info['Status'] != 'Active':
                        st.error("❌ உங்கள் கணக்கு 'Active' நிலையில் இருக்க வேண்டும்!")
                    else:
                        st.error("❌ போதிய வருமானம் இல்லை!")

        with menu_tab3:
            st.header(L["menu_tree"])
            l1_members = df_net[df_net['Sponsor'] == current_user]
            with st.container(border=True):
                st.markdown(f"👑 நீங்கள்: **{current_user}** ({user_info['Status']})")
                if l1_members.empty: st.info("உறுப்பினர்கள் யாரும் இல்லை.")
                else:
                    for _, l1_row in l1_members.iterrows():
                        st.success(f"└ 👤 {l1_row['Name']} - நிலை: {l1_row['Status']}")
