# Assignment Compliance Matrix

| Requirement | Implementation | Evidence | Status |
|---|---|---|---|
| Synthetic data generation | `src/data/generate_data.py` | `data/raw/semiconductor_manufacturing_raw.csv` created | PASS |
| Numerical + categorical features | Built into generation script | See `docs/data_dictionary.md` | PASS |
| Binary target | `defective` feature (0, 1) | Target generation section of script | PASS |
| High class imbalance | ~8% defect rate | Data generation script logs | PASS |
| Missing values | 5% missingness tied to sensor health | Script logic & output logs | PASS |
| Correlated anomalies | Thermal, Pressure, Equipment degradation | Script logic injecting anomalies to 5% rows | PASS |
| Data cleaning | `src/features/preprocessing.py` | SimpleImputer used in Pipeline | PASS |
| Sampling/imbalance handling | `src/features/preprocessing.py` | SMOTE implemented via imblearn Pipeline | PASS |
| Scaling | `src/features/preprocessing.py` | RobustScaler used for numericals | PASS |
| Feature engineering | `src/features/preprocessing.py` | Custom `FeatureEngineer` transformer | PASS |
| EDA visualization | `src/features/eda.py` | Plots saved in `reports/figures/` | PASS |
| Two ML algorithms | `src/models/train_model.py` | Logistic Regression & XGBoost evaluated | PASS |
| Domain-specific metrics | `src/models/train_model.py` | PR-AUC, Recall, Precision used | PASS |
| Hyperparameter tuning | `src/models/train_model.py` | RandomizedSearchCV applied to XGBoost | PASS |
| Model serialization | `src/models/train_model.py` | `models/final_defect_prediction_pipeline.joblib` created | PASS |
| REST API | | | PENDING (M4) |
| Input validation | | | PENDING (M4) |
| 5+ unit tests | | | PENDING (M4) |
| Interactive dashboard | | | PENDING (M5) |
