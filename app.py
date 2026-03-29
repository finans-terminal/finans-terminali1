import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans V9", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.markdown(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- HATA GEÇİRMEZ VERİ ÇEKME FONKSİYONU ---
def get_clean_price(symbol):
    try:
        # 5 günlük veri çekiyoruz (Hafta sonu boşluğunu aşmak için)
        df = yf.download(symbol, period="5d", interval="1d", progress=False)
        
        if not df.empty:
            # Multi-index sütun karmaşasını temizle
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Sadece 'Close' (Kapanış) sütununu al ve boş olanları sil
            close_data = df['Close'].dropna()
            
            if not close_data.empty:
                # KRİTİK NOKTA: .values[0] veya .iloc[-1] ile sadece İLK SAYIYI alıyoruz
                # Bu sayede "Series" hatası %100 çözülüyor.
                last_val = close_data.iloc[-1]
                
                # Eğer hala bir seri gelirse (nadir durum), içinden ilk rakamı çek
                if hasattr(last_val, '__len__'):
                    return float(last_val[0])
                return float(last_val)
        return None
    except Exception as e:
        return None

# --- ÜST PANEL: CANLI PİYASA ---
st.subheader("📊 Güncel Piyasa Verileri")
c1, c2, c3 = st.columns(3)

# Semboller
assets = {"Dolar / TL": "USDTRY=X", "Ons Altın": "GC=F", "BIST 100": "XU100.IS"}
cols = [c1, c2, c3]

for (name, sym), col in zip(assets.items(), cols):
    price = get_clean_price(sym)
    if price is not None:
        # 'price' artık kesinlikle bir sayı (float), formatlama güvenli:
        col.metric(label=name, value=f"{price:,.2f}")
    else:
        col.error(f"{name} çekilemedi.")

st.divider()

# --- GRAFİK BÖLÜMÜ ---
st.subheader("🔍 Hisse Senedi Analizi")
hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "EREGL.IS", "SASA.IS", "KCHOL.IS"])

try:
    df_hisse = yf.download(hisse, period="1mo", interval="1d", progress=False)
    if not df_hisse.empty:
        # Sütunları temizle
        if isinstance(df_hisse.columns, pd.MultiIndex):
            df_hisse.columns = df_hisse.columns.get_level_values(0)
        
        # Basit Çizgi Grafiği
        st.line_chart(df_hisse['Close'])
        st.caption(f"{hisse} - Son 30 Günlük Seyir")
except:
    st.error("Grafik şu an yüklenemiyor.")

# --- YAN PANEL ---
st.sidebar.markdown(f"### 🎯 KPSS Geri Sayım")
kalan = (datetime(2026, 8, 16) - datetime.now()).days
st.sidebar.header(f"{kalan} Gün")
st.sidebar.info("Pazartesi sabah 10:00'da veriler canlanacaktır.")
