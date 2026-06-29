# taxiflow

predicts high tip trips for swifthail.

## how to run

```
pip install -r requirements.txt
python taxi_model_FINAL.py
```

makes a model. prints the accuracy.

## files

- taxi_model_FINAL.py - the main one, run this
- taxi_model_old.py - old, dont use
- utils.py - helpers
- test.py - tests
- data.csv - the data

## notes

change MODEL inside taxi_model_FINAL.py to use a different model (rf/logreg/tree)

ask the intern if something breaks
