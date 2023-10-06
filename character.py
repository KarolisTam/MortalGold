#character.py
import pygame

class Character():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle, 1:run, 2:jump, 3:punch, 4:kick, 5:gethit
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

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
            #print(f"Loaded spritesheet for {self.player}: {sprite_sheet}")
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 8
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other action if not currently attacking
        if self.attacking == False:
            # movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
                #print(f"player id {self.player}: press A ")
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
                #print(f"player id {self.player}: press D ")

            # jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
                #print(f"player id {self.player}: press W ")


            # Attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                # determine wich attact type was used
                if key[pygame.K_r]:
                    self.attack_type = 1
                    #print(f"player id {self.player} press R")
                if key[pygame.K_t]:
                    self.attack_type = 2
                    #print(f"player id {self.player} press T")

            # Block
            if key[pygame.K_q]:
                self.blocking = True
            else:
                self.blocking = False

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 90:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 90 - self.rect.bottom

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update player possition
        self.rect.x += dx
        self.rect.y += dy
    
    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death
        elif self.hit == True:
            self.update_action(5)  # getHit
        elif self.blocking == True:
            self.update_action(7)  # block
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # attack
            elif self.attack_type == 2:
                self.update_action(4)  # attack 2
        elif self.jump == True:
            self.update_action(2)  # jump
        elif self.running == True:
            self.update_action(1)  # running
        else:
            self.update_action(0)  # idle

        # Call the update_animation() method to update the animation frames.
        self.update_animation()
        #print(f"Updated action for {self.player}: {self.action}")

        return self.health

    def update_animation(self):
        animation_cooldown = 50
        # Update image based on the current action
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # If the player is dead, end the animation
            if self.alive is False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # If the player was in the middle of an attack, then stop the attack
                    self.attacking = False
                    self.attack_cooldown = 20
                    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip), 
                self.rect.y, 
                2 * self.rect.width, 
                self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                if target.blocking:
                    target.health -= 1  # Reduce health by half if blocking
                else:
                    target.health -= 10  # Normal damage
                target.hit = True
        
            # pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        #print(f"Updated action for {self.player}: {self.action}")

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


class Opponent():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:punch #4:kick #5:gethit #6:death #7:dizzy #8:victory #9:
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

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
            print("image loaded")
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        print("oponentas nejuda")

        # can only perform other action if not currently attacking
        if self.attacking == False:
            # movement
            if self.action == 1:
                self.running = True
            if self.action == 1:
                self.running = True
                print("oponentas juda i sonus")

            # jump
            if self.action == 2 and self.jump == False:
                self.jump = True

            # Attack
            if self.action == 3 or self.action == 4:
                self.attack(surface, target)
                # determine wich attact type was used
                if self.action == 3:
                    self.attack_type = 1
                if self.action == 4:
                    self.attack_type = 2

            # Block
            if self.action == 7:
                self.blocking = True
            else:
                self.blocking = False
    
    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death
        elif self.hit == True:
            self.update_action(5)  # getHit
        elif self.blocking == True:
            self.update_action(7)  # block
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # attack
            elif self.attack_type == 2:
                self.update_action(4)  # attack 2
        elif self.jump == True:
            self.update_action(2)  # jump
        elif self.running == True:
            self.update_action(1)  # running
        else:
            self.update_action(0)  # idle

        # Call the update_animation() method to update the animation frames.
        self.update_animation()

        return self.health

    def update_animation(self):
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check if damage was taken~
                if self.action == 5:
                    self.hit = False
                    # if the player was in the middle of an attack then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
                    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip), 
                self.rect.y, 
                2 * self.rect.width, 
                self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                if target.blocking:
                    target.health -= 1  # Reduce health by half if blocking
                else:
                    target.health -= 10  # Normal damage
                target.hit = True
        
            # pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))