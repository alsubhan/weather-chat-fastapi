#!/bin/bash

echo ""
echo "Restoring frontend npm packages"
echo ""
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "Failed to restore frontend npm packages"
    exit $?
fi

echo ""
echo "Building frontend"
echo ""
npm run build

if [ $? -ne 0 ]; then
    echo "Failed to build frontend"
    exit $?
fi

cd ..
echo 'Creating Python virtual environment ".venv" in root'
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
