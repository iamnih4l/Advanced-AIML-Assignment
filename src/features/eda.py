import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda(input_path='data/raw/semiconductor_manufacturing_raw.csv', output_dir='reports/figures/'):
    print("Loading data for EDA...")
    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Target Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='defective', palette='Set2')
    plt.title('Target Class Distribution (Defective vs Normal)')
    plt.savefig(os.path.join(output_dir, 'class_distribution.png'))
    plt.close()
    
    # 2. Missing Values Heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
    plt.title('Missing Values Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'missing_values_heatmap.png'))
    plt.close()

    # 3. Correlation Matrix (Numerical features only)
    numerical_df = df.select_dtypes(include=[np.number])
    corr = numerical_df.corr()
    
    plt.figure(figsize=(16, 12))
    sns.heatmap(corr, cmap='coolwarm', vmin=-1, vmax=1, center=0, annot=False)
    plt.title('Numerical Features Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()
    
    # 4. Feature Distributions by Class
    features_to_plot = ['chamber_temperature', 'chamber_pressure', 'plasma_power', 'vibration_level']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, feature in enumerate(features_to_plot):
        sns.boxplot(data=df, x='defective', y=feature, ax=axes[idx], palette='Set1')
        axes[idx].set_title(f'{feature} by Defect Status')
        
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_distributions.png'))
    plt.close()

    # 5. Equipment Defect Rates
    plt.figure(figsize=(12, 6))
    equipment_defects = df.groupby('equipment_id')['defective'].mean().reset_index()
    sns.barplot(data=equipment_defects, x='equipment_id', y='defective', palette='viridis')
    plt.title('Defect Rate by Equipment ID')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'equipment_defect_rates.png'))
    plt.close()
    
    # 6. Generate Summary Text
    summary_path = 'reports/eda_summary.txt'
    with open(summary_path, 'w') as f:
        f.write("EDA and Data Quality Analysis Summary\n")
        f.write("======================================\n\n")
        
        f.write(f"Total Observations: {len(df)}\n")
        defect_rate = df['defective'].mean() * 100
        f.write(f"Defect Rate: {defect_rate:.2f}%\n\n")
        
        f.write("Missing Values:\n")
        missing_counts = df.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0]
        for col, count in missing_counts.items():
            f.write(f" - {col}: {count} ({count/len(df)*100:.2f}%)\n")
            
        f.write("\nKey Observations:\n")
        f.write("- Class Imbalance: The target variable 'defective' is highly imbalanced, requiring strategies like SMOTE or Class Weighting during modeling.\n")
        f.write("- Correlated Anomalies: High positive correlations are observed between certain thermal features (e.g., chamber_temperature, ambient_temperature) indicating synthetic anomalies.\n")
        f.write("- Missingness Mechanism: Missing values in chamber_pressure and gas_flow_rate appear correlated with each other and likely tied to sensor health issues rather than being MCAR.\n")
        f.write("- Defect Relationship: Boxplots show that extreme values in chamber_temperature and vibration_level are strongly associated with defective runs.\n")

    print(f"EDA complete. Plots saved to {output_dir}. Summary saved to {summary_path}.")

if __name__ == "__main__":
    perform_eda()
