import av
import numpy as np
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from PIL import Image, ImageDraw
from tqdm import tqdm

from openframe.text import TextClip


if TYPE_CHECKING:
    from av.container.output import OutputContainer
    from av.video.stream import VideoStream


@dataclass
class VideoEditor:
    """Manage clip composition and export of video timelines.

    Attributes:
        width (int): Frame width in pixels.
        height (int): Frame height in pixels.
        fps (int): Frames per second for the output video.
        output_path (str): Destination file path for the rendered video.
    """

    width: int
    height: int
    fps: int
    output_path: str = 'output_multi.mp4'
    text_clips: list[TextClip] = field(default_factory=list)
    output_container: 'OutputContainer | None' = field(init=False, default=None)
    stream: 'VideoStream | None' = field(init=False, default=None)

    def __post_init__(self) -> None:
        """Open the output container and configure the stream.

        Returns:
            None
        """

        self.output_container = av.open(self.output_path, mode='w')
        self.stream = self.output_container.add_stream('h264', rate=self.fps)
        self.stream.width = self.width
        self.stream.height = self.height
        self.stream.pix_fmt = 'yuv420p'

    def add(self, element: TextClip) -> None:
        """Add TextClip to render queue

        Args:
            element (TextClip): _description_
        """
        self.text_clips.append(element)
        

    def _create_frame(self, t: float) -> np.ndarray:
        """Render all visible clips onto a single RGBA frame.

        Args:
            t (float): Current time in seconds for visibility checks.

        Returns:
            np.ndarray: Frame image data in RGBA format.
        """

        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        for clip in self.text_clips:
            if clip.is_visible(t):
                draw.text(clip.position, clip.text, font=clip.load_font(), fill=clip.color)

        return np.array(img)

    def render(self, total_duration: float) -> None:
        """Encode frames for the requested duration with progress feedback.

        Args:
            total_duration (float): Total duration of the exported video in seconds.

        Returns:
            None
        """

        total_frames = int(total_duration * self.fps)

        for i in tqdm(range(total_frames), desc="Exporting", unit="frame", ncols=100):
            t = i / self.fps
            frame_data = self._create_frame(t)
            frame = av.VideoFrame.from_ndarray(frame_data, format='rgba')
            for packet in self.stream.encode(frame):
                self.output_container.mux(packet)

        for packet in self.stream.encode():
            self.output_container.mux(packet)

        self.output_container.close()
