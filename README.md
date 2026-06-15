# performance-lab

A small FastAPI and k6 lab for comparing functional correctness with backend
behavior under increasing concurrency.

## Why this repo exists

An API can keep returning `200 OK` while p95 latency rises and throughput stops
scaling. This repository makes that behavior visible with a controlled local
bottleneck and repeatable test scenarios.

## Local setup

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

`/work` simulates a backend operation with a five-request concurrency limit and
a configurable 150 ms processing delay. To use a different delay:

```bash
WORK_PROCESSING_DELAY_MS=200 uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/work
```

## Execution order

Run the scenarios in this order while the API is running:

1. Functional smoke tests

   ```bash
   pytest -q
   ```

2. Baseline

   ```bash
   k6 run performance/baseline.js
   ```

3. Load

   ```bash
   k6 run performance/load.js
   ```

4. Stress

   ```bash
   k6 run performance/stress.js
   ```

5. Review [the recorded findings](results/FINDINGS.md).

Use `BASE_URL` when the API is running at a different address:

```bash
BASE_URL=http://localhost:8000 k6 run performance/baseline.js
```

## What this demonstrates

This repository demonstrates that functional correctness alone does not
guarantee acceptable runtime behavior. pytest validates the API contract, while
k6 shows how latency and throughput change when demand exceeds capacity.
