import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle, Cpu, Loader2, Server, Settings2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { checkHealth, predictDefect, type PredictionRequest, type PredictionResponse } from './api';
import Wafer3DScene from './components/Wafer3D';

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
  const [appState, setAppState] = useState<'IDLE' | 'SCANNING' | 'LOW' | 'MEDIUM' | 'HIGH'>('IDLE');
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
    setFormData(prev => ({ ...prev, [name]: parsedValue }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAppState('SCANNING');
    setError(null);
    setResult(null);
    
    try {
      const res = await predictDefect(formData);
      // Simulate dramatic scanning delay for cinematic effect
      setTimeout(() => {
        setResult(res);
        setAppState(res.risk_level as any);
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail?.[0]?.msg || err.message || "Failed to predict");
      setAppState('IDLE');
    }
  };

  return (
    <>
      <div className="cinematic-bg" />
      
      <div className="app-container">
        <motion.header 
          className="header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <Cpu size={28} className="text-accent" color="#00f0ff" />
          <h1>Quality Intel UI</h1>
          <div style={{ marginLeft: 'auto' }}>
            <span className={`status-badge ${isBackendOnline ? 'online' : 'offline'}`}>
              <Server size={14} style={{ marginRight: '6px' }} />
              {isBackendOnline ? 'ML Engine Online' : 'API Offline'}
            </span>
          </div>
        </motion.header>

        <main className="main-content">
          {/* Left Panel: Telemetry Form */}
          <motion.section 
            className="glass-panel"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <form onSubmit={handleSubmit} className="form-section">
              <div>
                <div className="form-group-title">
                  <Settings2 size={18} />
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

              <div style={{ marginTop: '1.5rem' }}>
                <div className="form-group-title">
                  <Activity size={18} />
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

              <button type="submit" className="submit-btn" disabled={appState === 'SCANNING' || !isBackendOnline}>
                {appState === 'SCANNING' ? (
                  <>
                    <Loader2 className="spinner" size={18} style={{ animation: 'spin 1s linear infinite' }} /> Processing Telemetry...
                  </>
                ) : (
                  'Run Risk Prediction'
                )}
              </button>
            </form>
          </motion.section>

          {/* Right Panel: 3D Visualization & Results */}
          <motion.aside 
            className="visual-panel"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            {/* The React Three Fiber Canvas */}
            <div className="canvas-container glass-panel" style={{ padding: 0 }}>
              <Wafer3DScene riskLevel={appState} />
              
              {/* Overlay Text inside 3D Panel */}
              <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 10, color: 'rgba(255,255,255,0.7)', fontFamily: 'Space Grotesk' }}>
                LIVE WAFER SCAN
              </div>
            </div>

            {/* Results Display */}
            <AnimatePresence mode="wait">
              {result && (
                <motion.div 
                  key="result"
                  className="glass-panel"
                  initial={{ opacity: 0, y: 30, height: 0 }}
                  animate={{ opacity: 1, y: 0, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.5, type: "spring" }}
                >
                  <div className="result-display">
                    <div className={`risk-level result-${result.risk_level.toLowerCase()}`}>
                      {result.risk_level === 'LOW' && 'Process Stable'}
                      {result.risk_level === 'MEDIUM' && 'Elevated Risk'}
                      {result.risk_level === 'HIGH' && 'Critical Defect Risk'}
                    </div>
                    
                    <div className={`probability result-${result.risk_level.toLowerCase()}`}>
                      {(result.defect_probability * 100).toFixed(1)}%
                    </div>
                    
                    <div style={{ color: 'var(--text-secondary)', letterSpacing: '1px', textTransform: 'uppercase', fontSize: '0.9rem' }}>
                      Defect Probability
                    </div>

                    <div className="info-grid">
                      <div>
                        <div className="info-label">Prediction</div>
                        <div className="info-value">
                          {result.prediction === 1 ? (
                            <span style={{ color: 'var(--accent-red)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <AlertTriangle size={16} /> DEFECTIVE
                            </span>
                          ) : (
                            <span style={{ color: 'var(--accent-green)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <CheckCircle size={16} /> NORMAL
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <div>
                        <div className="info-label">Risk Threshold</div>
                        <div className="info-value">{result.risk_level}</div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
              
              {error && (
                <motion.div 
                  key="error"
                  className="glass-panel"
                  style={{ borderColor: 'var(--accent-red)', background: 'rgba(255,0,60,0.05)' }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent-red)' }}>
                    <AlertTriangle size={24} />
                    <span style={{ fontFamily: 'Space Grotesk' }}>{error}</span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.aside>
        </main>
      </div>
      
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </>
  );
}

export default App;
