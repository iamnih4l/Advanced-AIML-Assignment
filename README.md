# Advanced AI/ML Assignment
**Semiconductor Manufacturing Defect Prediction & Quality Intelligence**

This repository contains an end-to-end Machine Learning system that predicts manufacturing defects in semiconductors based on process telemetry and environmental conditions.

## 🚀 How to Run the System

To run the full end-to-end system (Backend API + Frontend Dashboard):

1. **Start the FastAPI Backend**
   Open a terminal in the root directory:
   ```bash
   pip install -r requirements.txt
   uvicorn backend.app.main:app --reload --port 8000
   ```

2. **Start the React Frontend**
   Open a second terminal in the root directory:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access the Dashboard**
   Open your browser and navigate to the URL provided by Vite (typically `http://localhost:5173`).

---

## 🏗️ Architecture & Modules

The system is built in 5 distinct milestones:
- **M1:** Synthetic Data Generation
- **M2:** EDA & Feature Engineering (with SMOTE)
- **M3:** Algorithmic Modeling (Logistic Regression & XGBoost)
- **M4:** FastAPI Backend & Pytest
- **M5:** React & Vite Dashboard

Please refer to the `docs/` folder for detailed documentation on each milestone.
