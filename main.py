from core.game import Game
from states.menu_state import MenuState


def main():
    """
    Fungsi utama untuk menjalankan permainan.
    
    Menginisialisasi objek Game dengan state awal MenuState dan memulai loop permainan.
    """
    Game(MenuState).run()


if __name__ == "__main__":
    main()
