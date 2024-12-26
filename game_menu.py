import pygame
from buttons import Button
from classes import Character, Mini_game_btn
import db


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()

    character = Character(width // 2, height // 2)
    all_sprites.add(character)
    down_btn = Button(50, 750, 300, 100, "red", "назад")
    all_sprites.add(down_btn)
    all_sprites.add(Mini_game_btn(1200, 500))

    counter_cash = db.read("cash")
    cash_font = pygame.font.SysFont("Arial", 48)

    counter_bg = -1

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
                        character.click()
                    elif down_btn.collide(*event.pos):
                        db.write("cash", counter_cash, "write")
                        running = False

        all_sprites.update()

        counter_bg = (counter_bg + 1) % 99
        screen.blit(pygame.image.load(f"video_bg/video_{counter_bg:03}.jpg"), (-200, 0))

        all_sprites.draw(screen)

        screen.blit(
            cash_font.render(str(counter_cash), True, "black"),
            (1200, 0),
        )

        pygame.display.flip()
