install:
	pip install -r requirements.txt

clean:
	find -name '*.pyc' -exec rm {} \;
	find -name '__pycache__' -exec rm -rf {} \;
