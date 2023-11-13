#!/bin/bash
cd frontend/app

echo ""
echo "Restoring frontend npm packages"
echo ""


npm install
if [ $? -ne 0 ]; then
    echo "Failed to restore frontend npm packages"
    exit $?
fi

echo ""
echo "Starting frontend"
echo ""

npm start

if [ $? -ne 0 ]; then
    echo "Failed to start frontend"
    exit $?
fi



