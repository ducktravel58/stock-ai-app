import streamlit as st
import yfinance as yf
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📊 AI 기반 11단계 종목 분석 시스템")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

PROMPTS = [
    "1. 이 회사의 사업을 아주 쉽게 설명해줘.",
    "2. 최근 뉴스와 이슈를 요약해줘.",
    "3. 산업 트렌드와 위치를 설명해줘.",
    "4. 경쟁우위를 분석해줘.",
    "5. 재무 건전성을 평가해줘.",
    "6. 주요 리스크를 정리해줘.",
    "7. 3년 시나리오 분석을 해줘.",
    "8. 거시환경 민감도를 분석해줘.",
    "9. 밸류에이션 맥락을 설명해줘.",
    "10. 장기 투자 테제를 작성해줘.",
    "11. 최종 종합 결론을 내려줘."
]

def ai_analyze(prompt):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text

def run_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    base_data = f"""
기업명: {info.get('longName')}
시가총액: {info.get('marketCap')}
PER: {info.get('trailingPE')}
PBR: {info.get('priceToBook')}
ROE: {info.get('returnOnEquity')}
매출성장률: {info.get('revenueGrowth')}
업종: {info.get('sector')}
"""

    full_report = ""

    for p in PROMPTS:
        query = f"{p}\n\n기업 데이터:\n{base_data}\n\n종목:{ticker}"
        answer = ai_analyze(query)
        full_report += f"\n\n### {p}\n{answer}\n"

    return full_report


if st.button("11단계 AI 분석 실행"):
    if ticker:
        with st.spinner("AI 분석 중..."):
            try:
                result = run_analysis(ticker)
                st.markdown(result)
            except Exception as e:
                st.error(e)
    else:
        st.warning("티커를 입력하세요.")
