import axios from 'axios';

const API_URL = 'http://localhost:8000';

export interface PredictionRequest {
  chamber_temperature: number;
  chamber_pressure: number;
  gas_flow_rate: number;
  deposition_time: number;
  plasma_power: number;
  process_voltage: number;
  process_current: number;
  equipment_id: string;
  equipment_age: number;
  vibration_level: number;
  sensor_health_score: number;
  maintenance_days_since: number;
  machine_utilization: number;
  ambient_temperature: number;
  ambient_humidity: number;
  cleanroom_temperature: number;
  cleanroom_humidity: number;
  wafer_type: string;
  material_type: string;
  process_recipe: string;
  production_shift: string;
  operator_shift: string;
  production_line: string;
  recent_maintenance_flag: number;
  machine_failure_count: number;
  previous_batch_defects: number;
}

export interface PredictionResponse {
  prediction: number;
  defect_probability: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  model_version: string;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
}

export const checkHealth = async (): Promise<HealthResponse> => {
  const response = await axios.get(`${API_URL}/health`);
  return response.data;
};

export const predictDefect = async (data: PredictionRequest): Promise<PredictionResponse> => {
  const response = await axios.post(`${API_URL}/predict`, data);
  return response.data;
};
