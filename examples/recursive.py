from openframe import Scene, TextClip, ImageClip, ContentMode


def build_title_scene() -> Scene:
    """Return a scene that draws a fading title text."""

    scene = Scene(start_at=0)
    scene.add(
        TextClip(
            text="OpenFrame Recursion",
            start_time=0,
            duration=3,
            position=(420, 150),
            font_size=56,
            fade_in_duration=1,
            fade_out_duration=1,
        )
    )
    return scene


def build_image_scene() -> Scene:
    """Return a scene that shows a centered image clip with animation."""

    scene = Scene(start_at=0)
    scene.add(
        ImageClip(
            path="assets/sample.jpg",
            start_time=0,
            duration=4,
            position=(400, 320),
            size=(800, 450),
            content_mode=ContentMode.FIT,
            fade_in_duration=1,
            fade_out_duration=1,
        )
    )
    return scene


def build_overlay_scene() -> Scene:
    """Return a scene that stacks other scenes to demo recursion."""

    scene = Scene(start_at=2)
    scene.add_scene(build_title_scene())
    scene.add_scene(build_image_scene())
    return scene


def build_recursive_scene() -> Scene:
    """Return the root scene that combines direct and nested scenes."""

    scene = Scene(start_at=0)
    scene.add_scene(build_title_scene())
    scene.add_scene(build_overlay_scene())
    return scene


def main() -> None:
    """Render the recursive scene example into a sample file."""

    recursive_scene = build_recursive_scene()
    recursive_scene.render(
        total_duration=8,
        width=1280,
        height=720,
        fps=24,
        output_path="assets/recursive_demo.mp4",
    )


if __name__ == "__main__":
    main()
