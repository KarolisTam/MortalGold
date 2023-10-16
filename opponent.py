import pygame

class Opponent():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0:idle, 1:run, 2:jump, 3:punch, 4:kick, 5:gethit, 6:death, 7:block
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index] 
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.blocking = False
        self.frame_indices = [0] * len(animation_steps)

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update_animation(self):
        animation_cooldown = 50
        
        if self.alive:
            if 0 <= self.action < len(self.animation_list):
                if 0 <= self.frame_indices[self.action] < len(self.animation_list[self.action]):
                    self.image = self.animation_list[self.action][self.frame_indices[self.action]]
                    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                        self.frame_indices[self.action] += 1
                        self.update_time = pygame.time.get_ticks()

                    if self.frame_indices[self.action] >= len(self.animation_list[self.action]):
                        self.frame_indices[self.action] = 0  # Reset animation frame for the current action

    # Add a new method to reset the frame index for a specific action
    def reset_frame_index(self, action):
        self.frame_indices[action] = 0

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        