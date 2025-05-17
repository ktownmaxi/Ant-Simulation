import time


class Stopwatch:
    def __init__(self):
        self.running = False
        self.start_time = 0.0
        self.elapsed = 0.0

    def start(self):
        """Start and resume stopwatch"""
        if not self.running:
            self.start_time = time.perf_counter() - self.elapsed
            self.running = True

    def stop(self):
        """Stop stopwatch"""
        if self.running:
            # erfasste Zeit sichern
            self.elapsed = time.perf_counter() - self.start_time
            self.running = False

    def reset(self):
        """Reset stopwatch"""
        self.running = False
        self.start_time = 0.0
        self.elapsed = 0.0

    def get_time(self) -> int:
        """
        Gives the already timed time back
        """
        if self.running:
            current = time.perf_counter() - self.start_time
        else:
            current = self.elapsed
        return int(current * 1000)

    @staticmethod
    def format_time(ms: int) -> str:
        """
        Formats the time in minutes:seconds:centis
        """
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        centis = (ms % 1000) // 10
        return f"{minutes:02d}:{seconds:02d}:{centis:02d}"
