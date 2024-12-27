import pygame
from modules import db
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.centery = height // 2
        self.speed = db.read("speed")

    def update(self):
        self.speedx = self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy = -self.speed
        if keystate[pygame.K_s]:
            self.speedy = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Coin(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width, width + self.rect.width)
        self.rect.y = random.randrange(0, height - self.rect.height)
        self.speedx = random.randrange(5, 10)
        self.width, self.height = width, height

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left < 0:
            self.rect.x = random.randrange(self.width, self.width + self.rect.width)
            self.rect.y = random.randrange(0, self.height - self.rect.height)
            self.speedx = random.randrange(3, 9)


def main(screen, clock, width, height, FPS):
    player_img = pygame.image.load("textures/male.png")
    coin_img = pygame.image.load("textures/video_coin/star coin rotate 1.png")

    all_sprites = pygame.sprite.Group()

    player = Player(width, height, player_img)
    all_sprites.add(player)

    coin = Coin(width, height, coin_img)
    all_sprites.add(coin)

    counter = 0
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return counter
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return counter
        all_sprites.update()

        hits = pygame.sprite.collide_mask(coin, player)
        if hits:
            coin.rect.x = random.randrange(coin.width, coin.width + coin.rect.width)
            coin.rect.y = random.randrange(0, coin.height - coin.rect.height)
            coin.speedx = random.randrange(3, 9)
            counter += 1

        screen.fill((10, 10, 10))
        all_sprites.draw(screen)
        pygame.display.flip()
