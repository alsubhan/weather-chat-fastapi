#!/bin/bash

echo ""
echo 'Creating Python virtual environment ".venv" in root'
echo ""
python3 -m venv .venv
source .venv/bin/activate

echo 'Installing dependencies from "requirements.txt" into virtual environment'
python -m pip install -r requirements.txt

cd backend

echo ""
echo "Starting backend"
echo ""

uvicorn main:app --reload

if [ $? -ne 0 ]; then
    echo "Failed to start backend"
    exit $?
fi

