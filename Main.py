import sys
import pygame
from gameObjects.Button import Button
from gui import GUI

if __name__ == '__main__':

    pygame.init()
    size = window_width, window_height = 1200, 600
    screen = pygame.display.set_mode(size)

    gui = GUI(screen, window_width, window_height)

    play_button = Button(window_width, gui.title.get_height(), "Play")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(gui.background, (0, 0))
        screen.blit(gui.title, ((window_width - gui.title.get_width()) // 2, gui.title.get_height() // 2))
        play_button.draw(screen)

        if play_button.is_over(pygame.mouse.get_pos()):
            play_button.button_bg = Button.ACTIVE_COLOR
        else:
            play_button.button_bg = Button.BG_COLOR

        pygame.display.flip()
