# Findings

## Objective

Validate whether an API can remain functionally successful while its runtime
behavior degrades as concurrency exceeds a controlled capacity limit.

## Setup

- FastAPI service and k6 ran locally.
- `GET /work` used a five-request concurrency limit.
- Each work operation used the default 150 ms processing delay.
- Results are approximate values from one local execution.

## Scenarios

| Scenario | Profile | p95 latency | Throughput | Failures |
| --- | --- | ---: | ---: | ---: |
| Baseline | 1 VU for 10s | ~153 ms | ~6.56 req/s | 0% |
| Load | 5 VUs for 30s | ~155 ms | ~32.55 req/s | 0% |
| Stress | Ramp to 20 VUs | ~606 ms | ~30.52 req/s | 0% |

## Observations

- **Latency:** p95 stayed near the 150 ms processing delay at one and five VUs,
  then increased to about 606 ms during stress.
- **Throughput:** throughput scaled from about 6.56 req/s at one VU to 32.55
  req/s at five VUs. Increasing concurrency beyond the configured capacity limit did not produce proportional throughput growth.
- **Errors:** all three runs reported 0% HTTP failures.

## Conclusion

The service continued returning successful responses under stress, but service
quality degraded. Once demand exceeded the five-request capacity, requests
waited for available capacity, p95 latency increased, and throughput no longer scaled proportionally with concurrency. HTTP `200 OK` alone did not describe the system's runtime behavior. Functional validation and runtime validation answer different risks.

## Limitations

- Results depend on the local machine and competing processes.
- The bottleneck is synthetic and intentionally controlled.
- These measurements do not represent production capacity.
- The scenarios ran for limited durations and do not assess long-term behavior.
