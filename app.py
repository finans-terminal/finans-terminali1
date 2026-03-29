import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Doğuş Can Terminal", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- TEŞHİS VE VERİ ÇEKME FONKSİYONU ---
def garantili_veri(sembol):
    try:
        # Ticker nesnesi oluştur
        t = yf.Ticker(sembol)
        # Son 1 haftalık veriyi çek
        df = t.history(period="7d", interval="1d")
        
        if not df.empty:
            # En son fiyatı ve tarihini al
            son_fiyat = float(df['Close'].iloc[-1])
            return son_fiyat
        return None
    except Exception as e:
        # Hata varsa ekranda küçük bir uyarı göster (Sadece geliştirici görsün)
        st.sidebar.error(f"{sembol} Hatası: {e}")
        return None

# --- ÜST PANEL ---
st.subheader("Piyasa Verileri")
c1, c2, c3 = st.columns(3)

# Sembolleri en kararlı halleriyle tanımlayalım
dolar = garantili_veri("USDTRY=X")
altin = garantili_veri("GC=F")
bist = garantili_veri("XU100.IS")

with c1:
    if dolar: st.metric("Dolar / TL", f"{dolar:.2f} ₺")
    else: st.warning("Dolar çekilemedi")

with c2:
    if altin: st.metric("Ons Altın", f"${altin:,.1f}")
    else: st.warning("Altın çekilemedi")

with c3:
    if bist: st.metric("BIST 100", f"{bist:,.0f}")
    else: st.warning("BIST çekilemedi")

st.divider()

# --- ÇALIŞAN GRAFİK MANTIĞI ---
st.subheader("📊 Hisse Senedi Analizi")
hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS"])

try:
    # Senin çalışan dediğin mantıkla grafiği çiziyoruz
    grafik_df = yf.download(hisse, period="1mo", interval="1d", progress=False)
    if not grafik_df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=grafik_df.index,
            open=grafik_df['Open'],
            high=grafik_df['High'],
            low=grafik_df['Low'],
            close=grafik_df['Close']
        )])
        fig.update_layout(template="plotly_dark", height=450, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Bu hisse için grafik verisi şu an kapalı.")
except:
    st.error("Grafik sunucusu yanıt vermiyor.")

# --- YAN PANEL ---
st.sidebar.markdown(f"### 🎯 KPSS Geri Sayım")
kalan = (datetime(2026, 8, 16) - datetime.now()).days
st.sidebar.header(f"{kalan} Gün Kaldı")
