import threading
import time

class ParallelScheduler:
    """
    Schedules and executes agent tasks across multiple targets in parallel,
    with optional rate-limiting.
    """

    def __init__(self, max_concurrent=5, rate_limit_per_sec=1):
        self.max_concurrent = max_concurrent
        self.rate_limit_per_sec = rate_limit_per_sec

    def run_tasks(self, tasks, agent_runner):
        threads = []
        for i, task in enumerate(tasks):
            while threading.active_count() > self.max_concurrent:
                time.sleep(0.1)
            t = threading.Thread(target=agent_runner, args=(task,))
            t.start()
            threads.append(t)
            time.sleep(1.0 / self.rate_limit_per_sec)
        for t in threads:
            t.join()