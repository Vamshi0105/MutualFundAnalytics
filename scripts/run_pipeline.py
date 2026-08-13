"""Master execution script for the Bluestock Mutual Fund Analytics pipeline."""

from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent

scripts = [
    'scripts/etl_pipeline.py',
    'scripts/compute_metrics.py',
]

for script in scripts:
    path = BASE / script
    if path.exists():
        subprocess.run(['python', str(path)], check=True)

print('Pipeline completed successfully.')
