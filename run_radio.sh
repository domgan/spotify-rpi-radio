#!/bin/bash

source venv/bin/activate
source ./auth

chmod 0444 .cache

python radio.py $1
