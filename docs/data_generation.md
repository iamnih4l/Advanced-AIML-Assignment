# Synthetic Data Generation Methodology

This document outlines the methodology used to generate the synthetic dataset for the Semiconductor Manufacturing Defect Prediction system.

## 1. Goal and Assumptions
The objective is to produce a dataset that mimics a real-world semiconductor manufacturing environment where complex combinations of process, equipment, and environmental variables influence the final quality (defect vs. non-defect) of a processed wafer. The relationships modeled here are assumed for the sake of the exercise and should not be treated as empirical physical laws.

## 2. Features and Distributions
Features are divided into logical groups:
- **Process Parameters**: Generated using normal distributions around assumed nominal operating points (e.g., Temp = 200C).
- **Equipment Parameters**: Simulates specific chambers, age, vibration, and sensor health.
- **Environmental**: Simulates ambient and cleanroom conditions.
- **Contextual**: Simulates batches, materials, and shifts.

## 3. Target Generation (`defective`)
The target is a binary classification (0 = Normal, 1 = Defective). 
A latent risk score is calculated by standardizing and combining deviations in key variables (e.g., temperature deviation, pressure deviation, vibration, and overdue maintenance). Poor sensor health is treated as a risk-increasing factor.
This score is passed through a scaled sigmoid function to calculate the probability of a defect. We then sample from a binomial distribution.
This creates a non-linear relationship between features and the target, and ensures the target is not perfectly predictable (overlap between classes).

## 4. Class Imbalance
The generation parameters (specifically the sigmoid threshold) are tuned to produce a realistic rare-defect setting, achieving a defect rate between 2% and 10%.

## 5. Correlated Anomalies
To satisfy the assignment requirements, we inject specific correlated anomalies into 5% of the data:
- **Thermal Anomaly**: Simultaneous spikes in chamber temperature, ambient temperature, plasma power, and process voltage.
- **Pressure/Gas Anomaly**: Abnormal pressure, decreased gas flow, and process current deviation.
- **Equipment Degradation**: High equipment age, elevated vibration, low sensor health, and overdue maintenance.

## 6. Missing Values
Missingness is not purely random (MCAR) for all variables. 
- Variables like `chamber_pressure`, `gas_flow_rate`, `plasma_power`, and `vibration_level` have a higher probability of being missing (5%) when the equipment's `sensor_health_score` drops below 60. Otherwise, the probability is 0.5%.
- `ambient_humidity` features 1% Missing Completely At Random (MCAR) values.

## 7. Sensor Drift
We simulate gradual sensor drift by adding a slight, monotonic linear increase (up to +3.0) to the `chamber_temperature` variable across the dataset index to simulate aging sensor calibration.

## 8. Reproducibility
The data generator uses a fixed random seed (`numpy.random.seed(42)` and `random.seed(42)`) to ensure identical datasets are generated across different runs. The dataset size is set to 25,000 observations.
