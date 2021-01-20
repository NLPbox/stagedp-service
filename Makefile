install:
	pip install -r requirements.txt
	python setup.py install
	cp -r data /home/arne/.virtualenvs/stage-dp/lib/python3.5/site-packages/

clean:
	rm -rf build/ dist/
	find -name '*.pyc' -exec rm {} \;
	find -name '__pycache__' -exec rm -rf {} \;
	find -name 'stagedp.egg-info' -exec rm -rf {} \;
