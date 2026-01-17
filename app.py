import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="무료 종목 분석 시스템", layout="centered")
st.title("📊 무료 종목 분석 시스템")

ticker = st.text_input("종목 티커 입력 (예: AAPL, TSLA)")

# ---------- AI 요약 ----------
def generate_summary(score):
    if score >= 80:
        return "재무 안정성과 성장성이 모두 우수한 장기 투자 적합 종목입니다."
    elif score >= 60:
        return "재무 구조는 양호하나 일부 지표에서 개선이 필요한 종목입니다."
    elif score >= 40:
        return "성장성과 안정성 모두에서 주의가 필요한 종목입니다."
    else:
        return "재무 구조상 투자 위험이 높은 종목입니다."

# ---------- 투자 이유 생성 ----------
def generate_reason(data):
    good = []
    bad = []

    if data["ROE"] > 0.15:
        good.append("ROE가 높아 자본 효율성이 우수합니다.")
    else:
        bad.append("ROE가 낮아 수익성이 부족합니다.")

    if data["PER"] and data["PER"] < 20:
        good.append("PER이 낮아 밸류에이션 부담이 크지 않습니다.")
    else:
        bad.append("PER이 높아 고평가 가능성이 있습니다.")

    if data["매출성장"] > 0.05:
        good.append("매출 성장률이 안정적으로 유지되고 있습니다.")
    else:
        bad.append("매출 성장성이 둔화되고 있습니다.")

    if data["부채비율"] and data["부채비율"] < 100:
        good.append("부채비율이 낮아 재무 안정성이 우수합니다.")
    else:
        bad.append("부채비율이 높아 재무 리스크가 존재합니다.")

    if data["잉여현금"] and data["잉여현금"] > 0:
        good.append("잉여현금흐름이 양호하여 현금 창출력이 좋습니다.")
    else:
        bad.append("잉여현금흐름이 부족합니다.")

    return good, bad

# ---------- 종목 분석 ----------
def analyze_stock(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    roe = info.get("returnOnEquity", 0)
    pe = info.get("trailingPE", 0)
    pb = info.get("priceToBook", 0)
    margin = info.get("profitMargins", 0)
    growth = info.get("revenueGrowth", 0)
    debt = info.get("debtToEquity", 0)
    beta = info.get("beta", 0)
    dividend = info.get("dividendYield", 0)
    cash = info.get("totalCash", 0)
    fcf = info.get("freeCashflow", 0)
    op_margin = info.get("operatingMargins", 0)

    score = 0
    if roe > 0.15: score += 1
    if pe and pe < 20: score += 1
    if pb and pb < 3: score += 1
    if margin > 0.1: score += 1
    if growth > 0.05: score += 1
    if debt and debt < 100: score += 1
    if beta and beta < 1.3: score += 1
    if dividend and dividend > 0.02: score += 1
    if cash: score += 1
    if fcf: score += 1
    if op_margin > 0.1: score += 1

    final_score = int(score / 11 * 100)

    if final_score >= 80:
        recommendation = "✅ 적극 매수"
    elif final_score >= 60:
        recommendation = "🟡 분할 매수"
    elif final_score >= 40:
        recommendation = "⚠️ 관망"
    else:
        recommendation = "❌ 매수 비추천"

    summary = generate_summary(final_score)

    good, bad = generate_reason({
        "ROE": roe,
        "PER": pe,
        "매출성장": growth,
        "부채비율": debt,
        "잉여현금": fcf
    })

    return {
        "ROE": roe,
        "PER": pe,
        "PBR": pb,
        "이익률": margin,
        "매출성장": growth,
        "부채비율": debt,
        "베타": beta,
        "배당률": dividend,
        "현금": cash,
        "잉여현금": fcf,
        "영업이익률": op_margin,
        "점수(100점)": final_score,
        "매수 판단": recommendation,
        "AI 요약": summary,
        "매수 근거": good,
        "매수 비추천 근거": bad
    }

# ---------- 실행 ----------
if st.button("분석 실행"):
    if ticker:
        try:
            data = analyze_stock(ticker)

            st.subheader("📈 종목 분석 결과")

            summary = data.pop("AI 요약")
            good = data.pop("매수 근거")
            bad = data.pop("매수 비추천 근거")

            st.table(pd.DataFrame(data.items(), columns=["항목","값"]))

            st.success(f"📌 최종 판단: {data['매수 판단']} / {data['점수(100점)']}점")
            st.info(f"🤖 AI 요약 평가: {summary}")

            st.subheader("📌 투자 판단 근거")

            if data["점수(100점)"] >= 60:
                for g in good:
                    st.write("✅ " + g)
            else:
                for b in bad:
                    st.write("❌ " + b)

        except Exception as e:
            st.error(f"에러 발생: {e}")
    else:
        st.warning("티커를 입력하세요.")
