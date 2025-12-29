from openframe import *


width, height, fps = 1280, 720, 30

scene = Scene(start_at=0)

scene.add(
    Rectangle(
        size=(520, 240),
        fill=(255, 90, 60, 255),
        stroke=(255, 255, 255, 255),
        stroke_width=6,
        position=(80, 80),
        duration=4,
        fade_in_duration=0.5,
        fade_out_duration=0.5,
        opacity=0.3
    )
)

scene.add(
    Circle(
        size=(220, 220),
        fill=(70, 190, 255, 255),
        stroke=(0, 40, 80, 255),
        stroke_width=4,
        position=(width // 2, height // 2),
        anchor_point=AnchorPoint.CENTER,
        start_time=0.5,
        duration=4,
        fade_in_duration=0.5,
        fade_out_duration=0.5,
    )
)

scene.add(
    Triangle(
        size=(260, 240),
        fill=(110, 255, 140, 255),
        stroke=(0, 80, 40, 255),
        stroke_width=4,
        position=(width - 140, height - 120),
        anchor_point=AnchorPoint.BOTTOM_RIGHT,
        start_time=1.0,
        duration=4,
        fade_in_duration=0.5,
        fade_out_duration=0.5,
    )
)

scene.render(output_path="output_shapes.mp4", width=width, height=height, fps=fps)
