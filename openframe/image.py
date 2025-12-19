from dataclasses import dataclass, field
from typing import Tuple
from PIL import Image, ImageDraw

from openframe.element import FrameElement


@dataclass
class ImageClip(FrameElement):
    """Represents an image overlay with timing, size, and placement."""

    path: str
    size: Tuple[int, int] | None = None
    image: Image.Image = field(init=False)

    def __post_init__(self) -> None:
        """Load and cache the RGBA image, resizing when needed."""

        loaded = Image.open(self.path).convert('RGBA')
        self.image = (
            loaded.resize(self.size, Image.Resampling.LANCZOS)
            if self.size
            else loaded
        )

    def render(self, canvas: Image.Image, _draw: ImageDraw.ImageDraw) -> None:
        """Paste the clip's image onto the canvas using its alpha channel."""

        canvas.paste(self.image, self.position, self.image)
