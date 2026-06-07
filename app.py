import streamlit as st
import pandas as pd
import uuid
import sqlite3

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="G A K Smart Marketing Private Limited", page_icon="💰", layout="centered")

DB_NAME = 'gak_marketing_v4.db'

# --- பன்மொழி அகராதி (Multi-Language Dictionary) ---
LANG_DICT = {
    "தமிழ்": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | MLM பிசினஸ் போர்ட்டல்",
        "tab_login": "🔐 லாகின் (Login)",
        "tab_signup": "📝 புதிய பதிவு (Sign Up)",
        "login_title": "👋 நல்வரவு! உங்கள் கணக்கில் நுழையவும்",
        "username": "பயனர் பெயர் (Username):",
        "password": "கடவுச்சொல் (Password):",
        "btn_login": "🚀 உள்நுழைக (Login)",
        "login_err": "❌ தவறான பயனர் பெயர் அல்லது கடவுச்சொல்!",
        "login_success": "🎉 வெற்றிகரமாக உள்நுழைந்துவிட்டீர்கள்!",
        "signup_title": "🤝 புதிய உறுப்பினரை இணைக்கவும்",
        "reg_user_lbl": "புதிய நபர் பெயர் (Space இல்லாமல்):",
        "reg_pass_lbl": "புதிய கடவுச்சொல் உருவாக்குங்கள்:",
        "sponsor_lbl": "அறிமுகப்படுத்துபவர் (Sponsor Name):",
        "btn_register": "✅ பதிவு செய்க (Register)",
        "reg_dup_err": "⚠️ இந்த பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!",
        "reg_success": "🎉 பதிவு வெற்றி! உங்கள் ரெஃபரல் ஐடி: ",
        "reg_fill_warn": "தயவுசெய்து அனைத்து விபரங்களையும் நிரப்பவும் நண்பா!",
        "logout": "🚪 லாக்-அவுட்",
        "welcome": "👋 வணக்கம், ",
        "menu_dash": "📊 டேஷாபோர்டு",
        "menu_with": "💰 பணம் வித்ரா",
        "menu_tree": "🌲 பைனரி நெ트வொர்க்",
        "menu_search": "🔍 டவுன்லைன் தேடல்",
        "ref_id": "🆔 உங்கள் ரெஃபரல் ஐடி",
        "my_sales": "📈 உங்கள் சொந்த விற்பனை",
        "my_earnings": "💰 மொத்த வருமானம் (Earnings)",
        "new_sale_title": "🛒 புதிய விற்பனைப் பதிவு",
        "sale_amt_lbl": "விற்பனைத் தொகை (Rs.):",
        "btn_sale_confirm": "🔥 விற்பனையை உறுதிசெய் (கமிஷன் பிரி)",
        "sale_success": "🎉 விற்பனைப் பதிவு செய்யப்பட்டது! கமிஷன் வெற்றிகரமாகப் பிரித்தளிக்கப்பட்டது.",
        "with_title": "💰 கமிஷன் வித்ரா கோரிக்கை",
        "curr_bal": "💵 உங்கள் தற்போதைய மொத்த வருமானம்: ",
        "with_amt_lbl": "வித்ரா செய்ய வேண்டிய தொகை (Rs.):",
        "with_method_lbl": "பணம் பெற விரும்பும் வழி (Payment Method):",
        "btn_with_submit": "🚀 வித்ரா கோரிக்கை அனுப்பு",
        "with_success": "🎉 வித்ரா கோரிக்கை அட்மினுக்கு வெற்றிகரமாக அனுப்பப்பட்டது!",
        "with_bal_err": "❌ உங்களிடம் போதிய வருமானம் இல்லை நண்பா!",
        "with_history": "📜 உங்கள் முந்தைய வித்ரா விபரங்கள்:",
        "with_no_history": "நீங்கள் இதுவரை பணம் வித்ரா கோரிக்கை எதுவும் செய்யவில்லை.",
        "tree_title": "🌲 உங்கள் பைனரி நெட்வொர்க் கட்டமைப்பு",
        "tree_desc": "உங்களுக்குக் கீழே உள்ள நேரடி மற்றும் இரண்டாம் நிலை டீம் அமைப்பை கீழே காணலாம்:",
        "tree_you": "👑 நீங்கள்: ",
        "tree_no_team": "உங்களுக்குக் கீழே இன்னும் டீம் அமையவில்லை நண்பா.",
        "tree_l1": "⬇️ லெவல் 1 (நேரடி டவுன்லைன்ஸ்):",
        "tree_empty": "     └ 👤 [யாரும் இல்லை]",
        "search_title": "🔍 டவுன்லைன் மெம்பர் தேடல்",
        "search_lbl": "தேட வேண்டிய மெம்பர் பெயர் (Username):",
        "search_no_user": "❌ இந்த பெயரில் உங்கள் நெட்வொர்க்கில் எந்த உறுப்பினரும் இல்லை நண்பா!",
        "search_details": "👤 பயனர் விபரம்: ",
        "lang_lbl": "🌐 மொழியைத் தேர்ந்தெடுக்கவும் / Select Language / භාෂාව තෝරන්න"
    },
    "English": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | MLM Business Portal",
        "tab_login": "🔐 Login",
        "tab_signup": "📝 Sign Up",
        "login_title": "👋 Welcome Back! Login to your account",
        "username": "Username:",
        "password": "Password:",
        "btn_login": "🚀 Login",
        "login_err": "❌ Invalid username or password!",
        "login_success": "🎉 Successfully logged in!",
        "signup_title": "🤝 Register New Member",
        "reg_user_lbl": "New Username (without spaces):",
        "reg_pass_lbl": "Create Password:",
        "sponsor_lbl": "Sponsor Name:",
        "btn_register": "✅ Register Member",
        "reg_dup_err": "⚠️ This username already exists in the network!",
        "reg_success": "🎉 Registration Success! Your Referral ID: ",
        "reg_fill_warn": "Please fill in all the details!",
        "logout": "🚪 Logout",
        "welcome": "👋 Welcome, ",
        "menu_dash": "📊 Dashboard",
        "menu_with": "💰 Withdrawal",
        "menu_tree": "🌲 Binary Network",
        "menu_search": "🔍 Downline Search",
        "ref_id": "🆔 Your Referral ID",
        "my_sales": "📈 Personal Sales",
        "my_earnings": "💰 Total Earnings",
        "new_sale_title": "🛒 New Sales Entry",
        "sale_amt_lbl": "Sales Amount (Rs.):",
        "btn_sale_confirm": "🔥 Confirm Sale & Distribute Commission",
        "sale_success": "🎉 Sales entry successful! Commission has been distributed.",
        "with_title": "💰 Commission Withdrawal Request",
        "curr_bal": "💵 Your Current Balance: ",
        "with_amt_lbl": "Withdrawal Amount (Rs.):",
        "with_method_lbl": "Select Payment Method:",
        "btn_with_submit": "🚀 Send Withdrawal Request",
        "with_success": "🎉 Withdrawal request sent to Admin successfully!",
        "with_bal_err": "❌ Insufficient balance in your account!",
        "with_history": "📜 Your Withdrawal History:",
        "with_no_history": "You haven't made any withdrawal requests yet.",
        "tree_title": "🌲 Your Binary Network Structure",
        "tree_desc": "Check your direct and secondary downline team structure below:",
        "tree_you": "👑 You: ",
        "tree_no_team": "No downline team members yet.",
        "tree_l1": "⬇️ Level 1 (Direct Downlines):",
        "tree_empty": "     └ 👤 [Empty Slot]",
        "search_title": "🔍 Downline Member Search",
        "search_lbl": "Enter Member Username:",
        "search_no_user": "❌ No member found with this name in your network!",
        "search_details": "👤 Member Details: ",
        "lang_lbl": "🌐 Select Language / மொழியைத் தேர்ந்தெடுக்கவும் / භාෂාව තෝරන්න"
    },
    "සිංහල": {
        "title": "💰 G A K Smart Marketing",
        "caption": "Private Limited | MLM ව්‍යාපාරික ද්වාරය",
        "tab_login": "🔐 ඇතුල් වන්න (Login)",
        "tab_signup": "📝 ලියාපදිංචි වන්න (Sign Up)",
        "login_title": "👋 සාදරයෙන් පිළිගනිමු! ඔබගේ ගිණුමට ඇතුළු වන්න",
        "username": "පරිශීලක නාමය (Username):",
        "password": "මුරපදය (Password):",
        "btn_login": "🚀 ඇතුල් වන්න (Login)",
        "login_err": "❌ පරිශීලක නාමය හෝ මුරපදය වැරදියි!",
        "login_success": "🎉 සාර්ථකව ඇතුළු විය!",
        "signup_title": "🤝 නව සාමාජිකයෙකු ලියාපදිංචි කරන්න",
        "reg_user_lbl": "නව පරිශීලක නාමය (හිස්තැන් නොමැතිව):",
        "reg_pass_lbl": "නව මුරපදයක් සාදන්න:",
        "sponsor_lbl": "හඳුන්වා දෙන්නාගේ නම (Sponsor Name):",
        "btn_register": "✅ ලියාපදිංචි කරන්න (Register)",
        "reg_dup_err": "⚠️ මෙම නම දැනටමත් ජාලයේ පවතී!",
        "reg_success": "🎉 ලියාපදිංචිය සාර්ථකයි! ඔබගේ රෙෆරල් අංකය: ",
        "reg_fill_warn": "කරුණාකර සියලු විස්තර පුරවන්න!",
        "logout": "🚪 පිටවන්න (Logout)",
        "welcome": "👋 ආයුබෝවන්, ",
        "menu_dash": "📊 උපකරණ පුවරුව",
        "menu_with": "💰 මුදල් ලබාගැනීම",
        "menu_tree": "🌲 ජාල ව්‍යුහය",
        "menu_search": "🔍 සාමාජිකයින් සෙවීම",
        "ref_id": "🆔 ඔබගේ රෙෆරල් අංකය",
        "my_sales": "📈 පෞද්ගලික විකුණුම්",
        "my_earnings": "💰 මුළු ආදායම",
        "new_sale_title": "🛒 නව විකුණුම් ඇතුලත් කිරීම",
        "sale_amt_lbl": "විකුණුම් මුදල (Rs.):",
        "btn_sale_confirm": "🔥 විකුණුම් තහවුරු කරන්න",
        "sale_success": "🎉 විකුණුම් ඇතුලත් කිරීම සාර්ථකයි! කොමිස් මුදල් බෙදා හරින ලදී.",
        "with_title": "💰 කොමිස් මුදල් ලබාගැනීමේ ඉල්ලීම",
        "curr_bal": "💵 ඔබගේ වත්මන් මුළු ආදායම: ",
        "with_amt_lbl": "ලබාගත යුතු මුදල (Rs.):",
        "with_method_lbl": "මුදල් ලබාගන්නා ක්‍රමය (Payment Method):",
        "btn_with_submit": "🚀 ඉල්ලීම යොමු කරන්න",
        "with_success": "🎉 ඉල්ලීම සාර්ථකව පරිපාලක වෙත යවන ලදී!",
        "with_bal_err": "❌ ඔබගේ ගිණුමේ ප්‍රමාණවත් මුදල් නොමැත!",
        "with_history": "📜 පෙර ලබාගැනීම් විස්තර:",
        "with_no_history": "ඔබ තවමත් මුදල් ලබාගැනීමේ ඉල්ලීම් කර නොමැත.",
        "tree_title": "🌲 ඔබගේ ද්විමය ජාල ව්‍යුහය",
        "tree_desc": "ඔබට පහළින් සිටින සාමාජිකයින්ගේ ව්‍යුහය පහතින් බලන්න:",
        "tree_you": "👑 ඔබ: ",
        "tree_no_team": "ඔබට පහළින් තවමත් සාමාජිකයින් සම්බන්ධ වී නොමැත.",
        "tree_l1": "⬇️ මට්ටම 1 (සෘජු සාමාජිකයින්):",
        "tree_empty": "     └ 👤 [හිස්තැනක්]",
        "search_title": "🔍 සාමාජිකයින් සොයන්න",
        "search_lbl": "සාමාජිකයාගේ නම ඇතුලත් කරන්න:",
        "search_no_user": "❌ මෙම නමින් සාමාජිකයෙකු ජාලයේ නොමැත!",
        "search_details": "👤 සාමාජික විස්තර: ",
        "lang_lbl": "🌐 භාෂාව තෝරන්න / மொழியைத் தேர்ந்தெடுக்கவும் / Select Language"
    }
}

