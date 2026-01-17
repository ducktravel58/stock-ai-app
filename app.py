import streamlit as st
import requests
import json

import google.generativeai as genai
genai.configure(api_key="너의키")
for m in genai.list_models():
    print(m.name)


API_KEY = "YOUR_GEMINI_API_KEY"

MODEL = "models/gemini-1.5-flash-001"

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return f"에러 발생: {response.text}"

    data = response.json()

    return data["candidates"][0]["content"]["parts"][0]["text"]

st.title("📊 Gemini 기반 종목 분석 AI")

ticker = st.text_input("종목 티커 입력")

if st.button("분석 실행"):
    if ticker:
        prompt = f"{ticker} 종목을 재무적 관점에서 장기투자 기준으로 분석해줘. PER, 성장성, 위험요소 포함해서 결론까지 내려줘."
        result = ask_gemini(prompt)
        st.write(result)
    else:
        st.warning("티커를 입력하세요.")
