import json
import requests

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]} 
        ]
    }

    response = requests.post(url, json=payload)

    try:
        data = response.json()
    except:
        return f"JSON 파싱 실패: {response.text}"

    if response.status_code != 200:
        return f"""
❌ API 에러
status: {response.status_code}

전체 응답:
{json.dumps(data, indent=2, ensure_ascii=False)}
"""

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return f"""
❌ 응답 구조 오류

전체 JSON:
{json.dumps(data, indent=2, ensure_ascii=False)}
"""
