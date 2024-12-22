import pygame
from buttons import StartButton

FPS = 60

pygame.init()
pygame.mixer.init()
width, height = 1536, 801  # 1000, 600
screen = pygame.display.set_mode((width, height), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Tap-Tap")
clock = pygame.time.Clock()


txt_version = pygame.font.Font("fonts/bubl.ttf", 40).render(
    "beta, by Timurazavr and Pashok7290", True, "black"
)
txt_name = pygame.font.Font("fonts/bubl.ttf", 200).render("Tap-Tap", True, "black")
start_button = StartButton(width // 2, height // 3 * 2, 500, 150, "red", "Играть")
all_sprites = pygame.sprite.Group()
all_sprites.add(start_button)
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            surface = pygame.display.set_mode(
                (width, height), pygame.SCALED | pygame.RESIZABLE
            )
    all_sprites.update()
    screen.fill("white")

    screen.blit(
        txt_version,
        (width - txt_version.get_width() - 10, height - txt_version.get_height() - 10),
    )
    screen.blit(
        txt_name,
        (
            width // 2 - txt_name.get_width() // 2,
            height // 5,
        ),
    )
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
