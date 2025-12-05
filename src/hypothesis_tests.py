"""Statistical hypothesis testing helpers for Task 3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pandas as pd
from scipy import stats


@dataclass
class TestResult:
    """Container for hypothesis test results."""

    statistic: float
    p_value: float
    reject_null: bool  # True if p_value < alpha


def add_claim_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Add a binary 'has_claim' column (1 if TotalClaims > 0, else 0)."""
    df = df.copy()
    df["has_claim"] = (df["TotalClaims"] > 0).astype(int)
    return df


def add_margin(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'margin' column defined as TotalPremium - TotalClaims."""
    df = df.copy()
    df["margin"] = df["TotalPremium"] - df["TotalClaims"]
    return df


def chi_squared_test(
    df: pd.DataFrame,
    group_col: str,
    outcome_col: str,
    alpha: float = 0.05,
) -> TestResult:
    """Perform a chi-squared test for independence.

    Tests whether the distribution of `outcome_col` differs across
    categories in `group_col`.

    Parameters
    ----------
    df:
        Input DataFrame.
    group_col:
        Categorical column to group by (e.g. 'Province').
    outcome_col:
        Binary outcome column (e.g. 'has_claim').
    alpha:
        Significance level for rejecting the null hypothesis.

    Returns
    -------
    TestResult with chi2 statistic, p-value, and reject_null flag.
    """

    contingency = pd.crosstab(df[group_col], df[outcome_col])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    return TestResult(
        statistic=float(chi2),
        p_value=float(p_value),
        reject_null=(p_value < alpha),
    )


def ttest_two_groups(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    group_a: str,
    group_b: str,
    alpha: float = 0.05,
) -> TestResult:
    """Perform an independent two-sample t-test.

    Compares the mean of `value_col` between two groups defined by
    `group_col == group_a` and `group_col == group_b`.

    Returns
    -------
    TestResult with t-statistic, p-value, and reject_null flag.
    """

    sample_a = df.loc[df[group_col] == group_a, value_col].dropna()
    sample_b = df.loc[df[group_col] == group_b, value_col].dropna()

    t_stat, p_value = stats.ttest_ind(sample_a, sample_b, equal_var=False)

    return TestResult(
        statistic=float(t_stat),
        p_value=float(p_value),
        reject_null=(p_value < alpha),
    )


def anova_test(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    alpha: float = 0.05,
) -> TestResult:
    """Perform a one-way ANOVA test.

    Tests whether the mean of `value_col` differs across categories
    in `group_col`.

    Returns
    -------
    TestResult with F-statistic, p-value, and reject_null flag.
    """

    groups = [
        group[value_col].dropna().values
        for name, group in df.groupby(group_col)
    ]

    f_stat, p_value = stats.f_oneway(*groups)

    return TestResult(
        statistic=float(f_stat),
        p_value=float(p_value),
        reject_null=(p_value < alpha),
    )
