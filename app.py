import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Doğuş Can Finans", layout="wide")

st.title("📈 Profesyonel Finans Terminali")

# --- VERİ ÇEKME FONKSİYONU ---
def get_price(symbol):
    try:
        # download metodu genellikle history'den daha stabildir
        df = yf.download(symbol, period="5d", interval="1d", progress=False)
        if not df.empty:
            # En son kapanış fiyatını alıyoruz
            price = df['Close'].iloc[-1]
            # Eğer hala bir liste/seri olarak geliyorsa ilk elemanı zorla alıyoruz
            if isinstance(price, (pd.Series, pd.DataFrame)):
                price = price.iloc[0]
            return float(price)
        return None
    except:
        return None

# --- EKRAN TASARIMI ---
c1, c2, c3 = st.columns(3)

# Semboller
assets = {
    "Dolar / TL": "USDTRY=X",
    "Ons Altın": "GC=F",
    "BIST 100": "^XU100" # Bazı sistemlerde XU100.IS yerine ^XU100 daha iyi çalışır
}

cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    price = get_price(sym)
    if price:
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} çekilemedi.")

st.divider()

# --- BASİT GRAFİK ---
st.subheader("📊 Hisse Grafiği")
hisse = st.text_input("Hisse Kodu Girin (Örn: THYAO.IS):", "THYAO.IS")

if st.button("Grafiği Göster"):
    data = yf.download(hisse, period="1mo", interval="1d")
    if not data.empty:
        st.line_chart(data['Close'])
    else:
        st.warning("Veri bulunamadı. Lütfen sembolü (Örn: SASA.IS) kontrol edin.")

st.sidebar.info("Hafta sonu verileri Cuma kapanışını gösterir.")
