import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((500, 600))  # pygame.image.load(".png")
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.center = x, y


def main(
    screen: pygame.Surface, clock: pygame.Clock, width: int, height: int, FPS: int
):
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Character(width // 2, height // 2))
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        all_sprites.update()
        screen.fill("white")
        all_sprites.draw(screen)
        pygame.display.flip()
