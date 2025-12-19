from openframe import *


def main():
    editor = VideoEditor(
        width=1920,
        height=1080,
        fps=30,
        output_path="assets/output.mp4"
    )
    
    text_project_name = TextClip(
        text="project alpha",
        start_time=0,
        duration=5,
        position=(800, 200),
        font_size=32
    )
    
    editor.add(text_project_name)
    editor.render(total_duration=10)
    

if __name__ == "__main__":
    main()