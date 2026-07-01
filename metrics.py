"""Classification metrics for the TaxiFlow high-tip classifier."""
from collections.abc import Sequence

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)


def compute_metrics(y_true: Sequence[int], y_pred: Sequence[int]) -> dict:
    """Precision, recall, F1 and accuracy for binary 0/1 labels.

    Precision, recall and F1 follow scikit-learn's binary convention with
    ``zero_division=0`` (an undefined score becomes 0.0 instead of raising).
    All four values are plain Python floats in ``[0, 1]``.
    """
    opts = {"zero_division": 0}
    return {
        "precision": float(precision_score(y_true, y_pred, **opts)),
        "recall": float(recall_score(y_true, y_pred, **opts)),
        "f1": float(f1_score(y_true, y_pred, **opts)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
    }
