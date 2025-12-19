import av
import numpy as np
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from PIL import Image
from tqdm import tqdm

from openframe.element import FrameElement


if TYPE_CHECKING:
    from av.container.output import OutputContainer
    from av.video.stream import VideoStream


@dataclass
class Scene:
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
    output_path: str = 'output.mp4'
    _elements: list[FrameElement] = field(default_factory=list)
    _scenes: list['Scene'] = field(default_factory=list)
    _output_container: 'OutputContainer | None' = field(init=False, default=None)
    _stream: 'VideoStream | None' = field(init=False, default=None)

    def __post_init__(self) -> None:
        """Open the output container and configure the stream.

        Returns:
            None
        """
        self._output_container = av.open(self.output_path, mode='w')
        self._stream = self._output_container.add_stream('h264', rate=self.fps)
        self._stream.width = self.width
        self._stream.height = self.height
        self._stream.pix_fmt = 'yuv420p'

    def add(self, element: FrameElement) -> None:
        """Enqueue a frame element for later rendering.

        Args:
            element (RenderableElement): Element that can draw itself.
        """
        self._elements.append(element)
        
    def add_scene(self, scene: 'Scene') -> None:
        """Enqueue a scene for later rendering."""
        self._scenes.append(scene)

    def _create_frame(self, t: float) -> np.ndarray:
        """Render all visible clips onto a single RGBA frame.

        Args:
            t (float): Current time in seconds for visibility checks.

        Returns:
            np.ndarray: Frame image data in RGBA format.
        """

        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))

        for clip in self._elements:
            if clip.is_visible(t):
                clip.render(img, t)

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
            for packet in self._stream.encode(frame):
                self._output_container.mux(packet)

        for packet in self._stream.encode():
            self._output_container.mux(packet)

        self._output_container.close()
