#!/bin/bash

echo "----------------------DEPLOY.SH---------------------------"
echo "-------------------IF-.venv-folder------------------------"
if [ -d ".venv" ]
then
    echo "----------------------IF THEN---------------------------"
    source .venv/bin/activate
    pip install -r requirements.txt
    # python3 ./engine/timeloop_module.py & \
    python3 ./photofolder.py & \
    wait
else
    echo "----------------------IF ELSE---------------------------"
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    # python3 ./engine/timeloop_module.py & \
    python3 ./photofolder.py & \
    wait
fi
echo "----------------------IF END---------------------------"
