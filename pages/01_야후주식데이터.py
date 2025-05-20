import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 글로벌 시가총액 Top 10 기업의 티커 목록 (2024년 기준)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Saudi Aramco': '2222.SR',  # 사우디 증권거래소
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Nvidia': 'NVDA',
    'Berkshire Hathaway': 'BRK-B',
    'Meta (Facebook)': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM'
}

st.title("📈 글로벌 시가총액 Top 10 기업의 최근 1년 주가 변화")
st.markdown("데이터 출처: [Yahoo Finance](https://finance.yahoo.com/)")

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 다운로드
@st.cache_data
def fetch_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    # 'Adj Close' 컬럼만 사용하고 단일 컬럼으로 정리
    if 'Adj Close' in data.columns:
        data = data[['Adj Close']]
    elif ('Adj Close', '') in data.columns:  # MultiIndex 대응
        data = data[('Adj Close', '')]
        data = data.to_frame(name='Adj Close')
    data['Symbol'] = ticker
    return data


# 모든 데이터 가져오기
data_dict = {}
for name, ticker in top10_tickers.items():
    df = fetch_data(ticker)
    if not df.empty:
        df['Company'] = name
        data_dict[name] = df

# Plotly 시각화
fig = go.Figure()
for company, df in data_dict.items():
    if 'Adj Close' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Adj Close'],
            mode='lines',
            name=company
        ))

fig.update_layout(
    title="글로벌 시가총액 상위 10개 기업의 주가 변화 (최근 1년)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    template="plotly_white",
    legend_title="기업명"
)

st.plotly_chart(fig, use_container_width=True)

