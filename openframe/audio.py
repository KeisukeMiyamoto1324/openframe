from dataclasses import dataclass
from enum import Enum
from functools import lru_cache

import av
import numpy as np


class AudioLayout(Enum):
    MONO = "mono"
    STEREO = "stereo"

@lru_cache(maxsize=64)
def _source_duration_cached(path: str) -> float:
    """Return cached duration for the given audio source.

    Args:
        path: File path for the audio asset.

    Returns:
        float: Duration in seconds.
    """

    container = av.open(path)
    stream = container.streams.audio[0]
    duration = float(stream.duration * stream.time_base)
    container.close()
    return duration


@lru_cache(maxsize=16)
def _decode_audio_cached(path: str, sample_rate: int, layout: str) -> np.ndarray:
    """Decode and cache audio samples for a given source and format.

    Args:
        path: File path for the audio asset.
        sample_rate: Target sample rate.
        layout: Audio layout name.

    Returns:
        np.ndarray: Audio samples shaped as (samples, channels).
    """

    container = av.open(path)
    stream = container.streams.audio[0]
    resampler = av.AudioResampler(format="fltp", layout=layout, rate=sample_rate)
    frames: list[np.ndarray] = []

    for frame in container.decode(stream):
        resampled = resampler.resample(frame) or []
        if not isinstance(resampled, list):
            resampled = [resampled]
        frames.extend([chunk.to_ndarray() for chunk in resampled])

    container.close()

    merged = np.concatenate(frames, axis=1)
    return merged.T.astype(np.float32)


@dataclass(kw_only=True)
class AudioClip:
    """Represent an audio segment placed on the scene timeline."""

    source_path: str
    start_time: float
    source_start: float = 0
    source_end: float | None = None

    @property
    def duration(self) -> float:
        """Return duration of the clip in seconds.

        Returns:
            float: Duration in seconds.
        """
        end = self.source_end if self.source_end is not None else self._source_duration()
        return end - self.source_start

    @property
    def end_time(self) -> float:
        """Return the timeline end time for this clip.

        Returns:
            float: End time in seconds.
        """
        return self.start_time + self.duration

    def render(self, sample_rate: int, channels: int) -> np.ndarray:
        """Decode and return audio samples aligned to the requested format.

        Args:
            sample_rate (int): Target sample rate.
            channels (int): Target number of channels (ignored; mono only).

        Returns:
            np.ndarray: Audio samples shaped as (samples, channels).
        """
        audio = self._decode_audio(sample_rate, AudioLayout.MONO.value)
        start_idx = int(self.source_start * sample_rate)
        end_idx = int(self.source_end * sample_rate) if self.source_end is not None else audio.shape[0]
        return audio[start_idx:end_idx]

    def _source_duration(self) -> float:
        """Return source audio duration in seconds.

        Returns:
            float: Duration in seconds.
        """
        return _source_duration_cached(self.source_path)

    def _decode_audio(self, sample_rate: int, layout: str) -> np.ndarray:
        """Decode audio file into a normalized float32 array.

        Args:
            sample_rate (int): Target sample rate.
            layout (str): Audio layout name.

        Returns:
            np.ndarray: Audio samples shaped as (samples, channels).
        """
        return _decode_audio_cached(self.source_path, sample_rate, layout)
