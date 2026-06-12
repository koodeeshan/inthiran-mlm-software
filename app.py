import streamlit as st
import pandas as pd

# CSS - Manage App பொத்தானை மறைக்க
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("💰 G A K Smart Marketing System")

# தரவுத்தளம் (எளிமையான முறையில்)
if 'members' not in st.session_state:
    st.session_state.members = pd.DataFrame(columns=["ID", "Name", "Referrer", "Level"])

# மெனு தேர்வு
menu = st.sidebar.radio("Navigation", ["Dashboard", "Register New Member", "Network Tree"])

if menu == "Dashboard":
    st.subheader("📊 Business Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Members", len(st.session_state.members))
    col2.metric("Total Payout", f"${len(st.session_state.members) * 10}")
    st.write("வணிக முன்னேற்ற அறிக்கை...")

elif menu == "Register New Member":
    st.subheader("📝 New Member Registration")
    with st.form("register"):
        name = st.text_input("Member Name")
        referrer = st.text_input("Referrer ID")
        if st.form_submit_button("Register"):
            new_data = {"ID": len(st.session_state.members)+1, "Name": name, "Referrer": referrer, "Level": 1}
            st.session_state.members = pd.concat([st.session_state.members, pd.DataFrame([new_data])], ignore_index=True)
            st.success(f"{name} வெற்றிகரமாக சேர்க்கப்பட்டார்!")

elif menu == "Network Tree":
    st.subheader("🌳 Organization Network")
    if not st.session_state.members.empty:
        st.table(st.session_state.members)
    else:
        st.info("உறுப்பினர்கள் யாரும் இல்லை.")
