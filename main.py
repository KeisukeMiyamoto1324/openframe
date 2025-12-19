from openframe import *


def main():
    editor = VideoEditor(
        width=1920,
        height=1080,
        fps=30,
        output_path="assets/output.mp4"
    )
    
    image_clip = ImageClip(
        path="assets/sample.jpg",
        start_time=0,
        duration=10,
        position=(200, 120),
        fade_in_duration=1.0,
        fade_out_duration=1.0
    )

    text_project_name = TextClip(
        text="project alpha",
        start_time=0,
        duration=5,
        position=(800, 200),
        font_size=32,
        fade_in_duration=0.6,
        fade_out_duration=0.6
    )

    editor.add(image_clip)
    editor.add(text_project_name)
    editor.render(total_duration=10)
    

if __name__ == "__main__":
    main()
