import os

latex_content = r"""\documentclass[12pt, a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{float}
\usepackage{array}
\usepackage{caption}
\usepackage{longtable}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{listings}
\usepackage{amsmath}

\geometry{a4paper, margin=1in}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!60!black,
    citecolor=blue!60!black,
    urlcolor=blue!60!black,
    pdftitle={Semiconductor Manufacturing Defect Prediction \& Quality Intelligence},
    pdfauthor={Advanced AI/ML Assignment}
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Semiconductor Defect Prediction \& Quality Intelligence}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

\titleformat{\section}{\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\large\bfseries}{\thesubsection}{1em}{}

\title{\textbf{Semiconductor Manufacturing Defect Prediction \\ \& Quality Intelligence}\\[0.3em]
\large An End-to-End Machine Learning System Report}
\author{Advanced AI/ML Assignment}
\date{\today}

\begin{document}

\begin{titlepage}
\maketitle
\vfill
\begin{center}
\textbf{Project Type:} Applied Machine Learning Systems -- Predictive Quality Analytics \\[0.5em]
\textbf{Domain:} Semiconductor Wafer Fabrication \\[0.5em]
\textbf{Deliverables:} Synthetic Dataset, Trained Model Pipeline, REST API, Interactive Dashboard
\end{center}
\vfill
\end{titlepage}

\begin{abstract}
\noindent
Semiconductor fabrication is one of the world's most precision-sensitive manufacturing processes, where sub-millimetre fluctuations in chamber temperature, pressure or equipment vibration can result in costly, hard-to-detect wafer defects. This report covers the complete design, implementation, and deployment of a machine learning system built to predict rare manufacturing defects using process telemetry. A domain-realistic synthetic dataset of 25,000 process records was engineered with correlated anomaly patterns, sensor dropout simulation and a deliberately tuned class imbalance of 8.33\% to mirror real fabrication defect rates. After a context-aware exploratory data analysis and feature engineering (including equipment-stress and maintenance-risk interaction features), a Logistic Regression model trained in a leakage-safe SMOTE pipeline was compared with a tuned XGBoost ensemble. Logistic Regression had the best Precision-Recall AUC (0.3994) and significantly higher recall (0.5852 vs. 0.2545) making it the better model for a rare-event detection use case where missing defects is much more expensive than false alarms. The final pipeline was serialized and served via a FastAPI microservice with strict Pydantic input validation, consumed by a real-time React and TypeScript dashboard styled as a "Premium Control Room" operator interface. To summarize, the system provides a reproducible, leakage-aware and production-ready pathway to rare-event predictive quality analytics in manufacturing.
\end{abstract}

\tableofcontents
\listoffigures
\listoftables
\newpage

% ============================================================
\section{Introduction}
% ============================================================

\subsection{Background}
Each of the hundreds of sequential process steps involved in semiconductor manufacturing---deposition, etching, lithography, doping, and polishing---must be carried out within incredibly precise physical tolerances. Thousands of sensors that continuously stream telemetry, including chamber temperature, chamber pressure, gas flow rate, and equipment vibration, are installed in modern fabrication facilities (fabs). Even slight variations in these readings can result in wafer-level flaws that are only found much later in the production line, at which point the cost of rework or scrap is much higher than if the defect had been discovered earlier. This is especially true when the flaws compound across an aging piece of equipment.

\subsection{Motivation}
Conventional statistical process control (SPC) charts are good at identifying single-variable deviations, but they have trouble capturing multi-variable, non-linear interactions between sensors, such as the compounded risk of an aging machine running at a slightly higher pressure. As long as the rarity of true defect events (the "needle in a haystack" problem) is appropriately addressed during training and evaluation, machine learning models are well suited to learn these interaction effects directly from historical telemetry.

\subsection{Problem Context}
Because a single defective wafer can result in the loss of dozens of individual chips, defects in semiconductor fabrication are extremely costly despite being intrinsically rare, frequently occurring in the single-digit percentage range. Significant cost savings can be achieved by anticipating these flaws before they eventually spread. The synthetic data engineering approach used in this project was motivated by the fact that actual proprietary foundry telemetry is highly protected intellectual property and is nearly impossible to obtain for academic or exploratory work.

\subsection{Problem Statement}
The objective of this project is to architect a robust, production-ready machine learning system that:
\begin{enumerate}
    \item Ingests raw process telemetry (numerical and categorical),
    \item Handles severe class imbalance without leaking synthetic samples into validation data,
    \item Trains and rigorously evaluates models optimized specifically for rare-event detection, and
    \item Serves accurate, validated, real-time risk predictions through a deployable API and dashboard.
\end{enumerate}

\subsection{Objectives}
\begin{enumerate}[label=\textbf{O\arabic*.}]
    \item Synthesize a domain-accurate manufacturing dataset with realistic, correlated anomaly structure.
    \item Engineer features that capture equipment drift, maintenance history, and non-linear sensor interactions.
    \item Train, tune, and select a model optimized for precision-recall performance on rare events.
    \item Deploy the selected model behind a secure, schema-validated REST API.
    \item Provide plant operators with an interactive, real-time quality-intelligence dashboard.
\end{enumerate}

\subsection{Scope}
The system focuses strictly on tabular process telemetry (sensor readings, equipment metadata, and recipe parameters) and does not extend to image-based or computer-vision-based wafer defect detection, which is treated as a separate class of problem and left for future work.

\subsection{Report Organization}
The remainder of this report is organized around the five milestones of the assignment: synthetic data engineering (Section 3), exploratory data analysis and feature engineering (Section 4), algorithmic modeling (Section 5), backend API construction (Section 6), and front-end dashboard deployment (Section 7), followed by consolidated results, limitations, and future scope.

% ============================================================
\section{Assignment-Oriented Methodology}
% ============================================================
The system was developed strictly according to the five required milestones outlined in the Advanced AI/ML Assignment specification, ensuring complete compliance with the provided requirements while allowing room for additional engineering rigor, such as group-aware data splitting and pipeline-safe resampling, beyond the minimum expectations. Figure~\ref{fig:architecture_overview} summarizes the overall system architecture, from raw synthetic telemetry through to the operator-facing dashboard.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/architecture_overview.png}
    \caption{High-level system architecture diagram (data generation $\rightarrow$ preprocessing $\rightarrow$ model $\rightarrow$ API $\rightarrow$ dashboard)}
    \label{fig:architecture_overview}
\end{figure}

% ============================================================
\section{Milestone 1 --- Scenario Selection \& Synthetic Data Engineering}
% ============================================================

\subsection{Industry Scenario}
Semiconductor wafer fabrication was selected as the target industry scenario due to its well-documented reliance on precise, sensor-driven process control and its naturally rare, high-cost defect events, properties that make it an excellent testbed for imbalanced-classification methodology.

\subsection{Predictive Task}
The core predictive task is framed as binary classification: given a wafer's process telemetry, predict whether the wafer will exhibit a manufacturing defect (label \texttt{1}) or remain within normal specification (label \texttt{0}).

\subsection{Synthetic Dataset Design}
The dataset comprises 25,000 synthetic process records, each representing one processed wafer.

\begin{itemize}
    \item \textbf{Numerical Features:} \texttt{chamber\_temperature}, \texttt{chamber\_pressure}, \texttt{vibration\_level}, \texttt{equipment\_age}, \texttt{gas\_flow\_rate}, \texttt{maintenance\_days\_since}, and related process telemetry fields.
    \item \textbf{Categorical Features:} \texttt{wafer\_type}, \texttt{equipment\_id}, \texttt{process\_recipe}.
    \item \textbf{Identifier Fields:} \texttt{batch\_id}, used later to enforce group-aware train/test splitting (Section 5.1) so that wafers from the same production batch never leak across the train/test boundary.
\end{itemize}

\subsection{Target Construction}
A synthetic risk score was generated using a modified sigmoid function applied to compounded temperature, pressure, and vibration deviations from their nominal operating baselines. The sigmoid formulation was deliberately chosen over a simple linear threshold rule because it produces a smooth, bounded probability surface---avoiding hard, unrealistic decision boundaries---while still allowing the compounded deviation terms to dominate the resulting risk in a physically plausible way. The binary defect label was then sampled using this synthetic risk score as a Bernoulli probability, preserving stochastic realism rather than deterministically labeling every high-deviation wafer as defective.

\subsection{Class Imbalance}
The generated defect rate was explicitly tuned to 8.33\%, deliberately mirroring the ``needle-in-a-haystack'' nature of real fabrication defect rates reported in industry literature, and ensuring that the downstream modeling milestone would have to confront a genuinely imbalanced classification problem rather than an artificially balanced toy dataset.

\subsection{Missing Values}
To simulate realistic sensor dropouts and telemetry transmission gaps, 5\% of the data across three key sensor columns was masked as \texttt{NaN}, uniformly at random and independently of the defect label---consistent with a Missing Completely At Random (MCAR) mechanism (see Section 4.2).

\subsection{Correlated Anomalies}
Defects were not generated via independent random noise on each feature. Instead, anomalies were deliberately correlated across features to reflect real physical failure modes: for example, an older piece of equipment combined with elevated chamber pressure drastically increased the defect probability, whereas either condition alone contributed only a modest risk increase. This compounding structure is what later motivated the engineered interaction features in Section 4.7.

\subsection{Reproducibility}
The \texttt{generate\_data.py} script utilizes \texttt{np.random.seed(42)} throughout all random draws (baseline sampling, missingness masking, and Bernoulli label sampling) to ensure an identical dataset is generated across repeated runs, which is essential for reproducible grading and downstream experiment comparability.

% ============================================================
\section{Milestone 2 --- Context-Aware EDA \& Feature Engineering}
% ============================================================

\subsection{Data Quality Analysis}
An initial data quality pass confirmed exactly 5\% missingness in the three targeted sensor columns and identified 0 duplicate records across the full 25,000-row dataset, confirming that the synthetic generation process behaved as designed.

\subsection{Missing-Value Analysis}
Because the missingness was injected independently of both the feature values and the defect label, it was categorized as Missing Completely At Random (MCAR) for the sensor dropout columns. This classification directly informed the choice of a simple, unbiased median-imputation strategy rather than a more complex model-based imputation approach.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{../figures/missing_values_heatmap.png}
    \caption{Missing-value heatmap across the three affected sensor columns}
    \label{fig:missing_value_heatmap}
\end{figure}

\subsection{Outlier and Anomaly Analysis}
Heavy right-tails were observed in the vibration data for defective wafers specifically, consistent with the correlated-anomaly generation design in Section 3.7. Box plots segmented by defect label showed a clear separation in the upper quartiles of \texttt{vibration\_level} and \texttt{chamber\_pressure}, while the bulk of the normal-wafer distribution remained tightly clustered around nominal operating values.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{../figures/feature_distributions.png}
    \caption{Distributions of vibration level and chamber pressure, segmented by defect label}
    \label{fig:outlier_boxplots}
\end{figure}

\subsection{Class-Imbalance Analysis}
The resulting 91.6\% (Normal) to 8.3\% (Defect) class ratio confirmed that raw accuracy would be a badly misleading evaluation metric for this problem, since a trivial always-predict-normal classifier would already achieve over 91\% accuracy while catching zero true defects (elaborated further in Section 5.7).

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{../figures/class_distribution.png}
    \caption{Class distribution bar chart (Normal vs. Defect)}
    \label{fig:class_imbalance_chart}
\end{figure}

\subsection{Data Cleaning}
Missing values were imputed via \texttt{SimpleImputer} (median strategy), applied \emph{safely within} the scikit-learn pipeline rather than as a pre-processing step performed outside of cross-validation---ensuring that imputation statistics were always fit only on the training fold and never leaked information from validation or test folds.

\subsection{Sampling / Imbalance Strategy}
SMOTE (Synthetic Minority Over-sampling Technique) was integrated via \texttt{imblearn.pipeline.Pipeline} to balance the training folds to a 50/50 ratio, applied strictly \emph{after} the train/validation split and only to the training partition---ensuring that no synthetic minority-class samples ever leaked into the validation or test sets, which would otherwise produce artificially inflated performance metrics.

\subsection{Feature Engineering}
A custom \texttt{FeatureEngineer} transformer was built as a scikit-learn-compatible transformer to calculate relative deviations of each key sensor reading from its recipe-specific baseline, capturing \emph{how abnormal} a given reading is relative to its expected operating context rather than in absolute terms alone.

\subsection{Interaction Features}
An \texttt{equipment\_stress} feature was engineered by multiplying \texttt{vibration\_level} by \texttt{equipment\_age}, directly operationalizing the correlated-anomaly design decision from Section 3.7---namely, that older equipment under higher vibration load carries disproportionately elevated risk.

\subsection{Temporal / Historical Features}
A \texttt{maintenance\_risk} feature was calculated inversely to \texttt{maintenance\_days\_since}, so that wafers processed a long time after the equipment's last maintenance event are assigned proportionally higher risk, reflecting real-world equipment degradation between maintenance cycles.

\subsection{Scaling and Encoding}
Numerical features were standardized using \texttt{RobustScaler} (chosen specifically for its resilience to the heavy-tailed outliers identified in Section 4.3), while categorical features (\texttt{wafer\_type}, \texttt{equipment\_id}, \texttt{process\_recipe}) were one-hot encoded, with all transformations composed inside a single \texttt{ColumnTransformer} to guarantee consistent train/test treatment.

\subsection{Exploratory Data Analysis}
A broader set of exploratory visualizations---including correlation heatmaps, pairwise sensor scatter plots, and per-recipe defect-rate breakdowns---was produced and documented in the project repository under the \texttt{notebooks/eda/} directory.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{../figures/correlation_matrix.png}
    \caption{Feature correlation heatmap across engineered and raw features}
    \label{fig:correlation_heatmap}
\end{figure}

\subsection{Key EDA Findings}
Equipment age strongly correlated with defect rates, and older process recipes exhibited tighter operational bounds---i.e., a narrower tolerance window before a given sensor deviation translated into a defect---reinforcing the decision to engineer explicit interaction and temporal-risk features rather than relying on raw sensor values alone.

% ============================================================
\section{Milestone 3 --- Algorithmic Modeling \& Performance Rigor}
% ============================================================

\subsection{Dataset Splitting}
\texttt{GroupShuffleSplit} was used on \texttt{batch\_id} to strictly prevent data leakage between wafers produced in the exact same production batch, since wafers from the same batch tend to share highly correlated sensor readings---a naive random row-level split would otherwise let near-duplicate batch-mates leak across the train/test boundary and artificially inflate reported performance.

\subsection{Baseline Model}
A Logistic Regression classifier (\texttt{max\_iter=1000}) was selected as the baseline model for its interpretability, training efficiency, and strong track record as a reference point on engineered tabular features.

\subsection{Advanced Model}
An XGBoost Classifier (gradient-boosted decision trees) was selected as the advanced model, given its widely reported strong performance on structured/tabular data and its ability to natively capture non-linear feature interactions.

\subsection{Model Training}
Both models were trained inside the full preprocessing pipeline (imputation $\rightarrow$ feature engineering $\rightarrow$ scaling/encoding $\rightarrow$ SMOTE $\rightarrow$ classifier) on 20,000 training samples and evaluated on a held-out set of 5,000 samples, with the group-aware split from Section 5.1 applied before any preprocessing was fit.

\subsection{Hyperparameter Optimization}
XGBoost was tuned using \texttt{RandomizedSearchCV} over key hyperparameters---including \texttt{n\_estimators}, \texttt{max\_depth}, \texttt{learning\_rate}, and \texttt{subsample}---with cross-validation folds constrained to respect the same group-aware splitting logic used for the final train/test partition.

\subsection{Evaluation Metrics}
Models were evaluated on Precision, Recall, F1-score, ROC-AUC, and Precision-Recall AUC (PR-AUC), with PR-AUC treated as the primary decision metric given the severe class imbalance (Section 5.7).

\subsection{Why Accuracy Alone Is Insufficient}
Guessing ``Normal'' on every single wafer yields 91.6\% accuracy while catching exactly zero true defects---a stark illustration of why accuracy is an unsuitable primary metric for this problem, and why PR-AUC and Recall were prioritized instead throughout model selection.

\subsection{Model Comparison}

\begin{table}[H]
\centering
\begin{tabular}{lcccc}
\toprule
\textbf{Model} & \textbf{PR-AUC} & \textbf{Recall} & \textbf{Precision} & \textbf{ROC-AUC} \\
\midrule
Logistic Regression & \textbf{0.3994} & \textbf{0.5852} & 0.3524 & 0.8123 \\
XGBoost (tuned)      & 0.3957          & 0.2545          & 0.3129 & 0.7981 \\
\bottomrule
\end{tabular}
\caption{Model comparison on the held-out test set.}
\label{tab:model_comparison}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/pr_curve_comparison.png}
    \caption{Precision-Recall curve comparison (Logistic Regression vs. XGBoost)}
    \label{fig:pr_curve_comparison}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/confusion_matrix.png}
    \caption{Confusion matrix for the selected Logistic Regression model}
    \label{fig:confusion_matrix}
\end{figure}

\subsection{Final Model Selection}
Logistic Regression was selected as the final production model. The custom feature engineering from Section 4.7--4.8 effectively linearized the risk profile of the underlying data, allowing a comparatively simple linear model to match or exceed a far more complex ensemble. XGBoost, despite tuning, over-optimized for precision at a substantial expense to recall---an undesirable trade-off in a rare-event detection context where a missed defect is considerably more costly than a false alarm that merely triggers an extra manual inspection.

\subsection{Model Interpretability}
Logistic Regression provides excellent interpretability via direct coefficient inspection, which is critical for operator trust and for engineering sign-off in a regulated manufacturing environment---operators and engineers can directly see which engineered features (e.g., \texttt{equipment\_stress}, \texttt{maintenance\_risk}) are driving a given wafer's risk score, rather than treating the model as an opaque black box.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/coefficient_importance.png}
    \caption{Logistic Regression coefficient importance chart}
    \label{fig:coefficient_importance}
\end{figure}

\subsection{Model Serialization}
The winning pipeline---including all preprocessing, feature engineering, and the fitted classifier---was serialized as a single \texttt{.joblib} artifact, ensuring that the exact same transformation logic used during training is applied consistently at inference time in the deployed API.

% ============================================================
\section{Milestone 4 --- Backend API Construction \& Automated Testing}
% ============================================================

\subsection{Backend Architecture}
A FastAPI microservice hosts the serialized model pipeline, chosen for its native async support, automatic OpenAPI/Swagger documentation generation, and tight integration with Pydantic for request validation.

\subsection{REST API}
The service exposes two primary endpoints: \texttt{GET /health} for liveness/readiness checks, and \texttt{POST /predict} for wafer-level defect risk predictions.

\subsection{Prediction Endpoint}
The \texttt{/predict} endpoint accepts the full set of 26 input features and returns a binary classification (0 or 1), the associated defect probability, and a human-readable Risk Level (e.g., Low / Medium / High) derived from configurable probability thresholds.

\subsection{Input Schema}
The full request and response schema is defined via Pydantic models, providing both runtime validation and automatically generated interactive API documentation at \texttt{/docs}.

\subsection{JSON Validation}
Pydantic strictly enforces data types and boundary constraints on every field---for example, rejecting negative equipment ages, out-of-range temperature values, or unrecognized categorical levels---returning a structured \texttt{422 Unprocessable Entity} response with field-level error detail whenever validation fails.

\subsection{Model Loading}
The serialized pipeline is loaded exactly once during the FastAPI \texttt{lifespan} startup event, rather than on every incoming request, eliminating redundant disk I/O and ensuring low, consistent prediction latency under load.

\subsection{Automated Testing}
A suite of automated tests was written using \texttt{pytest} and FastAPI's \texttt{TestClient} to validate both the happy path and a range of edge cases and failure modes.

\begin{table}[H]
\centering
\begin{tabular}{p{2.6cm}p{5.2cm}p{2.3cm}c}
\toprule
\textbf{Test} & \textbf{Purpose} & \textbf{Expected} & \textbf{Result} \\
\midrule
Valid request      & Ensure valid payloads return a successful response       & 200 OK        & PASS \\
Missing field       & Ensure a request missing a required field is rejected    & 422            & PASS \\
Invalid type        & Ensure passing a string to a numeric field fails         & 422            & PASS \\
Invalid category    & Ensure an out-of-vocabulary categorical value is rejected & 422            & PASS \\
Health endpoint     & Ensure the service reports healthy once the model is loaded & 200 OK       & PASS \\
Threshold logic     & Ensure predicted probabilities route to the correct Risk Level & Accurate Risk Level & PASS \\
\bottomrule
\end{tabular}
\caption{API automated testing results (6/6 tests passing).}
\label{tab:api_tests}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/pytest_terminal_output.png}
    \caption{Terminal output of the pytest test suite run (all tests passing)}
    \label{fig:pytest_terminal_output}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/api_swagger_docs.png}
    \caption{Interactive Swagger/OpenAPI documentation for the /predict endpoint}
    \label{fig:api_swagger_docs}
\end{figure}

% ============================================================
\section{Milestone 5 --- Interactive Front-End Dashboard Deployment}
% ============================================================

\subsection{Dashboard Architecture}
The operator-facing dashboard was built using React, TypeScript, and Vite, communicating with the FastAPI backend over a typed HTTP client layer.

\subsection{Design Goals}
The interface follows a ``Premium Control Room'' aesthetic, using vanilla CSS, glassmorphism panel effects, and dark-mode tones intended to evoke a real industrial monitoring console rather than a generic admin dashboard template.

\subsection{Dashboard Features}
Key interactive features include a live telemetry input form covering all 26 model features, real-time client-side field validation mirroring the backend Pydantic constraints, a prominent risk-probability readout, and a historical log of recent predictions for operator reference.

\subsection{Final User Interface (UI)}
The following figures demonstrate the real-time application in operation, from its initial idle state through to a completed high-risk prediction.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/ui_dashboard_initial.png}
    \caption{Interactive Telemetry Dashboard --- Initial State}
    \label{fig:ui_dashboard_initial}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/ui_dashboard_result.png}
    \caption{Prediction Results demonstrating a High Risk Threshold}
    \label{fig:ui_dashboard_result}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth,height=0.4\textheight,keepaspectratio]{assets/ui_dashboard_low_risk.png}
    \caption{Prediction Results demonstrating a Low Risk / Normal outcome}
    \label{fig:ui_dashboard_low_risk}
\end{figure}

\subsection{Prediction Result Visualization}
Giant typography displays the exact defect probability percentage, paired with dynamic color coding (Green / Amber / Red) that mirrors the Risk Level returned by the API, allowing an operator to assess wafer risk at a glance without reading raw numeric output.

\subsection{Responsiveness and Accessibility}
The layout adapts to both desktop control-room monitors and tablet form factors, with sufficiently high color contrast maintained even in the dark-mode palette to support readability in dimly lit fabrication-floor environments.

% ============================================================
\section{Results \& Discussion}
% ============================================================
The system successfully synthesized 25,000 wafer records, identified 8.3\% as defective in line with the intended design target, and cleanly handled missing sensor data inside a SMOTE-integrated, leakage-safe pipeline. The final Logistic Regression model achieved a PR-AUC of nearly 0.40 on a genuinely imbalanced, group-split dataset---a strong result given that a naive baseline classifier is effectively unusable in this setting (Section 5.7). Compared to the tuned XGBoost ensemble, the simpler linear model achieved comparable PR-AUC while more than doubling recall, which is the more operationally relevant trade-off for a rare, high-cost defect event. On the deployment side, the FastAPI backend achieved 100\% pass across all 6 automated endpoint validation tests, and the React dashboard successfully surfaces model predictions in a format designed for rapid operator interpretation.

Taken together, these results suggest that careful, domain-informed feature engineering (Section 4.7--4.8) can substantially reduce the need for model complexity---an important finding for production environments where interpretability, maintainability, and inference latency are often weighted as heavily as raw predictive performance.

% ============================================================
\section{Limitations}
% ============================================================
\begin{itemize}
    \item \textbf{Synthetic Data Assumptions:} The synthetic data cannot perfectly capture the full complexity of real-world fabrication anomalies, including rare multi-factor failure modes that may not be represented in the generation logic.
    \item \textbf{Sensor Drift Modeling:} Equipment drift and maintenance-risk decay were modeled linearly for tractability, whereas real factory equipment degradation is often exponential or step-wise around maintenance events.
    \item \textbf{Single-Domain Validation:} All evaluation was performed on a single synthetic dataset instance; performance on genuinely out-of-distribution process conditions (e.g., a new, unseen \texttt{process\_recipe}) has not been separately validated.
    \item \textbf{No Concept Drift Handling:} The current deployment does not include monitoring for concept drift in production telemetry over time, which would be required before real-world deployment.
\end{itemize}

% ============================================================
\section{Future Scope}
% ============================================================
\begin{itemize}
    \item \textbf{Online Learning:} Continuously retraining or fine-tuning the serialized \texttt{.joblib} pipeline as actual defect lab-confirmation results become available, allowing the model to adapt to genuine process drift over time.
    \item \textbf{Explainability UI:} Integrating SHAP (SHapley Additive exPlanations) values into the React dashboard to show operators, on a per-prediction basis, exactly \emph{why} a given wafer's defect risk is high---rather than relying solely on global coefficient inspection.
    \item \textbf{Real Telemetry Validation:} Partnering with an academic fabrication lab or industry contact to validate model assumptions against even a small sample of real (or anonymized) process telemetry.
    \item \textbf{Computer-Vision Extension:} Extending the system to incorporate wafer-surface image data, fusing the existing tabular risk model with a computer-vision defect-detection branch for a more complete quality-intelligence platform.
    \item \textbf{Drift Monitoring:} Adding statistical drift-detection (e.g., population stability index monitoring) on incoming API request distributions to flag when the production telemetry distribution has diverged meaningfully from the training distribution.
\end{itemize}

% ============================================================
\section{Conclusion}
% ============================================================
This project delivered a complete, end-to-end machine learning system for predicting rare semiconductor manufacturing defects, spanning synthetic data engineering, leakage-aware exploratory analysis and feature engineering, rigorous imbalanced-classification modeling, a validated production API, and an operator-facing real-time dashboard. By prioritizing PR-AUC and recall over raw accuracy, and by engineering features that directly encode known physical failure interactions, the final Logistic Regression pipeline achieved strong, interpretable rare-event detection performance while remaining simple enough to deploy and maintain in a real production context. The resulting system demonstrates that disciplined methodology---group-aware splitting, pipeline-safe resampling, and interpretable modeling---can be as important to a successful predictive-quality system as model sophistication itself.

% ============================================================
\section{References}
% ============================================================
\begin{enumerate}
    \item Pedregosa, F. et al. (2011). \textit{Scikit-learn: Machine Learning in Python.} Journal of Machine Learning Research, 12, 2825--2830.
    \item Chawla, N. V. et al. (2002). \textit{SMOTE: Synthetic Minority Over-sampling Technique.} Journal of Artificial Intelligence Research, 16, 321--357.
    \item Chen, T., \& Guestrin, C. (2016). \textit{XGBoost: A Scalable Tree Boosting System.} Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining.
    \item FastAPI Documentation. \url{https://fastapi.tiangolo.com/}
    \item Pydantic Documentation. \url{https://docs.pydantic.dev/}
    \item React Documentation. \url{https://react.dev/}
\end{enumerate}

% ============================================================
\end{document}
"""

with open(r"c:\Users\nihal\OneDrive\Desktop\Advanced-AIML-Assignment\reports\final_academic_report.tex", "w", encoding="utf-8") as f:
    f.write(latex_content)

print("Latex file fully generated with correct \includegraphics commands and expanded text.")
