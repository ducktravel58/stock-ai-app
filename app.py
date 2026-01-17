import streamlit as st
import yfinance as yf

st.set_page_config(page_title="개인 투자 분석기", layout="centered")
st.title("📊 티커 기반 자동 기업 분석기")

ticker = st.text_input("티커 입력 (예: AAPL, MSFT, TSLA)")

if ticker:

    stock = yf.Ticker(ticker)

    info = stock.info

    roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
    per = info.get("trailingPE", 0)
    pbr = info.get("priceToBook", 0)
    debt = info.get("debtToEquity", 0)

    st.subheader(f"📌 {ticker} 재무지표")

    st.write(f"ROE: {roe:.2f}%")
    st.write(f"PER: {per}")
    st.write(f"PBR: {pbr}")
    st.write(f"부채비율: {debt}")

    # ----------------
    # 점수 계산
    # ----------------
    score = 0
    reasons_good = []
    reasons_bad = []

    if roe >= 15:
        score += 25
        reasons_good.append("ROE가 매우 높아 수익성이 뛰어납니다.")
    elif roe >= 10:
        score += 15
        reasons_good.append("ROE가 안정적인 수준입니다.")
    else:
        score += 5
        reasons_bad.append("ROE가 낮아 수익성이 부족합니다.")

    if per <= 10:
        score += 25
        reasons_good.append("PER이 낮아 저평가 가능성이 있습니다.")
    elif per <= 20:
        score += 15
        reasons_good.append("PER이 무난한 수준입니다.")
    else:
        score += 5
        reasons_bad.append("PER이 높아 고평가 우려가 있습니다.")

    if pbr <= 1:
        score += 25
        reasons_good.append("PBR이 1 이하로 자산 대비 저평가입니다.")
    elif pbr <= 2:
        score += 15
        reasons_good.append("PBR이 적정 수준입니다.")
    else:
        score += 5
        reasons_bad.append("PBR이 높아 자산 대비 비쌉니다.")

    if debt <= 100:
        score += 25
        reasons_good.append("부채비율이 매우 안정적입니다.")
    elif debt <= 200:
        score += 15
        reasons_good.append("부채비율이 관리 가능한 수준입니다.")
    else:
        score += 5
        reasons_bad.append("부채비율이 높아 재무 리스크가 큽니다.")

    # ----------------
    # 판단
    # ----------------
    if score >= 80:
        decision = "✅ 매수 추천"
    elif score >= 60:
        decision = "⚠️ 관망"
    else:
        decision = "❌ 매수 비추천"

    # ----------------
    # 야구 비유
    # ----------------
    def baseball(label, val):
        if label == "roe":
            return "4할 타자" if val >= 15 else "3할 타자" if val >= 10 else "2군 후보"
        if label == "per":
            return "가성비 에이스" if val <= 10 else "주전급" if val <= 20 else "연봉만 높은 선수"
        if label == "pbr":
            return "숨은 보석" if val <= 1 else "평균 선수" if val <= 2 else "몸값만 큰 스타"
        if label == "debt":
            return "재정 탄탄" if val <= 100 else "운영 가능" if val <= 200 else "재정 위험"

    # ----------------
    # 출력
    # ----------------
    st.divider()
    st.subheader("📊 종합 결과")

    st.write(f"### 점수: {score}/100")
    st.write(f"### 투자 판단: {decision}")

    st.divider()
    st.subheader("⚾ 야구 비유 해석")

    st.write("ROE:", baseball("roe", roe))
    st.write("PER:", baseball("per", per))
    st.write("PBR:", baseball("pbr", pbr))
    st.write("부채비율:", baseball("debt", debt))

    st.divider()
    st.subheader("📈 매수 추천 이유")
    for r in reasons_good:
        st.write("✔️", r)

    st.divider()
    st.subheader("📉 매수 비추천 이유")
    for r in reasons_bad:
        st.write("❌", r)

    st.divider()
    st.caption("본 도구는 참고용이며 투자 책임은 사용자 본인에게 있습니다.")
