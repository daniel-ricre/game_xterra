import pygame

from game.database.session import init_db
from game.database.repository import Repository
from game.ui.game_ui import Game_UI
from game.ui.pygame_ui import Pygame_UI
from game.ui.new_player_ui import New_Player_UI
from game.ui.load_player_ui import Load_player_UI


def run():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("XTerra")

    while True:
        choice = Pygame_UI(screen).run()

        if choice == "New Player":
            name = New_Player_UI(screen).run()
            if name and name != "menu":
                repo = Repository()
                save = repo.create_save(name=name)
                Game_UI(screen, name, save.id, repo).run()
                repo.close()

        elif choice == "Load Player":
            save = Load_player_UI(screen).run()
            if save and save != "menu":
                repo = Repository()
                Game_UI(screen, save.name, save.id, repo).run()
                repo.close()

        else:
            break

    pygame.quit()


if __name__ == "__main__":
    init_db()
    run()