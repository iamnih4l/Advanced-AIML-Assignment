# Assignment Requirements Traceability Matrix

This matrix explicitly links the requirements derived from the Advanced AI/ML Assignment prompt to their implementation within the codebase and their corresponding evidence documentation.

| Assignment Requirement | Milestone | Implementation File | Evidence/Artifact | Report Section | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Industry scenario | M1 | `src/data/generate_data.py` | `docs/data_generation.md` | 3.1 | PASS |
| Predictive task | M1 | `src/data/generate_data.py` | `docs/data_dictionary.md` | 3.2 | PASS |
| Synthetic data generation | M1 | `src/data/generate_data.py` | `data/raw/*.csv` | 3.3 | PASS |
| Numerical features | M1 | `src/data/generate_data.py` | `docs/data_dictionary.md` | 3.3 | PASS |
| Categorical features | M1 | `src/data/generate_data.py` | `docs/data_dictionary.md` | 3.3 | PASS |
| Class imbalance injection | M1 | `src/data/generate_data.py` | `docs/eda_and_features.md` | 3.5 | PASS |
| Missing values injection | M1 | `src/data/generate_data.py` | `docs/eda_and_features.md` | 3.6 | PASS |
| Correlated anomalies | M1 | `src/data/generate_data.py` | `docs/data_generation.md` | 3.7 | PASS |
| Data cleaning | M2 | `src/features/preprocessing.py` | `scripts/verify_m2.py` | 4.5 | PASS |
| Sampling/imbalance handling | M2 | `src/features/preprocessing.py` | `scripts/verify_m2.py` (SMOTE) | 4.6 | PASS |
| Scaling | M2 | `src/features/preprocessing.py` | Pipeline Steps | 4.10 | PASS |
| Feature engineering | M2 | `src/features/preprocessing.py` | `docs/eda_and_features.md` | 4.7 | PASS |
| EDA visualizations | M2 | `src/features/eda.py` | `reports/figures/*.png` | 4.11 | PASS |
| Two ML algorithms | M3 | `src/models/train_model.py` | `reports/experiment_log.json` | 5.2, 5.3 | PASS |
| Domain-specific evaluation | M3 | `src/models/train_model.py` | `docs/modeling_and_evaluation.md`| 5.6 | PASS |
| Hyperparameter optimization | M3 | `src/models/train_model.py` | `reports/experiment_log.json` | 5.5 | PASS |
| Model serialization | M3 | `src/models/train_model.py` | `models/final_*.joblib` | 5.11 | PASS |
| REST endpoint | M4 | `backend/app/main.py` | `docs/backend_api.md` | 6.2 | PASS |
| Strong JSON validation | M4 | `backend/app/schemas.py` | `docs/backend_api.md` | 6.5 | PASS |
| 5+ unit tests | M4 | `backend/tests/test_api.py` | `reports/results/api_test_results.json` | 6.9 | PASS |
| Interactive dashboard | M5 | `frontend/src/App.tsx` | `frontend/` source code | 7.1 | PASS |
