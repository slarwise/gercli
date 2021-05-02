.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	python3 -m unittest discover --start-directory tests
