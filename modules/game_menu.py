import pygame
from modules.buttons import Button
from modules import db, snake_game, piu_piu_game, runner_game


class Character(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("textures/male.png"), (450, 480)
        )
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def collide(self, x, y):
        leftx, topy = self.rect.topleft
        try:
            if self.rect.collidepoint(x, y) and self.image.get_at(
                (x - leftx, y - topy)
            ) != (255, 255, 255, 0):
                return True
        except Exception:
            pass
        return False


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()

    character = Character(width // 2, height // 2)
    all_sprites.add(character)
    down_btn = Button(250, 800, 400, 100, "red", "Назад", "arial", 36)
    all_sprites.add(down_btn)
    snake = Button(1150, 350, pygame.image.load("textures/snake.png"))
    all_sprites.add(snake)
    snake.click = snake_game.main
    piu_piu = Button(
        1150,
        500,
        pygame.transform.scale(pygame.image.load("textures/ship.png"), (92, 92)),
    )
    all_sprites.add(piu_piu)
    piu_piu.click = piu_piu_game.main
    runner = Button(
        1150,
        650,
        pygame.transform.scale(pygame.image.load("textures/runner.png"), (92, 92)),
    )
    all_sprites.add(runner)
    runner.click = runner_game.main

    counter_cash = db.read("cash")
    cash_font = pygame.font.SysFont("Arial", 48)
    game_font = pygame.font.SysFont("Arial", 56)

    counter_bg = -1
    index_coin = 1
    counter_coin = 0

    surface_coin = pygame.image.load(
        f"textures/video_coin/star coin rotate {index_coin}.png"
    )
    hp_image = pygame.image.load("textures/hp.png")
    damage_image = pygame.image.load("textures/damage.png")
    speed_image = pygame.image.load("textures/speed.png")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.write("cash", counter_cash, "write")
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if character.collide(*event.pos):
                        counter_cash += 1
                    elif down_btn.collide(*event.pos):
                        db.write("cash", counter_cash, "write")
                        running = False
                    elif snake.collide(*event.pos):
                        counter_cash += snake.click(
                            screen, clock, width, height, FPS
                        ) * db.read("damage")
                    elif piu_piu.collide(*event.pos):
                        counter_cash += piu_piu.click(
                            screen, clock, width, height, FPS
                        ) * db.read("damage")
                    elif runner.collide(*event.pos):
                        counter_cash += runner.click(
                            screen, clock, width, height, FPS
                        ) * db.read("damage")

        all_sprites.update()

        counter_bg = (counter_bg + 1) % 99
        screen.blit(
            pygame.image.load(f"textures/video_bg/video_{counter_bg:03}.jpg"), (-200, 0)
        )

        counter_coin = (counter_coin + 1) % 60
        if not counter_coin % 7:
            index_coin = index_coin % 6 + 1
            surface_coin = pygame.image.load(
                f"textures/video_coin/star coin rotate {index_coin}.png"
            )
        surface_cash = cash_font.render(str(counter_cash), True, "white")
        screen.blit(
            surface_cash,
            (250, 23),
        )
        screen.blit(
            surface_coin,
            (200, 25),
        )
        screen.blit(
            game_font.render("Мини-игры:", True, "white"),
            (1050, 200),
        )
        screen.blit(
            damage_image,
            (50, 150),
        )
        screen.blit(
            hp_image,
            (50, 350),
        )
        screen.blit(
            speed_image,
            (50, 550),
        )

        all_sprites.draw(screen)

        pygame.display.flip()
