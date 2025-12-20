import av
import numpy as np
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Optional
from PIL import Image
from tqdm import tqdm

from openframe.element import FrameElement
from openframe.util import Layer


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
    

    def add(self, element: FrameElement, layer: Layer=Layer.TOP) -> None:
        """Enqueue a frame element for later rendering.

        Args:
            element (FrameElement): Element that can draw itself.
        """
        self._ensure_content_type(self.ContentType.ELEMENTS)
        
        if layer == Layer.TOP:
            self._elements.append(element)
        elif layer == Layer.BOTTOM:
            self._elements.insert(0, element)
        
    def add_scene(self, scene: 'Scene', layer: Layer=Layer.TOP) -> None:
        """Queue a nested scene and guard against mixing with frame elements.

        Args:
            scene (Scene): Scene whose timeline should be rendered as part of this scene.
        """
        self._ensure_content_type(self.ContentType.SCENES)
        
        if layer == Layer.TOP:
            self._scenes.append(scene)
        elif layer == Layer.BOTTOM:
            self._scenes.insert(0, scene)
        
    def _get_elements(self) -> list[FrameElement]:
        """Adjusts element start times and returns the configured element list.

        Returns:
            list[FrameElement]: Elements shifted according to this scene's start time.
        """
        if self._content_type == self.ContentType.ELEMENTS:
            return self._clone_with_offset(self._elements, self.start_at)

        if self._content_type == self.ContentType.SCENES:
            elements: list[FrameElement] = []
            for scene in self._scenes:
                child_elements = scene._get_elements()
                elements.extend(self._clone_with_offset(child_elements, self.start_at))
            return elements
        
    @property
    def total_duration(self) -> float:
        elements = self._get_elements()
        if not elements:
            return self.start_at

        return max(element.end_time for element in elements)
        

    @staticmethod
    def _clone_with_offset(elements: list[FrameElement], offset: float) -> list[FrameElement]:
        """Return copies of elements with their start times shifted.

        Args:
            elements (list[FrameElement]): Elements to clone.
            offset (float): Amount of seconds to add to each start time.

        Returns:
            list[FrameElement]: New elements with adjusted start times.
        """
        return [replace(element, start_time=element.start_time + offset) for element in elements]

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
        total_frames = int(self.total_duration * fps)
        
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
