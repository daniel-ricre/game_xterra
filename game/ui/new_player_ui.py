import pygame


class New_Player_UI:

    def __init__(self, screen):
        self.screen = screen
        self.options = ["Name: "]
        self.name = ""
        # Cargamos fondo y fuente una sola vez.
        self.background = pygame.image.load("game/assets/found.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1366, 768))
        self.font = pygame.font.SysFont("impact", 38)

    def run(self):
        pygame.key.start_text_input()
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"
                # Añadir texto al nombre.
                if event.type == pygame.TEXTINPUT:
                    self.name += event.text
                # Borrar última letra.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                # Enter: si hay nombre, devolverlo. NO cerrar pygame.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.name:
                        return self.name.capitalize()

            # Dibujo: fondo, "Name: " y el nombre al lado.
            self.screen.blit(self.background, (0, 0))
            for i, option in enumerate(self.options):
                surface = self.font.render(option, True, (0, 0, 0))
                rect = surface.get_rect(center=(640, 250 + i * 80))
                self.screen.blit(surface, rect)

                surface = self.font.render(self.name.capitalize(), True, (255, 255, 255))
                rect = surface.get_rect(center=(740, 250 + i * 80))
                self.screen.blit(surface, rect)

            pygame.display.flip()
            clock.tick(60)