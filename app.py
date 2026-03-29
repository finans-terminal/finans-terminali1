import streamlit as st
import yfinance as yf

st.title("Doğuş Can - Finans Terminali (Hata Giderildi)")

# Test Sembolleri
tickers = {"Dolar/TL": "USDTRY=X", "BIST 100": "XU100.IS", "THY": "THYAO.IS"}

for isim, kod in tickers.items():
    try:
        # Veriyi çekiyoruz
        data = yf.download(kod, period="5d", interval="1d")
        
        if not data.empty:
            # KRİTİK NOKTA: Veriyi float (sayı) tipine zorluyoruz
            # .iloc[-1] ile son satırı, ['Close'] ile kapanış sütununu alıyoruz
            # float() ekleyerek "Series" hatasını engelliyoruz
            son_fiyat = float(data['Close'].iloc[-1])
            
            st.metric(label=isim, value=f"{son_fiyat:.2f}")
        else:
            st.warning(f"{isim} için veri bulunamadı.")
            
    except Exception as e:
        st.error(f"{isim} yüklenirken hata: {e}")

st.info("Eğer sayılar geldiyse, 'Series' hatasını alt ettik demektir!")
