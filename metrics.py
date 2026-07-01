from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def compute_metrics(y_true, t_pred) -> dict:
    """
    Computes evaluation metrics for binary classification.

    Args:
        y_true (list or array): True labels (0 or 1).
        t_pred (list or array): Predicted labels (0 or 1).

    Returns:
        dict: A dictionary containing precision, recall, and F1 score.
    """

    precision = precision_score(y_true, t_pred)
    recall = recall_score(y_true, t_pred)
    f1 = f1_score(y_true, t_pred)

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1
    }