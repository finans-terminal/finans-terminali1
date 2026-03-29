import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("🚀 Profesyonel Finansal Analiz Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- GELİŞMİŞ VERİ ÇEKME FONKSİYONU (V7) ---
def get_clean_data(symbol, period="1mo"):
    try:
        # Veriyi çekiyoruz
        df = yf.download(symbol, period=period, interval="1d", progress=False)
        
        if not df.empty:
            # KRİTİK: yfinance yeni sürümündeki MultiIndex hatasını temizleme
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Sütun isimlerini küçük harfe çevirip boşlukları temizleyelim (Garanti olsun)
            df.columns = [str(col).strip() for col in df.columns]
            
            # Eğer veri Pazar günü nedeniyle son satırda boşsa, dolu olan son satırı al
            df = df.dropna(subset=['Close'])
            return df
        return None
    except Exception as e:
        st.sidebar.error(f"Bağlantı Hatası ({symbol}): {e}")
        return None

# --- ÜST PANEL: CANLI PİYASA ---
st.subheader("📊 Piyasa Özetleri")
c1, c2, c3 = st.columns(3)

# Semboller
assets = {"Dolar / TL": "USDTRY=X", "Ons Altın": "GC=F", "BIST 100": "XU100.IS"}
cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    data = get_clean_data(sym, "7d") # Son 7 gün garantisi
    if data is not None and len(data) > 0:
        price = float(data['Close'].iloc[-1])
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} çekilemedi.")

st.divider()

# --- ANALİZ BÖLÜMÜ ---
st.subheader("🔍 Hisse Senedi Analizi")
hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

df_hisse = get_clean_data(hisse, "1y")

if df_hisse is not None:
    # Plotly Mum Grafiği
    fig = go.Figure(data=[go.Candlestick(
        x=df_hisse.index,
        open=df_hisse['Open'],
        high=df_hisse['High'],
        low=df_hisse['Low'],
        close=df_hisse['Close']
    )])
    
    fig.update_layout(
        title=f"{hisse} Yıllık Grafik",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Seçilen hisse için veri şu an Yahoo Finance sunucularından çekilemiyor.")

# --- YAN PANEL ---
st.sidebar.markdown(f"### 🎯 KPSS Geri Sayım")
kalan = (datetime(2026, 8, 16) - datetime.now()).days
st.sidebar.header(f"{kalan} Gün")
st.sidebar.progress(max(0, min(100, 100 - (kalan/150*100))))
