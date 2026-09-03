import pandas as pd
import numpy as np
import os
import json
import joblib
from sklearn.model_selection import GroupShuffleSplit, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, 
    roc_auc_score, average_precision_score, confusion_matrix
)
import sys

# Add src to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.features.preprocessing import get_preprocessing_pipeline

def evaluate_model(model, X_test, y_test):
    """Evaluates the model and returns a dictionary of metrics."""
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'precision': precision_score(y_test, preds),
        'recall': recall_score(y_test, preds),
        'f1': f1_score(y_test, preds),
        'roc_auc': roc_auc_score(y_test, probs),
        'pr_auc': average_precision_score(y_test, probs),
        'confusion_matrix': confusion_matrix(y_test, preds).tolist()
    }
    return metrics

def train_and_evaluate():
    print("Loading data...")
    df = pd.read_csv('data/raw/semiconductor_manufacturing_raw.csv')
    
    # We will use GroupShuffleSplit on 'batch_id' to prevent data leakage
    # Wafers in the same batch share exact temporal/environmental conditions
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    
    X = df.drop(columns=['defective'])
    y = df['defective']
    groups = df['batch_id']
    
    train_idx, test_idx = next(gss.split(X, y, groups))
    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Testing set: {len(X_test)} samples")
    
    # 1. Baseline Model: Logistic Regression
    print("\n--- Training Baseline (Logistic Regression) ---")
    # Using pipeline with SMOTE
    lr_pipeline = get_preprocessing_pipeline(handle_imbalance=True)
    # Add estimator to pipeline
    lr_pipeline.steps.append(['classifier', LogisticRegression(max_iter=1000, random_state=42)])
    
    lr_pipeline.fit(X_train, y_train)
    lr_metrics = evaluate_model(lr_pipeline, X_test, y_test)
    
    print("Baseline Metrics:")
    for k, v in lr_metrics.items():
        if k != 'confusion_matrix':
            print(f"  {k}: {v:.4f}")

    # 2. Advanced Model: XGBoost
    print("\n--- Training Advanced (XGBoost) ---")
    xgb_pipeline = get_preprocessing_pipeline(handle_imbalance=True)
    xgb_pipeline.steps.append(['classifier', XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')])
    
    # Hyperparameter Tuning for XGBoost
    param_distributions = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [3, 5, 7],
        'classifier__learning_rate': [0.01, 0.1, 0.2],
        'classifier__subsample': [0.8, 1.0]
    }
    
    print("Tuning hyperparameters for XGBoost...")
    # RandomizedSearchCV to save time compared to GridSearchCV
    search = RandomizedSearchCV(
        xgb_pipeline, 
        param_distributions, 
        n_iter=5, 
        scoring='f1', # f1 uses hard predictions (1D) and avoids the probability dimension bug
        cv=3, 
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    search.fit(X_train, y_train)
    best_xgb = search.best_estimator_
    
    xgb_metrics = evaluate_model(best_xgb, X_test, y_test)
    
    print("Advanced XGBoost Metrics:")
    for k, v in xgb_metrics.items():
        if k != 'confusion_matrix':
            print(f"  {k}: {v:.4f}")
            
    print(f"Best XGBoost Params: {search.best_params_}")

    # 3. Model Comparison & Selection
    print("\n--- Model Comparison ---")
    print(f"Logistic Regression PR-AUC: {lr_metrics['pr_auc']:.4f}")
    print(f"XGBoost PR-AUC: {xgb_metrics['pr_auc']:.4f}")
    
    if xgb_metrics['pr_auc'] > lr_metrics['pr_auc']:
        print("XGBoost selected as the final model.")
        final_model = best_xgb
        final_metrics = xgb_metrics
        model_name = "XGBoost"
    else:
        print("Logistic Regression selected as the final model.")
        final_model = lr_pipeline
        final_metrics = lr_metrics
        model_name = "Logistic Regression"
        
    # 4. Serialize Pipeline
    os.makedirs('models', exist_ok=True)
    model_path = 'models/final_defect_prediction_pipeline.joblib'
    joblib.dump(final_model, model_path)
    print(f"\nFinal model serialized to {model_path}")
    
    # 5. Log Experiment
    os.makedirs('reports', exist_ok=True)
    log_data = {
        'baseline_logistic_regression': lr_metrics,
        'advanced_xgboost': xgb_metrics,
        'best_params': search.best_params_,
        'selected_model': model_name
    }
    
    with open('reports/experiment_log.json', 'w') as f:
        json.dump(log_data, f, indent=4)
    print("Experiment metrics logged to reports/experiment_log.json")

if __name__ == '__main__':
    train_and_evaluate()
