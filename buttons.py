import pygame
from multipledispatch import dispatch

class StartButton(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.width, self.height = 500, 150
        self.x = x
        self.y = y
        self.color = "red"

        self.counterx, self.countery = 0, 0
        self.flag = False

        self.draw(self.width, self.height)

    def draw(self, width: int, height: int):
        self.image = pygame.Surface((width, height))
        self.image.fill("white")
        pygame.draw.circle(
            self.image, self.color, (height // 2, height // 2), height // 2
        )
        pygame.draw.rect(
            self.image,
            self.color,
            (height // 2, 0, width - height, height // 2 * 2),
        )
        pygame.draw.circle(
            self.image, self.color, (width - height // 2, height // 2), height // 2
        )
        txt = pygame.font.SysFont("Arial", 56).render("Играть", True, "black")
        self.image.blit(
            txt,
            (
                width // 2 - txt.get_width() // 2,
                height // 2 - txt.get_height() // 2,
            ),
        )
        self.image.set_colorkey("white")

        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        if not self.collidepoint(*pygame.mouse.get_pos()):
            self.counterx += 1 if self.flag else -1
            self.countery += 0.5 if self.flag else -0.5
            self.draw(self.width + self.counterx, self.height + self.countery)
            if not 0 > self.counterx > -30:
                self.flag = not self.flag

    def collidepoint(self, x: int, y: int):
        left_x, top_y = self.rect.topleft
        try:
            if self.rect.collidepoint(x, y) and self.image.get_at(
                (x - left_x, y - top_y)
            ) != (255, 255, 255, 255):

                return True
        except Exception:
            pass
        return False


class Button(pygame.sprite.Sprite):
    def __init__(
        self, x, y, width=None, height=None, color=None, text=None, image=None
    ):
        super().__init__()
        if image is None:
            self.image = pygame.Surface((width, height))
            self.image.fill("white")
            pygame.draw.circle(
                self.image, color, (height // 2, height // 2), height // 2
            )
            pygame.draw.rect(
                self.image,
                color,
                (height // 2, 0, width - height, height),
            )
            pygame.draw.circle(
                self.image, color, (width - height // 2, height // 2), height // 2
            )
            self.color = color
        else:
            self.image = image
        if text:
            txt = pygame.font.SysFont("arial", 16).render(text, True, "black")
            self.image.blit(txt, (width // 2, height // 2))
            self.text = text
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.image.set_colorkey("white")

    def click(self):
        print("click", self.__class__.__name__)

    def collide(self, x, y):
        leftx, topy = self.rect.topleft
        try:
            print(self.image.get_at((x - leftx, y - topy)))
            if self.rect.collidepoint(x, y) and self.image.get_at(
                (x - leftx, y - topy)
            ) != (255, 255, 255, 255):
                return True
        except Exception:
            pass
        return False
