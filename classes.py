import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.image.load("male.png")
        self.rect = self.image.get_rect()
        self.rect.center = x, y

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
