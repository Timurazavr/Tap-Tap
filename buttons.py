import pygame


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
            (height // 2, 0, width - height, height),
        )
        pygame.draw.circle(
            self.image, self.color, (width - height // 2, height // 2), height // 2
        )
        txt = pygame.font.SysFont("Arial", 40).render("Играть", True, "black")
        self.image.blit(
            txt,
            (
                width // 2 - txt.get_width() // 2,
                height // 2 - txt.get_height() // 2,
            ),
        )

    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.counterx += 0.5 if self.flag else -0.5
            self.countery += 0.25 if self.flag else -0.25
            self.draw(self.width + self.counterx, self.height + self.countery)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y
            if self.counterx == -20 or self.counterx == 0:
                self.flag = not self.flag

    def call_back(self):
        print(0)
