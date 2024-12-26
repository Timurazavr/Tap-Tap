import pygame
from buttons import StartButton
import game_menu

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    FPS = 60
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Tap-Tap")
    clock = pygame.time.Clock()

    txt_version = pygame.font.Font("fonts/bubl.ttf", 40).render(
        "beta, by Timurazavr and Pashok7290", True, "black"
    )
    txt_name = pygame.font.Font("fonts/bubl.ttf", 200).render("Tap-Tap", True, "black")

    start_button = StartButton(width // 2, height // 3 * 2, 500, 150, "red", "Играть")
    all_sprites = pygame.sprite.Group()
    all_sprites.add(start_button)

    counter_bg = -1

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if start_button.collide(*event.pos):
                        game_menu.main(screen, clock, width, height, FPS)

        all_sprites.update()

        counter_bg = (counter_bg + 1) % 99
        screen.blit(pygame.image.load(f"video_bg/video_{counter_bg:03}.jpg"), (-200, 0))

        screen.blit(
            txt_version,
            (
                width - txt_version.get_width() - 10,
                height - txt_version.get_height() - 10,
            ),
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
