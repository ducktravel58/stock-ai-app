import streamlit as st
import yfinance as yf

st.set_page_config(page_title="📊 무료 종목 분석기", layout="wide")
st.title("📊 티커 하나로 종목 분석 (인포그래픽 + 기준표 포함)")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA, NVDA)")

# 지표 기준표
def get_rating(value, indicator):
    if indicator == "ROE":
        if value >= 0.15: return "👍 우수"
        elif value >= 0.08: return "⚖️ 보통"
        else: return "👎 낮음"
    elif indicator == "PER":
        if value < 15: return "👍 저평가"
        elif value < 25: return "⚖️ 적정"
        else: return "👎 고평가"
    elif indicator == "PBR":
        if value < 1.5: return "👍 저평가"
        elif value < 3: return "⚖️ 적정"
        else: return "👎 고평가"
    else:
        return "N/A"

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

    # 추천/비추천 요약
    if score >= 70:
        reason = "이 회사는 재무 건전성이 높고 ROE가 우수합니다. PER과 PBR도 합리적 수준입니다. 장기 투자 관점에서 안정적 성장을 기대할 수 있습니다."
    else:
        reason = "ROE가 낮거나 PER/PBR이 높아 상대적으로 고평가 상태입니다. 수익성과 가격 대비 매력이 떨어지며, 투자 리스크가 존재합니다."

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
        "roe_rating": get_rating(roe, "ROE"),
        "per_rating": get_rating(per, "PER"),
        "pbr_rating": get_rating(pbr, "PBR"),
        "score": score,
        "recommendation": recommendation,
        "reason": reason
    }

if st.button("분석 실행"):
    if not ticker:
        st.warning("티커를 입력하세요.")
    else:
        data = analyze(ticker)

        # 기업 기본 정보
        st.subheader(f"📌 {data['name']}")
        st.markdown(f"**업종:** {data['sector']}  |  **국가:** {data['country']}")
        st.markdown("---")

        # 재무 지표 카드 + 기준표
        col1, col2, col3 = st.columns(3)
        col1.metric("ROE", f"{data['roe']:.2f}", f"{data['roe_baseball']} | {data['roe_rating']}")
        col2.metric("PER", f"{data['per']:.2f}", f"{data['per_baseball']} | {data['per_rating']}")
        col3.metric("PBR", f"{data['pbr']:.2f}", f"{data['pbr_baseball']} | {data['pbr_rating']}")

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

        # 추천/비추천 이유
        st.subheader("📌 투자 의견 요약")
        st.markdown(data['reason'])
