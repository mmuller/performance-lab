# performance-lab

Small lab for validating backend behavior under load.

The goal is to compare functional correctness with runtime behavior using pytest smoke checks and k6 scenarios.

Core idea: an API can keep returning 200 OK while p95 latency rises and throughput stops scaling under pressure.

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

Run the smoke tests:

```bash
pytest -q
```

Run the k6 baseline while the API is running:

```bash
k6 run performance/baseline.js
```

Use `BASE_URL` when the API is running at a different address:

```bash
BASE_URL=http://localhost:8000 k6 run performance/baseline.js
```

The baseline sends requests from one virtual user for 10 seconds. It confirms
that `/work` remains functionally correct at minimal traffic and establishes a
local reference point before adding load or stress scenarios.
