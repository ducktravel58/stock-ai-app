import streamlit as st
import yfinance as yf
from transformers import pipeline

st.set_page_config(page_title="무료 AI 주식 분석기 (한국어)", layout="centered")
st.title("📊 티커 하나로 종목 분석 (한국어 무료 AI)")

# Hugging Face 한국어 GPT-2 모델 사용
# 설치: pip install transformers torch
ai = pipeline("text-generation", model="skt/kogpt2-base-v2")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA, NVDA)")

def analyze(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # 재무 지표 가져오기
    roe = info.get("returnOnEquity", 0)
    per = info.get("trailingPE", 0)
    pbr = info.get("priceToBook", 0)
    
    # 점수 계산 (100점 만점)
    score = 0
    if roe > 0.15: score += 40
    if per and per < 20: score += 30
    if pbr and pbr < 3: score += 30
    
    recommendation = "✅ 매수 추천" if score >= 70 else "❌ 관망 / 비추천"
    
    # AI 분석 프롬프트 (한국어)
    prompt = f"""
회사명: {info.get('longName', 'N/A')}
업종: {info.get('sector', 'N/A')}
국가: {info.get('country', 'N/A')}
ROE: {roe}
PER: {per}
PBR: {pbr}

위 정보를 바탕으로, 
- 11단계 주식 분석 요약
- 점수 100점 만점 기준
- 매수 추천/비추천 이유
- 야구 비유 포함
자연스러운 한국어로 설명해줘.
"""
    try:
        result_ai = ai(prompt, max_length=300, do_sample=True)[0]['generated_text']
    except Exception as e:
        result_ai = f"AI 분석 실패: {e}"
    
    # 결과 텍스트
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

🤖 AI 분석:
{result_ai}
"""
    return result

if st.button("분석 실행"):
    if ticker:
        st.text(analyze(ticker))
    else:
        st.warning("티커를 입력하세요.")
