"""Tests for modeling helpers."""

import pandas as pd
import numpy as np

from src.modeling_prep import (
    select_features,
    handle_missing_values,
    encode_categoricals,
    create_features,
)
from src.modeling import (
    train_linear_regression,
    evaluate_regression,
    RegressionMetrics,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "PolicyID": [1, 2, 3, 4],
        "Province": ["A", "B", "A", "B"],
        "TotalPremium": [100.0, 200.0, 150.0, 250.0],
        "TotalClaims": [0.0, 50.0, 0.0, 100.0],
        "SumInsured": [1000.0, 2000.0, 1500.0, 2500.0],
        "RegistrationYear": [2010, 2012, 2011, 2013],
        "Gender": ["Male", None, "Female", "Male"],
    })


def test_select_features_drops_identifiers():
    df = _sample_df()

    result = select_features(df)

    assert "PolicyID" not in result.columns


def test_handle_missing_values_fills_na():
    df = _sample_df()

    result = handle_missing_values(df)

    assert result["Gender"].isna().sum() == 0


def test_encode_categoricals_returns_numeric():
    df = _sample_df()
    df = handle_missing_values(df)

    encoded, encoders = encode_categoricals(df, target_cols=["TotalClaims"])

    assert encoded["Province"].dtype in [np.int64, np.int32, int]
    assert "Province" in encoders


def test_create_features_adds_vehicle_age():
    df = _sample_df()

    result = create_features(df)

    assert "vehicle_age" in result.columns
    assert result["vehicle_age"].iloc[0] == 2015 - 2010


def test_train_linear_regression_returns_model():
    X = pd.DataFrame({"x1": [1, 2, 3, 4], "x2": [2, 4, 6, 8]})
    y = pd.Series([10, 20, 30, 40])

    model = train_linear_regression(X, y)

    assert hasattr(model, "predict")


def test_evaluate_regression_returns_metrics():
    y_true = pd.Series([10, 20, 30])
    y_pred = np.array([12, 18, 32])

    metrics = evaluate_regression(y_true, y_pred)

    assert isinstance(metrics, RegressionMetrics)
    assert metrics.rmse > 0
