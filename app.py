import streamlit as st
import yfinance as yf
from openai import OpenAI

# OpenAI Client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI 주식 분석", layout="centered")

st.title("📊 AI 기반 11단계 종목 분석")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

def run_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    data = f"""
기업명: {info.get('longName')}
시가총액: {info.get('marketCap')}
PER: {info.get('trailingPE')}
PBR: {info.get('priceToBook')}
ROE: {info.get('returnOnEquity')}
매출성장률: {info.get('revenueGrowth')}
업종: {info.get('sector')}
"""

    prompt = f"""
다음 기업 데이터를 기반으로 아래 11단계를 순서대로 분석하고
마지막에 종합 투자 결론을 내려라.

1. 사업 설명
2. 최근 이슈
3. 산업 위치
4. 경쟁우위
5. 재무평가
6. 리스크
7. 3년 시나리오
8. 거시 민감도
9. 밸류에이션
10. 투자 테제
11. 최종 결론

기업 데이터:
{data}

종목: {ticker}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


if st.button("11단계 AI 분석 실행"):
    if ticker:
        with st.spinner("AI 분석 중..."):
            try:
                result = run_analysis(ticker)
                st.markdown(result)
            except Exception as e:
                st.error(f"에러 발생: {e}")
    else:
        st.warning("티커를 입력하세요.")
