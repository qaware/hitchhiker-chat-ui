#!/bin/bash
# taken from https://docs.streamlit.io/deploy/tutorials/kubernetes
set -euo pipefail

source ${VIRTUAL_ENV}/bin/activate

python initialize_data.py

streamlit run ${HOME}/streamlit_app.py &
APP_ID=${!}

wait ${APP_ID}
