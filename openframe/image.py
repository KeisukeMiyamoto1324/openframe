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

    def _render_content(self, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        """Paste the clip's image onto the overlay canvas using its alpha channel.

        Args:
            canvas: Overlay canvas that matches the target frame size.
            draw: Drawing helper (unused) that keeps signature consistent.
        """

        canvas.paste(self.image, self.position, self.image)
