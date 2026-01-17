import streamlit as st
import yfinance as yf
from huggingface_hub import InferenceClient

st.set_page_config(page_title="무료 AI 주식 분석기", layout="centered")
st.title("📊 티커 하나로 종목 분석 (무료 AI)")

# Hugging Face 무료 계정 토큰 (Spaces에서 Secret로 저장 가능)
HF_TOKEN = st.secrets.get("HF_API_TOKEN", "")  # 없으면 빈 문자열
client = InferenceClient(token=HF_TOKEN)

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

    # AI 분석 프롬프트
    prompt = f"""
회사명: {info.get('longName','N/A')}
업종: {info.get('sector','N/A')}
국가: {info.get('country','N/A')}
재무 지표: ROE {roe}, PER {per}, PBR {pbr}

위 정보를 기반으로:
- 핵심 투자 의견 요약
- 매수 추천/비추천 이유
- 야구 비유 포함

3~5문장 내외로 자연스러운 한국어로 설명해줘.
"""

    try:
        result_ai = client.text_generation(model="skt/kogpt2-base-v2", inputs=prompt, max_new_tokens=150)
        ai_text = result_ai.get('generated_text', 'AI 분석 실패')
    except Exception as e:
        ai_text = f"AI 분석 실패: {e}"

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

🤖 AI 분석:
{ai_text}
"""
    return result

if st.button("분석 실행"):
    if ticker:
        st.text(analyze(ticker))
    else:
        st.warning("티커를 입력하세요.")
