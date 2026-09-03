import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle, Cpu, Loader2, Server, Settings2 } from 'lucide-react';
import { checkHealth, predictDefect, type PredictionRequest, type PredictionResponse } from './api';

const DEFAULT_WAFER: PredictionRequest = {
  chamber_temperature: 205.5,
  chamber_pressure: 5.2,
  gas_flow_rate: 102.0,
  deposition_time: 30.5,
  plasma_power: 510.0,
  process_voltage: 225.0,
  process_current: 15.2,
  equipment_id: "CHAMBER-01",
  equipment_age: 5.5,
  vibration_level: 1.2,
  sensor_health_score: 85.0,
  maintenance_days_since: 30,
  machine_utilization: 0.8,
  ambient_temperature: 22.5,
  ambient_humidity: 45.0,
  cleanroom_temperature: 21.0,
  cleanroom_humidity: 40.0,
  wafer_type: "TYPE_A",
  material_type: "SILICON",
  process_recipe: "RECIPE_1",
  production_shift: "MORNING",
  operator_shift: "TEAM_ALPHA",
  production_line: "LINE_1",
  recent_maintenance_flag: 0,
  machine_failure_count: 1,
  previous_batch_defects: 2
};

function App() {
  const [formData, setFormData] = useState<PredictionRequest>(DEFAULT_WAFER);
  const [isBackendOnline, setIsBackendOnline] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkHealth()
      .then(res => setIsBackendOnline(res.status === 'healthy' && res.model_loaded))
      .catch(() => setIsBackendOnline(false));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    
    let parsedValue: string | number = value;
    if (type === 'number') {
      parsedValue = value === '' ? 0 : Number(value);
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: parsedValue
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const res = await predictDefect(formData);
      setResult(res);
    } catch (err: any) {
      setError(err.response?.data?.detail?.[0]?.msg || err.message || "Failed to predict");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header glass-panel">
        <Cpu size={28} className="text-accent" color="#3b82f6" />
        <h1>Semiconductor Quality Intelligence</h1>
        <div style={{ marginLeft: 'auto' }}>
          <span className={`status-badge ${isBackendOnline ? 'online' : 'offline'}`}>
            <Server size={14} style={{ marginRight: '6px' }} />
            {isBackendOnline ? 'ML Engine Online' : 'API Offline'}
          </span>
        </div>
      </header>

      <main className="main-content">
        {/* Left Panel: Telemetry Form */}
        <section className="glass-panel">
          <form onSubmit={handleSubmit} className="form-section">
            
            <div>
              <div className="form-group-title">
                <Settings2 size={18} color="#94a3b8" />
                Process Parameters
              </div>
              <div className="form-grid">
                <div className="input-wrapper">
                  <label>Chamber Temp (°C)</label>
                  <input type="number" step="0.1" name="chamber_temperature" value={formData.chamber_temperature} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Chamber Pressure (Torr)</label>
                  <input type="number" step="0.1" name="chamber_pressure" value={formData.chamber_pressure} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Gas Flow Rate (sccm)</label>
                  <input type="number" step="0.1" name="gas_flow_rate" value={formData.gas_flow_rate} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Deposition Time (s)</label>
                  <input type="number" step="0.1" name="deposition_time" value={formData.deposition_time} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Plasma Power (W)</label>
                  <input type="number" step="0.1" name="plasma_power" value={formData.plasma_power} onChange={handleChange} required />
                </div>
              </div>
            </div>

            <div style={{ marginTop: '1rem' }}>
              <div className="form-group-title">
                <Activity size={18} color="#94a3b8" />
                Equipment Status
              </div>
              <div className="form-grid">
                <div className="input-wrapper">
                  <label>Equipment ID</label>
                  <select name="equipment_id" value={formData.equipment_id} onChange={handleChange}>
                    <option value="CHAMBER-01">CHAMBER-01</option>
                    <option value="CHAMBER-02">CHAMBER-02</option>
                    <option value="CHAMBER-03">CHAMBER-03</option>
                  </select>
                </div>
                <div className="input-wrapper">
                  <label>Equipment Age (Yrs)</label>
                  <input type="number" step="0.1" name="equipment_age" value={formData.equipment_age} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Vibration Level</label>
                  <input type="number" step="0.1" name="vibration_level" value={formData.vibration_level} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Sensor Health (0-100)</label>
                  <input type="number" step="0.1" min="0" max="100" name="sensor_health_score" value={formData.sensor_health_score} onChange={handleChange} required />
                </div>
                <div className="input-wrapper">
                  <label>Machine Utilization (0-1)</label>
                  <input type="number" step="0.01" min="0" max="1" name="machine_utilization" value={formData.machine_utilization} onChange={handleChange} required />
                </div>
              </div>
            </div>

            <button type="submit" className="submit-btn" disabled={isLoading || !isBackendOnline}>
              {isLoading ? (
                <>
                  <Loader2 className="spinner" size={18} /> Processing Telemetry...
                </>
              ) : (
                'Run Risk Prediction'
              )}
            </button>
          </form>
        </section>

        {/* Right Panel: Results Display */}
        <aside className="results-panel">
          <div className="glass-panel" style={{ minHeight: '400px' }}>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '1.5rem', fontWeight: 500 }}>
              Prediction Engine
            </h2>

            {error && (
              <div className="error-msg">
                <AlertTriangle size={18} />
                {error}
              </div>
            )}

            {!result && !error && (
              <div style={{ textAlign: 'center', color: '#94a3b8', marginTop: '4rem' }}>
                <Activity size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                <p>Waiting for telemetry input...</p>
              </div>
            )}

            {result && (
              <div className={`result-card ${result.risk_level.toLowerCase()}`}>
                <div className="risk-title">
                  {result.risk_level === 'LOW' && 'Process Stable'}
                  {result.risk_level === 'MEDIUM' && 'Elevated Risk'}
                  {result.risk_level === 'HIGH' && 'Critical Defect Risk'}
                </div>
                
                <div className="prob-value">
                  {(result.defect_probability * 100).toFixed(1)}%
                </div>
                <div className="prob-label">Defect Probability</div>

                <div style={{ marginTop: '2rem', textAlign: 'left' }}>
                  <div className="info-row">
                    <span className="info-label">Prediction</span>
                    <span className="info-value">
                      {result.prediction === 1 ? (
                        <span style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <AlertTriangle size={14} /> DEFECTIVE
                        </span>
                      ) : (
                        <span style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <CheckCircle size={14} /> NORMAL
                        </span>
                      )}
                    </span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">Risk Threshold</span>
                    <span className="info-value">{result.risk_level}</span>
                  </div>
                  <div className="info-row">
                    <span className="info-label">Model Version</span>
                    <span className="info-value" style={{ fontSize: '0.8rem' }}>{result.model_version}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </aside>

      </main>
    </div>
  );
}

export default App;
