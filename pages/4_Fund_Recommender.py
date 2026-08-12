import streamlit as st
import pandas as pd
from pathlib import Path

st.title('🤖 Fund Recommender')

BASE = Path(__file__).resolve().parents[1]
scorecard = pd.read_csv(BASE / 'outputs' / 'fund_scorecard.csv')

profile = st.selectbox(
    'Investor Profile',
    [
        'Conservative',
        'Moderate',
        'Aggressive'
    ]
)

if profile == 'Conservative':
    recommended = scorecard.nsmallest(5, 'volatility')

elif profile == 'Moderate':
    recommended = scorecard.nlargest(5, 'sharpe_ratio')

else:
    recommended = scorecard.nlargest(5, 'cagr')

st.subheader(f'Recommended Funds for {profile} Investors')

st.dataframe(
    recommended[[
        'fund_name',
        'cagr',
        'volatility',
        'sharpe_ratio',
        'max_drawdown'
    ]],
    use_container_width=True
)

st.success('Recommendation generated based on historical performance and risk metrics.')