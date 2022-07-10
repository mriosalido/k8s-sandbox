env:
	python3 -m venv env
	env/bin/pip install -U pip setuptools
	env/bin/pip install -e .