import pygame
from modules.buttons import StartButton
from modules import game_menu
import sys

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    FPS = 60
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Tap-Tap")
    clock = pygame.time.Clock()

    version_font = pygame.font.Font("textures/fonts/bubl.ttf", 40).render(
        "beta, by Timurazavr and Pashok7290", True, "black"
    )
    version_coord = (
        width - version_font.get_width() - 10,
        height - version_font.get_height() - 10,
    )
    title_font = pygame.font.Font("textures/fonts/bubl.ttf", 200).render(
        "Tap-Tap", True, "black"
    )
    title_coord = (
        width // 2 - title_font.get_width() // 2,
        height // 5,
    )

    start_button = StartButton(width // 2, height // 3 * 2)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(start_button)

    counter_bg = -1
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if start_button.collidepoint(*event.pos):
                        game_menu.main(screen, clock, width, height, FPS)

        all_sprites.update()

        counter_bg = (counter_bg + 1) % 99
        screen.blit(
            pygame.image.load(f"textures/video_bg/video_{counter_bg:03}.jpg"), (-200, 0)
        )

        screen.blit(version_font, version_coord)
        screen.blit(title_font, title_coord)

        all_sprites.draw(screen)

        pygame.display.flip()
pygame.quit()
