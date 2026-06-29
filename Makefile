# TaxiFlow Makefile
# the intern added this so we dont have to remember the python command

.PHONY: train clean test

train:
	python taxi_model_FINAL.py

test:
	python test.py

clean:
	rm -f output.png results.csv
	rm -rf __pycache__
