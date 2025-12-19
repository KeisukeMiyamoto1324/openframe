import av
import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm

from openframe.text import TextClip


class VideoEditor:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.text_clips = []
        self.output_container = av.open('output_multi.mp4', mode='w')
        self.stream = self.output_container.add_stream('h264', rate=fps)
        self.stream.width = width
        self.stream.height = height
        self.stream.pix_fmt = 'yuv420p'

    def add_text(self, text, start_time, duration, position, font_size=50, color=(255, 255, 255, 255)):
        clip = TextClip(text, start_time, duration, position, font_size, color)
        self.text_clips.append(clip)

    def _create_frame(self, t):
        img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)

        for clip in self.text_clips:
            if clip.is_visible(t):
                draw.text(clip.position, clip.text, font=clip.font, fill=clip.color)

        return np.array(img)

    def render(self, total_duration):
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
