from openframe import *


def main():
    editor = Scene()
    
    image_clip = ImageClip(
        path="assets/sample.jpg",
        start_time=0,
        duration=10,
        position=(200, 120),
        size=(800, 100),
        content_mode=ContentMode.FILL,
        fade_in_duration=1
    )

    text_project_name = TextClip(
        text="project alpha",
        start_time=0,
        duration=5,
        position=(800, 200),
        font_size=32,
    )

    editor.add(image_clip)
    editor.add(text_project_name)
    editor.render(total_duration=10, width=1920, height=1080, fps=30, output_path="assets/output.mp4")
    

if __name__ == "__main__":
    main()
