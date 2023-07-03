import pygame

class AnimatedBackground:
    def __init__(self):
        self.background_images = [
            pygame.image.load("assets/images/background/bg.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg1.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg2.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg3.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg4.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg5.png").convert_alpha(),
            pygame.image.load("assets/images/background/bg6.png").convert_alpha(),
        ]
        self.current_frame = 0
        self.frame_count = len(self.background_images)
        self.animation_speed = 0.2  # Adjust the speed of the animation

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= self.frame_count:
            self.current_frame = 0

    def draw(self, surface):
        frame_index = int(self.current_frame)
        surface.blit(self.background_images[frame_index], (0, 0))



