import pygame
import sys

# Game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mortal Gold")

WHITE = (255, 255, 255)

class CharacterSelectionScreen:
    def __init__(self):
        self.selected_character = None
        self.font = pygame.font.SysFont(None, 50)
        self.title_text = self.font.render("Select a Character", True, WHITE)
        self.character_texts = [
            self.font.render("Putin", True, WHITE),
            self.font.render("Musk", True, WHITE)
        ]
        self.character_rects = [
            self.character_texts[0].get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)),
            self.character_texts[1].get_rect(center=(SCREEN_WIDTH // 4 * 3, SCREEN_HEIGHT // 2))
        ]
        self.active = True

    def draw(self, screen):
        screen.blit(self.title_text, (SCREEN_WIDTH // 2 - self.title_text.get_width() // 2, 100))
        for i, text in enumerate(self.character_texts):
            screen.blit(text, self.character_rects[i])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.character_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_character = i
                        self.active = False

    def run(self):
        while self.active:
            self.handle_events()
            screen.fill((0, 0, 0))
            self.draw(screen)
            pygame.display.flip()
