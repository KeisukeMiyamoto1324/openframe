from dataclasses import dataclass
from typing import Tuple


@dataclass
class FrameElement():
    start_time: float
    duration: float
    position: Tuple[int, int]
    
    @property
    def end_time(self) -> float:
        """Return when the clip should stop being visible."""

        return self.start_time + self.duration

    def is_visible(self, t: float) -> bool:
        """Report whether the clip should be visible at the given time."""

        return self.start_time <= t < self.end_time