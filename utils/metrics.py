import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timed(metric_name: str) -> Generator[float, None, None]:
    start = time.perf_counter()
    try:
        yield start
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        # Placeholder for integrating with metrics backend
        print(f"{metric_name} took {duration_ms:.2f} ms")

