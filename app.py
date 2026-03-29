import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- HATA GEÇİRMEZ VERİ ÇEKME FONKSİYONU ---
def get_single_price(symbol):
    try:
        # Son 7 günü çek (Hafta sonu boşluğunu aşmak için)
        df = yf.download(symbol, period="7d", interval="1d", progress=False)
        
        if not df.empty:
            # KRİTİK ÇÖZÜM: Multi-index sütun varsa sadece 'Close' sütununu çek
            if isinstance(df.columns, pd.MultiIndex):
                # Sadece 'Close' sütununa odaklan ve ilk sembolü al
                close_series = df['Close'].iloc[:, 0] if df['Close'].shape[1] > 1 else df['Close']
            else:
                close_series = df['Close']
            
            # Boş olmayan son değeri bul ve saf sayıya (float) çevir
            last_price = float(close_series.dropna().iloc[-1])
            return last_price
        return None
    except Exception as e:
        return None

# --- ÜST PANEL: CANLI PİYASA ---
st.subheader("📊 Piyasa Özetleri")
c1, c2, c3 = st.columns(3)

# Semboller
assets = {"Dolar / TL": "USDTRY=X", "Ons Altın": "GC=F", "BIST 100": "XU100.IS"}
cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    price = get_single_price(sym)
    if price is not None:
        # Artık 'price' kesinlikle bir sayıdır, formatlama hata vermez
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} verisi alınamadı.")

st.divider()

# --- GRAFİK BÖLÜMÜ ---
st.subheader("🔍 Hisse Senedi Analizi")
hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

try:
    df_hisse = yf.download(hisse, period="1mo", interval="1d", progress=False)
    if not df_hisse.empty:
        # Grafik için de sütun temizliği
        if isinstance(df_hisse.columns, pd.MultiIndex):
            df_hisse.columns = df_hisse.columns.get_level_values(0)
            
        fig = go.Figure(data=[go.Scatter(x=df_hisse.index, y=df_hisse['Close'], mode='lines', name=hisse)])
        fig.update_layout(template
