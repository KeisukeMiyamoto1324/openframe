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
    """Manage clip composition and export of video timelines."""
    _elements: list[FrameElement] = field(default_factory=list)
    _scenes: list['Scene'] = field(default_factory=list)
    

    def add(self, element: FrameElement) -> None:
        """Enqueue a frame element for later rendering.

        Args:
            element (RenderableElement): Element that can draw itself.
        """
        self._elements.append(element)
        
    def add_scene(self, scene: 'Scene') -> None:
        """Enqueue a scene for later rendering."""
        self._scenes.append(scene)

    def _create_frame(self, t: float, width: int, height: int) -> np.ndarray:
        """Render all visible clips onto a single RGBA frame.

        Args:
            t (float): Current time in seconds for visibility checks.

        Returns:
            np.ndarray: Frame image data in RGBA format.
        """

        img = Image.new('RGBA', (width, height), (0, 0, 0, 255))

        for clip in self._elements:
            if clip.is_visible(t):
                clip.render(img, t)

        return np.array(img)

    def render(
        self, 
        total_duration: float, 
        width: int = 1920, 
        height: int = 1080, 
        fps: int = 30, 
        output_path: str = "output.mp4"
    ) -> None:
        """Encode frames for the requested duration with progress feedback.

        Args:
            total_duration (float): Total duration of the exported video in seconds.

        Returns:
            None
        """
        output_container = av.open(output_path, mode='w')
        stream = output_container.add_stream('h264', rate=fps)
        stream.pix_fmt = 'yuv420p'
        stream.width, stream.height = width, height
        total_frames = int(total_duration * fps)

        for i in tqdm(range(total_frames), desc="Exporting", unit="frame", ncols=100):
            t = i / fps
            frame_data = self._create_frame(t, width, height)
            frame = av.VideoFrame.from_ndarray(frame_data, format='rgba')
            for packet in stream.encode(frame):
                output_container.mux(packet)

        for packet in stream.encode():
            output_container.mux(packet)

        output_container.close()
