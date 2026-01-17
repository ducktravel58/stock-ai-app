import streamlit as st

st.set_page_config(page_title="개인 투자 분석기", layout="centered")

st.title("📊 개인 투자용 기업 분석 도구")

st.write("재무지표를 입력하면 투자 판단 + 야구 비유 해석까지 제공합니다.")

# ----------------------
# 입력
# ----------------------
roe = st.number_input("ROE (%)", value=15.0)
per = st.number_input("PER", value=12.0)
pbr = st.number_input("PBR", value=1.2)
debt = st.number_input("부채비율 (%)", value=80.0)

# ----------------------
# 점수 계산
# ----------------------
score = 0
reasons_good = []
reasons_bad = []

# ROE
if roe >= 15:
    score += 25
    reasons_good.append("ROE가 높아 자본을 매우 효율적으로 활용하는 기업입니다.")
elif roe >= 10:
    score += 15
    reasons_good.append("ROE가 평균 이상으로 안정적인 수익성을 보입니다.")
else:
    score += 5
    reasons_bad.append("ROE가 낮아 수익성이 부족합니다.")

# PER
if per <= 10:
    score += 25
    reasons_good.append("PER이 낮아 저평가 가능성이 있습니다.")
elif per <= 20:
    score += 15
    reasons_good.append("PER이 합리적인 수준입니다.")
else:
    score += 5
    reasons_bad.append("PER이 높아 고평가 우려가 있습니다.")

# PBR
if pbr <= 1:
    score += 25
    reasons_good.append("PBR이 1 이하로 자산 대비 저평가 상태입니다.")
elif pbr <= 2:
    score += 15
    reasons_good.append("PBR이 무난한 수준입니다.")
else:
    score += 5
    reasons_bad.append("PBR이 높아 자산 대비 비싸게 거래됩니다.")

# 부채비율
if debt <= 100:
    score += 25
    reasons_good.append("부채비율이 안정적입니다.")
elif debt <= 200:
    score += 15
    reasons_good.append("부채비율이 관리 가능한 수준입니다.")
else:
    score += 5
    reasons_bad.append("부채비율이 높아 재무 리스크가 큽니다.")

# ----------------------
# 투자 판단
# ----------------------
if score >= 80:
    decision = "✅ 매수 추천"
elif score >= 60:
    decision = "⚠️ 관망"
else:
    decision = "❌ 매수 비추천"

# ----------------------
# 야구 비유 해석
# ----------------------
def baseball_roe(val):
    if val >= 15:
        return "4할 타자급 — 팀의 중심 타선"
    elif val >= 10:
        return "3할 타자 — 안정적인 주전"
    else:
        return "2할 초반 — 2군 후보급"

def baseball_per(val):
    if val <= 10:
        return "연봉 대비 성적 미친 가성비 선수"
    elif val <= 20:
        return "적당한 연봉의 주전급 선수"
    else:
        return "연봉만 비싼 FA 계약 선수"

def baseball_pbr(val):
    if val <= 1:
        return "몸값보다 실력이 더 좋은 숨은 보석"
    elif val <= 2:
        return "시장 평균 선수"
    else:
        return "몸값만 높아진 스타 선수"

def baseball_debt(val):
    if val <= 100:
        return "팀 재정 탄탄"
    elif val <= 200:
        return "운영 가능 수준"
    else:
        return "구단 재정 적자 위험"

# ----------------------
# 출력
# ----------------------
st.divider()
st.subheader("📌 종합 평가")

st.write(f"### 점수: **{score} / 100**")
st.write(f"### 투자 판단: **{decision}**")

st.divider()

st.subheader("⚾ 야구 비유 해석")

st.write(f"ROE: {baseball_roe(roe)}")
st.write(f"PER: {baseball_per(per)}")
st.write(f"PBR: {baseball_pbr(pbr)}")
st.write(f"부채비율: {baseball_debt(debt)}")

st.divider()

st.subheader("📈 매수 추천 이유")

if reasons_good:
    for r in reasons_good:
        st.write("✔️ " + r)
else:
    st.write("없음")

st.divider()

st.subheader("📉 매수 비추천 이유")

if reasons_bad:
    for r in reasons_bad:
        st.write("❌ " + r)
else:
    st.write("없음")

st.divider()

st.caption("※ 본 도구는 참고용 분석이며 투자 책임은 사용자 본인에게 있습니다.")
