import pygame
from PIL import Image

def load_gif_frames(path, scale_size=None):
    """
    Memuat frame-frame dari file GIF menggunakan PIL dan mengonversinya menjadi surface Pygame.

    Args:
        path (str): Path ke file GIF.
        scale_size (tuple, optional): Ukuran target (width, height) untuk mengubah skala setiap frame.

    Returns:
        list: Daftar objek pygame.Surface yang merepresentasikan setiap frame animasi.
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
