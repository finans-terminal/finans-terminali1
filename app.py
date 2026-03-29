import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Doğuş Can Terminal V4", layout="wide")

st.title("📈 Finans Terminali - Canlı Takip")

# --- GELİŞMİŞ VERİ ÇEKME FONKSİYONU ---
def get_live_price(symbol):
    try:
        # 1. Adım: Veriyi 7 günlük geniş bir aralıkta çek (Hafta sonu boşluğunu aşmak için)
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="7d", interval="1d")
        
        if not df.empty:
            # 2. Adım: Son kapanış fiyatını al (Series hatasını önlemek için .values[0] kullanıyoruz)
            last_price = df['Close'].iloc[-1]
            return float(last_price)
        else:
            return None
    except Exception as e:
        # Hatayı terminalde değil, sessizce yönetiyoruz
        return None

# --- EKRAN TASARIMI ---
st.subheader("Piyasa Göstergeleri")
c1, c2, c3 = st.columns(3)

# Sembol Listesi
assets = {
    "Dolar / TL": "USDTRY=X",
    "Ons Altın": "GC=F",
    "BIST 100": "XU100.IS"
}

cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    price = get_live_price(sym)
    if price:
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.warning(f"{name} verisi alınamadı.")

st.divider()

# --- HİSSE GRAFİK BÖLÜMÜ ---
st.subheader("Hisse Senedi Analizi")
hisse = st.selectbox("Bir hisse seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS"])

try:
    # Grafik için download fonksiyonunu kullanıyoruz
    data = yf.download(hisse, period="1mo", interval="1d", progress=False)
    if not data.empty:
        # Veri setini sadeleştiriyoruz (Hata payını azaltmak için)
        chart_data = data['Close']
        st.line_chart(chart_data)
        st.caption(f"{hisse} - Son 30 Günlük Kapanış Seyri")
    else:
        st.error("Grafik verisi şu an çekilemiyor. (Yahoo Finance kaynaklı olabilir)")
except Exception as e:
    st.error(f"Grafik hatası: {e}")

st.sidebar.markdown("### 🟢 Sistem Aktif")
st.sidebar.info("Hafta sonu verileri son Cuma kapanışını baz alır.")
