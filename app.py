import streamlit as st
import yfinance as yf
from transformers import pipeline

st.set_page_config(page_title="무료 AI 주식 분석기", layout="centered")
st.title("📊 Hugging Face Spaces용 무료 AI 주식 분석기")

# Hugging Face 무료 모델 사용
ai = pipeline("text-generation", model="gpt2")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA, NVDA)")

def analyze(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    roe = info.get("returnOnEquity", 0)
    per = info.get("trailingPE", 0)
    pbr = info.get("priceToBook", 0)
    
    score = 0
    if roe > 0.15: score += 40
    if per and per < 20: score += 30
    if pbr and pbr < 3: score += 30
    
    recommendation = "✅ 매수 추천" if score >= 70 else "❌ 관망 / 비추천"
    
    prompt = f"""
회사명: {info.get('longName', 'N/A')}
업종: {info.get('sector', 'N/A')}
국가: {info.get('country', 'N/A')}
ROE: {roe}
PER: {per}
PBR: {pbr}

위 정보를 바탕으로 11단계 분석,
점수 100점 만점, 매수 추천 여부, 야구 비유를 포함해 설명해줘.
"""
    try:
        result_ai = ai(prompt, max_length=300)[0]['generated_text']
    except Exception as e:
        result_ai = f"AI 분석 실패: {e}"
    
    result = f"""
📌 기업명: {info.get('longName','N/A')}
📌 업종: {info.get('sector','N/A')}
📌 국가: {info.get('country','N/A')}

📊 재무 지표
- ROE: {roe}
- PER: {per}
- PBR: {pbr}

⚾ 야구 비유
ROE는 타율입니다 → {'3할 타자급' if roe>0.15 else '평균 타자급'}
PER은 연봉 대비 성적 → {'가성비 좋은 선수' if per and per<20 else '몸값 비쌈'}
PBR은 몸값 대비 실력 → {'저평가 선수' if pbr and pbr<3 else '고평가 선수'}

🎯 종합 점수: {score} / 100
📢 투자 의견: {recommendation}

🤖 무료 AI 분석:
{result_ai}
"""
    return result

if st.button("분석 실행"):
    if ticker:
        st.text(analyze(ticker))
    else:
        st.warning("티커를 입력하세요.")
