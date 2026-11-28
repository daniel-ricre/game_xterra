import pygame


class Pygame_UI:

    def __init__(self, screen):
        self.screen = screen
        self.options = ["New Player", "Load Player", "Exit"]
        self.selection = 0
        self.rects = []
        self.background = pygame.image.load("game/assets/found.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (1366, 768))
        self.font = pygame.font.SysFont("impact", 38)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Exit"

                # Teclado: flechas y Enter.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selection = (self.selection - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selection = (self.selection + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        running = False

                # Ratón encima de una opción: la selecciona.
                # IMPORTANTE: si no está encima de ninguna, NO tocamos self.selection.
                if event.type == pygame.MOUSEMOTION:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(event.pos):
                            self.selection = i
                            break

                # Click izquierdo sobre una opción: la confirma.
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, rect in enumerate(self.rects):
                        if rect.collidepoint(event.pos):
                            self.selection = i
                            running = False
                            break

            # Dibujo: fondo + opciones resaltando la seleccionada.
            self.screen.blit(self.background, (0, 0))
            self.rects = []
            for i, option in enumerate(self.options):
                color = (0, 0, 0) if i == self.selection else (255, 255, 255)
                surface = self.font.render(option, True, color)
                rect = surface.get_rect(center=(683, 250 + i * 80))
                self.screen.blit(surface, rect)
                self.rects.append(rect)

            pygame.display.flip()
            clock.tick(60)

        return self.options[self.selection]