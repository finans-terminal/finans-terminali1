import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans V4", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write("**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- GÜVENLİ VERİ ÇEKME FONKSİYONU ---
def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        # Hafta sonu boşluğunu aşmak için 7 günlük veri çekiyoruz
        df = ticker.history(period="7d")
        
        if not df.empty:
            # HATANIN ÇÖZÜMÜ BURASI: .iloc[-1] sonrasına .item() ekleyerek 
            # veriyi "Series" formatından "Saf Sayı" formatına çeviriyoruz.
            last_price = df['Close'].iloc[-1]
            return float(last_price) 
        return None
    except Exception as e:
        return None

# --- EKRAN DÜZENİ ---
c1, c2, c3 = st.columns(3)

# Semboller
assets = {
    "Dolar / TL": "USDTRY=X",
    "Ons Altın": "GC=F",
    "BIST 100": "XU100.IS"
}

cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    price = get_price(sym)
    if price is not None:
        # Burada artık hata almayacaksın çünkü 'price' kesinlikle bir sayı (float)
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} verisi alınamadı.")

st.divider()

# --- GRAFİK BÖLÜMÜ ---
st.subheader("📊 Hisse Senedi Analizi")
hisse = st.selectbox("Bir hisse seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS"])

try:
    data = yf.download(hisse, period="1mo", interval="1d", progress=False)
    if not data.empty:
        # Grafikte hata çıkmaması için Close sütununu açıkça belirtiyoruz
        st.line_chart(data['Close'])
        st.caption(f"{hisse} - Son 30 Günlük Kapanış Seyri")
    else:
        st.warning("Grafik verisi şu an çekilemiyor.")
except Exception as e:
    st.error(f"Grafik Hatası: {e}")

st.sidebar.success("Sistem: Aktif")
st.sidebar.info("Veriler Yahoo Finance üzerinden anlık çekilir.")
