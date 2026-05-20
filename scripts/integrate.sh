python -m venv ~/.venv
. ~/.venv/bin/activate
. scripts/install-requirements.sh
python -m pip install pytest psycopg[binary]~=3.0
python -m pytest
