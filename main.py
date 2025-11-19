from core.game import Game
from states.menu_state import MenuState


def main():
    Game(MenuState).run()


if __name__ == "__main__":
    main()
