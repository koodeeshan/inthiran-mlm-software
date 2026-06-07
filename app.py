import streamlit as st

# பக்கத்தின் தலைப்பு மற்றும் வடிவமைப்பு
st.set_page_config(page_title="MLM Commission Calculator", page_icon="💰", layout="centered")
st.title("💰 MLM Commission Calculator")
st.subheader("முழுமையான எம்.எல்.எம் கமிஷன் மேலாண்மை")
st.write("---")

# செஷன் ஸ்டேட் (Session State) மூலம் மெம்பர்களின் விபரங்களைச் சேமித்தல்
if "network" not in st.session_state:
    # ஆரம்பக்கட்ட நெட்வொர்க் அமைப்பு
    st.session_state.network = {
        "Inthiran": {"sponsor": None, "sales": 0, "earnings": 0},
        "Anand": {"sponsor": "Inthiran", "sales": 0, "earnings": 0},
        "Bala": {"sponsor": "Anand", "sales": 0, "earnings": 0}
    }

def add_new_member(name, sponsor_name):
    """புதிய நபரை நெட்வொர்க்கில் இணைத்தல்"""
    if name and name not in st.session_state.network:
        st.session_state.network[name] = {"sponsor": sponsor_name, "sales": 0, "earnings": 0}
        return True
    return False

def process_sale(salesperson, amount):
    """விற்பனைத் தொகையைப் பகிர்ந்து கமிஷன் கணக்கிடுதல்"""
    # சொந்த விற்பனையைச் சேர்த்தல்
    st.session_state.network[salesperson]["sales"] += amount
    
    # 1. சொந்த விற்பனைக்கு 10% கமிஷன்
    own_comm = amount * 0.10
    st.session_state.network[salesperson]["earnings"] += own_comm
    st.info(f"🔹 **{salesperson}** செய்த விற்பனைத் தொகை: **Rs.{amount:,}**")
    st.write(f"👉 **{salesperson}** பெற்ற நேரடி கமிஷன் (10%): `Rs.{own_comm:,}`")
    
    # 2. மேல் மட்ட ஸ்பான்சர்களுக்கு கமிஷன் பிரித்தல்
    current_sponsor = st.session_state.network[salesperson]["sponsor"]
    level = 1
    commission_rates = {1: 0.05, 2: 0.03} # லெவல் 1 = 5%, லெவல் 2 = 3%
    
    while current_sponsor and level in commission_rates:
        rate = commission_rates[level]
        indirect_comm = amount * rate
        st.session_state.network[current_sponsor]["earnings"] += indirect_comm
        st.write(f"➡️ லெவல் {level} ஸ்பான்சர் **{current_sponsor}** பெற்ற கமிஷன் ({int(rate*100)}%): `Rs.{indirect_comm:,}`")
        
        # அடுத்த மேல் மட்டத்திற்குச் செல்லுதல்
        current_sponsor = st.session_state.network[current_sponsor]["sponsor"]
        level += 1

# --- பக்கவாட்டுப் பகுதி (Sidebar) - புதிய நபரைச் சேர்த்தல் ---
st.sidebar.header("➕ புதிய நபரைச் சேர்க்கவும்")
new_name = st.sidebar.text_input("புதிய நபர் பெயர் (ஆங்கிலத்தில்):")
sponsor_select = st.sidebar.selectbox("அவரைச் சேர்த்த ஸ்பான்சர் யார்?", list(st.session_state.network.keys()))

if st.sidebar.button("Add to Network (இணைக்கவும்)"):
    if new_name:
        if add_new_member(new_name, sponsor_select):
            st.sidebar.success(f"🎉 {new_name} வெற்றிகரமாக இணைக்கப்பட்டார்!")
            st.rerun()
        else:
            st.sidebar.error("இந்தப் பெயர் ஏற்கனவே நெட்வொர்க்கில் உள்ளது!")
    else:
        st.sidebar.warning("தயவுசெய்து பெயரை டைப் செய்யவும்!")

# --- பிரதான பகுதி (Main Page) - கமிஷன் கணக்கீடு ---
st.subheader("📊 புதிய விற்பனை விபரங்களை உள்ளிடவும்")

# நெட்வொர்க்கில் உள்ளவர்களில் யார் விற்றார்கள் என்பதைத் தேர்ந்தெடுக்கும் வசதி
seller = st.selectbox("விற்பனை செய்த நபரைக் தேர்வு செய்யவும்:", list(st.session_state.network.keys()))
sale_amount = st.number_input("விற்பனைத் தொகை (Rs):", min_value=0, value=10000, step=500)

if st.button("Calculate Commission (கணக்கிடு)"):
    st.write("---")
    process_sale(seller, sale_amount)
    st.write("---")

# --- தற்போதைய வருமான நிலை (Live Dashboard) ---
st.subheader("🏆 நெட்வொர்க் நபர்களின் தற்போதைய வருமானம்")

# டேபிளாகக் காண்பித்தல்
for member, details in st.session_state.network.items():
    sponsor_text = f" (Sponsor: {details['sponsor']})" if details['sponsor'] else " (Main Boss)"
    st.success(f"👤 **{member}** {sponsor_text} | மொத்த வருமானம்: **Rs.{details['earnings']:,}**")
