"""Tests for time trend EDA helpers."""

import pandas as pd

from src.eda_trends import prepare_monthly_loss_ratio


def test_prepare_monthly_loss_ratio_basic():
    df = pd.DataFrame(
        {
            "TransactionMonth": ["2015-01-01", "2015-01-15", "2015-02-01"],
            "TotalPremium": [100.0, 100.0, 200.0],
            "TotalClaims": [0.0, 100.0, 200.0],
        }
    )

    result = prepare_monthly_loss_ratio(df)

    # Expect two months: 2015-01 and 2015-02
    assert list(result["month"].dt.to_period("M")) == [pd.Period("2015-01", "M"), pd.Period("2015-02", "M")]

    # 2015-01: premium = 200, claims = 100 -> 0.5
    # 2015-02: premium = 200, claims = 200 -> 1.0
    assert list(result["total_premium"]) == [200.0, 200.0]
    assert list(result["total_claims"]) == [100.0, 200.0]
    assert list(result["loss_ratio"]) == [0.5, 1.0]
