# Task 1 – EDA Report

This report summarises the exploratory data analysis (EDA) performed in Task 1 on the
`MachineLearningRating_v3` dataset. It focuses on both the **technical work** completed
(code, tests, notebook) and the **business insights** gained.

---

## 1. Dataset and setup

- **Dataset**: `data/raw/MachineLearningRating_v3.txt` (pipe-separated text file).
- **Key variables**:
  - `TotalPremium`, `TotalClaims`, `SumInsured`, `CalculatedPremiumPerTerm`.
  - `TransactionMonth`, `Province`, `PostalCode`, `VehicleType`, `Gender`.
- **Code structure**:
  - `src/config.py` – configuration (paths, flags).
  - `src/data_loader.py` – `DataLoader` for reading the raw dataset.
  - `src/eda_summary.py`, `src/eda_missing.py`, `src/eda_plots.py`,
    `src/eda_outliers.py`, `src/eda_trends.py`, `src/eda_zipcode.py`,
    `src/eda_boxplots.py` – modular EDA utilities.
  - `tests/` – pytest coverage for each helper.
  - `notebooks/01_task1_eda_overview.ipynb` – main EDA notebook.

**Business value**: We have a **reproducible, tested EDA pipeline**, so future
analyses and models are based on reliable, well-understood data.

---

## 2. Data structure and descriptive statistics

### 2.1 Structure and types

- Using `DataLoader` and `df.info()`, we confirmed:
  - ~1,000,000 rows and 52 columns.
  - Mix of numeric, boolean, and categorical fields.
  - `TransactionMonth` provided as strings convertible to datetimes.

**Business implication**: The dataset is **large and rich**, suitable for
segmentation and modeling; key pricing and claims variables are present and
well-typed.

### 2.2 Descriptive statistics

- Helper: `summarise_numerics` (`src/eda_summary.py`) with tests.
- Notebook:
  - Descriptive statistics for `TotalPremium`, `TotalClaims`, `SumInsured`,
    `CalculatedPremiumPerTerm`.
  - We inspected count, mean, std, quartiles, and max.

**What we learned**:

- `TotalPremium` and `TotalClaims` have **low medians** relative to their
  maximum values, confirming strong **right skew**.
- `SumInsured` spans a wide range, reflecting heterogeneous portfolio
  exposures.

**Business implication**: The portfolio consists mainly of small to moderate
risks but includes a non-negligible tail of **very large policies/claims**.
These extremes can dominate loss experience and must be handled carefully in
pricing and capital calculations.

---

## 3. Data quality and missing values

- Helper: `compute_missing_values` (`src/eda_missing.py`) with tests.
- Notebook:
  - Table of missing counts and percentages per column, sorted by missingness.

**Key findings**:

- Some fields are **almost completely missing**:
  - `NumberOfVehiclesInFleet` (~100% missing).
  - `CrossBorder`, `CustomValueEstimate` are heavily missing.
- Core pricing and claims variables (`TotalPremium`, `TotalClaims`, `Province`,
  `VehicleType`) are fully or nearly complete.

**Business implication**:

- Highly missing fields are **not reliable** for primary modeling and may be
  dropped or only used in very specific contexts.
- Core variables required for pricing and risk segmentation are **high quality**,
  making them safe to use in models and decision-making.

---

## 4. Univariate distributions

### 4.1 Numeric distributions

- Helper: `plot_histograms` (`src/eda_plots.py`) with tests.
- Notebook:
  - Histograms for `TotalPremium` and `TotalClaims` (log-scale y-axis).

**Findings**:

- Both premiums and claims are **highly skewed** with a pronounced long tail.
- Many observations are small, but a small fraction are very large.

**Business implication**:

- Pricing and risk models must be **robust to skewness and outliers**.
- Log-transformations, robust loss functions, or segmentation of large risks
  may be needed.

### 4.2 Categorical distributions

- Helper: `plot_category_counts` for counts by category.
- Notebook:
  - Bar charts for number of policies by `Province` and by `VehicleType`.

**Findings**:

- Some provinces and vehicle types account for a **large share of the book**.

**Business implication**:

- High-volume segments (e.g. dominant provinces or passenger vehicles) have a
  **disproportionate impact** on portfolio performance and should be a focus
  for pricing and risk management.

---

## 5. Loss ratios and segment-level performance

### 5.1 Overall loss ratio

- Helper: `compute_loss_ratio_overall`.
- Notebook:
  - Single scalar loss ratio for the entire portfolio.

**Findings**:

- Overall loss ratio is **around 1 or slightly above**, meaning total claims
  are comparable to total premiums.

**Business implication**:

- At an aggregate level, the portfolio is **borderline profitable or slightly
  unprofitable**, leaving limited margin for expenses and profit.
- This motivates the search for **profitable sub-segments** and **risky
  segments** where pricing and underwriting can be adjusted.

### 5.2 By Province

- Helper: `compute_loss_ratio_by_group`.
- Notebook:
  - Table of loss ratios by `Province`.
  - Bar chart of loss ratio by `Province`.

**Findings**:

