from pydantic import BaseModel, Field
from typing import Optional

class PredictionRequest(BaseModel):
    # Process Parameters
    chamber_temperature: float = Field(..., description="Temperature inside the processing chamber (Celsius)")
    chamber_pressure: float = Field(..., description="Pressure inside the chamber (Torr)")
    gas_flow_rate: float = Field(..., description="Flow rate of process gases (sccm)")
    deposition_time: float = Field(..., description="Time spent in the deposition phase (seconds)")
    plasma_power: float = Field(..., description="Power applied to generate plasma (Watts)")
    process_voltage: float = Field(..., description="Voltage across the process electrodes (Volts)")
    process_current: float = Field(..., description="Current across the process electrodes (Amps)")
    
    # Equipment Features
    equipment_id: str = Field(..., description="Unique identifier for the chamber/machine")
    equipment_age: float = Field(..., description="Age of the equipment in years")
    vibration_level: float = Field(..., description="Vibration sensor reading")
    sensor_health_score: float = Field(..., description="Score indicating sensor reliability (0-100)", ge=0, le=100)
    maintenance_days_since: int = Field(..., description="Days elapsed since last maintenance", ge=0)
    machine_utilization: float = Field(..., description="Machine utilization percentage (0.0-1.0)", ge=0.0, le=1.0)
    
    # Environmental Conditions
    ambient_temperature: float = Field(..., description="Ambient temperature outside cleanroom (Celsius)")
    ambient_humidity: float = Field(..., description="Ambient humidity (%)")
    cleanroom_temperature: float = Field(..., description="Cleanroom temperature (Celsius)")
    cleanroom_humidity: float = Field(..., description="Cleanroom humidity (%)")
    
    # Contextual and Historical
    wafer_type: str = Field(..., description="Type of the wafer being processed")
    material_type: str = Field(..., description="Base material type")
    process_recipe: str = Field(..., description="Specific manufacturing recipe applied")
    production_shift: str = Field(..., description="Shift during which processing occurred")
    operator_shift: str = Field(..., description="Team operating the equipment")
    production_line: str = Field(..., description="Production line ID")
    
    recent_maintenance_flag: int = Field(..., description="1 if maintenance was in last 7 days, else 0", ge=0, le=1)
    machine_failure_count: int = Field(..., description="Count of previous major failures for this machine", ge=0)
    previous_batch_defects: int = Field(..., description="Number of defective wafers in previous batch", ge=0)

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 for Normal, 1 for Defective")
    defect_probability: float = Field(..., description="Probability of a defect (0.0 to 1.0)", ge=0.0, le=1.0)
    risk_level: str = Field(..., description="Risk Classification: LOW, MEDIUM, or HIGH")
    model_version: str = Field(..., description="Identifier for the model currently loaded")
