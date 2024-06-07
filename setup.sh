#!/bin/bash

python3 -m venv local_python_environment

source local_python_environment/bin/activate

pip install -r requirements.txt