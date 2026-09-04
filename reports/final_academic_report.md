# Advanced AI/ML Academic Report
**Semiconductor Manufacturing Defect Prediction & Quality Intelligence**

---

# Abstract
This report details the end-to-end development of a machine learning system designed to predict rare manufacturing defects in semiconductor fabrication. By synthesizing 25,000 process records with correlated anomalies and applying SMOTE within a strict scikit-learn pipeline, we constructed a Logistic Regression model that outperformed advanced ensembles (XGBoost) on Precision-Recall AUC (0.3994). The model is served via a FastAPI REST endpoint with rigorous Pydantic validation and is consumed by a real-time React dashboard.

---

# 1. Introduction

## 1.1 Background
Semiconductor manufacturing is a highly precise industry where tiny fluctuations in temperature, pressure, or equipment vibration can lead to catastrophic wafer defects.

## 1.2 Problem Context
Defects are inherently rare but extremely costly. Machine learning offers a pathway to predict these defects before they propagate down the production line. However, obtaining real proprietary foundry data is practically impossible for academic purposes.

## 1.3 Problem Statement
The objective is to architect a robust, production-ready ML system that ingests raw telemetry, handles severe class imbalances, and serves accurate risk predictions in real-time.

## 1.4 Objectives
1. Synthesize a domain-accurate manufacturing dataset.
2. Engineer features that capture equipment drift and non-linear anomalies.
3. Train and select a model optimized for rare-event detection.
4. Deploy the model behind a secure, validated API.
5. Provide operators with an interactive intelligence dashboard.

## 1.5 Scope
The system focuses strictly on tabular process telemetry and does not include image-based defect detection (computer vision).

---

# 2. Assignment-Oriented Methodology
The system was developed strictly according to the five required milestones outlined in the Advanced AI/ML Assignment, ensuring complete compliance with the provided specifications.

---

# 3. Milestone 1 — Scenario Selection & Synthetic Data Engineering

## 3.1 Industry Scenario
Semiconductor Wafer Fabrication.

## 3.2 Predictive Task
Binary classification: Predicting whether a processed wafer will exhibit a manufacturing defect (`1`) or be normal (`0`).

## 3.3 Synthetic Dataset Design
The dataset (`data/raw/semiconductor_manufacturing_raw.csv`) comprises 25,000 records. 
- **Numerical Features**: `chamber_temperature`, `chamber_pressure`, `vibration_level`, `equipment_age`, etc.
- **Categorical Features**: `wafer_type`, `equipment_id`, `process_recipe`.

## 3.4 Target Construction
A synthetic risk score was generated using a modified sigmoid function applied to compounded temperature, pressure, and vibration deviations. 

## 3.5 Class Imbalance
The generated defect rate was explicitly tuned to 8.33%, mirroring the "needle-in-a-haystack" nature of real manufacturing defects.

## 3.6 Missing Values
To simulate sensor dropouts, 5% of the data across three key columns (`chamber_temperature`, `vibration_level`, `gas_flow_rate`) was masked as NaN.

## 3.7 Correlated Anomalies
Defects were not generated via random noise. Instead, anomalies were correlated: an older machine (`equipment_age > 8`) combined with high `chamber_pressure` drastically increased the defect probability.

## 3.8 Reproducibility
The `src/data/generate_data.py` script utilizes `np.random.seed(42)` to ensure identical dataset generation across runs.

## 3.9 AI Tool Usage
AI assistance (Antigravity IDE) was utilized to rapidly prototype the complex mathematical compounding functions used for realistic anomaly generation in Python.

---

# 4. Milestone 2 — Context-Aware EDA & Feature Engineering

## 4.1 Data Quality Analysis
Analysis revealed exactly 5% missingness in the targeted columns and identified 0 duplicates.

## 4.2 Missing-Value Analysis
Missing data was categorized as Missing Completely At Random (MCAR) for sensor dropouts.

