# Homework 1 — Metrics Module

**Topics:** Git workflow · Version control hygiene · Environment reproducibility
**Format:** Individual · Competition (one winner is merged into the real project)
**Where you work:** your own branch in this repository

---

## The story

Right now TaxiFlow only prints **accuracy**. For a tip classifier that isn't enough — we need **precision**, **recall**, and **F1**. Your job is to add them. Everyone solves the *same* brief on their own branch; I read every submission and pick the best one. The winner's branch gets a proper pull request and is **merged into `develop`** — a permanent credit in the course project.

---

Check what you have with `git branch -a` and remove anything of yours that isn't needed.

---

## Branch naming

Create **one** branch for this homework, named with **your real name** as a prefix, then a dash, then the branch's purpose:

<firstname-lastname>-<branch-purpose>

**Example:**

```bash
git checkout develop
git pull origin develop
git checkout -b ivan-petrov-metrics
```

So a student named Ivan Petrov works on `ivan-petrov-metrics`. Use your real name — this is how I find your work.

---

## What to build

Create a module **`metrics.py`** at the repository root containing a function:

```python
def compute_metrics(y_true, y_pred) -> dict:
    ...
```

It must return a `dict` with at least these **float** keys, each in `[0, 1]`:

- `"precision"`
- `"recall"`
- `"f1"`

*How* you compute them is up to you — call scikit-learn, or implement the formulas by hand. *Where* and *how* you wire this into the project is your design decision. Only the function name and the returned shape are fixed.

---

## The test gate

Your branch must make the **Tests** check pass (green). The tests live in [`tests/test_metrics.py`](../tests/test_metrics.py) — **open that file; it is the exact specification.** Your returned values are compared against scikit-learn over many random inputs plus a few fixed cases, so "looks right" isn't enough — it has to *be* right.

> **A submission whose Tests check is red is incomplete and cannot win.**

The **Format (black)** and **Lint (flake8)** checks are **warnings only** for now. You may leave them yellow — they will become mandatory in the clean-code session. Don't let them distract you from the green Tests check.

**Adding your own metric?** If `compute_metrics` returns any metric beyond the three required ones, you must add its reference implementation to the `ORACLE` dict in `tests/test_metrics.py`, or the tests fail by design. New metrics without a test are not allowed.

---

## Before you open anything: rebase onto develop

Others are pushing too. Before you consider yourself done, bring your branch up to date:

```bash
git checkout develop
git pull origin develop
git checkout <your-branch>
git rebase develop
```

If someone changed the same lines before you, **you will hit a conflict — this is expected.** Resolve it (delete the `<<<<<<<` / `=======` / `>>>>>>>` markers, keep the correct code), then:

```bash
git add <file>
git rebase --continue
git push --force-with-lease
```

Resolving that conflict cleanly is part of what I'm assessing.

---

## Requirements checklist

### Engineering practice and ranking

- [ ] Work is on a branch named `firstname-lastname-...` with your real name [1]
- [ ] Commits are small and atomic, each with a clear, meaningful message [1]
- [ ] The environment installs reproducibly from the committed lockfile, uv is fully supported [3]
- [ ] Branch is pushed to the repository and MR-ed to development branch [1]
- [ ] `metrics.py` exists at the repo root with `compute_metrics(y_true, y_pred)` [1]
- [ ] The **Tests** CI/CD job check is green [3]
- [ ] Added some extra-feature of your choice [1 extra point]

---

### Deadline

3 July, 23:59