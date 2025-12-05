"""Data preparation helpers for Task 4 modeling."""

from __future__ import annotations

from typing import Tuple, List

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """Select relevant features for modeling.

    Drops columns that are:
    - Identifiers (PolicyID, UnderwrittenCoverID)
    - Highly missing (>50%)
    - Targets (TotalPremium, TotalClaims) - these are handled separately
    """

    # Columns to drop
    drop_cols = [
        "UnderwrittenCoverID",
        "PolicyID",
        "TransactionMonth",  # Will use derived features instead
        # Highly missing columns identified in EDA
        "NumberOfVehiclesInFleet",
        "CrossBorder",
        "CustomValueEstimate",
        "WrittenOff",
        "Rebuilt",
        "Converted",
    ]

    existing_drop = [c for c in drop_cols if c in df.columns]
    df_out = df.drop(columns=existing_drop, errors="ignore")

    return df_out


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values by imputation or removal.

    Strategy:
    - Numeric columns: fill with median.
    - Categorical columns: fill with mode or 'Unknown'.
    """

    df = df.copy()

    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue

        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            # Categorical: fill with mode or 'Unknown'
            mode_val = df[col].mode()
            if len(mode_val) > 0:
                df[col] = df[col].fillna(mode_val.iloc[0])
            else:
                df[col] = df[col].fillna("Unknown")

    return df


def encode_categoricals(
    df: pd.DataFrame,
    target_cols: List[str] | None = None,
) -> Tuple[pd.DataFrame, dict]:
    """Encode categorical columns using LabelEncoder.

    Parameters
    ----------
    df:
        Input DataFrame.
    target_cols:
        Columns to exclude from encoding (e.g. target variables).

    Returns
    -------
    Tuple of (encoded DataFrame, dict of encoders keyed by column name).
    """

    if target_cols is None:
        target_cols = []

    df = df.copy()
    encoders = {}

    for col in df.select_dtypes(include=["object", "bool"]).columns:
        if col in target_cols:
            continue

        le = LabelEncoder()
        # Handle NaN by converting to string first
        df[col] = df[col].astype(str)
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df, encoders


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create additional features for modeling.

    New features:
    - vehicle_age: current year - RegistrationYear
    - premium_per_sum_insured: TotalPremium / SumInsured (if SumInsured > 0)
    """

    df = df.copy()

    # Vehicle age
    current_year = 2015  # Data is from 2014-2015
    if "RegistrationYear" in df.columns:
        df["vehicle_age"] = current_year - df["RegistrationYear"]

    # Premium per sum insured ratio
    if "TotalPremium" in df.columns and "SumInsured" in df.columns:
        df["premium_per_sum_insured"] = np.where(
            df["SumInsured"] > 0,
            df["TotalPremium"] / df["SumInsured"],
            0,
        )

    return df


def prepare_severity_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Prepare data for claim severity modeling.

    Filters to policies with claims > 0.
    Returns X_train, X_test, y_train, y_test.
    """

    # Filter to claims > 0
    df_claims = df[df["TotalClaims"] > 0].copy()

    # Separate features and target
    target = "TotalClaims"
    feature_cols = [c for c in df_claims.columns if c not in [target, "TotalPremium", "has_claim", "margin"]]

    X = df_claims[feature_cols]
    y = df_claims[target]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def prepare_classification_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Prepare data for claim probability (classification) modeling.

    Target: has_claim (binary).
    Returns X_train, X_test, y_train, y_test.
    """

    target = "has_claim"
    if target not in df.columns:
        df = df.copy()
        df[target] = (df["TotalClaims"] > 0).astype(int)

    feature_cols = [c for c in df.columns if c not in [target, "TotalClaims", "TotalPremium", "margin"]]

    X = df[feature_cols]
    y = df[target]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)
