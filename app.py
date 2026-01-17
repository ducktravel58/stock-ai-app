import streamlit as st
import yfinance as yf
import google.generativeai as genai

st.set_page_config(page_title="Gemini 주식 분석", layout="centered")

st.title("📊 Gemini 기반 11단계 종목 분석")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 🔥 모델명 수정
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def gemini_analysis(info, ticker):
    data = f"""
기업명:{info.get('longName')}
시가총액:{info.get('marketCap')}
PER:{info.get('trailingPE')}
PBR:{info.get('priceToBook')}
ROE:{info.get('returnOnEquity')}
매출성장:{info.get('revenueGrowth')}
업종:{info.get('sector')}
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

종목:{ticker}
"""

    response = model.generate_content(prompt)
    return response.text


if st.button("Gemini 11단계 분석 실행"):
    if ticker:
        with st.spinner("Gemini 분석 중..."):
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                result = gemini_analysis(info, ticker)
                st.markdown(result)
            except Exception as e:
                st.error(f"에러 발생: {e}")
    else:
        st.warning("티커를 입력하세요.")
