from openframe import *

from dataclasses import dataclass
import time


@dataclass
class SceneConfig:
    telop: str
    slide: str
    

width = 1920
height = 1080
fps = 30


def create_scene(bg: str, telop: str, slide: str) -> Scene:
    scene = Scene(start_at=0)
    
    telop_clip = TextClip(
        text=telop,
        start_time=0,
        duration=3,
        position=(width//2, height//2),
        anchor_point=AnchorPoint.CENTER,
        text_align=TextAlign.RIGHT,
        font_size=64,
        fade_in_duration=0.5,
        fade_out_duration=0.5
    )
    
    slide_clip = ImageClip(
        path=slide,
        start_time=0,
        duration=3,
        position=(width//2, height//2),
        anchor_point=AnchorPoint.CENTER,
        size=(800, 800),
        content_mode=ContentMode.FIT,
        fade_in_duration=0.5,
        fade_out_duration=0.5
    )
    
    bg_clip = ImageClip(
        path=bg,
        start_time=0,
        duration=3,
        position=(0, 0),
        size=(1920, 1080),
        content_mode=ContentMode.FILL
    )

    scene.add(bg_clip)
    scene.add(slide_clip)
    scene.add(telop_clip)

    return scene

def main():
    start = time.time()
    
    scene_configs = [
        SceneConfig(telop="Every night, \nTom waited at the small train station.", slide="assets/sample1.jpg"),
        SceneConfig(telop="The lights were weak, and the air was cold.", slide="assets/sample2.jpg"),
        SceneConfig(telop="No one else came.", slide="assets/sample3.jpg"),
    ]
    
    editor = Scene(start_at=0)
    
    for scene_config in scene_configs:
        scene = create_scene(bg="assets/sample.jpg", telop=scene_config.telop, slide=scene_config.slide)
        scene.start_at = editor.total_duration
        editor.add_scene(scene)

    audio_clip = AudioClip(
        source_path="assets/audio1.mp3",
        start_time=0,
        source_start=0,
        source_end=editor.total_duration,
    )
    editor.add_audio(audio_clip)
    
    end = time.time()
    
    print(f"{end-start}")
    
    editor.render(output_path="assets/youtube.mp4")


if __name__ == "__main__":
    main()
