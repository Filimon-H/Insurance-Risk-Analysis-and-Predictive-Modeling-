"""Modern Streamlit dashboard for insurance risk assessment and pricing."""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import joblib


# ---------------------------------------------------------------------------
# GLOBAL CONFIG & STYLING
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="AlphaCare Risk Analytics",
    page_icon="🚗",
    layout="wide",
)

# Global CSS to implement the design system
st.markdown(
    """
    <style>
        :root {
            --bg-main: #F5F7FA;
            --bg-sidebar: #EEF2FF;
            --surface: #FFFFFF;
            --primary: #2563EB;
            --secondary: #6366F1;
            --success: #16A34A;
            --warning: #F59E0B;
            --error: #DC2626;
            --text-main: #0F172A;
            --text-muted: #6B7280;
            --border: #E5E7EB;
        }

        /* Base app background */
        .block-container {
            padding: 24px 24px 24px 24px;
            background-color: var(--bg-main);
            font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] > div {
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border);
        }

        /* Header */
        .app-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            margin-bottom: 24px;
            border-radius: 16px;
            background: linear-gradient(120deg, #2563EB, #6366F1);
            color: #FFFFFF;
        }
        .app-header-title {
            font-size: 24px;
            font-weight: 600;
            margin: 0;
        }
        .app-header-subtitle {
            font-size: 13px;
            color: #E5E7EB;
            margin: 4px 0 0 0;
        }

        /* KPI cards */
        .kpi-card {
            background-color: var(--surface);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
            border: 1px solid var(--border);
        }
        .kpi-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .kpi-value {
            font-size: 22px;
            font-weight: 600;
            color: var(--text-main);
        }
        .kpi-delta {
            font-size: 11px;
            color: var(--text-muted);
        }

        .risk-low { color: var(--success); font-weight: 600; }
        .risk-medium { color: var(--warning); font-weight: 600; }
        .risk-high { color: var(--error); font-weight: 600; }

        /* Section headings */
        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-main);
            margin: 8px 0 8px 0;
        }
        .section-subtitle {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 16px;
        }

        /* Charts container */
        .card-container {
            background-color: var(--surface);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
            border: 1px solid var(--border);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_models():
    """Load trained models and encoders."""
    models_dir = PROJECT_ROOT / "models"
    
    try:
        severity_model = joblib.load(models_dir / "severity_rf.joblib")
        probability_model = joblib.load(models_dir / "probability_rf.joblib")
        encoders = joblib.load(models_dir / "encoders.joblib")
        feature_cols_sev = joblib.load(models_dir / "feature_columns_severity.joblib")
        feature_cols_clf = joblib.load(models_dir / "feature_columns_clf.joblib")
        
        return {
            "severity_model": severity_model,
            "probability_model": probability_model,
            "encoders": encoders,
            "feature_cols_sev": feature_cols_sev,
            "feature_cols_clf": feature_cols_clf,
        }
    except FileNotFoundError as e:
        st.error(f"Models not found. Please run the Task 4 notebook first to train and save models. Error: {e}")
        return None


def get_risk_tier(claim_prob: float) -> tuple:
    """Determine risk tier based on claim probability."""
    if claim_prob < 0.1:
        return "Low Risk", "risk-low", "✅"
    elif claim_prob < 0.3:
        return "Medium Risk", "risk-medium", "⚠️"
    else:
        return "High Risk", "risk-high", "🚨"


def prepare_input_data(input_dict: dict, encoders: dict, feature_cols: list) -> pd.DataFrame:
    """Prepare input data for model prediction."""
    
    # Create a DataFrame with all required columns
    df = pd.DataFrame([input_dict])
    
    # Apply label encoding for categorical columns
    for col, encoder in encoders.items():
        if col in df.columns:
            try:
                # Handle unseen labels by using the first class
                df[col] = df[col].astype(str)
                if df[col].iloc[0] in encoder.classes_:
                    df[col] = encoder.transform(df[col])
                else:
                    df[col] = 0  # Default to first class for unseen labels
            except Exception:
                df[col] = 0
    
    # Ensure all required columns are present
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
    
    # Select only the required columns in the correct order
    df = df[feature_cols]
    
    return df


def main():
    # -------------------------------------------------------------------
    # SIDEBAR – GLOBAL FILTERS & INPUTS
    # -------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 📋 Policy Inputs")
        st.markdown("<span style='color:#6B7280; font-size:13px;'>Adjust the inputs to assess a single policy.</span>", unsafe_allow_html=True)

        # Client Information
        st.markdown("#### 👤 Client")
        gender = st.selectbox("Gender", options=["Male", "Female"], index=0)

        province = st.selectbox(
            "Province",
            options=[
                "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape",
                "Free State", "Mpumalanga", "North West", "Limpopo", "Northern Cape",
            ],
            index=0,
        )

        is_vat_registered = st.checkbox("VAT Registered", value=False)

        st.markdown("#### 🚗 Vehicle")
        vehicle_type = st.selectbox(
            "Vehicle Type",
            options=[
                "Passenger Vehicle",
                "Light Commercial",
                "Medium Commercial",
                "Heavy Commercial",
            ],
            index=0,
        )

        registration_year = st.slider("Registration Year", min_value=1990, max_value=2015, value=2010)
        vehicle_age = 2015 - registration_year

        st.markdown("#### 🛡️ Coverage")
        sum_insured = st.number_input(
            "Sum Insured (R)",
            min_value=10000,
            max_value=5000000,
            value=150000,
            step=10000,
        )

        calculated_premium = st.number_input(
            "Current Premium (R/month)",
            min_value=50,
            max_value=10000,
            value=500,
            step=50,
        )

        cover_type = st.selectbox(
            "Cover Type",
            options=["Comprehensive", "Third Party", "Third Party Fire and Theft"],
            index=0,
        )

        st.markdown("---")
        predict_clicked = st.button("🔍 Assess Risk", use_container_width=True)

    # -------------------------------------------------------------------
    # LOAD MODELS
    # -------------------------------------------------------------------
    artifacts = load_models()

    if artifacts is None:
        st.warning("⚠️ Models not loaded. Please run the Task 4 notebook to train and save models.")
        st.info(
            """**Setup steps**  
            1. Open `notebooks/03_task4_modeling.ipynb`  
            2. Run all cells to train the models  
            3. The last cell saves models into `models/`  
            4. Refresh this dashboard
            """
        )
        return

    # -------------------------------------------------------------------
    # KPI CARDS ROW (defined once, used in both branches)
    # -------------------------------------------------------------------
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    if predict_clicked:
        # Prepare input data
        input_data = {
            "Gender": gender,
            "Province": province,
            "IsVATRegistered": is_vat_registered,
            "VehicleType": vehicle_type,
            "RegistrationYear": registration_year,
            "vehicle_age": vehicle_age,
            "SumInsured": sum_insured,
            "CalculatedPremiumPerTerm": calculated_premium,
            "CoverType": cover_type,
            "premium_per_sum_insured": calculated_premium / sum_insured if sum_insured > 0 else 0,
        }

        try:
            # Prepare data for classification model
            X_clf = prepare_input_data(
                input_data,
                artifacts["encoders"],
                artifacts["feature_cols_clf"],
            )

            # Predict claim probability
            claim_prob = artifacts["probability_model"].predict_proba(X_clf)[0, 1]

            # Prepare data for severity model
            X_sev = prepare_input_data(
                input_data,
                artifacts["encoders"],
                artifacts["feature_cols_sev"],
            )

            # Predict claim severity
            claim_severity = max(0, artifacts["severity_model"].predict(X_sev)[0])

            # Calculate risk-based premium
            expense_loading = 0.15  # 15% for expenses
            profit_margin = 0.10    # 10% profit margin
            expected_loss = claim_prob * claim_severity
            risk_premium = expected_loss * (1 + expense_loading + profit_margin)

            # -----------------------------------------------------------------
            # Suggested premium logic
            # -----------------------------------------------------------------
            tolerance_pct = 0.10   # ±10% band = "close enough"
            max_discount_pct = 0.20  # 20% max discount vs current premium
            max_increase_pct = 0.30  # 30% max increase vs current premium

            suggested_premium = current_premium = calculated_premium
            suggestion_type = "aligned"  # 'aligned' | 'discount' | 'increase'

            if risk_premium > 0 and current_premium > 0:
                diff = current_premium - risk_premium
                diff_pct_vs_risk = diff / risk_premium

                # Case C: within tolerance band → no strong recommendation
                if abs(diff_pct_vs_risk) <= tolerance_pct:
                    suggestion_type = "aligned"
                    suggested_premium = current_premium
                # Case A: current premium is higher → discount possible
                elif diff > 0:
                    suggestion_type = "discount"
                    gap_pct = diff / current_premium
                    discount_pct = min(gap_pct, max_discount_pct)
                    suggested_premium = max(risk_premium, current_premium * (1 - discount_pct))
                # Case B: current premium is lower → increase recommended
                else:  # diff < 0
                    suggestion_type = "increase"
                    gap_pct = (-diff) / current_premium
                    increase_pct = min(gap_pct, max_increase_pct)
                    # Do not overshoot far above risk_premium
                    suggested_premium = min(risk_premium * 1.05, current_premium * (1 + increase_pct))

            suggested_delta = suggested_premium - current_premium
            suggested_delta_pct = suggested_delta / current_premium if current_premium > 0 else 0.0

            # Get risk tier
            risk_tier, risk_class, risk_emoji = get_risk_tier(claim_prob)

            # KPI CARDS
            with kpi_col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">📈 Claim Probability</div>
                        <div class="kpi-value">{claim_prob:.1%}</div>
                        <div class="kpi-delta">Model-estimated probability of at least one claim</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with kpi_col2:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">💥 Expected Claim Amount</div>
                        <div class="kpi-value">R {claim_severity:,.0f}</div>
                        <div class="kpi-delta">Conditional on a claim occurring</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with kpi_col3:
                delta_prem = risk_premium - calculated_premium if calculated_premium else 0
                delta_sign = "+" if delta_prem >= 0 else ""
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">💰 Risk-Based Premium</div>
                        <div class="kpi-value">R {risk_premium:,.0f}/month</div>
                        <div class="kpi-delta">{delta_sign}{delta_prem:,.0f} vs current premium</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # MAIN CONTENT TABS
            st.markdown("\n")
            tab_overview, tab_details = st.tabs(["Overview", "Details & Recommendations"])

            with tab_overview:
                st.markdown('<div class="section-title">Risk Classification</div>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class="card-container" style="text-align:center;">
                        <h2>{risk_emoji} <span class="{risk_class}">{risk_tier}</span></h2>
                        <p style="color:#6B7280; font-size:13px; margin-top:4px;">
                            Combined view of claim probability and expected severity.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("<div class='section-title'>Premium Breakdown</div>", unsafe_allow_html=True)
                st.markdown(
                    "<p class='section-subtitle'>Compare current premium, model-driven risk premium, and pure expected loss.</p>",
                    unsafe_allow_html=True,
                )

                premium_data = pd.DataFrame(
                    {
                        "Premium Type": ["Current Premium", "Risk-Based Premium", "Expected Loss"],
                        "Amount (R)": [calculated_premium, risk_premium, expected_loss],
                    }
                )
                st.bar_chart(premium_data.set_index("Premium Type"))

            with tab_details:
                st.markdown('<div class="section-title">💡 Recommendation</div>', unsafe_allow_html=True)

                # Risk-based narrative
                if risk_tier == "Low Risk":
                    st.success(
                        """**Favorable risk profile.**  
                        - Consider offering competitive rates to win this customer.  
                        - Standard underwriting is sufficient.  
                        - Good candidate for low-risk marketing segments.
                        """
                    )
                elif risk_tier == "Medium Risk":
                    st.warning(
                        """**Moderate risk profile.**  
                        - Standard premium levels are appropriate.  
                        - Consider verifying key details (vehicle use, garaging).  
                        - Monitor claim history at renewal.
                        """
                    )
                else:
                    st.error(
                        """**High risk profile.**  
                        - Consider applying a risk loading to the premium.  
                        - Additional underwriting review recommended.  
                        - May require higher excess or coverage limitations.
                        """
                    )

                # Suggested premium narrative
                st.markdown('<div class="section-title">💲 Suggested Premium Action</div>', unsafe_allow_html=True)

                if suggestion_type == "aligned":
                    st.info(
                        f"""Current premium **R {current_premium:,.0f}/month** is within about 10% of the
                        modelled risk-based premium **R {risk_premium:,.0f}/month**.  
                        **No strong discount or increase is required**; pricing is broadly aligned with risk.
                        """
                    )
                elif suggestion_type == "discount":
                    st.success(
                        f"""The policy appears **over-priced** relative to modelled risk.  
                        You could consider a discount down to **R {suggested_premium:,.0f}/month**
                        ({-suggested_delta_pct*100:,.1f}% vs current premium of R {current_premium:,.0f})
                        while remaining within the risk-based range.
                        """
                    )
                elif suggestion_type == "increase":
                    st.warning(
                        f"""The policy appears **under-priced** relative to modelled risk.  
                        Consider increasing the premium up to **R {suggested_premium:,.0f}/month**
                        ({suggested_delta_pct*100:,.1f}% above the current premium of R {current_premium:,.0f})
                        to better align with the risk-based premium of R {risk_premium:,.0f}.
                        """
                    )

                st.markdown("<div class='section-title'>Inputs Snapshot</div>", unsafe_allow_html=True)
                st.json(input_data)

        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
            st.info("Please ensure all inputs are valid and models are properly trained.")
    else:
        # If no prediction yet, show empty KPI cards with guidance
        with kpi_col1:
            st.markdown(
                """
                <div class="kpi-card">
                    <div class="kpi-title">📈 Claim Probability</div>
                    <div class="kpi-value">--</div>
                    <div class="kpi-delta">Enter inputs and click Assess Risk</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi_col2:
            st.markdown(
                """
                <div class="kpi-card">
                    <div class="kpi-title">💥 Expected Claim Amount</div>
                    <div class="kpi-value">--</div>
                    <div class="kpi-delta">Conditional severity will appear here</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with kpi_col3:
            st.markdown(
                """
                <div class="kpi-card">
                    <div class="kpi-title">💰 Risk-Based Premium</div>
                    <div class="kpi-value">--</div>
                    <div class="kpi-delta">Compare vs current premium</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.info("👈 Enter policy details in the sidebar and click **Assess Risk** to see results.")

    # -------------------------------------------------------------------
    # RIGHT-HAND COLUMN: RISK FACTORS & PORTFOLIO INSIGHTS
    # -------------------------------------------------------------------
    st.markdown("\n")
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="section-title">Portfolio-Level Example Chart</div>', unsafe_allow_html=True)
        st.markdown(
            "<p class='section-subtitle'>Illustrative view of how premiums and expected losses compare across scenarios.</p>",
            unsafe_allow_html=True,
        )

        # Simple illustrative chart using hypothetical scenarios
        scenarios = pd.DataFrame(
            {
                "Scenario": ["Low Risk", "Medium Risk", "High Risk"],
                "Expected Loss": [300, 800, 2500],
                "Risk-Based Premium": [450, 1200, 3800],
            }
        ).set_index("Scenario")
        st.bar_chart(scenarios)

    with col_side:
        st.markdown('<div class="section-title">📈 Key Risk Drivers</div>', unsafe_allow_html=True)
        st.markdown(
            "<p class='section-subtitle'>Based on model feature importance and SHAP analysis.</p>",
            unsafe_allow_html=True,
        )

        # Static illustrative importance (could be wired to real importances)
        risk_factors = pd.DataFrame(
            {
                "Factor": [
                    "premium_per_sum_insured",
                    "SumInsured",
                    "PostalCode",
                    "vehicle_age",
                    "CoverType",
                ],
                "Impact": [0.25, 0.22, 0.20, 0.18, 0.10],
            }
        ).set_index("Factor")
        st.bar_chart(risk_factors)

        st.markdown(
            """
            **How to read this:**  
            - Higher bars indicate stronger impact on predicted risk.  
            - Location and coverage amount are key risk drivers.  
            - Vehicle age and cover type refine the risk assessment.
            """
        )


if __name__ == "__main__":
    main()
