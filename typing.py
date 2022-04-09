import settings as settings
import time
import pygame


class Typing:
    # Initializes the typing class
    def __init__(self):
        self.wpm = 0
        self.percentage = 0
        self.counter = 0
        self.sentence = settings.words
        self.correct = {}
        self.incorrect = ""
        self.letters = {x: pygame.key.key_code(x) for x in "abcdefghijklmnopqrstuvwxyz"}
        self.input = 0

    # Updates the screen and class based on the input it receives
    def update(self, keys):
        self.check_input(keys)
        self.calculate_percentage()
        self.calculate_wpm()

    # Checks for the type of input and the letter it corresponds to
    def check_input(self, keys):
        # If the user types more letters than the length of the sentence
        if self.counter == len(self.sentence):
            return

        letter = self.sentence[self.counter]

        # If the key is a backspace
        if keys == 8:
            if self.counter == 0:
                return

            self.counter -= 1

            if self.correct[len(self.correct) - 1] is False:
                self.incorrect = self.incorrect[:-1]

            self.correct.pop(len(self.correct) - 1)

            return

        # If the letter is capital and the input has shift
        if 65 <= ord(letter) <= 90 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
            if keys - 32 == ord(letter):
                self.correct[self.counter] = True
                self.counter += 1
                self.input += 1

            else:
                self.incorrect += chr(keys)
                self.correct[self.counter] = False
                self.counter += 1
                self.input += 1

        # If the letter is capital and the input does not have shift
        elif 65 <= ord(letter) <= 90:
            self.incorrect += chr(keys)
            self.correct[self.counter] = False
            self.counter += 1
            self.input += 1

        # If the key is lowercase and correct
        else:
            if keys == ord(letter):
                self.correct[self.counter] = True
                self.counter += 1
                self.input += 1

            else:
                self.incorrect += chr(keys)
                self.correct[self.counter] = False
                self.counter += 1
                self.input += 1

    # Calculates the correctness of the input
    def calculate_percentage(self):
        self.percentage = (len(self.sentence) - len(self.incorrect))/len(self.sentence)

        self.percentage = round(self.percentage * 100, 1)

    # Calculates WPM based on the WPM formula
    def calculate_wpm(self):
        if self.counter == len(self.sentence):
            return

        self.wpm = (self.input / 5) / (time.process_time() / 60)
        self.wpm = round(self.wpm)

    # Updates the screen
    def draw(self):
        # Creates the pygame font
        font = pygame.font.SysFont(settings.font_type, settings.FSIZE)

        input_length = len(self.correct)

        position = 15
        height = settings.screen_h/2

        wrong_counter = 0

        # Changes the color of each letter depending on the user's input
        for i in range(input_length):

            if self.correct[i] is True:
                text = font.render(settings.words[i], True, settings.GREEN)
                text_rect = text.get_rect(center=(position, height))
                settings.screen.blit(text, text_rect)

            else:
                if self.incorrect[wrong_counter] == " ":
                    text = font.render("_", True, settings.RED)
                    text_rect = text.get_rect(center=(position, height))

                else:
                    text = font.render(self.incorrect[wrong_counter], True, settings.RED)
                    text_rect = text.get_rect(center=(position, height))

                settings.screen.blit(text, text_rect)
                wrong_counter += 1

            position += 15

            if position >= settings.screen_w - 15:
                position = 15
                height += 30

        # Draws the rest of the letters the user hasn't encountered yet
        for i in range(input_length, len(settings.words)):
            text = font.render(settings.words[i], True, settings.WHITE)
            text_rect = text.get_rect(center=(position, height))
            settings.screen.blit(text, text_rect)
            position += 15

            if position >= settings.screen_w - 15:
                position = 15
                height += 30

        wpm_text = font.render("WPM: "+str(self.wpm), True, settings.WHITE)
        wpm_rect = wpm_text.get_rect(center=(60, settings.screen_h - settings.FSIZE))

        percentage_text = font.render("Percentage: " + str(self.percentage) + "%", True, settings.WHITE)
        percentage_rect = percentage_text.get_rect(center=(settings.screen_w - 150, settings.screen_h - settings.FSIZE))

        # Displays the WPM and Percentage text onto the screen
        settings.screen.blit(wpm_text, wpm_rect)
        settings.screen.blit(percentage_text, percentage_rect)

        # Updates the screen
        pygame.display.update()
