from dataclasses import dataclass, field
from typing import Tuple
from PIL import Image, ImageDraw

from openframe.element import FrameElement
from openframe.util import ContentMode, _compute_scaled_size

@dataclass
class ImageClip(FrameElement):
    """Represents an image overlay with timing, size, and placement."""

    path: str
    image: Image.Image = field(init=False)
    content_mode: ContentMode = ContentMode.NONE

    def __post_init__(self) -> None:
        """Load and cache the RGBA image, resizing when needed."""

        loaded = Image.open(self.path).convert('RGBA')
        if self.size is None or self.content_mode == ContentMode.NONE:
            self.image = loaded
            return

        scaled = _compute_scaled_size(loaded.size, self.size, self.content_mode)
        resized = loaded.resize(scaled, Image.Resampling.LANCZOS)
        if self.content_mode == ContentMode.FILL:
            target_width, target_height = self.size
            left = (resized.width - target_width) // 2
            top = (resized.height - target_height) // 2
            right = left + target_width
            bottom = top + target_height
            self.image = resized.crop((left, top, right, bottom))
            return

        self.image = resized

    def _render_content(self, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        """Paste the clip's image onto the overlay canvas using its alpha channel.

        Args:
            canvas: Overlay canvas that matches the target frame size.
            draw: Drawing helper (unused) that keeps signature consistent.
        """

        canvas.paste(self.image, self.render_position, self.image)

    @property
    def bounding_box_size(self) -> Tuple[int, int]:
        """Return the dimensions of the image that will be drawn."""

        return self.image.size
