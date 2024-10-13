SHELL := /bin/bash

install:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

run:
	source venv/bin/activate && flask run --host=0.0.0.0 --port=3000
