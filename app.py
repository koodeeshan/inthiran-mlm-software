import streamlit as st
import pandas as pd
import uuid
import sqlite3
import os

# 1. பக்கத்தின் வடிவமைப்பு
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

DB_NAME = 'gak_marketing_v6.db'
UPLOAD_DIR = 'uploaded_receipts'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- பன்மொழி அகராதி ---
LANG_DICT = {
    "தமிழ்": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | சர்வதேச MLM பிசினஸ் போர்ட்டல்",
        "tab_login": "🔐 லாகின் (Login)",
        "tab_signup": "📝 புதிய பதிவு (Sign Up)",
        "username": "பயனர் பெயர் (Username):",
        "password": "கடவுச்சொல் (Password):",
        "btn_login": "🚀 உள்நுழைக",
        "login_err": "❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!",
        "login_success": "🎉 வெற்றிகரமாக உள்நுழைந்துவிட்டீர்கள்!",
        "reg_title": "🤝 புதிய உறுப்பினராக இணையுங்கள்",
        "reg_name": "உங்கள் முழுப் பெயர்:",
        "reg_email": "மின்னஞ்சல் முகவரி (Email):",
        "reg_phone": "தொலைபேசி இலக்கம் (Phone):",
        "reg_pass": "புதிய கடவுச்சொல் (Password):",
        "reg_sponsor": "அறிமுகப்படுத்துபவர் (Sponsor Name):",
        "reg_pkg": "📦 வியாபாரத் தொகுப்பைத் தெரிவு செய்க ($):",
        "btn_register": "✅ விண்ணப்பத்தை சமர்ப்பிக்கவும்",
        "logout": "🚪 லாக்-அவுட்",
        "welcome": "👋 வணக்கம், ",
        "menu_dash": "📊 டேஷாபோர்டு",
        "menu_with": "💰 பணம் வித்ரா",
        "menu_tree": "🌲 நெட்வொர்க்",
        "menu_search": "🔍 தேடல்",
        "ref_id": "🆔 ரெஃபரல் ஐடி",
        "my_sales": "📈 சொந்த விற்பனை",
        "my_earnings": "💰 மொத்த வருமானம்",
        "ref_link_lbl": "🔗 உங்கள் ரெஃபரல் லிங்க் (இதனைப் பகிருங்கள்):"
    },
    "English": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | Global MLM Business Portal",
        "tab_login": "🔐 Login",
        "tab_signup": "📝 Sign Up",
        "username": "Username:",
        "password": "Password:",
        "btn_login": "🚀 Login",
        "login_err": "❌ Invalid username or password!",
        "login_success": "🎉 Successfully logged in!",
        "reg_title": "🤝 Join as a New Member",
        "reg_name": "Full Name:",
        "reg_email": "Email Address:",
        "reg_phone": "Phone Number:",
        "reg_pass": "Create Password:",
        "reg_sponsor": "Sponsor Name:",
        "reg_pkg": "📦 Select Business Package ($):",
        "btn_register": "✅ Submit Registration",
        "logout": "🚪 Logout",
        "welcome": "👋 Welcome, ",
        "menu_dash": "📊 Dashboard",
        "menu_with": "💰 Withdrawal",
        "menu_tree": "🌲 Network Tree",
        "menu_search": "🔍 Search",
        "ref_id": "🆔 Referral ID",
        "my_sales": "📈 Personal Sales",
        "my_earnings": "💰 Total Earnings",
        "ref_link_lbl": "🔗 Your Referral Link (Share this):"
    }
}

# கமிஷன் வீதம் மற்றும் தொகையைக் கணக்கிடும் பங்க்ஷன்
def get_package_commission_details(pkg_value):
    if pkg_value in [5, 10]:
        rate = 10
    elif pkg_value in [20, 40, 50]:
        rate = 12
    elif pkg_value in [80, 100, 150]:
        rate = 15
    elif pkg_value in [250, 500]:
        rate = 18
    elif pkg_value in [1000]:
        rate = 20
    else:
        rate = 0
    comm_amount = (pkg_value * rate) / 100
    return rate, comm_amount

def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            Name TEXT UNIQUE, Email TEXT, Phone TEXT, Password TEXT,
            Sponsor TEXT, Sales REAL, Earnings REAL, Unique_ID TEXT,
            Language TEXT DEFAULT 'தமிழ்', Package REAL DEFAULT 0, Status TEXT DEFAULT 'Active'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_users (
            ID TEXT PRIMARY KEY, Name TEXT, Email TEXT, Phone TEXT, Password TEXT,
            Sponsor TEXT, Package REAL, Receipt_Path TEXT, Status TEXT DEFAULT 'Pending'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            ID TEXT PRIMARY KEY, Name TEXT, Amount REAL, Method TEXT, Status TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('Inthiran', 'inthiran@gak.com', '0771112223', '123', 'None', 0.0, 0.0, 'GAK001', 'English', 1000, 'Active'))
        cursor.execute("INSERT INTO network VALUES (?,?,?,?,?,?,?,?,?,?,?)", ('Anand', 'anand@gak.com', '0774445556', '123', 'Inthiran', 0.0, 0.0, 'GAK002', 'English', 100, 'Active'))
        conn.commit()
    conn.close()

