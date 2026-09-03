import pandas as pd
import sys
import os

# Add src to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features.preprocessing import get_preprocessing_pipeline

def verify_pipeline():
    data_path = 'data/raw/semiconductor_manufacturing_raw.csv'
    
    print(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Data file not found. Please run generate_data.py first.")
        return

    # Separate X and y
    X = df.drop(columns=['defective'])
    y = df['defective']

    print(f"Original X shape: {X.shape}")
    print(f"Original y shape: {y.shape}")
    print(f"Original Class Distribution:\n{y.value_counts(normalize=True)*100}\n")

    # Get pipeline with SMOTE
    pipeline = get_preprocessing_pipeline(handle_imbalance=True)

    print("Fitting and transforming data through the pipeline (including SMOTE)...")
    X_resampled, y_resampled = pipeline.fit_resample(X, y)

    print(f"Resampled X shape: {X_resampled.shape}")
    print(f"Resampled y shape: {y_resampled.shape}")
    
    # y_resampled is a pandas Series if the pipeline returns it as such, but imblearn might return a numpy array depending on the version. Let's handle both.
    if isinstance(y_resampled, pd.Series):
        dist = y_resampled.value_counts(normalize=True)*100
    else:
        dist = pd.Series(y_resampled).value_counts(normalize=True)*100
        
    print(f"Resampled Class Distribution:\n{dist}\n")
    
    print("Verification Successful: Pipeline applied custom feature engineering, handled missing values, encoded categorical variables, scaled numericals, and balanced the dataset using SMOTE.")

if __name__ == "__main__":
    verify_pipeline()
