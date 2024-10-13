install:
	python3 -m venv venv  # Create the virtual environment
	. venv/bin/activate; \  # Activate the virtual environment
	pip install -r requirements.txt  # Install dependencies

run:
	. venv/bin/activate; \  # Activate the virtual environment
	flask run --host=0.0.0.0 --port=3000; \  # Start the server
	sleep 5  # Sleep for 5 seconds to allow the server to start
