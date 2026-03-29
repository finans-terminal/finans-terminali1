import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.write(f"**Geliştirici:** Doğuş Can Şen | Ekonomi & Finans")

# --- GÜVENLİ VERİ ÇEKME FONKSİYONU ---
def get_data_safe(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        # 1 gün yerine 7 günlük veri çekiyoruz (Hafta sonu takılmaması için)
        df = ticker.history(period="7d")
        if not df.empty:
            return df['Close'].iloc[-1]
        else:
            return None
    except:
        return None

# --- PİYASA ÖZETİ ---
st.subheader("Canlı Piyasa Verileri")
c1, c2, c3 = st.columns(3)

# Verileri çekiyoruz
usd_price = get_data_safe("USDTRY=X")
gold_price = get_data_safe("GC=F")
bist_price = get_data_safe("XU100.IS")

with c1:
    if usd_price:
        st.metric("Dolar / TL", f"{usd_price:.2f} ₺")
    else:
        st.error("Dolar verisi alınamadı.")

with c2:
    if gold_price:
        st.metric("Ons Altın", f"${gold_price:.1f}")
    else:
        st.error("Altın verisi alınamadı.")

with c3:
    if bist_price:
        st.metric("BIST 100", f"{bist_price:.0f}")
    else:
        st.error("BIST verisi alınamadı.")

st.divider()

# --- HİSSE ANALİZ BÖLÜMÜ ---
st.subheader("Hisse Senedi Analizi")
hisse_listesi = {
    "Türk Hava Yolları": "THYAO.IS",
    "Aselsan": "ASELS.IS",
    "Sasa Polyester": "SASA.IS",
    "Ereğli Demir Çelik": "EREGL.IS",
    "Koç Holding": "KCHOL.IS"
}

secilen_ad = st.selectbox("Analiz edilecek hisseyi seçin:", list(hisse_listesi.keys()))
secilen_ticker = hisse_listesi[secilen_ad]

try:
    # Son 1 aylık veriyi çek ve grafik çiz
    grafik_verisi = yf.download(secilen_ticker, period="1mo", interval="1d")
    
    if not grafik_verisi.empty:
        st.line_chart(grafik_verisi['Close'])
        st.caption(f"{secilen_ad} ({secilen_ticker}) - Son 1 Aylık Kapanış Grafiği")
    else:
        st.warning(f"{secilen_ad} için şu an grafik verisi çekilemiyor.")
except Exception as e:
    st.error(f"Bir hata oluştu: {e}")

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.success("Terminal Durumu: Aktif")
st.sidebar.info("Hafta sonları ve tatil günlerinde veriler son kapanış fiyatlarını gösterir.")
