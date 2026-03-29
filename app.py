import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- GELİŞMİŞ VE GARANTİCİ VERİ ÇEKME ---
def get_data_v6(symbol):
    try:
        # Son 7 günü çekiyoruz ki hafta sonu boşluğuna düşmeyelim
        data = yf.download(symbol, period="7d", interval="1d", progress=False)
        
        if not data.empty:
            # Multi-index sütun temizliği
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # En son 'NaN' olmayan (dolu) satırı buluyoruz
            valid_data = data.dropna(subset=['Close'])
            return valid_data
        return None
    except:
        return None

# --- ÜST PANEL ---
st.subheader("Piyasa Özetleri (Son Kapanışlar)")
c1, c2, c3 = st.columns(3)

# Semboller (Bazı sunucularda ^XU100 daha stabil çalışır)
assets = {"Dolar / TL": "USDTRY=X", "Ons Altın": "GC=F", "BIST 100": "XU100.IS"}
cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    df_mini = get_data_v6(sym)
    if df_mini is not None and len(df_mini) > 0:
        last_price = float(df_mini['Close'].iloc[-1])
        # Bir önceki günle kıyaslama (Değişim oranı)
        if len(df_mini) > 1:
            prev_price = float(df_mini['Close'].iloc[-2])
            delta = ((last_price - prev_price) / prev_price) * 100
            col.metric(label=name, value=f"{last_price:,.2f}", delta=f"{delta:.2f}%")
        else:
            col.metric(label=name, value=f"{last_price:,.2f}")
    else:
        col.error(f"{name} verisi alınamadı.")

st.divider()

# --- GRAFİK BÖLÜMÜ ---
st.subheader("📊 Hisse Senedi Analizi")
hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

df_hisse = get_data_v6(hisse)
if df_hisse is not None:
    # SMA ve RSI Hesaplama
    df_hisse['SMA_20'] = ta.sma(df_hisse['Close'], length=20)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_hisse.index, y=df_hisse['Close'], name='Fiyat'))
    fig.update_layout(template="plotly_dark", height=400) # Karanlık tema daha profesyonel durur
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Hisse verisi şu an çekilemiyor, lütfen az sonra tekrar deneyin.")

# --- YAN PANEL ---
st.sidebar.markdown(f"### 🎯 KPSS Geri Sayım")
kalan = (datetime(2026, 8, 16) - datetime.now()).days
st.sidebar.header(f"{kalan} Gün")
