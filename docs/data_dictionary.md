# Semiconductor Manufacturing Data Dictionary

This document details the features present in the synthetic semiconductor manufacturing dataset.

## Target Variable
- **defective**: `int` [0, 1]. The binary classification target. 0 indicates a normal, non-defective wafer/process run. 1 indicates a defective wafer.

## Process Parameters
- **chamber_temperature**: `float`. Temperature inside the processing chamber (Celsius). Expected nominal is ~200°C. 
- **chamber_pressure**: `float`. Pressure inside the chamber (Torr or Pascal equivalent). Expected nominal is ~5.0. Contains missing values.
- **gas_flow_rate**: `float`. Flow rate of process gases (sccm). Expected nominal is ~100. Contains missing values.
- **deposition_time**: `float`. Time spent in the deposition/process phase (seconds). Nominal is ~30s.
- **plasma_power**: `float`. Power applied to generate plasma (Watts). Nominal is ~500W. Contains missing values.
- **process_voltage**: `float`. Voltage across the process electrodes (Volts). Nominal ~220V.
- **process_current**: `float`. Current across the process electrodes (Amps). Nominal ~15A.

## Equipment Features
- **equipment_id**: `categorical`. Unique identifier for the chamber/machine (e.g., CHAMBER-01 to CHAMBER-10).
- **equipment_age**: `float`. Age of the equipment in years. (0.5 to 10.0)
- **vibration_level**: `float`. Vibration sensor reading. Nominal ~1.0. Contains missing values.
- **sensor_health_score**: `float`. Aggregated score (0-100) indicating the reliability of the machine's sensors.
- **maintenance_days_since**: `int`. Days elapsed since the last major maintenance on the equipment.
- **machine_utilization**: `float`. Percentage (0.0 - 1.0) of time the machine has been actively processing in the current shift/period.

## Environmental Conditions
- **ambient_temperature**: `float`. Ambient temperature outside the cleanroom/chamber (Celsius).
- **ambient_humidity**: `float`. Ambient humidity outside the cleanroom (%). Contains missing values.
- **cleanroom_temperature**: `float`. Closely controlled cleanroom temperature (Celsius).
- **cleanroom_humidity**: `float`. Closely controlled cleanroom humidity (%).

## Production Context
- **batch_id**: `categorical`. Identifier for the production batch.
- **wafer_type**: `categorical`. The type/size of the wafer being processed (e.g., TYPE_A).
- **material_type**: `categorical`. Base material (e.g., SILICON, SILICON_CARBIDE).
- **process_recipe**: `categorical`. The specific manufacturing recipe applied (e.g., RECIPE_1).
- **production_shift**: `categorical`. Shift during which processing occurred (MORNING, EVENING, NIGHT).
- **operator_shift**: `categorical`. Team operating the equipment.
- **production_line**: `categorical`. Specific production line ID.

## Historical / Operational Features
- **recent_maintenance_flag**: `int` [0, 1]. 1 if maintenance was performed in the last 7 days, else 0.
- **machine_failure_count**: `int`. Mocked historical count of previous major failures for this machine.
- **previous_batch_defects**: `int`. Number of defective wafers in the immediately preceding batch for this machine/line.
