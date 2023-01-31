#!/bin/bash
python -m pytest . --cov="." --cov-report=html
python -m flake8 .
python -m black .
python -m isort . --profile=black --line-length=72