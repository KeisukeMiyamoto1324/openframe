from openframe import *


def main():
    editor = VideoEditor(1920, 1080, 30)

    editor.add_text(
        text="Project Alpha",
        start_time=0, 
        duration=3, 
        position=(800, 200), 
        font_size=120, 
        color=(255, 100, 100, 255)
    )

    editor.add_text(
        text="Directed by UNO Student",
        start_time=2, 
        duration=5, 
        position=(100, 800), 
        font_size=60
    )

    editor.add_text(
        text="Thank you for watching",
        start_time=6, 
        duration=4, 
        position=(600, 500), 
        font_size=80,
        color=(100, 255, 100, 255)
    )

    editor.render(total_duration=10)
    

if __name__ == "__main__":
    main()