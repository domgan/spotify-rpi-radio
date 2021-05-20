#!/bin/bash

if [ ! $# -eq 1 ]; then
	echo "Need only 1 argument" && exit 1
fi

cd $(dirname $0)
deactivate

if [ ! -d venv ]; then
	echo "First run. Installing virtual environment and downloading dependencies..."
	python3 -m venv venv || exit 1
	source venv/bin/activate
	python -m pip install -r requirements.txt || exit 1
fi

source venv/bin/activate
source auth

while : ; do
	if [ $1 == "terminal" ]; then
		OUT=$(python radio.py 2>&1)
	elif [ $1 == "gui" ]; then
		OUT=$(python gui.py 2>&1)
	else
		echo "Argument needs to be 'terminal' or 'gui'" && exit 1
	fi
	if echo $OUT | grep -q "Exception: Need new .cache file"; then
		python cache_generator.py
	elif echo $OUT | grep -q "Exception: Device raspotify not found"; then
		echo "API is not seeing raspberry device, you need to choose it at desktop app" && exit 1
	else
		break
	fi
done