## 4.3 Outlier and Anomaly Analysis
Heavy right-tails were observed in the vibration data for defective wafers.

## 4.4 Class-Imbalance Analysis
The 91.6% (Normal) to 8.3% (Defect) ratio confirmed that accuracy would be a misleading metric.

## 4.5 Data Cleaning
Missing values were imputed via `SimpleImputer` (median strategy) safely within the scikit-learn pipeline.

## 4.6 Sampling/Imbalance Strategy
SMOTE (Synthetic Minority Over-sampling Technique) was integrated via `imblearn.pipeline.Pipeline` to balance the training folds to a 50/50 ratio without leaking synthetic samples into the validation sets.

## 4.7 Feature Engineering
A custom `FeatureEngineer` transformer was built to calculate relative deviations from baseline.

## 4.8 Interaction Features
`equipment_stress` was engineered by multiplying `vibration_level` by `equipment_age`.

## 4.9 Temporal/Historical Features
`maintenance_risk` was calculated inversely to `maintenance_days_since`.

## 4.10 Scaling and Encoding
Numerical features were standardized using `RobustScaler` (resistant to outliers), and categoricals were one-hot encoded.

## 4.11 Exploratory Data Analysis
Visualizations (correlation matrices, defect distributions) were saved to `reports/figures/`.

## 4.12 Key EDA Findings
Equipment age strongly correlated with defect rates, and older recipes showed tighter operational bounds.

---

# 5. Milestone 3 — Algorithmic Modeling & Performance Rigor

## 5.1 Dataset Splitting
`GroupShuffleSplit` was used on `batch_id` to strictly prevent data leakage between wafers produced in the exact same batch.

## 5.2 Baseline Model
Logistic Regression (max_iter=1000).

## 5.3 Advanced Model
XGBoost Classifier (Gradient Boosted Trees).

## 5.4 Model Training
Models were trained inside the full preprocessing pipeline on 20,000 samples and evaluated on 5,000.

## 5.5 Hyperparameter Optimization
XGBoost was tuned using `RandomizedSearchCV` across `n_estimators`, `max_depth`, and `learning_rate`, optimizing for `f1`.

## 5.6 Evaluation Metrics
Models were evaluated on Precision, Recall, F1, ROC-AUC, and PR-AUC.

## 5.7 Why Accuracy Alone Is Insufficient
Guessing "Normal" on every wafer yields 91.6% accuracy but catches 0 defects. 

## 5.8 Model Comparison
Results extracted from `reports/results/model_metrics.json`:
- **Logistic Regression**: PR-AUC 0.3994, Recall 0.5852
- **XGBoost**: PR-AUC 0.3957, Recall 0.2545

## 5.9 Final Model Selection
**Logistic Regression** was selected. The custom feature engineering effectively linearized the risk profile, rendering the complex non-linear splits of XGBoost unnecessary. XGBoost over-optimized for Precision at a massive expense to Recall.

## 5.10 Model Interpretability
Logistic Regression provides excellent interpretability via coefficient inspection, critical for operator trust.

## 5.11 Model Serialization
The winning pipeline was serialized to `models/final_defect_prediction_pipeline.joblib`.

---

# 6. Milestone 4 — Backend API Construction & Automated Testing

## 6.1 Backend Architecture
A FastAPI microservice hosting the serialized model.

## 6.2 REST API
Exposes `GET /health` and `POST /predict`.

## 6.3 Prediction Endpoint
Accepts 26 features and returns a classification (0 or 1), probability, and Risk Level.

## 6.4 Input Schema
Defined via Pydantic (`schemas.py`).

## 6.5 JSON Validation
Pydantic strictly enforces data types and boundary constraints (e.g., humidity <= 100).

## 6.6 Model Loading
Loaded exactly once during the `lifespan` event to eliminate disk I/O on every request.

