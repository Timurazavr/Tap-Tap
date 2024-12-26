import pygame


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


class StartButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.color = color
        self.counterx, self.countery = 0, 0
        self.flag = False
        self.draw(width, height)

    def draw(self, width, height):
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

    def update(self):
        if not self.collide(*pygame.mouse.get_pos()):
            self.counterx += 1 if self.flag else -1
            self.countery += 0.5 if self.flag else -0.5
            self.draw(self.width + self.counterx, self.height + self.countery)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y
            if self.counterx == -30 or self.counterx == 0:
                self.flag = not self.flag

    def collide(self, x, y):
        leftx, topy = self.rect.topleft
        try:
            if self.rect.collidepoint(x, y) and self.image.get_at(
                (x - leftx, y - topy)
            ) != (255, 255, 255, 255):

                return True
        except Exception:
            pass
        return False
