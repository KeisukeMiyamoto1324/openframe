# OpenFrame

OpenFrame is a **pure Python** video editing toolkit that lets you blend text, images, video, and audio without ever leaving the language or spawning subprocesses. It is designed for fast exports (uses `av` with `ultrafast`/`zerolatency` presets) while keeping the API expressive and minimal so you can build timelines with a few dataclass-based objects.

## Installation

```bash
pip install openframe
```

## Quick start

```python
from openframe import *

scene = Scene(start_at=0)

scene.add(
    ImageClip(
        path="assets/sample.jpg",
        start_time=0,
        duration=5,
        position=(300, 200),
        size=(800, 450),
        content_mode=ContentMode.FIT,
        fade_in_duration=1,
        fade_out_duration=1,
    )
)

scene.add(
    TextClip(
        text="OpenFrame Demo",
        start_time=1,
        duration=6,
        position=(960, 540),
        anchor_point=AnchorPoint.CENTER,
        font_size=48,
        text_align=TextAlign.CENTER,
        fade_in_duration=0.5,
        fade_out_duration=0.5,
    )
)

scene.render(output_path="output.mp4", width=1920, height=1080, fps=30)
```
