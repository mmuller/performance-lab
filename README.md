# performance-lab

Small lab for validating backend behavior under load.

The goal is to compare functional correctness with runtime behavior using pytest smoke checks and k6 scenarios.

Core idea: an API can keep returning 200 OK while p95 latency rises and throughput stops scaling under pressure.