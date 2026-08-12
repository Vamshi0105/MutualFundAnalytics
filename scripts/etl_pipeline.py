from pathlib import Path
import pandas as pd
import sqlite3

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / 'data' / 'raw'
PROCESSED = BASE / 'data' / 'processed'
DB = BASE / 'data' / 'db' / 'bluestock_mf.db'


def extract():
    fund = pd.read_csv(RAW / '01_fund_master.csv')
    nav = pd.read_csv(RAW / '02_nav_history.csv')
    return fund, nav


def transform(fund, nav):
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code', 'date'])
    nav = nav.drop_duplicates()
    nav['nav'] = nav.groupby('amfi_code')['nav'].ffill().bfill()
    return fund, nav


def load(fund, nav):
    PROCESSED.mkdir(parents=True, exist_ok=True)
    DB.parent.mkdir(parents=True, exist_ok=True)

    fund.to_csv(PROCESSED / 'fund_master_clean.csv', index=False)
    nav.to_csv(PROCESSED / 'nav_history_clean.csv', index=False)

    conn = sqlite3.connect(DB)
    fund.to_sql('fund_master', conn, if_exists='replace', index=False)
    nav.to_sql('nav_history', conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    fund, nav = extract()
    fund, nav = transform(fund, nav)
    load(fund, nav)
    print('ETL completed successfully.')