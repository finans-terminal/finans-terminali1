import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans Terminali V5", layout="wide")

st.title("📈 Profesyonel Finans & Analiz Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- GÜVENLİ VERİ ÇEKME FONKSİYONU ---
def get_data(symbol):
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if not df.empty:
            # Sütun isimlerini garantiye alıyoruz
            df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
            return df
        return None
    except:
        return None

# --- ÜST PANEL: CANLI PİYASA ---
st.subheader("Piyasa Özetleri")
c1, c2, c3 = st.columns(3)

assets = {"Dolar / TL": "USDTRY=X", "Ons Altın": "GC=F", "BIST 100": "^XU100"}
cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    data = get_data(sym)
    if data is not None:
        price = float(data['Close'].iloc[-1])
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} çekilemedi.")

st.divider()

# --- ORTA PANEL: TEKNİK ANALİZ VE GRAFİK ---
st.subheader("📊 Gelişmiş Hisse Analizi")
hisse = st.selectbox("Analiz edilecek hisseyi seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

if hisse:
    df_hisse = get_data(hisse)
    
    if df_hisse is not None:
        # Teknik Gösterge Hesaplama (SMA ve RSI)
        df_hisse['SMA_20'] = ta.sma(df_hisse['Close'], length=20)
        df_hisse['RSI'] = ta.rsi(df_hisse['Close'], length=14)
        
        # Plotly ile İnteraktif Grafik
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_hisse.index, y=df_hisse['Close'], name='Fiyat', line=dict(color='royalblue', width=2)))
        fig.add_trace(go.Scatter(x=df_hisse.index, y=df_hisse['SMA_20'], name='SMA 20 (Ortalama)', line=dict(color='orange', dash='dot')))
        
        fig.update_layout(title=f"{hisse} Fiyat ve Hareketli Ortalama", xaxis_title="Tarih", yaxis_title="Fiyat (TL)", height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # RSI Göstergesi
        current_rsi = df_hisse['RSI'].iloc[-1]
        st.write(f"**Güncel RSI Değeri:** {current_rsi:.2f}")
        if current_rsi > 70: st.warning("Aşırı Alım Bölgesi (RSI > 70)")
        elif current_rsi < 30: st.success("Aşırı Satım Bölgesi (RSI < 30)")
    else:
        st.error("Hisse verileri şu an yüklenemiyor.")

# --- YAN PANEL: KPSS GERİ SAYIM ---
sinav = datetime(2026, 8, 16) # KPSS Tarihi
kalan = (sinav - datetime.now()).days
st.sidebar.markdown(f"### 🎯 KPSS Geri Sayım")
st.sidebar.subheader(f"{kalan} Gün Kaldı")
st.sidebar.progress(max(0, min(100, 100 - (kalan/150*100))))
