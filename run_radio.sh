#!/bin/bash

source venv/bin/activate
source ./auth
python radio.py $1
