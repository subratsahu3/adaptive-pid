"""AdaptivePID: Dynamic Concurrency Regulator using Little's Law & Control Theory."""

import time


class AdaptivePIDLimiter:
    """
    Adaptive admission controller replacing static threshold circuit breakers.
    Continuously modulates inflight concurrency window based on measured round-trip time.
    """

    def __init__(
        self,
        target_rtt_ms: float = 50.0,
        kp: float = 0.5,
        ki: float = 0.05,
        kd: float = 0.02,
        min_limit: float = 2.0,
        max_limit: float = 500.0,
    ):
        self.target_rtt = float(target_rtt_ms)
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.min_limit = float(min_limit)
        self.max_limit = float(max_limit)

        self.limit = self.min_limit * 2.0
        self.integral = 0.0
        self.prev_error = 0.0
        self.inflight = 0

    def try_acquire(self) -> bool:
        """Attempts to admit an incoming request under current concurrency budget."""
        if self.inflight < int(self.limit):
            self.inflight += 1
            return True
        return False

    def release(self, observed_rtt_ms: float) -> float:
        """
        Signals completion of request with measured RTT.
        Updates closed-loop PID error and returns new concurrency limit.
        """
        self.inflight = max(0, self.inflight - 1)
        error = self.target_rtt - observed_rtt_ms

        # PID integration with anti-windup clamping
        self.integral = max(-100.0, min(100.0, self.integral + error))
        derivative = error - self.prev_error
        self.prev_error = error

        adjustment = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.limit = max(self.min_limit, min(self.max_limit, self.limit + adjustment * 0.1))
        return self.limit
