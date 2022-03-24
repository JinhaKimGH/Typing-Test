import settings
import time
import constants as cs
import pygame

class Typing:
    def __init__(self):
        self.wpm = 0
        self.percentage = 0
        self.counter = 0
        self.sentence = settings.words
        self.correct = {}
        self.incorrect = ""
        self.letters = {x: pygame.key.key_code(x) for x in "abcdefghijklmnopqrstuvwxyz"}
        self.input = 0

    def update(self, keys):
        self.check_input(keys)
        self.calculate_percentage()
        self.calculate_wpm()

    def check_input(self, keys):
        if self.counter == len(self.sentence):
            return

        letter = self.sentence[self.counter]

        if keys == 8:
            if self.counter == 0:
                return

            self.counter -= 1

            if self.correct[len(self.correct) - 1] == False:
                self.incorrect = self.incorrect[:-1]

            self.correct.pop(len(self.correct) - 1)

            return


        #If the letter is capital and the input has shift
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


        #If the letter is capital and the input does not have shift
        elif 65 <= ord(letter) <= 90:
            self.incorrect += chr(keys)
            self.correct[self.counter] = False
            self.counter += 1
            self.input += 1


        #If the key is lowercase and correct
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

    def calculate_percentage(self):
        self.percentage = (len(self.sentence) - len(self.incorrect))/len(self.sentence)

        self.percentage = round(self.percentage * 100, 1)

    def calculate_wpm(self):
        if self.counter == len(self.sentence):
            return

        self.wpm = ((self.input) / 5) / (time.process_time() / 60)
        self.wpm = round(self.wpm)

    def draw(self):
        font = pygame.font.SysFont(settings.font_type, cs.FSIZE)

        input_length = len(self.correct)

        position = (settings.screen_w//2) - (len(settings.words) * cs.FSIZE//2)//2
        height = settings.screen_h/2

        wrong_counter = 0

        for i in range(input_length):

            if self.correct[i] == True:
                text = font.render(settings.words[i], True, cs.GREEN)
                text_rect = text.get_rect(center=(position, height))
                settings.screen.blit(text, text_rect)

            else:
                if self.incorrect[wrong_counter] == " ":
                    text = font.render("_", True, cs.RED)
                    text_rect = text.get_rect(center=(position, height))

                else:
                    text = font.render(self.incorrect[wrong_counter], True, cs.RED)
                    text_rect = text.get_rect(center=(position, height))

                settings.screen.blit(text, text_rect)
                wrong_counter += 1

            position += 15

            if position >= settings.screen_w - 15:
                position = (settings.screen_w//2) - (len(settings.words) * cs.FSIZE//2)//2
                height += 30

        for i in range(input_length, len(settings.words)):
            text = font.render(settings.words[i], True, cs.WHITE)
            text_rect = text.get_rect(center=(position, height))
            settings.screen.blit(text, text_rect)
            position += 15

            if position >= settings.screen_w - 15:
                position = (settings.screen_w//2) - (len(settings.words) * cs.FSIZE//2)//2
                height += 30

        wpm_text = font.render("WPM: "+str(self.wpm), True, cs.WHITE)
        wpm_rect = wpm_text.get_rect(center=(60, settings.screen_h - cs.FSIZE))

        percentage_text = font.render("Percentage: " + str(self.percentage) + "%", True, cs.WHITE)
        percentage_rect = percentage_text.get_rect(center=(settings.screen_w - 150, settings.screen_h - cs.FSIZE))

        settings.screen.blit(wpm_text, wpm_rect)
        settings.screen.blit(percentage_text, percentage_rect)

        pygame.display.update()