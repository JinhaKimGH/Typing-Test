from typing import *
from settings import *
import pygame


def main():
    # Initializes the pygame library
    pygame.init()
    run = True

    # Creates an instance of the Typing class
    sentences = Typing()
    pygame.key.set_repeat()
    while run:
        # Displays the sentence on the pygame screen
        sentences.draw()

        # Goes through each event that occurs in a frame
        for event in pygame.event.get():
            sentences.calculate_wpm()

            # If quit button is pressed, screen closes
            if event.type == pygame.QUIT:
                run = False

            # If a key is pressed, the screen updates
            if event.type == pygame.KEYDOWN:
                if 0 <= event.key <= 127 and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    sentences.update(event.key)

                elif 0 <= event.key <= 127:
                    sentences.update(event.key)

        # Turns the entire screen black so that it can be updated
        settings.screen.fill(BLACK)

    # Deactivates the pygame library
    pygame.quit()


if __name__ == "__main__":
    main()
