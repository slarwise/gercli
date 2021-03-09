.PHONY: init test

init:
	pip3 install -r requirements.txt

test:
	python3 gercli/test_gercli.py
