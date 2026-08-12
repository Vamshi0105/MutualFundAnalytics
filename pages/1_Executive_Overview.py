import streamlit as st
import pandas as pd
from pathlib import Path

st.title('📊 Executive Overview')

BASE = Path(__file__).resolve().parents[1]
scorecard = pd.read_csv(BASE / 'outputs' / 'fund_scorecard.csv')

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Funds', len(scorecard))
col2.metric('Average CAGR', f"{scorecard['cagr'].mean():.2%}")
col3.metric('Average Sharpe', f"{scorecard['sharpe_ratio'].mean():.2f}")
col4.metric('Average Volatility', f"{scorecard['volatility'].mean():.2%}")

st.subheader('Top 10 Funds by CAGR')

top = scorecard.nlargest(10, 'cagr')

st.bar_chart(
    top.set_index('fund_name')['cagr']
)

st.subheader('Fund Summary')
st.dataframe(scorecard.head(20), use_container_width=True)