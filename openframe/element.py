from dataclasses import dataclass
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont


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
    
    def render(self, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        """Raise an error because base element does not provide rendering logic."""

        raise NotImplementedError("FrameElement.render should be implemented by subclasses.")
