from dataclasses import dataclass
from typing import Tuple
from PIL import ImageFont

from openframe.element import FrameElement

DEFAULT_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"


@dataclass
class TextClip(FrameElement):
    """Represents a text overlay with timing, styling, and position.

    Attributes:
        text: The text string to render.
        start_time: Seconds at which the clip appears.
        duration: Seconds the clip stays on-screen.
        position: (x, y) pixel coordinates for placement.
        font_size: Point size used for rendering text.
        color: RGBA tuple used to draw the text.
        font: Loaded FreeType font instance for rendering.
    """
    
    text: str
    start_time: float
    duration: float
    position: Tuple[int, int]
    font_size: int
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    font: str = DEFAULT_FONT_PATH

    def load_font(self) -> ImageFont.FreeTypeFont:
        """Load the configured font at the clip's size.

        Returns:
            ImageFont.FreeTypeFont: The font ready for rendering text.
        """

        return ImageFont.truetype(self.font, self.font_size)