init_db()

def get_network_df():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

# அட்மின் ஒப்புதல் அளித்த பின் கமிஷன் அப்லைனருக்குச் செல்லும் பங்க்ஷன்
def approve_user_and_pay_commission(pending_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("SELECT Name, Email, Phone, Password, Sponsor, Package FROM pending_users WHERE ID = ?", (pending_id,))
    res = cursor.fetchone()
    if res:
        name, email, phone, password, sponsor, package = res
        short_id = "GAK" + str(uuid.uuid4().int)[:4]
        
        # 1. புதிய நபரை மெம்பர் டேபிளில் இணைத்தல்
        try:
            cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                           (name, email, phone, password, sponsor, package, 0.0, short_id, 'தமிழ்', package, 'Active'))
        except sqlite3.IntegrityError:
            return False, "பயனர் பெயர் ஏற்கனவே உள்ளது!"
            
        # 2. அப்லைனருக்கு (Sponsor) கmission வழங்குதல்
        if sponsor and sponsor != "None":
            _, comm_to_pay = get_package_commission_details(package)
            cursor.execute("UPDATE network SET Sales = Sales + ?, Earnings = Earnings + ? WHERE Name = ?", (package, comm_to_pay, sponsor))
            
        # 3. நிலுவை அட்டவணையை மாற்றுதல்
        cursor.execute("UPDATE pending_users SET Status = 'Approved' WHERE ID = ?", (pending_id,))
        conn.commit()
    conn.close()
    return True, "வெற்றிகரமாக அப்ரூவ் செய்யப்பட்டு கமிஷன் அப்லைனருக்குச் சென்றடைந்தது!"

if 'logged_in_user' not in st.session_state: st.session_state.logged_in_user = None
if 'current_lang' not in st.session_state: st.session_state.current_lang = "தமிழ்"
if 'is_admin_logged' not in st.session_state: st.session_state.is_admin_logged = False

# URL இலிருந்து தானாக ரெஃபரல் ஐடியைப் படித்தல் (Auto Referral Check)
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
        
        # ரெஃபரல் லிங்க் மூலம் வந்திருந்தால் ஸ்பான்சர் பெயர் தானாக லாக் ஆகும்
        all_sponsors = df_net['Name'].tolist()
        default_sponsor_idx = 0
        if url_ref and url_ref in all_sponsors:
            default_sponsor_idx = all_sponsors.index(url_ref)
            st.success(f"🔗 Referred by: **{url_ref}**")
            
        r_name = st.text_input(L["reg_name"], placeholder="Siva")
        r_email = st.text_input(L["reg_email"], placeholder="siva@gmail.com")
        r_phone = st.text_input(L["reg_phone"], placeholder="077XXXXXXX")
        r_pass = st.text_input(L["reg_pass"], type="password")
        
        r_sponsor = st.selectbox(L["reg_sponsor"], all_sponsors, index=default_sponsor_idx)
        
        # பேக்கேஜ் தெரிவு செய்தல்
        packages = [5, 10, 20, 40, 50, 80, 100, 150, 250, 500, 1000]
        selected_pkg = st.selectbox(L["reg_pkg"], packages)
        
        # கமிஷன் விபரங்களை நேரலையாகக் காட்டுதல்
        pkg_rate, pkg_comm = get_package_commission_details(selected_pkg)
        st.info(f"📊 இந்த தொகுப்பிற்கான கமிஷன் வீதம்: **{pkg_rate}%** | அப்லைனருக்குச் செல்லும் தொகை: **${pkg_comm}**")
        
        # ரசீது பதிவேற்றம்
        uploaded_file = st.file_uploader("📸 பண ரசீதை இங்கே அப்லோடு செய்யவும் (Receipt Upload):", type=["png", "jpg", "jpeg"])
        
        if st.button(L["btn_register"], use_container_width=True):
            if r_name.strip() and r_email.strip() and r_phone.strip() and r_pass.strip() and uploaded_file:
                conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute("SELECT Name FROM network WHERE Name = ?", (r_name.strip(),))
                if cursor.fetchone():
                    st.error("⚠️ இந்த பயனர் பெயர் ஏற்கனவே உள்ளது நண்பா!")
                    conn.close()
                else:
                    # ரசீதைச் சேமித்தல்
                    file_path = os.path.join(UPLOAD_DIR, f"{r_name.strip()}_{uploaded_file.name}")
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    p_id = "PEND" + str(uuid.uuid4().int)[:4]
                    cursor.execute("INSERT INTO pending_users VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')",
                                   (p_id, r_name.strip(), r_email.strip(), r_phone.strip(), r_pass.strip(), r_sponsor, selected_pkg, file_path))
                    conn.commit()
                    conn.close()
                    st.success("🎉 உங்கள் பதிவு அட்மினுக்கு அனுப்பப்பட்டுள்ளது! ரசீதைச் சரிபார்த்த பின்பு கணக்கு துவங்கப்படும் நண்பா.")
            else:
                st.warning("⚠️ தயவுசெய்து ரசீது உட்பட அனைத்து விபரங்களையும் பூர்த்தி செய்யவும் நண்பா!")

