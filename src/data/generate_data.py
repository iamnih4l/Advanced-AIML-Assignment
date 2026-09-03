import pandas as pd
import numpy as np
import os
import random

def generate_synthetic_data(n_samples=10000, random_seed=42):
    """
    Generates synthetic semiconductor manufacturing data with realistic features, 
    anomalies, missing values, and a binary defect target.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)

    # 1. Base Features
    # ------------------------------------------------------------
    
    # Process Parameters
    chamber_temperature = np.random.normal(200.0, 5.0, n_samples)
    chamber_pressure = np.random.normal(5.0, 0.2, n_samples)
    gas_flow_rate = np.random.normal(100.0, 3.0, n_samples)
    deposition_time = np.random.normal(30.0, 1.0, n_samples)
    plasma_power = np.random.normal(500.0, 15.0, n_samples)
    process_voltage = np.random.normal(220.0, 2.0, n_samples)
    process_current = np.random.normal(15.0, 0.5, n_samples)

    # Equipment Features
    equipment_id = np.random.choice([f'CHAMBER-{str(i).zfill(2)}' for i in range(1, 11)], n_samples)
    equipment_age = np.random.uniform(0.5, 10.0, n_samples) # years
    vibration_level = np.random.normal(1.0, 0.2, n_samples)
    sensor_health_score = np.random.uniform(50.0, 100.0, n_samples)
    maintenance_days_since = np.random.randint(1, 120, n_samples)
    machine_utilization = np.random.uniform(0.4, 0.95, n_samples)

    # Environmental Conditions
    ambient_temperature = np.random.normal(22.0, 1.5, n_samples)
    ambient_humidity = np.random.normal(45.0, 5.0, n_samples)
    cleanroom_temperature = np.random.normal(21.0, 0.5, n_samples)
    cleanroom_humidity = np.random.normal(40.0, 2.0, n_samples)

    # Production Context
    batch_id = [f'BATCH-{str(i//50).zfill(4)}' for i in range(n_samples)]
    wafer_type = np.random.choice(['TYPE_A', 'TYPE_B', 'TYPE_C'], n_samples, p=[0.5, 0.3, 0.2])
    material_type = np.random.choice(['SILICON', 'GALLIUM_ARSENIDE', 'SILICON_CARBIDE'], n_samples, p=[0.7, 0.2, 0.1])
    process_recipe = np.random.choice(['RECIPE_1', 'RECIPE_2', 'RECIPE_3', 'RECIPE_4'], n_samples)
    production_shift = np.random.choice(['MORNING', 'EVENING', 'NIGHT'], n_samples)
    operator_shift = np.random.choice(['TEAM_ALPHA', 'TEAM_BETA', 'TEAM_GAMMA', 'TEAM_DELTA'], n_samples)
    production_line = np.random.choice(['LINE_1', 'LINE_2', 'LINE_3'], n_samples)

    # Construct DataFrame
    df = pd.DataFrame({
        'batch_id': batch_id,
        'equipment_id': equipment_id,
        'wafer_type': wafer_type,
        'material_type': material_type,
        'process_recipe': process_recipe,
        'production_shift': production_shift,
        'operator_shift': operator_shift,
        'production_line': production_line,
        
        'chamber_temperature': chamber_temperature,
        'chamber_pressure': chamber_pressure,
        'gas_flow_rate': gas_flow_rate,
        'deposition_time': deposition_time,
        'plasma_power': plasma_power,
        'process_voltage': process_voltage,
        'process_current': process_current,
        
        'equipment_age': equipment_age,
        'vibration_level': vibration_level,
        'sensor_health_score': sensor_health_score,
        'maintenance_days_since': maintenance_days_since,
        'machine_utilization': machine_utilization,
        
        'ambient_temperature': ambient_temperature,
        'ambient_humidity': ambient_humidity,
        'cleanroom_temperature': cleanroom_temperature,
        'cleanroom_humidity': cleanroom_humidity
    })

    # 2. Add Sensor Drift
    # ------------------------------------------------------------
    # Simulating gradual drift in chamber_temperature over time (index)
    drift = np.linspace(0, 3.0, n_samples)
    df['chamber_temperature'] += drift

    # 3. Inject Correlated Anomalies
    # ------------------------------------------------------------
    num_anomalies = int(n_samples * 0.05) # 5% anomalies
    anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)
    
    # Split anomalies into types
    thermal_idx = anomaly_indices[:len(anomaly_indices)//3]
    pressure_idx = anomaly_indices[len(anomaly_indices)//3:2*len(anomaly_indices)//3]
    degradation_idx = anomaly_indices[2*len(anomaly_indices)//3:]

    # Thermal Anomaly: temp up, ambient temp up, power up, voltage up
    df.loc[thermal_idx, 'chamber_temperature'] += np.random.normal(15.0, 5.0, len(thermal_idx))
    df.loc[thermal_idx, 'ambient_temperature'] += np.random.normal(5.0, 2.0, len(thermal_idx))
    df.loc[thermal_idx, 'plasma_power'] += np.random.normal(40.0, 10.0, len(thermal_idx))
    df.loc[thermal_idx, 'process_voltage'] += np.random.normal(10.0, 2.0, len(thermal_idx))

    # Pressure/Gas Anomaly: pressure dev, gas flow dev, power instability, current dev
    df.loc[pressure_idx, 'chamber_pressure'] += np.random.choice([-1, 1], len(pressure_idx)) * np.random.normal(0.8, 0.2, len(pressure_idx))
    df.loc[pressure_idx, 'gas_flow_rate'] -= np.random.normal(15.0, 5.0, len(pressure_idx))
    df.loc[pressure_idx, 'process_current'] += np.random.normal(3.0, 1.0, len(pressure_idx))
    
    # Equipment Degradation: age high, vibration high, sensor health low, maintenance high
    df.loc[degradation_idx, 'vibration_level'] += np.random.normal(1.5, 0.3, len(degradation_idx))
    df.loc[degradation_idx, 'sensor_health_score'] -= np.random.uniform(20.0, 40.0, len(degradation_idx))
    df.loc[degradation_idx, 'maintenance_days_since'] = np.random.randint(90, 150, len(degradation_idx))
    df.loc[degradation_idx, 'machine_utilization'] = np.random.uniform(0.85, 0.99, len(degradation_idx))

    # 4. Generate Target (defective)
    # ------------------------------------------------------------
    # Calculate a latent risk score based on deviations from normal ranges and equipment state
    
    # Standardize some features temporarily to compute risk
    temp_dev = np.abs(df['chamber_temperature'] - 200.0) / 5.0
    pressure_dev = np.abs(df['chamber_pressure'] - 5.0) / 0.2
    gas_dev = np.abs(df['gas_flow_rate'] - 100.0) / 3.0
    power_dev = np.abs(df['plasma_power'] - 500.0) / 15.0
    
    maint_risk = df['maintenance_days_since'] / 120.0
    vib_risk = (df['vibration_level'] - 1.0) / 0.2
    
    # Non-linear combination for risk score
    risk_score = (
        0.5 * temp_dev**1.2 + 
        0.4 * pressure_dev + 
        0.3 * gas_dev + 
        0.3 * power_dev + 
        0.6 * maint_risk + 
        0.4 * np.maximum(0, vib_risk)**1.5 - 
        0.5 * (df['sensor_health_score'] - 50) / 50.0 # higher health lowers risk
    )
    
    # Convert risk score to probability using a scaled sigmoid
    # Scale adjusted to achieve roughly ~5-10% defect rate
    prob = 1 / (1 + np.exp(-(risk_score - 4.5))) 
    
    # Sample defective status based on probability
    df['defective'] = np.random.binomial(1, prob)

    # 5. Historical / Operational Features (Calculate after sorting by time/batch)
    # ------------------------------------------------------------
    # We will compute a simple rolling metric to simulate historical context
    df['recent_maintenance_flag'] = (df['maintenance_days_since'] < 7).astype(int)
    
    # Mock some historical failures for features
    df['machine_failure_count'] = np.random.poisson(lam=0.5, size=n_samples) + df['equipment_age'].astype(int) // 3
    df['previous_batch_defects'] = np.random.poisson(lam=1.5, size=n_samples)
    
    # 6. Inject Missing Values
    # ------------------------------------------------------------
    # Missingness tied to poor sensor health and random chance
    # Low sensor health -> higher chance of missing chamber_pressure and gas_flow_rate
    missing_prob = np.where(df['sensor_health_score'] < 60, 0.05, 0.005)
    
    for col in ['chamber_pressure', 'gas_flow_rate', 'plasma_power', 'vibration_level']:
        mask = np.random.random(n_samples) < missing_prob
        df.loc[mask, col] = np.nan
        
    # Ambient missing completely at random (MCAR) ~ 1%
    mcar_mask = np.random.random(n_samples) < 0.01
    df.loc[mcar_mask, 'ambient_humidity'] = np.random.choice([np.nan], len(df[mcar_mask]))
    
    # Shuffle dataset to break the artificial ordering created by anomaly injection if any
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    print("Generating synthetic semiconductor manufacturing dataset...")
    df = generate_synthetic_data(n_samples=25000)
    
    # Directory setup for safety
    os.makedirs('data/raw', exist_ok=True)
    
    output_path = 'data/raw/semiconductor_manufacturing_raw.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Dataset generated and saved to {output_path}")
    print(f"Total observations: {len(df)}")
    print(f"Defect percentage: {(df['defective'].mean() * 100):.2f}%")
    print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
