from dataclasses import dataclass
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

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
    font_size: int
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    font: str = DEFAULT_FONT_PATH

    def load_font(self) -> ImageFont.FreeTypeFont:
        """Load the configured font at the clip's size.

        Returns:
            ImageFont.FreeTypeFont: The font ready for rendering text.
        """

        return ImageFont.truetype(self.font, self.font_size)

    def _render_content(self, canvas: Image.Image, draw: ImageDraw.ImageDraw) -> None:
        """Draw the text clip on the provided overlay context.

        Args:
            canvas: Overlay canvas matching the target frame size.
            draw: Drawing helper for text rendering.
        """

        draw.text(self.position, self.text, font=self.load_font(), fill=self.color)

    @property
    def bounding_box_size(self) -> Tuple[int, int]:
        """Compute the pixel area required to render the clip's text."""

        font = self.load_font()
        overlay = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(overlay)
        left, top, right, bottom = draw.textbbox((0, 0), self.text, font=font)
        return right - left, bottom - top
