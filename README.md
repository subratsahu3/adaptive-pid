# AdaptivePID: Dynamic Concurrency Regulator

A production-grade, closed-loop PID admission controller based on Little's Law ($L = \lambda W$) to prevent cascading brownouts in distributed microservices.

## Features
- **Continuous Latency Feedback:** Modulates concurrency limits according to gradient RTT deviations.
- **Anti-Windup Integral Clamping:** Prevents overshoot and runaway oscillatory throttling.
- **Microsecond Overhead:** Single-digit microsecond evaluation per request cycle.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com
