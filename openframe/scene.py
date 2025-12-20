import av
import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from PIL import Image
from tqdm import tqdm

from openframe.element import FrameElement


@dataclass
class Scene:
    """Hold a set of elements or child scenes and export their combined timeline."""
    class ContentType(Enum):
        ELEMENTS = "elements"
        SCENES = "scenes"

    start_at: float
    _elements: list[FrameElement] = field(default_factory=list)
    _scenes: list['Scene'] = field(default_factory=list)
    _content_type: Optional['Scene.ContentType'] = field(default=None, init=False)
    

    def add(self, element: FrameElement) -> None:
        """Enqueue a frame element for later rendering.

        Args:
            element (FrameElement): Element that can draw itself.
        """
        self._ensure_content_type(self.ContentType.ELEMENTS)
        self._elements.append(element)
        
    def add_scene(self, scene: 'Scene') -> None:
        """Queue a nested scene and guard against mixing with frame elements.

        Args:
            scene (Scene): Scene whose timeline should be rendered as part of this scene.
        """
        self._ensure_content_type(self.ContentType.SCENES)
        self._scenes.append(scene)
        
    def _get_elements(self) -> list[FrameElement]:
        """Adjusts element start times and returns the configured element list.

        Returns:
            list[FrameElement]: Elements shifted according to this scene's start time.
        """
        if self._content_type == self.ContentType.ELEMENTS:
            for element in self._elements:
                element.start_time += self.start_at
            return self._elements
        
        elif self._content_type == self.ContentType.SCENES:
            pass

    def _ensure_content_type(self, desired: 'Scene.ContentType') -> None:
        """Set the content type once and prevent mixing elements with scenes.

        Args:
            desired (Scene.ContentType): Intended content type for this scene.
        """
        if self._content_type is None:
            self._content_type = desired
            return
        if self._content_type is not desired:
            raise ValueError(
                "Scene already configured for "
                f"{self._content_type.value}, cannot add {desired.value}."
            )

    def _create_frame(self, t: float, width: int, height: int) -> np.ndarray:
        """Render all visible clips onto a single RGBA frame.

        Args:
            t (float): Current time in seconds for visibility checks.
            width (int): Frame width in pixels.
            height (int): Frame height in pixels.

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
        """Encode all configured elements into a video file.

        Args:
            total_duration (float): Total duration of the exported video in seconds.
            width (int): Frame width in pixels.
            height (int): Frame height in pixels.
            fps (int): Frames per second for the exported video.
            output_path (str): File path to write the encoded video into.

        Returns:
            None
        """
        output_container = av.open(output_path, mode='w')
        stream = output_container.add_stream('h264', rate=fps)
        stream.pix_fmt = 'yuv420p'
        stream.width, stream.height = width, height
        total_frames = int(total_duration * fps)
        
        self._elements = self._get_elements()

        for i in tqdm(range(total_frames), desc="Exporting", unit="frame", ncols=100):
            t = i / fps
            frame_data = self._create_frame(t, width, height)
            frame = av.VideoFrame.from_ndarray(frame_data, format='rgba')
            for packet in stream.encode(frame):
                output_container.mux(packet)

        for packet in stream.encode():
            output_container.mux(packet)

        output_container.close()
