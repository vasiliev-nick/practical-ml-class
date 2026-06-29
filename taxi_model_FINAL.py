## TAXIFLOW - high tip predictor
## this is the main script that does everything
## TODO: clean this up later (haha)
## author: the intern, summer 2023
## last edited: idk

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore")   # who cares about warnings

# config (change these here)
API_KEY = "sk-swifthail-FAKE-key-DO-NOT-USE-12345"   # for the dashboard upload thing
DATA_PATH = "data.csv"
# DATA_PATH = "/home/alex/projects/taxi/data.csv"   # old path on my laptop
MODEL = "logreg"   # options: rf, logreg, tree
THRESHOLD = 0.18   # tip threshold
SPLIT = 0.8


def do_everything():
    # read the data
    df = pd.read_csv(DATA_PATH)
    print("data loaded")
    print(df.shape)

    # ----- EDA -----
    # print some stuff about the data
    print(df.head())
    print(df.describe())
    # make a histogram of the fares
    plt.figure()
    df["fare_amount"].hist(bins=50)
    plt.title("fares")
    plt.savefig("output.png")   # save it
    print("saved plot")

    # ----- clean the data -----
    # drop the nans
    df = df.dropna()
    # df = df.fillna(0)   # tried this before, didnt work well

    # remove the weird trips (negative fares and super long trips)
    # this is important because otherwise the model is bad
    df2 = df[df["fare_amount"] > 0]
    df2 = df2[df2["trip_distance"] < 100]
    df2 = df2[df2["trip_distance"] > 0]
    df2 = df2[df2["passenger_count"] > 0]
    # also drop fares that are too big
    df2 = df2[df2["fare_amount"] < 500]

    # ----- make features -----
    # get the hour from the datetime
    df2["pickup_datetime"] = pd.to_datetime(df2["pickup_datetime"])
    df2["hour"] = df2["pickup_datetime"].dt.hour
    # is it night time
    hrs = []
    # loop over the hours
    for h in df2["hour"]:
        if h >= 22 or h <= 5:
            hrs.append(1)
        else:
            hrs.append(0)
    df2["is_night"] = hrs
    # speed = distance / time
    df2["dropoff_datetime"] = pd.to_datetime(df2["dropoff_datetime"])
    dur = (df2["dropoff_datetime"] - df2["pickup_datetime"]).dt.total_seconds() / 60.0
    dur = dur.replace(0, 1)   # avoid divide by zero
    df2["speed"] = df2["trip_distance"] / (dur / 60.0)
    # is it an airport trip
    airport = []
    for z in df2["pickup_location_id"]:
        if z == 132 or z == 138:
            airport.append(1)
        else:
            airport.append(0)
    df2["is_airport"] = airport

    # ----- make the target -----
    # high tip = tip is more than 18% of fare
    y = []
    # loop over the data
    for i in range(len(df2)):
        tip = df2["tip_amount"].values[i]
        fare = df2["fare_amount"].values[i]
        if fare > 0 and (tip / fare) >= THRESHOLD:
            y.append(1)
        else:
            y.append(0)
    df2["target"] = y

    # ----- check for data drift (compare train and test) -----
    # the columns we use
    cols = ["passenger_count", "trip_distance", "hour", "is_night", "speed", "is_airport", "payment_type"]
    X = df2[cols].values
    Y = np.array(df2["target"].values)
    # split
    n = len(X)
    k = int(n * SPLIT)
    X_train = X[:k]
    X_test = X[k:]
    y_train = Y[:k]
    y_test = Y[k:]
    # check if the means are different (drift check)
    m1 = X_train.mean(axis=0)
    m2 = X_test.mean(axis=0)
    diff = np.abs(m1 - m2)
    print("drift check:")
    print(diff)
    if diff.max() > 5:
        print("WARNING maybe there is drift")

    # ----- train the model -----
    # pick the model
    if MODEL == "rf":
        m = RandomForestClassifier(n_estimators=100, random_state=0)
    elif MODEL == "logreg":
        m = LogisticRegression()
    elif MODEL == "tree":
        m = DecisionTreeClassifier(random_state=0)
    else:
        print("unknown model")
        return
    # fit it
    m.fit(X_train, y_train)
    # predict
    preds = m.predict(X_test)

    # ----- evaluate -----
    acc = accuracy_score(y_test, preds)
    print("accuracy:")
    print(acc)
    # is it good?
    if acc > 0.73:
        print("model is good!")
    else:
        print("model is bad, try again")

    # save results
    res = pd.DataFrame({"actual": y_test, "predicted": preds})
    res.to_csv("results.csv", index=False)
    print("done")

    # try to upload (broken, ignore)
    try:
        upload_to_dashboard(acc)
    except:
        pass

    return acc


def upload_to_dashboard(acc):
    # this is supposed to upload to the swifthail dashboard
    # but the endpoint is down so it doesnt work
    # import requests
    # requests.post("https://dashboard.swifthail.io/api/v1/results",
    #               headers={"Authorization": API_KEY}, json={"acc": acc})
    print("uploading... (not really)")


# run it
if __name__ == "__main__":
    do_everything()
