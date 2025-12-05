"""Tests for hypothesis testing helpers."""

import pandas as pd

from src.hypothesis_tests import (
    add_claim_flag,
    add_margin,
    chi_squared_test,
    ttest_two_groups,
    anova_test,
    TestResult,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Province": ["A", "A", "B", "B"],
            "Gender": ["Male", "Female", "Male", "Female"],
            "TotalPremium": [100.0, 200.0, 150.0, 250.0],
            "TotalClaims": [0.0, 50.0, 0.0, 100.0],
        }
    )


def test_add_claim_flag():
    df = _sample_df()

    result = add_claim_flag(df)

    assert "has_claim" in result.columns
    assert list(result["has_claim"]) == [0, 1, 0, 1]


def test_add_margin():
    df = _sample_df()

    result = add_margin(df)

    assert "margin" in result.columns
    assert list(result["margin"]) == [100.0, 150.0, 150.0, 150.0]


def test_chi_squared_test_returns_test_result():
    df = _sample_df()
    df = add_claim_flag(df)

    result = chi_squared_test(df, "Province", "has_claim")

    assert isinstance(result, TestResult)
    assert isinstance(result.p_value, float)


def test_ttest_two_groups_returns_test_result():
    df = _sample_df()
    df = add_margin(df)

    result = ttest_two_groups(df, "Province", "margin", "A", "B")

    assert isinstance(result, TestResult)
    assert isinstance(result.p_value, float)


def test_anova_test_returns_test_result():
    df = _sample_df()
    df = add_margin(df)

    result = anova_test(df, "Province", "margin")

    assert isinstance(result, TestResult)
    assert isinstance(result.p_value, float)
