import pygame


class Game_UI:

    def __init__(self, screen, save_name, save_id, repo):
        self.screen = screen
        self.save_name = save_name
        self.save_id = save_id
        self.repo = repo

        self.ps = repo.get_player_state(save_id)
        if self.ps is None:
            raise ValueError(f"No existe PlayerState para save_id={save_id}")

        # self.background = pygame.image.load("game/assets/found.png").convert_alpha()
        # self.background = pygame.transform.scale(self.background, (1366, 768))

        self.idle_frame = pygame.image.load("game/assets/idle.png").convert_alpha()
        self.idle_frame = pygame.transform.scale(self.idle_frame, (48, 64))

        self.run_frames = []
        for i in range(1, 5):
            frame = pygame.image.load(f"game/assets/run{i}.png").convert_alpha()
            frame = pygame.transform.scale(frame, (48, 64))
            self.run_frames.append(frame)

        self.jump_frame = pygame.image.load("game/assets/jump.png").convert_alpha()
        self.jump_frame = pygame.transform.scale(self.jump_frame, (96, 128))

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.is_moving = False

        # Dirección: True = mira a la derecha, False = mira a la izquierda.
        self.facing_right = True

        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 15

        self.font = pygame.font.SysFont("impact", 38)

        self.rect = pygame.Rect(self.ps.x, self.ps.y, 96, 128)
        self.speed = 5

    def run(self):
        running = True
        clock = pygame.time.Clock()
        frames = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.repo.update_player_state(
                        self.save_id, self.rect.x, self.rect.y,
                        self.ps.hp, self.ps.attack
                    )
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.repo.update_player_state(
                        self.save_id, self.rect.x, self.rect.y,
                        self.ps.hp, self.ps.attack
                    )
                    return False

            wasd = pygame.key.get_pressed()

            # Actualizar dirección según la tecla horizontal pulsada.
            if wasd[pygame.K_a]:
                self.rect.x -= self.speed
                self.facing_right = False
            if wasd[pygame.K_d]:
                self.rect.x += self.speed
                self.facing_right = True

            # Movimiento vertical (no cambia la dirección).
            if wasd[pygame.K_w]:
                self.rect.y -= self.speed
            if wasd[pygame.K_s]:
                self.rect.y += self.speed

            self.is_moving = any([
                wasd[pygame.K_a], wasd[pygame.K_d],
                wasd[pygame.K_w], wasd[pygame.K_s]
            ])

            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.is_moving:
                    self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                else:
                    self.current_frame = 0

            if self.attacking:
                self.attack_timer += 1
                if self.attack_timer >= self.attack_duration:
                    self.attacking = False
                    self.attack_timer = 0

            # frames += 1
            # if frames % 30 == 0:
            #     self.repo.update_player_state(
            #         self.save_id, self.rect.x, self.rect.y,
            #         self.ps.hp, self.ps.attack
            #     )

            # self.screen.blit(self.background, (0, 0))
            self.screen.fill((0, 0, 0))

            # Elegir sprite según estado.
            if self.attacking:
                image = self.idle_frame
            elif self.is_moving:
                image = self.run_frames[self.current_frame]
            else:
                image = self.idle_frame

            # Si mira a la izquierda, voltear horizontalmente.
            if not self.facing_right:
                image = pygame.transform.flip(image, True, False)

            self.screen.blit(image, (self.rect.x, self.rect.y))

            name_surf = self.font.render(self.save_name, True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(683, 50))
            self.screen.blit(name_surf, name_rect)

            esc_surf = self.font.render("ESC to menu", True, (255, 255, 255))
            esc_rect = esc_surf.get_rect(center=(683, 720))
            self.screen.blit(esc_surf, esc_rect)

            pygame.display.flip()
            clock.tick(60)