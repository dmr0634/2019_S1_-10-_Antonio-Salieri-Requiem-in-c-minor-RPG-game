if __name__ == '__main__':

    import pygame

    from pygame.locals import *
    from player import Player

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    WINDOW_SIZE = (800, 600)

    RUNNING = True

    TITLE = 'CONTROL METHOD TEST'

    CLOCK = pygame.time.Clock()

    FPS = 60

    WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    player = Player(WINDOW)

    pygame.display.set_caption(TITLE)

    def update():
        player.update()

    def draw(screen):
        player.draw()

    while RUNNING:
        for event in pygame.event.get():
            if event.type is QUIT:
                quit()
            if event.type is KEYDOWN and event.key is K_q:
                quit()
            if event.type is KEYDOWN and event.key is K_ESCAPE:
                quit()

        WINDOW.fill((0,0,0))

        update()
        draw(WINDOW)

        CLOCK.tick(FPS)

        pygame.display.flip()

