# Assignment Compliance Matrix

| Requirement | Implementation | Evidence | Status |
|---|---|---|---|
| Synthetic data generation | `src/data/generate_data.py` | `data/raw/semiconductor_manufacturing_raw.csv` created | PASS |
| Numerical + categorical features | Built into generation script | See `docs/data_dictionary.md` | PASS |
| Binary target | `defective` feature (0, 1) | Target generation section of script | PASS |
| High class imbalance | ~8% defect rate | Data generation script logs | PASS |
| Missing values | 5% missingness tied to sensor health | Script logic & output logs | PASS |
| Correlated anomalies | Thermal, Pressure, Equipment degradation | Script logic injecting anomalies to 5% rows | PASS |
| Data cleaning | | | PENDING (M2) |
| Sampling/imbalance handling | | | PENDING (M2) |
| Scaling | | | PENDING (M2) |
| Feature engineering | | | PENDING (M2) |
| EDA visualization | | | PENDING (M2) |
| Two ML algorithms | | | PENDING (M3) |
| Domain-specific metrics | | | PENDING (M3) |
| Hyperparameter tuning | | | PENDING (M3) |
| Model serialization | | | PENDING (M3) |
| REST API | | | PENDING (M4) |
| Input validation | | | PENDING (M4) |
| 5+ unit tests | | | PENDING (M4) |
| Interactive dashboard | | | PENDING (M5) |
