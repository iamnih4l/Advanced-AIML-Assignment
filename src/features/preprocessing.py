import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

# Custom Transformer for Feature Engineering
class FeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        X_out = X.copy()
        
        # We need to make sure we don't divide by zero and handle column names correctly
        # Assuming X is a pandas DataFrame coming in.
        if not isinstance(X_out, pd.DataFrame):
            raise ValueError("FeatureEngineer expects a pandas DataFrame")
            
        # 1. Thermal Deviation
        if 'chamber_temperature' in X_out.columns:
            X_out['temperature_deviation'] = np.abs(X_out['chamber_temperature'] - 200.0)
            
        # 2. Pressure Deviation
        if 'chamber_pressure' in X_out.columns:
            X_out['pressure_deviation'] = np.abs(X_out['chamber_pressure'] - 5.0)
            
        # 3. Process Power (if not exactly provided or as a redundant safety check)
        if 'process_voltage' in X_out.columns and 'process_current' in X_out.columns:
            X_out['process_power_calc'] = X_out['process_voltage'] * X_out['process_current']
            
        # 4. Equipment Stress
        if all(c in X_out.columns for c in ['equipment_age', 'vibration_level', 'machine_utilization']):
            X_out['equipment_stress'] = X_out['equipment_age'] * X_out['vibration_level'] * X_out['machine_utilization']
            
        # 5. Maintenance Risk
        if 'maintenance_days_since' in X_out.columns:
            X_out['maintenance_risk'] = X_out['maintenance_days_since'] / 120.0
            
        # 6. Interaction: Temp x Power
        if 'chamber_temperature' in X_out.columns and 'plasma_power' in X_out.columns:
            X_out['temp_x_power'] = X_out['chamber_temperature'] * X_out['plasma_power']
            
        return X_out

def get_preprocessing_pipeline(handle_imbalance=True, random_state=42):
    """
    Constructs a complete preprocessing and balancing pipeline.
    If handle_imbalance is True, returns an imblearn Pipeline incorporating SMOTE.
    Otherwise, returns a standard sklearn Pipeline.
    """
    
    # Define feature groups
    # Note: excluding 'defective' (target) and 'batch_id' (identifier)
    numerical_features = [
        'chamber_temperature', 'chamber_pressure', 'gas_flow_rate', 'deposition_time', 
        'plasma_power', 'process_voltage', 'process_current', 'equipment_age', 
        'vibration_level', 'sensor_health_score', 'maintenance_days_since', 
        'machine_utilization', 'ambient_temperature', 'ambient_humidity', 
        'cleanroom_temperature', 'cleanroom_humidity', 'recent_maintenance_flag',
        'machine_failure_count', 'previous_batch_defects'
    ]
    
    categorical_features = [
        'equipment_id', 'wafer_type', 'material_type', 'process_recipe', 
        'production_shift', 'operator_shift', 'production_line'
    ]

    # New features added by the FeatureEngineer transformer
    engineered_features = [
        'temperature_deviation', 'pressure_deviation', 'process_power_calc', 
        'equipment_stress', 'maintenance_risk', 'temp_x_power'
    ]
    
    all_numerical = numerical_features + engineered_features

    # 1. Numerical Preprocessing: Impute missing values -> Scale
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler()) # RobustScaler handles extreme anomalies better
    ])

    # 2. Categorical Preprocessing: Impute -> OneHotEncode
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='MISSING')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # 3. Column Transformer: Apply transformations to respective columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, all_numerical),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop' # Drop batch_id or any unspecified columns
    )

    # 4. Construct Full Pipeline
    if handle_imbalance:
        # Use imblearn Pipeline which handles SMOTE only during fit_resample (training)
        # and skips it during transform (inference)
        pipeline = ImbPipeline(steps=[
            ('feature_engineering', FeatureEngineer()),
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=random_state))
        ])
    else:
        # Standard sklearn pipeline
        pipeline = Pipeline(steps=[
            ('feature_engineering', FeatureEngineer()),
            ('preprocessor', preprocessor)
        ])
        
    return pipeline
