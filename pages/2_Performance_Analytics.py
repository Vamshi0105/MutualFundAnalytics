import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title('📈 Performance Analytics')

BASE = Path(__file__).resolve().parents[1]
scorecard = pd.read_csv(BASE / 'outputs' / 'fund_scorecard.csv')

fund = st.selectbox(
    'Select Fund',
    scorecard['fund_name']
)

selected = scorecard[
    scorecard['fund_name'] == fund
]

col1, col2 = st.columns(2)

col1.metric(
    'CAGR',
    f"{selected['cagr'].iloc[0]:.2%}"
)

col2.metric(
    'Sharpe Ratio',
    f"{selected['sharpe_ratio'].iloc[0]:.2f}"
)

fig = px.scatter(
    scorecard,
    x='volatility',
    y='cagr',
    hover_name='fund_name',
    title='Risk vs Return'
)

st.plotly_chart(fig, use_container_width=True)

st.subheader('Top Performing Funds')

st.dataframe(
    scorecard.sort_values(
        'cagr',
        ascending=False
    ).head(10),
    use_container_width=True
)