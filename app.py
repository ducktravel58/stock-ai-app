import streamlit as st
import openai

st.set_page_config(page_title="Stock Research AI", layout="wide")
st.title("📊 원스톱 주식 연구 AI")

openai.api_key = st.secrets["OPENAI_API_KEY"]

ticker = st.text_input("분석할 종목 티커 입력 (예: AAPL, TSLA)")

prompts = [
    "이 회사의 사업을 쉽게 설명해줘.",
    "최근 뉴스, 실적, 주요 이벤트 요약 (출처 포함).",
    "산업 트렌드, 성장동력, 주요 리스크 설명.",
    "경제적 해자 분석.",
    "재무 건전성 요약.",
    "레드 플래그 정리.",
    "3~5년 시나리오 분석.",
    "거시 민감도.",
    "밸류에이션 맥락.",
    "장기 투자 테제.",
    "지속 모니터링 포인트."
]

def ask(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

if st.button("🚀 원스톱 분석 실행") and ticker:
    st.success(f"{ticker} 자동 분석 시작")

    for i, p in enumerate(prompts, 1):
        with st.spinner(f"{i}단계 분석 중..."):
            result = ask(f"{p}\n종목: {ticker}")
            st.subheader(f"{i}. {p}")
            st.write(result)
