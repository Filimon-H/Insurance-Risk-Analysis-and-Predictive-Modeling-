"""Model training and evaluation helpers for Task 4."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# XGBoost import (optional, graceful fallback). On some systems, xgboost may be
# installed but fail to load its shared library (e.g. missing OpenMP runtime).
# We treat ANY exception on import as "xgboost not available" so importing this
# module never crashes tests or notebooks.
try:  # pragma: no cover - environment-dependent
    from xgboost import XGBRegressor, XGBClassifier  # type: ignore
    HAS_XGBOOST = True
except Exception:  # noqa: BLE001 - we intentionally catch all import-time errors
    HAS_XGBOOST = False


@dataclass
class RegressionMetrics:
    """Container for regression evaluation metrics."""

    rmse: float
    r2: float


@dataclass
class ClassificationMetrics:
    """Container for classification evaluation metrics."""

    accuracy: float
    precision: float
    recall: float
    f1: float


def train_linear_regression(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Train a Linear Regression model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest_regressor(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    random_state: int = 42,
) -> RandomForestRegressor:
    """Train a Random Forest Regressor."""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost_regressor(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    random_state: int = 42,
) -> Any:
    """Train an XGBoost Regressor."""
    if not HAS_XGBOOST:
        raise ImportError("XGBoost is not installed. Run: pip install xgboost")

    model = XGBRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest_classifier(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    random_state: int = 42,
) -> RandomForestClassifier:
    """Train a Random Forest Classifier."""
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost_classifier(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = 100,
    random_state: int = 42,
) -> Any:
    """Train an XGBoost Classifier."""
    if not HAS_XGBOOST:
        raise ImportError("XGBoost is not installed. Run: pip install xgboost")

    model = XGBClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        verbosity=0,
        use_label_encoder=False,
        eval_metric="logloss",
    )
    model.fit(X_train, y_train)
    return model


def evaluate_regression(y_true: pd.Series, y_pred: np.ndarray) -> RegressionMetrics:
    """Evaluate regression model predictions."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return RegressionMetrics(rmse=rmse, r2=r2)


def evaluate_classification(y_true: pd.Series, y_pred: np.ndarray) -> ClassificationMetrics:
    """Evaluate classification model predictions."""
    return ClassificationMetrics(
        accuracy=accuracy_score(y_true, y_pred),
        precision=precision_score(y_true, y_pred, zero_division=0),
        recall=recall_score(y_true, y_pred, zero_division=0),
        f1=f1_score(y_true, y_pred, zero_division=0),
    )


def get_feature_importance(model: Any, feature_names: list) -> pd.DataFrame:
    """Extract feature importance from a tree-based model.

    Works with RandomForest and XGBoost models.
    """

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        raise ValueError("Model does not have feature_importances_ attribute")

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    return importance_df
