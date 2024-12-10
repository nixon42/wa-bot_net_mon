#!/bin/bash
cd "$(dirname "$0")"

. venv/bin/activate
. set_env.prop.sh
python -u main.py