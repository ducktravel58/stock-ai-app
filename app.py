import streamlit as st
import yfinance as yf
from openai import OpenAI

st.set_page_config(page_title="종목 분석 시스템", layout="centered")

st.title("📊 종목 분석 시스템 (무료 + AI 혼합)")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

client = None
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def free_analysis(info):
    return f"""
📌 기업명: {info.get("longName")}
📌 시가총액: {info.get("marketCap")}
📌 PER: {info.get("trailingPE")}
📌 PBR: {info.get("priceToBook")}
📌 ROE: {info.get("returnOnEquity")}
📌 매출 성장률: {info.get("revenueGrowth")}
📌 업종: {info.get("sector")}

📊 무료 종합 해석:
이 종목은 재무 기준으로 
{'수익성 우수' if info.get("returnOnEquity",0)>0.15 else '수익성 보통'} 수준이며,
PER 기준 {'저평가' if info.get("trailingPE",99)<20 else '고평가'} 구간입니다.
"""

def ai_analysis(info, ticker):
    data = f"""
기업명:{info.get('longName')}
PER:{info.get('trailingPE')}
PBR:{info.get('priceToBook')}
ROE:{info.get('returnOnEquity')}
매출성장:{info.get('revenueGrowth')}
업종:{info.get('sector')}
"""

    prompt = f"""
다음 기업 데이터를 기반으로 11단계 종합 투자 분석을 수행하고
마지막에 투자 결론을 내려라.

기업 데이터:
{data}

종목:{ticker}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text


if st.button("분석 실행"):
    if ticker:
        stock = yf.Ticker(ticker)
        info = stock.info

        st.subheader("📌 무료 재무 기반 분석")
        st.text(free_analysis(info))

        if client:
            st.subheader("🤖 AI 종합 분석")
            try:
                ai_result = ai_analysis(info, ticker)
                st.markdown(ai_result)
            except:
                st.warning("AI 사용량 초과 → 무료 분석 모드로 동작 중입니다.")
        else:
            st.warning("AI 키 없음 → 무료 분석 모드로 실행 중입니다.")

    else:
        st.warning("티커를 입력하세요.")
