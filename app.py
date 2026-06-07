import streamlit as st

# பக்கத்தின் தலைப்பு மற்றும் வடிவமைப்பு
st.set_page_config(page_title="MLM Commission Calculator", page_icon="💰", layout="centered")
st.title("💰 எளிய எம்.எல்.எம் (MLM) கமிஷன் கணக்கீடு")
st.write("---")

class Member:
    def __init__(self, name, sponsor=None):
        self.name = name
        self.sponsor = sponsor  # இவருக்கு மேல் இருக்கும் நபர்
        self.sales = 0          # இவருடைய சொந்த விற்பனை
        self.earnings = 0       # இவருடைய மொத்த வருமானம் / கமிஷன்

    def add_sale(self, amount):
        """விற்பனைத் தொகையைச் சேர்த்து, மேல் நிலைகளில் உள்ளவர்களுக்கு கமிஷன் பிரித்தல்"""
        self.sales += amount
        st.info(f"🔹 **{self.name}** செய்த விற்பனைத் தொகை: **Rs.{amount:,}**")
        
        # 1. சொந்த விற்பனைக்கு 10% கமிஷன்
        own_commission = amount * 0.10
        self.earnings += own_commission
        st.write(f"👉 **{self.name}** பெற்ற நேரடி கமிஷன் (10%): `Rs.{own_commission:,}`")

        # 2. மேல் மட்டத்தில் உள்ள ஸ்பான்சர்களுக்கு கமிஷன் பிரித்தல் (Up-lines)
        current_sponsor = self.sponsor
        level = 1
        
        # மேல் மட்ட கமிஷன் விகிதங்கள்: லெவல் 1 = 5%, லெவல் 2 = 3%
        commission_rates = {1: 0.05, 2: 0.03}

        while current_sponsor and level in commission_rates:
            rate = commission_rates[level]
            indirect_commission = amount * rate
            current_sponsor.earnings += indirect_commission
            st.write(f"➡️ லெவல் {level} ஸ்பான்சர் **{current_sponsor.name}** பெற்ற கமிஷன் ({int(rate*100)}%): `Rs.{indirect_commission:,}`")
            
            # அடுத்த மேல் மட்டத்திற்குச் செல்லுதல்
            current_sponsor = current_sponsor.sponsor
            level += 1

# --- எம்.எல்.எம் நெட்வொர்க் உருவாக்கம் ---

# லெவல் 0: நிறுவனத்தின் முதன்மை நபர்
boss = Member("Inthiran")

# லெவல் 1: இந்திரன் சேர்த்த நபர் (ஆனந்த்)
member_a = Member("Anand", sponsor=boss)

# லெவல் 2: ஆனந்த் சேர்த்த நபர் (பாலா)
member_b = Member("Bala", sponsor=member_a)


# --- விற்பனை மற்றும் கமிஷன் இயக்கம் ---
st.subheader("📊 நடப்பு விற்பனை விபரங்கள்")
# பாலா Rs.10,000 மதிப்புள்ள பொருளை விற்கிறார்
member_b.add_sale(10000)


# --- இறுதி வருமான நிலை ---
st.write("")
st.write("---")
st.subheader("🏆 ஒவ்வொருவரின் இறுதி வருமானம்")

# அழகான பச்சை நிறப் பெட்டிகளில் அவுட்புட்டைக் காண்பித்தல்
st.success(f"👤 **{boss.name}** இன் மொத்த வருமானம்: **Rs.{boss.earnings:,}**")
st.success(f"👤 **{member_a.name}** இன் மொத்த வருமானம்: **Rs.{member_a.earnings:,}**")
st.success(f"👤 **{member_b.name}** இன் மொத்த வருமானம்: **Rs.{member_b.earnings:,}**")
        
