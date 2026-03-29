import streamlit as st
import yfinance as yf
import pandas as pd

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Finans Terminali V3", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.markdown(f"**Hoş geldin Doğuş Can Şen** | Ekonomi & Finans Portföy Takibi")

# Veri Çekme Fonksiyonu
def get_data(ticker):
    data = yf.Ticker(ticker)
    return data.history(period="1d")['Close'].iloc[-1]

# Canlı Göstergeler (Semboller: USDTRY=X, TRY=X vb.)
st.subheader("Canlı Piyasa Özeti")
c1, c2, c3, c4 = st.columns(4)

with c1:
    dolar = get_data("USDTRY=X")
    st.metric("Dolar / TL", f"{dolar:.2f} ₺")
with c2:
    altin = get_data("GC=F") # Ons Altın
    st.metric("Ons Altın", f"${altin:.1f}")
with c3:
    bist = get_data("XU100.IS")
    st.metric("BIST 100", f"{bist:.0f}")
with c4:
    btc = get_data("BTC-USD")
    st.metric("Bitcoin", f"${btc:,.0f}")

st.markdown("---")

# Hisse Analiz Bölümü
st.subheader("Hisse Senedi Teknik Görünüm")
hisse = st.selectbox("Analiz edilecek hisse:", ["THYAO.IS", "ASELS.IS", "SASA.IS", "EREGL.IS", "KCHOL.IS"])

if hisse:
    df = yf.download(hisse, period="6mo")
    st.line_chart(df['Close'])
    st.write(f"{hisse} Son 6 Aylık Grafik")

st.sidebar.success("V3 Sürümü Yayında!")
st.sidebar.info("Bu terminal Python & Streamlit ile geliştirilmiştir.")
