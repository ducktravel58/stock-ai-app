def run_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    data = f"""
기업명:{info.get('longName')}
PER:{info.get('trailingPE')}
PBR:{info.get('priceToBook')}
ROE:{info.get('returnOnEquity')}
매출성장:{info.get('revenueGrowth')}
업종:{info.get('sector')}
"""

    prompt = f"""
다음 기업 데이터를 기반으로 아래 11단계를 순서대로 분석하고
마지막에 종합 투자 결론을 내려라.

1. 사업 설명
2. 최근 이슈
3. 산업 위치
4. 경쟁우위
5. 재무평가
6. 리스크
7. 3년 시나리오
8. 거시 민감도
9. 밸류에이션
10. 투자테제
11. 최종 결론

기업 데이터:
{data}

종목:{ticker}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text
