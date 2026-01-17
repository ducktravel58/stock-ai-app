import streamlit as st
import yfinance as yf

st.set_page_config(page_title="무료 종목 분석기", layout="centered")
st.title("📊 티커 하나로 종목 분석 (AI 없이)")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA, NVDA)")

def analyze(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # 재무 지표
    roe = info.get("returnOnEquity", 0)
    per = info.get("trailingPE", 0)
    pbr = info.get("priceToBook", 0)

    # 점수 계산
    score = 0
    if roe > 0.15: score += 40
    if per and per < 20: score += 30
    if pbr and pbr < 3: score += 30
    recommendation = "✅ 매수 추천" if score >= 70 else "❌ 관망 / 비추천"

    # 야구 비유
    roe_baseball = "3할 타자급" if roe>0.15 else "평균 타자급"
    per_baseball = "가성비 좋은 선수" if per and per<20 else "몸값 비쌈"
    pbr_baseball = "저평가 선수" if pbr and pbr<3 else "고평가 선수"

    # 최종 결과
    result = f"""
📌 기업명: {info.get('longName','N/A')}
📌 업종: {info.get('sector','N/A')}
📌 국가: {info.get('country','N/A')}

📊 재무 지표
- ROE: {roe}
- PER: {per}
- PBR: {pbr}

⚾ 야구 비유
- ROE: {roe_baseball}
- PER: {per_baseball}
- PBR: {pbr_baseball}

🎯 종합 점수: {score} / 100
📢 투자 의견: {recommendation}
"""
    return result

if st.button("분석 실행"):
    if ticker:
        st.text(analyze(ticker))
    else:
        st.warning("티커를 입력하세요.")
