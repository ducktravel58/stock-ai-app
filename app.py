import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📊 무료 종목 분석기", layout="wide")
st.title("📊 티커 하나로 종목 분석 (인포그래픽 스타일)")

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

    return {
        "name": info.get('longName','N/A'),
        "sector": info.get('sector','N/A'),
        "country": info.get('country','N/A'),
        "roe": roe,
        "per": per,
        "pbr": pbr,
        "roe_baseball": roe_baseball,
        "per_baseball": per_baseball,
        "pbr_baseball": pbr_baseball,
        "score": score,
        "recommendation": recommendation
    }

if st.button("분석 실행"):
    if not ticker:
        st.warning("티커를 입력하세요.")
    else:
        data = analyze(ticker)

        # 기업 기본 정보
        with st.container():
            st.subheader(f"📌 {data['name']}")
            st.markdown(f"**업종:** {data['sector']}  |  **국가:** {data['country']}")

        st.markdown("---")

        # 재무 지표 카드
        col1, col2, col3 = st.columns(3)
        col1.metric("ROE", f"{data['roe']:.2f}", f"{data['roe_baseball']}")
        col2.metric("PER", f"{data['per']:.2f}", f"{data['per_baseball']}")
        col3.metric("PBR", f"{data['pbr']:.2f}", f"{data['pbr_baseball']}")

        st.markdown("---")

        # 종합 점수
        st.subheader("🎯 종합 점수")
        st.progress(data['score']/100)
        st.markdown(f"**점수:** {data['score']} / 100")

        # 투자 의견 강조
        if data['score'] >= 70:
            st.success(f"📢 투자 의견: {data['recommendation']}")
        else:
            st.error(f"📢 투자 의견: {data['recommendation']}")
