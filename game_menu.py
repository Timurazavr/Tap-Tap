import pygame
from buttons import Button
from classes import Character
import db
import Snake
import Piu_Piu
import Runner


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()

    character = Character(width // 2, height // 2)
    all_sprites.add(character)
    down_btn = Button(250, 800, 400, 100, "red", "Назад", "arial", 36)
    all_sprites.add(down_btn)
    snake = Button(1150, 350, pygame.image.load("snake.png"))
    all_sprites.add(snake)
    snake.click = Snake.main
    piu_piu = Button(
        1150, 500, pygame.transform.scale(pygame.image.load("ship.png"), (92, 92))
    )
    all_sprites.add(piu_piu)
    piu_piu.click = Piu_Piu.main
    runner = Button(
        1150, 650, pygame.transform.scale(pygame.image.load("runner.png"), (92, 92))
    )
    all_sprites.add(runner)
    runner.click = Runner.main

    counter_cash = db.read("cash")
    cash_font = pygame.font.SysFont("Arial", 48)
    game_font = pygame.font.SysFont("Arial", 56)

    counter_bg = -1
    index_coin = 1
    counter_coin = 0

    surface_coin = pygame.image.load(f"video_coin/star coin rotate {index_coin}.png")
    hp_image = pygame.image.load("hp.png")
    damage_image = pygame.image.load("damage.png")
    speed_image = pygame.image.load("speed.png")

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
        screen.blit(pygame.image.load(f"video_bg/video_{counter_bg:03}.jpg"), (-200, 0))

        counter_coin = (counter_coin + 1) % 60
        if not counter_coin % 7:
            index_coin = index_coin % 6 + 1
            surface_coin = pygame.image.load(
                f"video_coin/star coin rotate {index_coin}.png"
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