## 6.7 Prediction Response
```json
{
  "prediction": 0,
  "defect_probability": 0.1245,
  "risk_level": "LOW",
  "model_version": "LogisticRegression-Pipeline-v1"
}
```

## 6.8 Error Handling
Malformed payloads yield descriptive 422 HTTP errors.

## 6.9 Automated Testing
Tested via `pytest` and `TestClient` (`api_test_results.json`).

| Test | Purpose | Expected Result | Actual Result |
| :--- | :--- | :--- | :--- |
| Valid request | Ensure valid payloads return 200 | 200 OK | PASS |
| Missing field | Ensure missing fields return 422 | 422 Unprocessable Entity | PASS |
| Invalid type | Ensure passing strings to float fails | 422 Unprocessable Entity | PASS |
| Invalid category | Ensure out-of-bounds metrics fail | 422 Unprocessable Entity | PASS |
| Health endpoint | Ensure service load health check | 200 OK | PASS |
| Threshold logic | Ensure probabilities route correctly | Accurate Risk Level | PASS |

---

# 7. Milestone 5 — Interactive Front-End Dashboard Deployment

## 7.1 Dashboard Architecture
The operator-facing dashboard was built using React, TypeScript, and Vite, communicating with the FastAPI backend over a typed HTTP client layer.

## 7.2 Design Goals
A "Premium Control Room" aesthetic using Vanilla CSS, Glassmorphism, and dark-mode tones.

## 7.3 Final User Interface (UI)
The dashboard provides a "Premium Control Room" aesthetic using Vanilla CSS, Glassmorphism, and dark-mode tones.

Below is the initial state of the interactive telemetry dashboard:
![Interactive Telemetry Dashboard - Initial State](/C:/Users/nihal/OneDrive/Desktop/Advanced-AIML-Assignment/reports/assets/ui_dashboard_initial.png)

Below is the dashboard after processing a prediction, demonstrating a High Risk Threshold:
![Prediction Results demonstrating a High Risk Threshold](/C:/Users/nihal/OneDrive/Desktop/Advanced-AIML-Assignment/reports/assets/ui_dashboard_result.png)

## 7.4 Process Monitoring
26 inputs tracking all critical telemetry.

## 7.5 Equipment Intelligence
Dropdowns and bounds for specific machine age and vibration.

## 7.6 Defect Prediction Interface
Dynamic glass pane that updates on form submission.

## 7.7 Alert/Notification Feed
Semantic colors: Green (Low Risk), Amber (Medium Risk), Red (High Risk).

## 7.8 API Integration
Managed via `axios` in `src/api.ts`.

## 7.9 Prediction Result Visualization
Giant typography displaying exact defect percentage probabilities.

## 7.10 User Interaction Flow
User submits telemetry -> Loading Spinner -> API processes pipeline -> Dashboard updates instantly.

---

# 8. Results & Discussion
The system successfully synthesized 25,000 wafers, identified 8.33% (2,083 wafers) as defective, cleanly handled 5% missing data inside a SMOTE pipeline without leakage, and deployed an optimized Logistic Regression model that achieved a PR-AUC of 0.3994 and a Recall of 0.5852 on a highly complex imbalanced dataset. The API achieved 100% test passage across 6 discrete endpoint validations.

---

# 9. Assignment Compliance
See `reports/assignment_compliance_report.md` for the explicit requirement traceability matrix.

---

# 10. Limitations
- **Synthetic Assumptions**: The data, while mathematically robust, cannot perfectly capture real-world quantum or chemical anomalies in physical wafers.
- **Sensor Drift Limits**: Drift was modeled linearly, whereas real factory degradation is often exponential.

---

# 11. Future Scope
- **Online Learning**: Retraining the joblib model continuously as actual defect lab results come back.
- **Explainability UI**: Adding SHAP values to the React dashboard to tell the operator exactly *why* the defect risk is high (e.g., "Temperature is driving this risk").
