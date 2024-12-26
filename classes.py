import pygame
import Snake


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

    def click(self, *args):
        1
        # print("click", self.__class__.__name__)


class Mini_game_btn(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # pygame.image.load("male.png")
        self.image.fill("green")
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

    def click(self, screen):
        Snake.main(screen)
