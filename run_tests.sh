#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run tests
pytest test_app.py -v

# Return pytest's exit code (0 = pass, non-zero = fail)
exit $?