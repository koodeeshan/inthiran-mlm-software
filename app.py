import streamlit as st
import pandas as pd

# 1. பக்கத்தின் தலைப்பு மற்றும் லேஅவுட் அமைத்தல்
st.set_page_config(page_title="A K G Smart Commission Marketing Pvt Ltd", page_icon="💰", layout="centered")

# 2. கூகுள் சீட்டை CSV வடிவில் நேரடியாகப் படிக்கும் எளிய முகவரி
# (இதன் மூலம் பர்மிஷன் சிக்கல்கள் முற்றிலும் தவிர்க்கப்படும்)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1uu7CfjOA4ISDSQKxPVQCLDZufJummYbkMsFnjwWvvWc/export?format=csv"

# 3. தரவுகளைப் படிக்கும் ஃபங்க்ஷன்
def load_data():
    try:
        # கூகுள் சீட்டை ஆன்லைனில் இருந்து நேரடியாகப் படிக்கிறது
        df = pd.read_csv(SHEET_CSV_URL)
        # தூண்கள் (Columns) சரியாக இருப்பதை உறுதி செய்தல்
        required_cols = ['Name', 'Sponsor', 'Sales', 'Earnings']
        if not all(col in df.columns for col in required_cols):
            raise Exception("Columns mismatch")
        return df
    except Exception as e:
        # ஆன்லைனில் படிக்க முடியாவிட்டால் காட்டப்படும் ஆரம்பக்கட்ட உள்ளூர் தரவு
        initial_data = [
            {"Name": "Inthiran", "Sponsor": "None", "Sales": 0, "Earnings": 0},
            {"Name": "Anand", "Sponsor": "Inthiran", "Sales": 0, "Earnings": 0},
            {"Name": "Bala", "Sponsor": "Anand", "Sales": 0, "Earnings": 0}
        ]
        return pd.DataFrame(initial_data)

# தரவை லோடு செய்தல்
if 'network' not in st.session_state:
    st.session_state.network = load_data()

# 4. புதிய விற்பனை மற்றும் கமிஷன் பிரிப்பு
def add_sale_and_distribute(sales_person, amount):
    df = st.session_state.network.copy()
    
    # நேரடி விற்பனையாளருக்கு கூட்டுதல்
    df.loc[df['Name'] == sales_person, 'Sales'] += amount
    df.loc[df['Name'] == sales_person, 'Earnings'] += amount
    
    current_person = sales_person
    level = 1
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
            if sponsor_name == "Inthiran":
                df.loc[df['Name'] == sponsor_name, 'Earnings'] += (amount * 0.20)
                
        current_person = sponsor_name
        level += 1
        
    st.session_state.network = df

# 5. புதிய நபரைச் சேர்த்தல்
def add_new_member(name, sponsor):
    df = st.session_state.network.copy()
    if name in df['Name'].values:
        st.error(f"⚠️ '{name}' என்ற பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது நண்பா!")
        return False
        
    new_row = {"Name": name, "Sponsor": sponsor, "Sales": 0, "Earnings": 0}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.network = df
    return True

# --- இணையதள வடிவமைப்பு (UI Design) ---
st.title("💰 A K G Smart Commission Marketing Pvt Ltd")
st.write("---")

st.sidebar.header("🛠️ நிர்வாகக் கட்டுப்பாடுகள்")

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

st.sidebar.subheader("📈 புதிய விற்பனைப் பதிவு")
active_members = st.session_state.network['Name'].tolist()
selected_seller = st.sidebar.selectbox("விற்பனை செய்தவர்:", active_members)
sale_amount = st.sidebar.number_input("விற்பனைத் தொகை (Rs.):", min_value=10.0, step=10.0, value=100.0)

if st.sidebar.button("விற்பனையைச் சேர் (கமிஷன் பிரி)"):
    add_sale_and_distribute(selected_seller, sale_amount)
    st.sidebar.success(f"🔥 Rs.{sale_amount} கமிஷன் பிரித்தளிக்கப்பட்டது!")
    st.rerun()

st.header("👥 நபர்களின் தற்போதைய வருமானம்")

for index, row in st.session_state.network.iterrows():
    name = row['Name']
    sponsor = row['Sponsor']
    sales = row['Sales']
    earnings = row['Earnings']
    
    if sponsor == "None":
        identity = f"**{name}** (Main Boss)"
    else:
        identity = f"**{name}** (Sponsor: {sponsor})"
        
    st.info(f"👤 {identity} | **மொத்த விற்பனை:** Rs.{sales:,.1f} | 💰 **மொத்த வருமானம்:** Rs.{earnings:,.1f}")
