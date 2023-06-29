import pygame
import os


class GameView(View):
    template_name = 'game.html'

    def get(self, request):
        # Initialize Pygame
        pygame.init()
        
        # Set up the Pygame screen
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("My Game")

        # Load game assets
        image_path = os.path.join('static', 'game', 'image.png')
        image = pygame.image.load(image_path)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Game logic and drawing
            screen.fill((0, 0, 0))  # Fill the screen with black
            screen.blit(image, (0, 0))  # Draw the image on the screen
            
            pygame.display.flip()  # Update the display
            
        # Clean up Pygame
        pygame.quit()

        return render(request, self.template_name)