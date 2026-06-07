import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="A K G Smart Commission Marketing Pvt Ltd", page_icon="💰", layout="centered")

# 2. கூகுள் சீட் இணைப்பு முகவரி
SHEET_URL = "Https://docs.google.com/spreadsheets/d/1uu7CfjOA4ISDSQKxPVQCLDZufJummYbkMsFnjwWvvWc/edit?usp=drivesdk"

# 3. கூகுள் சீட்டுடன் கனெக்ட் செய்யும் ஃபங்க்ஷன்
@st.cache_resource
def get_google_sheet(url):
    # பொது பொது அணுகல் (Anyone with link as Editor) என்பதால் பொதுவான முறையில் இணைக்கிறோம்
    gc = gspread.public_api()
    sh = gc.open_by_url(url)
    return sh.get_worksheet(0)

try:
    sheet = get_google_sheet(SHEET_URL)
except Exception as e:
    st.error("கூகுள் சீட்டுடன் இணைப்பதில் சிக்கல் உள்ளது நண்பா. பர்மிஷனை 'Editor' என்று மாற்றியுள்ளீர்களா எனச் சரிபார்க்கவும்.")
    st.stop()

# 4. கூகுள் சீட்டில் இருந்து தரவுகளைப் படித்தல்
def load_data():
    records = sheet.get_all_records()
    # தரவுகள் காலியாக இருந்தால் ஆரம்ப விபரங்களை உருவாக்குதல்
    if not records:
        initial_data = [
            {"Name": "Inthiran", "Sponsor": "None", "Sales": 0, "Earnings": 0},
            {"Name": "Anand", "Sponsor": "Inthiran", "Sales": 0, "Earnings": 0},
            {"Name": "Bala", "Sponsor": "Anand", "Sales": 0, "Earnings": 0}
        ]
        for row in initial_data:
            sheet.append_row(list(row.values()))
        records = initial_data
    return pd.DataFrame(records)

df_data = load_data()

# Streamlit-இன் தற்காலிக நினைவகத்தில் டேட்டாஃபிரேமை ஏற்றுதல்
if 'network' not in st.session_state:
    st.session_state.network = df_data

# 5. கமிஷன் மற்றும் வருமானத்தை அப்டேட் செய்யும் ஃபங்க்ஷன்
def update_sheet_from_dataframe(df):
    # கூகுள் சீட்டை முழுமையாகத் துடைத்துவிட்டு புதிய டேட்டாவை எழுதுதல்
    sheet.clear()
    sheet.append_row(list(df.columns)) # தலைப்புகள்
    for index, row in df.iterrows():
        sheet.append_row(list(row))

def add_sale_and_distribute(sales_person, amount):
    df = st.session_state.network.copy()
    
    # 1. நேரடி விற்பனை செய்தவருக்கு விற்பனைத் தொகையைக் கூட்டுதல்
    df.loc[df['Name'] == sales_person, 'Sales'] += amount
    
    # 2. லெவல் கமிஷன் விதிகள்
    # நேரடி விற்பனையாளர்: 100%
    df.loc[df['Name'] == sales_person, 'Earnings'] += amount
    
    # ஸ்பான்சர்களைக் கண்டுபிடித்து கமிஷன் வழங்குதல்
    current_person = sales_person
    level = 1
    
    # கமிஷன் விகிதங்கள்: லெவல் 1 = 50%, லெவல் 2 = 30%, முதன்மை பாஸ் (Inthiran) = மீதி அனைத்தும்
    commission_rates = {1: 0.50, 2: 0.30}
    
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
            # லெவல் 2-க்கு மேல் போனால் அல்லது பிரதான பாஸ் 'Inthiran'-க்கு மீதி 20% கமிஷன்
            if sponsor_name == "Inthiran":
                df.loc[df['Name'] == sponsor_name, 'Earnings'] += (amount * 0.20)
                
        current_person = sponsor_name
        level += 1
        
    # மாற்றங்களை கூகுள் சீட்டிலும் தற்காலிக நினைவகத்திலும் சேமித்தல்
    update_sheet_from_dataframe(df)
    st.session_state.network = df

# 6. புதிய நபரை நெட்வொர்க்கில் சேர்க்கும் ஃபங்க்ஷன்
def add_new_member(name, sponsor):
    df = st.session_state.network.copy()
    if name in df['Name'].values:
        st.error(f"⚠️ '{name}' என்ற பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!")
        return False
        
    new_row = {"Name": name, "Sponsor": sponsor, "Sales": 0, "Earnings": 0}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # கூகுள் சீட்டில் சேர்த்தல்
    update_sheet_from_dataframe(df)
    st.session_state.network = df
    return True

# --- இணையதள வடிவமைப்பு (UI Design) ---

st.title("💰 A K G Smart Commission Marketing Pvt Ltd")
st.write("---")

# பக்கவாட்டு மெனு (Sidebar) - நிர்வாகப் பகுதிகள்
st.sidebar.header("🛠️ நிர்வாகக் கட்டுப்பாடுகள்")

# 1. புதிய நபரைச் சேர்த்தல்
st.sidebar.subheader("👤 புதிய உறுப்பினரைச் சேர்")
new_name = st.sidebar.text_input("உறுப்பினர் பெயர்:")
sponsor_list = st.session_state.network['Name'].tolist()
selected_sponsor = st.sidebar.selectbox("ஸ்பான்சர் (அறிமுகப்படுத்துபவர்):", sponsor_list)

if st.sidebar.button("உறுப்பினரை இணைக்கவும்"):
    if new_name.strip() != "":
        if add_new_member(new_name.strip(), selected_sponsor):
            st.sidebar.success(f"🎉 {new_name} வெற்றிகரமாகச் சேர்க்கப்பட்டார்!")
            st.rerun()
    else:
        st.sidebar.warning("தயவுசெய்து பெயரை டைப் செய்யவும் நண்பா!")

st.sidebar.write("---")

# 2. புதிய விற்பனையைப் பதிவு செய்தல்
st.sidebar.subheader("📈 புதிய விற்பனைப் பதிவு")
active_members = st.session_state.network['Name'].tolist()
selected_seller = st.sidebar.selectbox("விற்பனை செய்தவர்:", active_members)
sale_amount = st.sidebar.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)

if st.sidebar.button("விற்பனையைச் சேர் (கமிஷன் பிரி)"):
    add_sale_and_distribute(selected_seller, sale_amount)
    st.sidebar.success(f"🔥 Rs.{sale_amount} கமிஷன் பிரித்தளிக்கப்பட்டது!")
    st.rerun()

# பிரதானப் பக்கம் - தற்போதைய வருமான நிலை விபரங்கள்
st.header("👥 நபர்களின் தற்போதைய வருமானம்")

for index, row in st.session_state.network.iterrows():
    name = row['Name']
    sponsor = row['Sponsor']
    sales = row['Sales']
    earnings = row['Earnings']
    
    # லேபிள்கள் வடிவமைப்பு
    if sponsor == "None":
        identity = f"**{name}** (Main Boss)"
    else:
        identity = f"**{name}** (Sponsor: {sponsor})"
        
    # அழகான கார்டுகள் வடிவமைப்பு
    st.info(f"👤 {identity} | **மொத்த விற்பனை:** Rs.{sales:,.1f} | 💰 **மொத்த வருமானம்:** Rs.{earnings:,.1f}")
    
