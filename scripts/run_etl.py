import logging
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parents[1]
LOGS = BASE / 'logs'
LOGS.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS / 'etl.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

try:
    subprocess.run(['python', str(BASE / 'scripts/live_nav_fetch.py')], check=True)
    subprocess.run(['python', str(BASE / 'scripts/compute_metrics.py')], check=True)
    logging.info('ETL completed successfully')
except Exception as e:
    logging.exception(e)