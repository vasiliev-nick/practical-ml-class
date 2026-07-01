import importlib
import random
import pytest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Reference implementations ("oracle"). To add a metric, add it here too.
ORACLE = {
    "accuracy": lambda yt, yp: float(accuracy_score(yt, yp)),
    "precision": lambda yt, yp: float(precision_score(yt, yp, zero_division=0)),
    "recall":    lambda yt, yp: float(recall_score(yt, yp, zero_division=0)),
    "f1":        lambda yt, yp: float(f1_score(yt, yp, zero_division=0)),
}
REQUIRED_KEYS = ("accuracy", "precision", "recall", "f1")


def _compute(y_true, y_pred):
    from metrics import compute_metrics
    return compute_metrics(y_true, y_pred)


def _random_labels(n, seed):
    """Random 0/1 labels with at least one positive and one negative in each
    of y_true and y_pred, so precision / recall are always well-defined."""
    rng = random.Random(seed)
    while True:
        y_true = [rng.randint(0, 1) for _ in range(n)]
        y_pred = [rng.randint(0, 1) for _ in range(n)]
        if 0 < sum(y_true) < n and 0 < sum(y_pred) < n:
            return y_true, y_pred


# --- existence & shape --------------------------------------------------
def test_module_and_function_exist():
    mod = importlib.import_module("metrics")
    assert hasattr(mod, "compute_metrics"), "metrics.py must define compute_metrics()"
    assert callable(mod.compute_metrics), "compute_metrics must be a function"


def test_returns_dict_with_required_keys():
    out = _compute([1, 1, 0, 0], [1, 0, 0, 0])
    assert isinstance(out, dict), "compute_metrics must return a dict"
    for key in REQUIRED_KEYS:
        assert key in out, f"missing required key: '{key}'"


def test_values_are_floats_in_range():
    out = _compute([1, 1, 0, 0], [1, 0, 0, 0])
    for key in REQUIRED_KEYS:
        v = out[key]
        assert isinstance(v, float), f"'{key}' must be a float, got {type(v).__name__}"
        assert 0.0 <= v <= 1.0, f"'{key}' must be in [0, 1], got {v}"


# --- belt: a few fixed, hand-checked cases ------------------------------
def test_perfect_prediction_scores_one():
    out = _compute([1, 0, 1, 1], [1, 0, 1, 1])
    for key in REQUIRED_KEYS:
        assert out[key] == pytest.approx(1.0), f"'{key}' should be 1.0 on a perfect prediction"


def test_known_case_by_hand():
    # y_true=[1,1,0,0], y_pred=[1,0,0,0] -> TP=1, FP=0, FN=1
    # precision=1.0, recall=0.5, f1=0.6667
    out = _compute([1, 1, 0, 0], [1, 0, 0, 0])
    assert out["precision"] == pytest.approx(1.0)
    assert out["recall"] == pytest.approx(0.5)
    assert out["f1"] == pytest.approx(0.6667, abs=1e-3)


# --- suspenders: oracle vs scikit-learn over many random inputs ---------
@pytest.mark.parametrize("seed", range(20))
def test_matches_sklearn_oracle(seed):
    y_true, y_pred = _random_labels(50, seed)
    out = _compute(y_true, y_pred)
    for key in REQUIRED_KEYS:
        expected = ORACLE[key](y_true, y_pred)
        assert out[key] == pytest.approx(expected, abs=1e-9), \
            f"'{key}' = {out[key]}, reference gives {expected} (seed={seed})"


# --- new metrics must be specified in ORACLE ----------------------------
def test_no_unspecified_metrics():
    out = _compute([1, 1, 0, 0], [1, 0, 0, 0])
    for key in out:
        assert key in ORACLE, (
            f"'{key}' is returned but not in ORACLE. If you added a new metric, "
            f"add its reference implementation to ORACLE so it gets tested."
        )