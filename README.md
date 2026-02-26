# 📦 MLOps Rolling Signal Pipeline

---

## 📌 Overview

This project implements a minimal, production-style batch data pipeline that demonstrates core MLOps engineering principles:

- Deterministic execution via configuration and seeded randomness  
- Structured logging for observability  
- Machine-readable metrics output  
- Robust input validation and error handling  
- Dockerized, reproducible execution  

The pipeline processes cryptocurrency OHLCV data and generates a binary trading signal based on a rolling mean of the `close` price.

This mirrors real-world trading signal pipelines used in quantitative systems.

---

## 🎯 Objective

The goal of this implementation is to simulate a reproducible and deployment-ready batch job that:

1. Loads configuration from YAML
2. Validates inputs robustly
3. Computes rolling statistics
4. Generates trading signals
5. Outputs structured metrics
6. Logs execution details
7. Runs identically inside Docker

---

## 🧠 Processing Logic

### Step 1 — Load & Validate Configuration

- Reads `config.yaml`
- Validates required fields:
  - `seed`
  - `window`
  - `version`
- Sets deterministic seed:
  
```python
numpy.random.seed(seed)
```

This guarantees reproducibility across runs.

---

### Step 2 — Validate Dataset

The pipeline safely handles:

- Missing input file
- Invalid CSV format
- Empty dataset
- Missing required column (`close`)
- Invalid configuration structure

All errors generate a structured JSON response and exit cleanly.

---

### Step 3 — Rolling Mean Computation

Rolling mean is computed using:

```python
df["rolling_mean"] = df["close"].rolling(window=window).mean()
```

- The first `window-1` rows produce `NaN`
- Signal generation naturally excludes them via comparison logic
- Behavior is deterministic and consistent

---

### Step 4 — Signal Generation

Binary signal logic:

```python
signal = 1 if close > rolling_mean else 0
```

Vectorized implementation:

```python
df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
```

---

### Step 5 — Metrics & Timing

The pipeline computes:

- `rows_processed`
- `signal_rate` (mean of signal column)
- `latency_ms` (total runtime in milliseconds)

Metrics are written to `metrics.json` in both success and error cases.

---

## 📊 Example Output (metrics.json)

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4990,
    "latency_ms": 127,
    "seed": 42,
    "status": "success"
}
```

---

## ❌ Error Output Format

On failure:

```json
{
    "version": "v1",
    "status": "error",
    "error_message": "Description of what went wrong"
}
```

> Metrics file is written in both success and error cases, as required.

---

## 📜 Logging (run.log)

The pipeline logs:

- Job start timestamp
- Configuration validation
- Rows loaded
- Rolling mean computation
- Signal generation
- Metrics summary
- Job completion status
- Any exceptions or validation failures

This ensures full observability.

---

## 📁 Project Structure

```text
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
```

---

## ⚙️ Configuration (config.yaml)

```yaml
seed: 42
window: 5
version: "v1"
```

---

## 🛠 Dependencies

- Python 3.9+
- pandas
- numpy
- pyyaml
- Docker

Install locally:

```bash
pip install -r requirements.txt
```

---

## ▶️ Local Execution

```bash
python run.py \
    --input data.csv \
    --config config.yaml \
    --output metrics.json \
    --log-file run.log
```

No hardcoded paths are used.

---

## 🐳 Docker Execution

### Build Image

```bash
docker build -t mlops-task .
```

### Run Container

```bash
docker run --rm mlops-task
```

Container behavior:

- Includes `data.csv` and `config.yaml`
- Generates `metrics.json`
- Generates `run.log`
- Prints final metrics JSON to stdout
- Exits with code 0 on success
- Exits with non-zero code on failure

---

## 🔁 Reproducibility

The pipeline guarantees deterministic results via:

- Config-driven parameters
- Explicit seed setting
- Controlled runtime environment (Docker)
- No hidden state or randomness

Running the pipeline multiple times produces identical outputs.

---

## 🏗 Design Principles

- Clean CLI interface
- Strict input validation
- Clear separation of configuration and logic
- Structured, machine-readable outputs
- Production-style error handling
- Dockerized deployment
- Deterministic and testable behavior

---

## 🧪 Compliance Checklist

- ✅ No hardcoded paths
- ✅ Deterministic execution
- ✅ Metrics written in success and error cases
- ✅ Docker build and run cleanly
- ✅ Structured logs
- ✅ Structured metrics output
- ✅ Clear documentation