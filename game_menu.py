import pygame
from buttons import Button


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((500, 600))  # pygame.image.load(".png")
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.text = ""

    def click(self):
        print("click", self.__class__.__name__)


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Character(width // 2, height // 2))
    all_sprites.add(Button(50, 750, 300, 100, "red", "назад"))
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for i in all_sprites.sprites():
                        if i.rect.collidepoint(*event.pos):
                            if i.text == "назад":
                                running = False
                            else:
                                i.click()

        all_sprites.update()
        screen.fill("white")
        all_sprites.draw(screen)
        pygame.display.flip()
