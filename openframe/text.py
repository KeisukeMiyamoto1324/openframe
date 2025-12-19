from PIL import ImageFont


class TextClip:
    def __init__(self, text, start_time, duration, position, font_size, color=(255, 255, 255, 255)):
        self.text = text
        self.start_time = start_time
        self.end_time = start_time + duration
        self.position = position 
        self.font_size = font_size
        self.color = color
        self.font = self._load_font()

    def _load_font(self):
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.font_size)
        except IOError:
            return ImageFont.load_default()

    def is_visible(self, t):
        return self.start_time <= t < self.end_time

