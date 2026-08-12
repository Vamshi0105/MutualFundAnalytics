import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title('⚠️ Risk Analytics')

BASE = Path(__file__).resolve().parents[1]
scorecard = pd.read_csv(BASE / 'outputs' / 'fund_scorecard.csv')

var = pd.read_csv(BASE / 'outputs' / 'var_cvar.csv')

st.subheader('Value at Risk (95%)')

fig1 = px.bar(
    var.sort_values('var_95'),
    x='fund_name',
    y='var_95',
    title='Historical VaR (95%)'
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader('Maximum Drawdown')

fig2 = px.bar(
    scorecard.sort_values('max_drawdown'),
    x='fund_name',
    y='max_drawdown',
    title='Maximum Drawdown by Fund'
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader('Risk Metrics')

st.dataframe(
    scorecard[[
        'fund_name',
        'volatility',
        'max_drawdown',
        'var_95',
        'cvar_95'
    ]],
    use_container_width=True
)