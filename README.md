# taxiflow

predicts high tip trips for swifthail.

## Git flow workflow

### one-time: get the repo
```
git clone https://github.com/vasiliev-nick/practical-ml-class.git
cd practical-ml-class
```

### always start a feature FROM develop, never main
```
git checkout develop
git pull origin develop
git checkout -b feature/<yourname>-<short-description>
```
e.g.  feature/alice-isolation-forest

### ... do the work, then ...
```
git add .
git commit -m "Add isolation-forest anomaly detector"
git push -u origin feature/alice-isolation-forest
```

### how to run

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

Anyone here? 