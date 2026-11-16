import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from adaptive_pid.core import AdaptivePIDLimiter


class TestAdaptivePIDLimiter(unittest.TestCase):
    def setUp(self):
        self.limiter = AdaptivePIDLimiter(target_rtt_ms=40.0, min_limit=2.0, max_limit=100.0)

    def test_acquire_and_release(self):
        acquired = self.limiter.try_acquire()
        self.assertTrue(acquired)
        self.assertEqual(self.limiter.inflight, 1)

        new_limit = self.limiter.release(observed_rtt_ms=30.0)
        self.assertEqual(self.limiter.inflight, 0)
        self.assertGreaterEqual(new_limit, 2.0)

    def test_expansion_on_fast_latencies(self):
        initial_limit = self.limiter.limit
        for _ in range(10):
            self.limiter.try_acquire()
            self.limiter.release(observed_rtt_ms=10.0)  # Very fast latency
        self.assertGreater(self.limiter.limit, initial_limit)

    def test_throttling_on_latency_spikes(self):
        initial_limit = self.limiter.limit
        for _ in range(15):
            self.limiter.try_acquire()
            self.limiter.release(observed_rtt_ms=200.0)  # Heavy latency spike
        self.assertLess(self.limiter.limit, initial_limit)
        self.assertGreaterEqual(self.limiter.limit, self.limiter.min_limit)

    def test_max_limit_clamping(self):
        for _ in range(100):
            self.limiter.try_acquire()
            self.limiter.release(observed_rtt_ms=1.0)
        self.assertLessEqual(self.limiter.limit, self.limiter.max_limit)


if __name__ == "__main__":
    unittest.main()
