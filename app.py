import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Doğuş Can - Finans Terminali", layout="wide")

st.title("📈 Profesyonel Finans Terminali")
st.info("Veriler Yahoo Finance üzerinden canlı çekilmektedir.")

# --- Gelişmiş Veri Çekme Fonksiyonu ---
def veriyi_getir(sembol):
    try:
        # Hata payını azaltmak için 7 günlük veri çekiyoruz
        ticker = yf.Ticker(sembol)
        df = ticker.history(period="7d")
        
        if not df.empty:
            # En son geçerli fiyatı al ve sayıya (float) çevir
            son_fiyat = float(df['Close'].iloc[-1])
            return son_fiyat
        else:
            return None
    except Exception as e:
        return None

# --- Ekran Düzeni ---
col1, col2, col3 = st.columns(3)

# Semboller (Önemli: Yazımlar tam bu şekilde olmalı)
veriler = {
    "Dolar / TL": "USDTRY=X",
    "BIST 100": "XU100.IS",
    "Ons Altın": "GC=F"
}

# Verileri Dağıtma
sutunlar = [col1, col2, col3]

for (isim, kod), sutun in zip(veriler.items(), sutunlar):
    fiyat = veriyi_getir(kod)
    if fiyat:
        sutun.metric(label=isim, value=f"{fiyat:,.2f}")
    else:
        sutun.error(f"{isim} verisi şu an alınamıyor.")

st.divider()

# --- Grafik Bölümü ---
st.subheader("📊 Hisse Senedi Analizi")
secilen_hisse = st.selectbox("Hisse Seçin:", ["THYAO.IS", "ASELS.IS", "SASA.IS", "EREGL.IS"])

try:
    # Grafik verisi için son 1 ayı çek
    grafik_df = yf.download(secilen_hisse, period="1mo", interval="1d")
    if not grafik_df.empty:
        st.line_chart(grafik_df['Close'])
        st.caption(f"{secilen_hisse} Son 1 Aylık Gelişim Grafiği")
    else:
        st.warning("Grafik verisi yüklenemedi.")
except:
    st.error("Grafik çizilirken bir sorun oluştu.")

st.sidebar.markdown("### Terminal Durumu: 🟢 Aktif")
st.sidebar.write("Piyasalar kapalıyken son kapanış fiyatları gösterilir.")
