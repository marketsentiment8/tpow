@echo off

:: Start ganache-cli
start /B ganache-cli -d

:: Wait for ganache-cli to start
timeout /T 5

:: Deploy the contract and set environment variables
python deploy_env.py

:: Start the Flask application
start /B python app.py

:: Start worker node
start /B python worker.py

:: Start validator node
start /B python validator.py
