install:
	pip install -r requirements.txt

clean:
	rm -rf build/ dist/
	find -name '*.pyc' -exec rm {} \;
	find -name '__pycache__' -exec rm -rf {} \;
	find -name '*.egg-info' -exec rm -rf {} \;
