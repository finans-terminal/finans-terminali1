import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- ÜST PANEL: PİYASA ÖZETLERİ ---
st.subheader("Piyasa Özetleri (Son Kapanışlar)")
c1, c2, c3 = st.columns(3)

# 1. DOLAR VERİSİ
try:
    dolar_data = yf.download("USDTRY=X", period="5d", interval="1d", progress=False)
    if not dolar_data.empty:
        dolar_fiyat = float(dolar_data['Close'].iloc[-1])
        c1.metric(label="Dolar / TL", value=f"{dolar_fiyat:.2f} ₺")
    else:
        c1.error("Dolar verisi alınamadı.")
except:
    c1.error("Dolar bağlantı hatası.")

# 2. ALTIN VERİSİ
try:
    altin_data = yf.download("GC=F", period="5d", interval="1d", progress=False)
    if not altin_data.empty:
        altin_fiyat = float(altin_data['Close'].iloc[-1])
        c2.metric(label="Ons Altın", value=f"${altin_fiyat:,.1f}")
    else:
        c2.error("Altın verisi alınamadı.")
except:
    c2.error("Altın bağlantı hatası.")

# 3. BIST 100 VERİSİ
try:
    bist_data = yf.download("XU100.IS", period="5d", interval="1d", progress=False)
    if not bist_data.empty:
        bist_fiyat = float(bist_data['Close'].iloc[-1])
        c3.metric(label="BIST 100", value=f"{bist_fiyat:,.0f}")
    else:
        c3.error("BIST 100 verisi alınamadı.")
except:
    c3.error("BIST 100 bağlantı hatası.")

st.divider()

# --- ALT PANEL: ÇALIŞAN MUM GRAFİĞİ (THY VE DİĞERLERİ) ---
st.subheader("🕯️ Hisse Mum Grafiği (Teknik Analiz)")
hisse_secim = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

try:
    # Mum grafiği için veriyi çekiyoruz
    df = yf.download(hisse_secim, period="1mo", interval="1d", progress=False)
    
    if not df.empty:
        # Mum Grafiği (Candlestick) Oluşturma
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name=hisse_secim)])
        
        fig.update_layout(title=f"{hisse_secim} Günlük Mum Grafiği", 
                          template="plotly_dark", 
                          xaxis_rangeslider_visible=False,
                          height=500)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Grafik verisi çekilemedi.")
except Exception as e:
    st.error(f"Grafik oluşturulurken hata oluştu: {e}")

# --- YAN PANEL: KPSS GERİ SAYIM ---
st.sidebar.markdown("### 🎯 KPSS Geri Sayım")
kalan = (datetime(2026, 8, 16) - datetime.now()).days
st.sidebar.header(f"{kalan} Gün")
st.sidebar.progress(max(0, min(100, 100 - (kalan/150*100))))
