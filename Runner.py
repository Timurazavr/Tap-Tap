import pygame
import db
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
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
    def __init__(self, width, height, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width, width + self.rect.width)
        self.rect.y = random.randrange(0, height - self.rect.height)
        self.speedx = random.randrange(3, 9)
        self.width, self.height = width, height

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left < 0:
            self.rect.x = random.randrange(self.width, self.width + self.rect.width)
            self.rect.y = random.randrange(0, self.height - self.rect.height)
            self.speedx = random.randrange(3, 9)


def main(screen, clock, width, height, FPS):
    player_img = pygame.image.load("male.png")
    coin_img = pygame.image.load("video_coin/star coin rotate 1.png")

    all_sprites = pygame.sprite.Group()
    player = Player(player_img)
    all_sprites.add(player)
    coin = Coin(width, height, coin_img)
    all_sprites.add(coin)
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        hits = player.rect.colliderect(coin.rect)
        if hits:
            coin.rect.x = random.randrange(coin.width, coin.width + coin.rect.width)
            coin.rect.y = random.randrange(0, coin.height - coin.rect.height)
            coin.speedx = random.randrange(3, 9)
        screen.fill((10, 10, 10))
        all_sprites.draw(screen)
        pygame.display.flip()

    return 1
