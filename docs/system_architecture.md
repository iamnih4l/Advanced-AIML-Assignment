# System Architecture

The following diagram illustrates the exact data, model, and inference flow of the implemented Semiconductor Manufacturing Defect Prediction system.

```mermaid
graph TD
    %% Synthetic Data Generation Layer
    subgraph Data Layer
        A[Synthetic Data Generator<br>src/data/generate_data.py] -->|Outputs 25,000 rows| B[(Raw Semiconductor Dataset<br>data/raw/semiconductor_manufacturing_raw.csv)]
    end

    %% Preprocessing & Feature Engineering Layer
    subgraph Feature Engineering & Pipeline
        B -->|Pandas Load| C[Data Quality / Cleaning<br>Handling missing values]
        C --> D[EDA + Feature Engineering<br>src/features/preprocessing.py]
        D -->|FeatureEngineer| E[Preprocessing Pipeline]
        E -->|SMOTE| F[Class Imbalance Handling]
    end

    %% Model Training & Serialization Layer
    subgraph Algorithmic Modeling
        F --> G[Baseline: Logistic Regression]
        F --> H[Advanced: XGBoost]
        G --> I[Model Evaluation + Tuning<br>PR-AUC & RandomizedSearchCV]
        H --> I
        I -->|joblib.dump| J[(Serialized ML Pipeline<br>models/final_defect_prediction_pipeline.joblib)]
    end

    %% Application Layer
    subgraph Production & API
        J -.->|Loaded on Lifespan| K[FastAPI Prediction Service<br>backend/app/main.py]
        L[Quality Intelligence UI<br>React/Vite Dashboard] -->|JSON Payload| K
        K -->|Defect Probability %| L
    end
```

## Architectural Responsibilities

1. **Synthetic Data Generator (`generate_data.py`)**: Responsible for injecting domain-specific thermal anomalies, equipment degradation over time (drift), and realistic missing data patterns into a synthetic wafer dataset.
2. **Preprocessing Pipeline (`preprocessing.py`)**: A modular scikit-learn pipeline wrapping custom transformers (`FeatureEngineer`), imputation, scaling, and `imblearn`'s SMOTE. Responsible for ensuring no data leaks occur between training folds.
3. **Training Script (`train_model.py`)**: Responsible for utilizing `GroupShuffleSplit` (on `batch_id`) to strictly separate dependent wafers, running hyperparameter tuning, and selecting the best model based on PR-AUC.
4. **FastAPI Service (`main.py`)**: Responsible for strong Pydantic validation (rejecting malformed inputs) and hosting the `joblib` pipeline efficiently via a lifespan context manager.
5. **React Dashboard (`App.tsx`)**: Responsible for the operator-facing interface, capturing telemetry, and translating probabilities into color-coded operational Risk Thresholds.
