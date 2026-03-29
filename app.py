import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Sayfa Genişliği ve Tema
st.set_page_config(page_title="Doğuş Can - Finans V6", layout="wide", initial_sidebar_state="expanded")

# --- ÖZEL STİL (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #31333f; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Ekonomi & Finans Analiz Terminali (V6)")
st.markdown(f"**Geliştirici:** Doğuş Can Şen | MAKU Ekonomi ve Finans")

# --- VERİ ÇEKME MOTORU ---
def veri_cek(sembol, periyot="1mo"):
    try:
        # Pazar günü hatasını aşmak için download metodu
        df = yf.download(sembol, period=periyot, interval="1d", progress=False)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        return None
    except:
        return None

# --- ÜST PANEL: CANLI PİYASA METRİKLERİ ---
st.subheader("🌐 Küresel Piyasalar")
m1, m2, m3, m4 = st.columns(4)

piyasa_listesi = {
    "Dolar / TL": "USDTRY=X",
    "Ons Altın": "GC=F",
    "BIST 100": "XU100.IS",
    "Bitcoin": "BTC-USD"
}

metrikler = [m1, m2, m3, m4]

for (ad, sem), kutu in zip(piyasa_listesi.items(), metrikler):
    veri = veri_cek(sem, "7d")
    if veri is not None:
        fiyat = float(veri['Close'].iloc[-1])
        onseki_fiyat = float(veri['Close'].iloc[-2])
        degisim = ((fiyat
