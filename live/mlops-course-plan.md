# MLOps Course Plan — DataBees Interns 2026

A professional, industry-grade curriculum aligned with what companies actually hire for (ML Engineer, MLOps Engineer, Data Scientist + deployment skills).

---

## Course Overview

**Title:** MLOps: From Experiment to Production
**Duration:** 8 weeks (1–2 sessions/week)
**Track:** ML Track (Vivek Prasad)
**Outcome:** Intern can deploy, monitor, and maintain ML models in production like a junior MLOps Engineer

---

## Module Breakdown

### Module 1 — MLOps Foundations (Week 1)

**Why companies need this:** Every ML team wastes months rebuilding infra. MLOps standardizes it.

- What is MLOps? (vs DevOps, DataOps)
- The ML Lifecycle: experiment → staging → production → monitoring
- Key pain points in production ML (model drift, reproducibility, versioning)
- Tool landscape overview: MLflow, DVC, Kubeflow, Vertex AI, SageMaker, Databricks MLflow

**Deliverable:** Written comparison of 2 MLOps tools (e.g., MLflow vs SageMaker)

---

### Module 2 — Experiment Tracking & Model Registry (Week 2)

**Why companies need this:** Teams can't reproduce results without it. A top interview question.

- MLflow: tracking runs, logging params/metrics/artifacts
- Model versioning and the Model Registry (Staging → Production lifecycle)
- Comparing experiments across runs
- Databricks-specific: Unity Catalog Model Registry

**Deliverable:** Train any model, log to MLflow, promote to Production stage

---

### Module 3 — Data & Feature Engineering in Production (Week 3)

**Why companies need this:** 80% of ML failures are data problems, not model problems.

- Feature Stores: what, why, when (Databricks Feature Store, Feast)
- Data versioning with DVC
- Data validation with Great Expectations / Pandera
- Handling data drift at ingestion

**Deliverable:** Build a feature store table in Databricks for a sample dataset

---

### Module 4 — Model Packaging & Serving (Week 4)

**Why companies need this:** A model in a notebook is not a product.

- Serialization: pickle, ONNX, MLflow `pyfunc`
- Serving patterns: batch inference vs real-time REST API
- MLflow Model Serving / Databricks Model Serving endpoints
- Containers: Docker basics for ML (packaging your model as an image)
- FastAPI as a lightweight serving layer

**Deliverable:** Deploy a model as a REST endpoint, call it with a Python client

---

### Module 5 — CI/CD for ML (Week 5)

**Why companies need this:** No serious team ships models manually.

- What is CI/CD in the ML context
- GitHub Actions: run training + tests on every PR
- Automated model evaluation gates (only promote if accuracy > threshold)
- MLflow + GitHub Actions integration
- Introduction to ML pipelines (Databricks Workflows / Jobs)

**Deliverable:** GitHub Actions workflow that trains, evaluates, and registers a model automatically

---

### Module 6 — Orchestration & ML Pipelines (Week 6)

**Why companies need this:** Production ML is a pipeline, not a script.

- Pipeline thinking: data ingestion → feature engineering → training → evaluation → serving
- Databricks Workflows (Jobs + Task dependencies)
- Intro to Airflow / Prefect (concept level)
- Triggering pipelines on schedule and on data arrival

**Deliverable:** Build an end-to-end Databricks Workflow with 4+ tasks

---

### Module 7 — Model Monitoring & Observability (Week 7)

**Why companies need this:** Models degrade silently. Monitoring is how you catch it.

- Types of drift: data drift, concept drift, prediction drift
- Statistical tests: KS test, PSI (Population Stability Index)
- Lakehouse Monitoring (Databricks native)
- Setting alerts when metrics degrade
- Logging predictions for retraining feedback loops

**Deliverable:** Set up a monitoring dashboard for a live model endpoint

---

### Module 8 — Capstone Project (Week 8)

**End-to-end MLOps project, production-grade**

Interns build and present a complete pipeline:

1. Raw dataset → feature engineering → model training
2. All logged to MLflow, promoted via Model Registry
3. Deployed as a REST endpoint
4. CI/CD with GitHub Actions
5. Monitoring dashboard with drift alerts

**Deliverable:** Demo + 5-minute presentation to mentors

---

## Skills Matrix (What Companies Hire For)

| Skill | Module | Industry Relevance |
|---|---|---|
| MLflow experiment tracking | 2 | Very High — almost universal |
| Model Registry & versioning | 2 | High |
| Feature Stores | 3 | High (Uber, LinkedIn, Airbnb pioneered this) |
| Docker / model packaging | 4 | Very High |
| REST model serving | 4 | Very High |
| CI/CD for ML | 5 | High — growing fast |
| Pipeline orchestration | 6 | High |
| Drift monitoring | 7 | High — often the gap in junior hires |

---

## Tools Stack

| Category | Tool |
|---|---|
| Experiment tracking | MLflow (Databricks) |
| Data versioning | DVC |
| Serving | Databricks Model Serving, FastAPI |
| CI/CD | GitHub Actions |
| Orchestration | Databricks Workflows |
| Monitoring | Databricks Lakehouse Monitoring |
| Containers | Docker (basics) |
| Language | Python |

---

## Job Titles This Prepares For

- MLOps Engineer (most direct fit)
- ML Engineer (model serving + pipelines focus)
- Data Scientist (who can actually ship to production)
- AI Platform Engineer
