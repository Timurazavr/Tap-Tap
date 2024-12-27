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
    db_dict = db.all_read()

    character = Character(width // 2, height // 2)
    all_sprites.add(character)
    down_btn = Button(250, 800, 400, 100, "red", "Назад", "arial", 36)
    all_sprites.add(down_btn)
    damage_btn = Button(
        400, 215, 250, 100, "red", f"-{db_dict['damage']**2 * 100}", "arial", 56
    )
    all_sprites.add(damage_btn)
    if db_dict["hp"] != 3:
        hp_btn = Button(
            400, 415, 250, 100, "red", f"-{db_dict['hp'] * 1000}", "arial", 56
        )
        all_sprites.add(hp_btn)
    speed_btn = Button(
        400, 615, 250, 100, "red", f"-{db_dict['speed']**2 * 50}", "arial", 56
    )
    all_sprites.add(speed_btn)
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

    text_font = pygame.font.SysFont("Arial", 48)
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
                db.all_write(db_dict)
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if character.collide(*event.pos):
                        db_dict["cash"] += 1
                    elif down_btn.collide(*event.pos):
                        db.all_write(db_dict)
                        running = False
                    elif snake.collide(*event.pos):
                        db_dict["cash"] += (
                            snake.click(screen, clock, width, height, FPS)
                            * db_dict["damage"]
                        )
                    elif piu_piu.collide(*event.pos):
                        db_dict["cash"] += (
                            piu_piu.click(screen, clock, width, height, FPS)
                            * db_dict["damage"]
                        )
                    elif runner.collide(*event.pos):
                        db_dict["cash"] += (
                            runner.click(screen, clock, width, height, FPS)
                            * db_dict["damage"]
                        )
                    elif (
                        damage_btn.collide(*event.pos)
                        and db_dict["damage"] ** 2 * 100 <= db_dict["cash"]
                    ):
                        db_dict["cash"] -= db_dict["damage"] ** 2 * 100
                        db_dict["damage"] += 1
                        all_sprites.remove(damage_btn)
                        damage_btn = Button(
                            400,
                            215,
                            250,
                            100,
                            "red",
                            f"-{db_dict['damage']**2 * 100}",
                            "arial",
                            56,
                        )
                        all_sprites.add(damage_btn)
                    elif (
                        db_dict["hp"] != 3
                        and hp_btn.collide(*event.pos)
                        and db_dict["hp"] * 1000 <= db_dict["cash"]
                    ):
                        db_dict["cash"] -= db_dict["hp"] * 1000
                        db_dict["hp"] += 1
                        all_sprites.remove(hp_btn)
                        if db_dict["hp"] != 3:
                            hp_btn = Button(
                                400,
                                415,
                                250,
                                100,
                                "red",
                                f"-{db_dict['hp'] * 1000}",
                                "arial",
                                56,
                            )
                            all_sprites.add(hp_btn)
                    elif (
                        speed_btn.collide(*event.pos)
                        and db_dict["speed"] ** 2 * 50 <= db_dict["cash"]
                    ):
                        db_dict["cash"] -= db_dict["speed"] ** 2 * 50
                        db_dict["speed"] += 1
                        all_sprites.remove(speed_btn)
                        speed_btn = Button(
                            400,
                            615,
                            250,
                            100,
                            "red",
                            f"-{db_dict['speed']**2 * 50}",
                            "arial",
                            56,
                        )
                        all_sprites.add(speed_btn)

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
        surface_cash = text_font.render(str(db_dict["cash"]), True, "white")
        screen.blit(
            surface_cash,
            (250, 23),
        )
        screen.blit(
            surface_coin,
            (200 - surface_coin.width // 2, 25),
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
            text_font.render(str(db_dict["damage"]), True, "white"),
            (175, 180),
        )
        screen.blit(
            hp_image,
            (50, 350),
        )
        screen.blit(
            text_font.render(str(db_dict["hp"]), True, "white"),
            (175, 380),
        )
        screen.blit(
            speed_image,
            (50, 550),
        )
        screen.blit(
            text_font.render(str(db_dict["speed"]), True, "white"),
            (175, 580),
        )

        all_sprites.draw(screen)

        pygame.display.flip()
