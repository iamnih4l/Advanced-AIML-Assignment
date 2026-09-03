# Context-Aware EDA & Feature Engineering

This document details the exploratory data analysis findings and the feature engineering logic applied to the Semiconductor Manufacturing Defect Prediction dataset.

## Exploratory Data Analysis (EDA)

The EDA phase aimed to uncover meaningful relationships between process parameters, equipment conditions, and the ultimate defect outcomes. Visualizations and summaries can be found in `reports/figures/` and `reports/eda_summary.txt`.

### Key Findings:
1. **Target Imbalance**: The defect rate is approximately 8.3%. This is a severe imbalance that will drastically affect naive model performance. A classifier that predicts '0' (non-defective) every time would achieve ~91.7% accuracy, rendering accuracy a useless metric.
2. **Missingness Mechanism**: Features like `chamber_pressure`, `gas_flow_rate`, `plasma_power`, and `vibration_level` show non-random missingness. They are missing concurrently in specific instances. This simulates a realistic scenario where an overarching sensor health issue causes a drop in multiple telemetry streams.
3. **Process Parameter Deviations**: Boxplots (`feature_distributions.png`) show that the defective class has a wider spread in process parameters (e.g., `chamber_temperature`, `plasma_power`). Extreme deviations from nominal operating conditions are strong indicators of defect risk.
4. **Correlated Anomalies**: The correlation matrix (`correlation_matrix.png`) identifies strong positive correlations injected during the data generation phase (e.g., thermal anomalies where chamber and ambient temperatures rise alongside power).

## Feature Engineering

Based on domain understanding of semiconductor manufacturing, several synthetic features were engineered to provide the model with explicit contextual indicators:

- **`temperature_deviation`**: Absolute deviation of `chamber_temperature` from the nominal 200°C. Captures the magnitude of thermal instability.
- **`pressure_deviation`**: Absolute deviation of `chamber_pressure` from the nominal 5.0 Torr.
- **`process_power_calc`**: Interaction of `process_voltage` * `process_current`. Represents the total power flowing through the process.
- **`maintenance_risk`**: `maintenance_days_since` divided by 120 (the assumed maximum safe maintenance interval). Values approaching 1.0 indicate high risk of failure due to lack of servicing.
- **`equipment_stress`**: A multi-variable interaction term (`equipment_age * vibration_level * machine_utilization`). High values indicate an older machine vibrating excessively while running at high utilization.
- **`temp_x_power`**: Interaction term capturing the combined effect of high temperature and high plasma power.

## Class Imbalance Strategy (SMOTE)

To handle the ~8.3% defect rate, we selected **SMOTE (Synthetic Minority Over-sampling Technique)**.

### Justification:
- Simple undersampling would discard over 20,000 observations of valuable normal operating data.
- Class weighting is viable, but SMOTE actively generates synthetic examples of the minority (defective) class by interpolating between existing defective instances. This allows the model to learn a more robust, generalized decision boundary for the rare defect conditions.
- **Crucial Implementation Detail**: SMOTE must *never* be applied to validation or test data, as it causes severe data leakage and inflated performance metrics. We utilize `imblearn.pipeline.Pipeline`, which ensures SMOTE is strictly applied only during the `fit()` stage (training), and is bypassed during `transform()` or `predict()` (inference).

## Reusable Preprocessing Pipeline

The entire workflow (imputation, custom feature engineering, scaling, one-hot encoding, and SMOTE) is wrapped in a serializable `scikit-learn` Pipeline inside `src/features/preprocessing.py`. This ensures identical transformations can be safely applied to live API requests during inference in Milestone 4.
