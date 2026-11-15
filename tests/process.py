from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    pid: str
    arrival_time: int
    burst_time: int

    def as_tuple(self):
        return (self.pid, self.arrival_time, self.burst_time)
