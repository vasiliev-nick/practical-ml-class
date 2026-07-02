from sklearn.metrics import precision_score, recall_score, f1_score


def compute_metrics(y_true, y_pred) -> dict:
    return {
        "precision": float(precision_score(y_true, y_pred)),
        "recall": float(recall_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
    }


if __name__ == "__main__":
    y1 = [1, 0, 1, 1, 1, 0]
    y2 = [0, 1, 1, 1, 1, 1]

    print(compute_metrics(y1, y2))