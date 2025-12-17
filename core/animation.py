import pygame
from PIL import Image

def load_gif_frames(path, scale_size=None):
    """
    Loads frames from a GIF file using PIL and converts them to Pygame surfaces.
    """
    frames = []
    try:
        pil_image = Image.open(path)
        for frame_index in range(pil_image.n_frames):
            pil_image.seek(frame_index)
            frame_rgba = pil_image.convert("RGBA")
            pygame_image = pygame.image.fromstring(
                frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
            )
            if scale_size:
                pygame_image = pygame.transform.scale(pygame_image, scale_size)
            frames.append(pygame_image)
    except Exception as e:
        print(f"Error loading GIF {path}: {e}")
    return frames
