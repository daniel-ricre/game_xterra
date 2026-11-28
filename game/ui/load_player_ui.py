import pygame
from game.database.repository import Repository


class Load_player_UI:

    def __init__(self, screen):
        self.screen = screen
        self.all_saves = Repository().get_all_saves()
        self.selection = 0
        self.background = pygame.image.load("game/assets/found.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1366, 768))
        self.font = pygame.font.SysFont("impact", 38)
        self.rects = []

    def run(self):
        clock = pygame.time.Clock()
        running = True
        back = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    back = True
                    running = False
                # Solo procesar navegación si hay partidas.
                if self.all_saves:
                    if event.type == pygame.MOUSEMOTION:
                        for i, rect in enumerate(self.rects):
                            if rect.collidepoint(event.pos):
                                self.selection = i
                                break
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for i, rect in enumerate(self.rects):
                            if rect.collidepoint(event.pos):
                                self.selection = i
                                running = False
                                break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.selection = (self.selection - 1) % len(self.all_saves)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        self.selection = (self.selection + 1) % len(self.all_saves)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        running = False

            self.screen.blit(self.background, (0, 0))

            if not self.all_saves:
                # Mensaje si no hay partidas.
                surface = self.font.render("Not found saves", True, (0, 0, 0))
                rect = surface.get_rect(center=(683, 350))
                self.screen.blit(surface, rect)
                
            else:
                # Lista de partidas, resaltando la seleccionada.
                self.rects = []
                for i, save in enumerate(self.all_saves):
                    color = (0, 0, 0) if i == self.selection else (255, 255, 255)
                    surface = self.font.render(save.name, True, color)
                    rect = surface.get_rect(center=(683, 250 + i * 80))
                    self.screen.blit(surface, rect)
                    self.rects.append(rect)

            pygame.display.flip()
            clock.tick(60)

        if back or not self.all_saves:
            return "menu"
        return self.all_saves[self.selection]