# 👑 அட்மின் திரை
elif st.session_state.is_admin_logged:
    st.title("👑 GAK Admin Command Center")
    if st.sidebar.button("🚪 அட்மின் லாக்-அவுட்", type="primary"):
        st.session_state.is_admin_logged = False; st.rerun()
        
    st.write("---")
    adm_tab1, adm_tab2 = st.tabs(["📥 Pending Approvals (புதிய ரசீதுகள்)", "👥 Full Network & Ranks"])
    
    with adm_tab1:
        st.subheader("மெம்பர்களின் புதிய பதிவு மற்றும் ரசீது சரிபார்ப்பு")
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        df_pending = pd.read_sql_query("SELECT * FROM pending_users WHERE Status = 'Pending'", conn)
        conn.close()
        
        if df_pending.empty:
            st.info("தற்போது சரிபார்ப்பிற்கு எந்தவொரு புதிய விண்ணப்பமும் நிலுவையில் இல்லை நண்பா!")
        else:
            for _, p_row in df_pending.iterrows():
                with st.container(border=True):
                    st.subheader(f"👤 பயனர்: {p_row['Name']}")
                    st.write(f"📧 **Email:** {p_row['Email']} | 📞 **Phone:** {p_row['Phone']}")
                    st.write(f"📦 **தேர்ந்தெடுத்த பிசினஸ்:** ${p_row['Package']} | 🔗 **Sponsor:** {p_row['Sponsor']}")
                    
                    # ரசீதுப் படம் காட்டுதல்
                    if os.path.exists(p_row['Receipt_Path']):
                        st.image(p_row['Receipt_Path'], caption="உறுப்பினர் அப்லோட் செய்த ரசீது", width=300)
                    
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"✅ Approve & Pay Commission ({p_row['ID']})", key=f"app_{p_row['ID']}", use_container_width=True):
                            success, msg = approve_user_and_pay_commission(p_row['ID'])
                            if success: st.success(msg); st.rerun()
                            else: st.error(msg)
                    with btn_col2:
                        if st.button(f"❌ Reject ({p_row['ID']})", key=f"rej_{p_row['ID']}", type="danger", use_container_width=True):
                            conn = sqlite3.connect(DB_NAME, check_same_thread=False)
                            cursor = conn.cursor()
                            cursor.execute("UPDATE pending_users SET Status = 'Rejected' WHERE ID = ?", (p_row['ID'],))
                            conn.commit()
                            conn.close()
                            st.error("விண்ணப்பம் நிராகரிக்கப்பட்டது!")
                            st.rerun()

    with adm_tab2:
        st.subheader("மாஸ்டர் நெட்வொர்க் டேட்டாபேஸ்")
        st.dataframe(df_net, use_container_width=True)

# 👤 சாதாரண மெம்பர் திரை
else:
    df_net = get_network_df()
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    st.title(f"👋 {L['welcome']}{current_user}!")
    st.caption("G A K Smart Marketing Private Limited")
    
    if st.sidebar.button(L["logout"], type="secondary"):
        st.session_state.logged_in_user = None; st.rerun()
        
    st.write("---")
    
    # ரெஃபரல் லிங்க் உருவாக்கம் (அவரவர் கணக்கில் லிங்க் காட்டும்)
    # நீங்கள் லைவ் செய்யும்போது இந்த 'localhost:8501' என்ற இடத்தை உங்கள் வெப்சைட் லிங்காக மாற்றிக்கொள்ளலாம் நண்பா
    shareable_ref_link = f"http://localhost:8501/?ref={current_user}"
    st.info(f"{L['ref_link_lbl']} `{shareable_ref_link}`")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(L["ref_id"], str(user_info['Unique_ID']))
    with col2: st.metric(L["my_sales"], f"${user_info['Sales']:,.1f}")
    with col3: st.metric(L["my_earnings"], f"${user_info['Earnings']:,.1f}")
