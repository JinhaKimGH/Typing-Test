from constants import *
from settings import *
import pygame

def main():
    pygame.init()
    run = True

    sentences = Typing()
    pygame.key.set_repeat()
    while run:
        #If quit button is pressed, screen closes
        sentences.draw()

        for event in pygame.event.get():
            sentences.calculate_wpm()
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if 0 <= event.key <= 127 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    sentences.update(event.key)

                elif 0 <= event.key <= 127:
                    sentences.update(event.key)

        settings.screen.fill(BLACK)
    pygame.quit()

if __name__ == "__main__":
    main()