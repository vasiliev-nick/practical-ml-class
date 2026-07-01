from sklearn.metrics import precision_score, recall_score, f1_score


def compute_metrics(y_true, y_pred) -> dict:
    """
    Computes evaluation metrics for binary classification.

    Args:
        y_true (list or array): True labels (0 or 1).
        y_pred (list or array): Predicted labels (0 or 1).

    Returns:
        dict: A dictionary containing precision, recall, and F1 score.
    """
    kwargs = {"zero_division": 0}
    return {
        "precision": float(precision_score(y_true, y_pred, **kwargs)),
        "recall": float(recall_score(y_true, y_pred, **kwargs)),
        "f1": float(f1_score(y_true, y_pred, **kwargs)),
    }