# --- நிரந்தர டேட்டாபேஸ் சிஸ்டம் (Language Column Added) ---
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    # நெட்வொர்க் அட்டவணை (Language உடன்)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS network (
            Name TEXT UNIQUE,
            Password TEXT,
            Sponsor TEXT,
            Sales REAL,
            Earnings REAL,
            Unique_ID TEXT,
            Language TEXT DEFAULT 'தமிழ்'
        )
    ''')
    
    # வித்ரா கோரிக்கை அட்டவணை
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            ID TEXT PRIMARY KEY,
            Name TEXT,
            Amount REAL,
            Method TEXT,
            Status TEXT
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM network")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?, ?)", ('Inthiran', '123', 'None', 0.0, 0.0, 'GAK001', 'தமிழ்'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?, ?)", ('Anand', '123', 'Inthiran', 0.0, 0.0, 'GAK002', 'English'))
        cursor.execute("INSERT INTO network VALUES (?, ?, ?, ?, ?, ?, ?)", ('Bala', '123', 'Anand', 0.0, 0.0, 'GAK003', 'සිංහල'))
        conn.commit()
    conn.close()

init_db()

def get_network_df():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM network", conn)
    conn.close()
    return df

def update_user_language(username, lang):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE network SET Language = ? WHERE Name = ?", (lang, username))
    conn.commit()
    conn.close()

def get_withdrawals_df(username):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    df = pd.read_sql_query("SELECT Amount, Method, Status FROM withdrawals WHERE Name = ?", conn, params=(username,))
    conn.close()
    return df

if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'current_lang' not in st.session_state:
    st.session_state.current_lang = "தமிழ்"

df_net = get_network_df()
L = LANG_DICT[st.session_state.current_lang]

# கமிஷன் விநியோக முறை
def add_sale_and_distribute(sales_person, amount):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
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
def register_new_member(username, password, sponsor_name, default_lang):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM network WHERE Name = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, L["reg_dup_err"]
    
    short_id = "GAK" + str(uuid.uuid4().int)[:4]
    cursor.execute("INSERT INTO network VALUES (?, ?, ?, 0.0, 0.0, ?, ?)", (username, password, sponsor_name, short_id, default_lang))
    conn.commit()
    conn.close()
    return True, f"{L['reg_success']} {short_id}"

# புதிய வித்ரா கோரிக்கை சேர்த்தல்
def request_withdrawal(username, amount, method):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    req_id = str(uuid.uuid4().int)[:6]
    cursor.execute("INSERT INTO withdrawals VALUES (?, ?, ?, ?, ?)", (req_id, username, amount, method, 'Pending'))
    conn.commit()
    conn.close()

# --- இணையதள வடிவமைப்பு ---

# லாகின் செய்யாத பொது காட்டும் திரை
if st.session_state.logged_in_user is None:
    # லாகினுக்கு முன் பொதுவான மொழித் தேர்வு
    st.session_state.current_lang = st.selectbox(L["lang_lbl"], ["தமிழ்", "English", "සිංஹල"], index=["தமிழ்", "English", "සිංஹල"].index(st.session_state.current_lang))
    L = LANG_DICT[st.session_state.current_lang]
    
    st.title(L["title"])
    st.caption(L["caption"])
    st.write("---")
    
    tab1, tab2 = st.tabs([L["tab_login"], L["tab_signup"]])
    
    with tab1:
        st.subheader(L["login_title"])
        login_user = st.text_input(L["username"], key="l_user", placeholder="...")
        login_pass = st.text_input(L["password"], type="password", key="l_pass", placeholder="...")
        
        st.write("")
        if st.button(L["btn_login"], use_container_width=True):
            user_row = df_net[(df_net['Name'] == login_user) & (df_net['Password'].astype(str) == str(login_pass))]
            if not user_row.empty:
                st.session_state.logged_in_user = login_user
                # பயனரின் தனிப்பட்ட மொழித் தேர்வை டேட்டாபேஸிலிருந்து எடுக்கிறோம்
                st.session_state.current_lang = user_row.iloc[0]['Language']
                st.success(L["login_success"])
                st.rerun()
            else:
                st.error(L["login_err"])
                
    with tab2:
        st.subheader(L["signup_title"])
        reg_user = st.text_input(L["reg_user_lbl"], key="r_user", placeholder="Siva")
        reg_pass = st.text_input(L["reg_pass_lbl"], type="password", key="r_pass", placeholder="...")
        
        all_sponsors = df_net['Name'].tolist()
        selected_sponsor = st.selectbox(L["sponsor_lbl"], all_sponsors)
        
        st.write("")
        if st.button(L["btn_register"], use_container_width=True):
            if reg_user.strip() != "" and reg_pass.strip() != "":
                success, msg = register_new_member(reg_user.strip(), reg_pass.strip(), selected_sponsor, st.session_state.current_lang)
                if success:
                    st.success(msg)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning(L["reg_fill_warn"])

# லாகின் செய்த பின் காட்டும் மெம்பர் திரை
else:
    df_net = get_network_df()
    current_user = st.session_state.logged_in_user
    user_info = df_net[df_net['Name'] == current_user].iloc[0]
    
    # லாகின் செய்த பின், தற்போதைய மெம்பர் தனது மொழியை மாற்றினால் அது டேட்டாபேஸிலும் சேமிக்கப்படும்
    st.session_state.current_lang = user_info['Language']
    L = LANG_DICT[st.session_state.current_lang]
    
    # டாப் பார் மொழித் தேர்வு மாற்றி
    chosen_lang = st.sidebar.selectbox("🌐 Language / மொழி / භාෂාව", ["தமிழ்", "English", "සිංஹල"], index=["தமிழ்", "English", "සිංஹල"].index(st.session_state.current_lang))
    if chosen_lang != st.session_state.current_lang:
        update_user_language(current_user, chosen_lang)
        st.session_state.current_lang = chosen_lang
        st.rerun()

    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title(f"{L['welcome']}{current_user}!")
        st.caption("G A K Smart Marketing Private Limited")
    with col_logout:
        st.write("")
        if st.button(L["logout"], type="secondary"):
            st.session_state.logged_in_user = None
            st.rerun()
        
    st.write("---")
    
    # பன்மொழித் தாவல்கள் (Multi-Language Tabs)
    menu_tab1, menu_tab2, menu_tab3, menu_tab4 = st.tabs([
        L["menu_dash"], L["menu_with"], L["menu_tree"], L["menu_search"]
    ])
    
    # --- TAB 1: DASHBOARD ---
    with menu_tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label=L["ref_id"], value=str(user_info['Unique_ID']))
        with col2:
            st.metric(label=L["my_sales"], value=f"Rs.{user_info['Sales']:,.1f}")
        with col3:
            st.metric(label=L["my_earnings"], value=f"Rs.{user_info['Earnings']:,.1f}")
            
        st.write("---")
        
        st.header(L["new_sale_title"])
        sale_amount = st.number_input(L["sale_amt_lbl"], min_value=10.0, step=10.0, value=100.0, key="sale_val")
        
        if st.button(L["btn_sale_confirm"], use_container_width=True):
            add_sale_and_distribute(current_user, sale_amount)
            st.success(L["sale_success"])
            st.rerun()
            
    # --- TAB 2: WITHDRAWAL REQUEST ---
    with menu_tab2:
        st.header(L["with_title"])
        st.write(f"{L['curr_bal']} **Rs. {user_info['Earnings']:,.1f}**")
        
        with st.form("withdraw_form"):
            w_amount = st.number_input(L["with_amt_lbl"], min_value=100.0, value=500.0, step=100.0)
            w_method = st.selectbox(L["with_method_lbl"], [
                "Bank of Ceylon (BOC)", "Dialog eZ Cash", "Mobitel mCash", "USDT (Crypto)"
            ])
            submit_w = st.form_submit_button(L["btn_with_submit"], use_container_width=True)
            
            if submit_w:
                if w_amount <= user_info['Earnings']:
                    request_withdrawal(current_user, w_amount, w_method)
                    st.success(L["with_success"])
                else:
                    st.error(L["with_bal_err"])
                    
        st.write("---")
        st.subheader(L["with_history"])
        df_w = get_withdrawals_df(current_user)
        if df_w.empty:
            st.info(L["with_no_history"])
        else:
            st.dataframe(df_w, use_container_width=True)

    # --- TAB 3: BINARY / DOWNLINE TREE ---
    with menu_tab3:
        st.header(L["tree_title"])
        st.write(L["tree_desc"])
        
        l1_members = df_net[df_net['Sponsor'] == current_user]
        
        with st.container(border=True):
            st.markdown(f"{L['tree_you']} **{current_user}** ({user_info['Unique_ID']})")
            
            if l1_members.empty:
                st.info(L["tree_no_team"])
            else:
                st.write(L["tree_l1"])
                for _, l1_row in l1_members.iterrows():
                    col_l1, col_l2 = st.columns([1, 1])
                    with col_l1:
                        st.success(f"👤 {l1_row['Name']} ({l1_row['Unique_ID']})")
                    
                    with col_l2:
                        l2_members = df_net[df_net['Sponsor'] == l1_row['Name']]
                        if l2_members.empty:
                            st.caption(L["tree_empty"])
                        else:
                            for _, l2_row in l2_members.iterrows
