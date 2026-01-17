import streamlit as st
import yfinance as yf

st.title("📊 무료 종목 분석 시스템")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

def analyze(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    result = f"""
📌 기업명: {info.get("longName","N/A")}
📌 시가총액: {info.get("marketCap","N/A")}
📌 PER: {info.get("trailingPE","N/A")}
📌 PBR: {info.get("priceToBook","N/A")}
📌 ROE: {info.get("returnOnEquity","N/A")}
📌 매출 성장률: {info.get("revenueGrowth","N/A")}
📌 업종: {info.get("sector","N/A")}
📌 국가: {info.get("country","N/A")}

📊 종합 해석:
이 종목은 재무 지표 기준으로 장기 투자 관점에서 
{'우수' if info.get("returnOnEquity",0)>0.15 else '보통'}한 수익성을 보이고 있으며,
PER 기준으로 {'저평가' if info.get("trailingPE",99)<20 else '고평가'} 구간입니다.
"""

    return result

if st.button("분석 실행"):
    if ticker:
        try:
            result = analyze(ticker)
            st.text(result)
        except:
            st.error("티커 오류 또는 데이터 없음")
    else:
        st.warning("티커를 입력하세요.")
