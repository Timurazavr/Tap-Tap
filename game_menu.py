import pygame
from buttons import Button
import db


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("male.png")
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.text = ""

    def collide(self, x, y):
        leftx, topy = self.rect.topleft
        try:
            if self.rect.collidepoint(x, y) and self.image.get_at(
                (x - leftx, y - topy)
            ) != (0, 0, 0, 0):
                return True
        except Exception:
            pass
        return False

    def click(self):
        1
        # print("click", self.__class__.__name__)


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()
    character = Character(width // 2, height // 2)
    all_sprites.add(character)
    all_sprites.add(Button(50, 750, 300, 100, "red", "назад"))
    counter_cash = db.read("cash")
    txt_cash = pygame.font.SysFont("Arial", 48)
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
                    for i in all_sprites.sprites():
                        if i.collide(*event.pos):
                            if i.text == "назад":
                                db.write("cash", counter_cash, "write")
                                running = False
                            else:
                                counter_cash += 1
                                i.click()

        all_sprites.update()
        screen.fill("white")
        all_sprites.draw(screen)
        screen.blit(
            txt_cash.render(str(counter_cash), True, "black"),
            (1200, 0),
        )
        pygame.display.flip()
