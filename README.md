# 📦 MLOps Rolling Signal Pipeline
---------------
## 📌 Overview

This project implements a miniature MLOps-style batch pipeline that demonstrates:

Deterministic execution using configuration

Structured logging

Rolling mean computation

Signal generation

Machine-readable metrics output

Robust error handling

Dockerized reproducible execution

The pipeline processes cryptocurrency OHLCV data and computes a signal based on rolling averages of the close price.

## 🧠 Pipeline Logic

The application performs the following steps:

Load configuration from config.yaml

Set deterministic random seed

Validate and ingest CSV input

Compute rolling mean on close column

Generate trading signal:

1 if close > rolling_mean

0 otherwise

Compute metrics:

Total rows processed

Signal rate (mean of signals)

Execution latency (ms)

Write structured JSON output

Log all execution steps

## 📁 Project Structure
mlops-rolling-signal-pipeline/
│
├── run.py
├── config.yaml
├── requirements.txt
├── Dockerfile
├── README.md
├── data.csv
├── metrics.json
└── run.log
## ⚙️ Configuration (config.yaml)
seed: 42
window: 5
version: "v1"
## 🛠 Dependencies

Python 3.10+

pandas

numpy

pyyaml

## Docker

Install locally using:
```bash
pip install -r requirements.txt
```
## ▶️ Local Execution

Run the pipeline locally:

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
## 🐳 Docker Execution (Recommended)
Build Docker Image
```bash
docker build -t mlops-pipeline .
```
Run Container
```bash
docker run --rm mlops-pipeline
```
The container:

Executes automatically on startup

Generates metrics.json

Generates run.log

Prints metrics JSON to stdout

Exits with code 0 on success

📊 Example Output (metrics.json)
{
    "version": "v1",
    "rows_processed": 8,
    "metric": "signal_rate",
    "value": 0.5,
    "latency_ms": 25,
    "seed": 42,
    "status": "success"
}
## 📜 Logging

Logs are written to run.log and include:

Job start timestamp

Configuration verification

Data ingestion details

Rolling mean calculation

Signal generation

Metrics summary

Job completion status

Error reporting (if applicable)

## ❌ Error Handling

The pipeline gracefully handles:

Missing input file

Invalid CSV format

Empty CSV file

Missing close column

Invalid configuration structure

On error, a structured JSON response is returned:

{
    "version": "v1",
    "status": "error",
    "error_message": "Description of the issue"
}
## 🔁 Reproducibility

Deterministic execution via fixed random seed

Config-driven parameters

Fully containerized environment

No hardcoded file paths

Running the pipeline multiple times produces identical results.

## 🏗 Design Principles

Clean CLI interface

Separation of configuration and logic

Observability through structured logging

Machine-readable metrics

Production-style error handling

Docker-based reproducibility
