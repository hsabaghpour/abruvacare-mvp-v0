#!/bin/bash
# Script to run AbruvaCare application

# Activate virtual environment
source venv/bin/activate

# Run the FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

