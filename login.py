#login.py
import pygame
from pygame.locals import *

class LoginScreen:
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Login Screen')
        self.WHITE = (255, 255, 255, 200)
        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 32)
        self.username = ''
        self.password = ''
        self.username_active = True
        self.password_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if self.is_username_active():
                        self.username = self.username[:-1]
                    elif self.is_password_active():
                        self.password = self.password[:-1]
                elif event.key == K_TAB:
                    self.toggle_username_active()
                    self.toggle_password_active()
                elif event.key == K_RETURN:
                    if self.username and self.password:
                        return True
                else:
                    if self.is_username_active() and len(self.username) < 25:
                        self.username += event.unicode
                    elif self.is_password_active() and len(self.password) < 30:
                        self.password += event.unicode
        return None

    def display(self):
        background = pygame.image.load('assets/images/background/bg.png')  
        background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        self.screen.blit(background, (0, 0))
        title_text = self.font.render('Login', True, self.WHITE)
        username_text = self.font.render('Username:', True, self.WHITE)
        password_text = self.font.render('Password:', True, self.WHITE)

        # Truncate the username to a maximum of 25 characters
        truncated_username = self.username[:25]

        username_input = self.font.render(truncated_username, True, self.BLACK)
        password_input = self.font.render('*' * len(self.password), True, self.BLACK)
        username_rect = pygame.Rect(200, 200, 400, 50)
        password_rect = pygame.Rect(200, 300, 400, 50)
        pygame.draw.rect(self.screen, self.WHITE, username_rect, 2)
        pygame.draw.rect(self.screen, self.WHITE, password_rect, 2)
        self.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, 100))
        self.screen.blit(username_text, (76, 211))
        self.screen.blit(password_text, (82, 312))

        # Adjust the X coordinate to center the text in the input boxes
        username_input_x = 210 + (380 - username_input.get_width()) // 2
        password_input_x = 210 + (380 - password_input.get_width()) // 2

        # Adjust the Y coordinate to center the text vertically
        username_input_y = 214
        password_input_y = 319

        self.screen.blit(username_input, (username_input_x, username_input_y))
        self.screen.blit(password_input, (password_input_x, password_input_y))
        pygame.display.flip()


    def is_username_active(self):
        return self.username_active

    def is_password_active(self):
        return self.password_active

    def toggle_username_active(self):
        self.username_active = not self.is_username_active()

    def toggle_password_active(self):
        self.password_active = not self.is_password_active()

    def run(self):
        while True:
            result = self.handle_events()
            if result is not None:
                return result
            self.display()

