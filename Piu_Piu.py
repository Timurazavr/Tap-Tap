import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("ship.png"), (150, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.width, self.height = width, height
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 9)
        self.speedx = random.randrange(-3, 3)
        self.width, self.height = width, height

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > self.height + 10
            or self.rect.left < -25
            or self.rect.right > self.width + 20
        ):
            self.rect.x = random.randrange(self.width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 9)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def main(screen, clock, width, height, FPS):
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    player = Player(width, height)
    all_sprites.add(player)
    for _ in range(10):
        m = Asteroid(width, height)
        all_sprites.add(m)
        asteroids.add(m)

    counter = 0
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.shoot(all_sprites, shots)

        all_sprites.update()

        hits = pygame.sprite.groupcollide(asteroids, shots, True, True)
        for _ in hits:
            m = Asteroid(width, height)
            all_sprites.add(m)
            asteroids.add(m)
            counter += 1

        hits = pygame.sprite.spritecollide(player, asteroids, False)
        if hits:
            return counter

        screen.fill("black")
        all_sprites.draw(screen)

        pygame.display.flip()