- Some provinces (e.g. Gauteng) have **significantly higher loss ratios** than
  others.
- There is clear **geographic variation in risk**.

**Business implication**:

- Geography is a **key rating factor**.
- High-loss provinces may require **higher premiums, tighter underwriting, or
  targeted risk mitigation**.

### 5.3 By VehicleType

- Notebook:
  - Loss ratio by `VehicleType`.

**Findings**:

- **Heavy and medium commercial** vehicles tend to have **higher loss ratios**
  than passenger vehicles.

**Business implication**:

- Vehicle usage/class is another **critical rating variable**.
- Commercial classes may require **more granular pricing** or different
  coverage structures.

### 5.4 By Gender

- Notebook:
  - Loss ratio by `Gender`.

**Findings**:

- We can compare male, female, and unknown gender categories to see if loss
  ratios differ materially.

**Business implication**:

- If differences are large and stable, gender could be a relevant risk factor
  (subject to **regulatory and ethical constraints**).
- If differences are minimal, gender may not be useful for pricing.

---

## 6. Outliers and tails

### 6.1 Quantiles and IQR

- Helper: `compute_high_quantiles`, `compute_iqr_bounds` (`src/eda_outliers.py`).
- Notebook:
  - High quantiles (q75, q90, q95, q99) for `TotalPremium` and `TotalClaims`.

**Findings**:

- Premiums and claims at the 99th percentile are **much larger** than typical
  values, confirming the presence of **extreme outliers**.

**Business implication**:

- Large individual policies/claims can **distort averages** and heavily impact
  profitability.
- These require **special treatment** (e.g. reinsurance, separate rating
  structures, or limits).

### 6.2 Boxplots

- Helper: `plot_boxplot` (`src/eda_boxplots.py`).
- Notebook:
  - Boxplots for `TotalPremium` and `TotalClaims` (optionally log-scale).

**Findings**:

- Boxplots highlight the **median and IQR**, with a large number of points
  above the upper whisker.

**Business implication**:

- Visual confirmation that the portfolio has a **long tail of large risks**.
- Reinforces the need for **tail risk management** in pricing and capital
  planning.

---

## 7. Time trends

- Helper: `prepare_monthly_loss_ratio` (`src/eda_trends.py`).
- Notebook:
  - Monthly loss ratio table.
  - Line chart of monthly loss ratio over time.

**Findings**:

- Loss ratio **varies month to month**, with some months performing worse than
  others.

**Business implication**:

- Time trends may reflect **seasonality**, economic conditions, or changes in
  underwriting/pricing.
- Identifying **bad months** can motivate deeper investigation (e.g. large
  events, operational changes).

---

## 8. ZipCode (PostalCode) analysis

- Helpers: `compute_monthly_totals_by_postal`, `summarise_postal_averages`
  (`src/eda_zipcode.py`).
- Notebook:
  - Monthly totals of premiums/claims by `PostalCode` and month.
  - Summary of **average monthly premium, claims, and loss ratio** per
    `PostalCode`.
  - Table of **top 20 postal codes** by average monthly premium.
  - Scatter plot: average monthly premium vs average monthly claims for top 20
    ZipCodes.

**Findings**:

- Certain ZipCodes generate **much more premium** and/or **higher claims**.
- Some high-premium ZipCodes also show **high average claims**, indicating
  concentrations of risk.

**Business implication**:

- ZipCode-level analysis supports **fine-grained geographic rating** beyond
  province-level factors.
- High-premium, high-claims ZipCodes may need targeted action (pricing,
  underwriting, marketing, or portfolio rebalancing).

---

## 9. Overall Task 1 business conclusions

From Task 1, we now have:

1. **Clear understanding of data quality and structure**
   - Key variables are present and mostly clean.
   - Several peripheral fields are highly missing and should not be central to
     modeling.

2. **Evidence that risk is heterogeneous across segments**
   - **Geography** (Province, PostalCode) shows strong variation in loss
     ratios.
   - **VehicleType** (especially commercial vs passenger) has distinct risk
     profiles.
   - **Gender** can be analysed for potential differences.

3. **Recognition of skewness and outliers**
   - Premiums and claims are **heavily skewed with long tails**.
   - Outliers are visually and statistically confirmed.

4. **Understanding of temporal dynamics**
   - Monthly loss ratios reveal **time-varying portfolio performance**.

**Business impact**:

- We can now **identify promising low-risk segments** (e.g. certain provinces
  or vehicle types with loss ratios below 1) where premiums might be reduced
  to attract business.
- We can also **flag high-risk segments** (e.g. particular provinces, vehicle
  types, or ZipCodes) where pricing may need to be adjusted or underwriting
  tightened.
- This EDA forms the foundation for:
  - **Task 2** – introducing DVC for reproducible data management.
  - **Task 3** – formal hypothesis testing (e.g. comparing provinces, ZipCodes,
    genders, margins).
  - **Task 4** – predictive modeling and risk-based pricing.

In summary, Task 1 has delivered a **deep, quantified, and well-documented
understanding** of the portfolio’s risk profile, enabling data-driven
strategic and pricing decisions in subsequent tasks.
