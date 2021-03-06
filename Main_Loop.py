# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:26:38 2020

@author: Jared Britton
"""

import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (RLEACCEL,
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        K_SPACE,
        K_p,
        K_r,
        K_n,
        K_s,
        QUIT,)

class Pipe(pygame.sprite.Sprite):
        def __init__(self, pipe_y):
            super(Pipe,self).__init__()
            self.surf = pygame.image.load("pipe.png").convert() #.convert_alpha()
            self.rect = self.surf.get_rect()
            self.rect.topleft = (850, pipe_y) #x,*y*
        def attack(self):
            self.rect.move_ip(-3,0)
            if self.rect.right < 50:
                self.kill()
                
class Pipe_d(pygame.sprite.Sprite):
        def __init__(self, pipe_y):
            super(Pipe_d,self).__init__()
            self.surf = pygame.image.load("pipe_down.png").convert() #.convert_alpha()
            self.rect = self.surf.get_rect()
            self.rect.bottomleft = (850, pipe_y) #x,*y*
        def attack(self):
            self.rect.move_ip(-3,0)
            if self.rect.right < 50:
                self.kill()

class Bird(pygame.sprite.Sprite):
        def __init__(self):
            super(Bird,self).__init__()
            self.original_surf = pygame.image.load("blue_flappy_2.png").convert_alpha()
            self.surf = self.original_surf
            self.rect = self.surf.get_rect()
            self.rect.center = (80, 250)
        def fly(self, pressed_keys):
            self.rect.move_ip(0,4)
            temp_center = self.rect.center
            self.surf = pygame.transform.rotate(self.original_surf, -18).convert_alpha()
            self.rect = self.surf.get_rect()
            self.rect.center = temp_center
            if self.rect.top < 0:
                self.rect.center = (80,60)
            if pressed_keys[K_SPACE]:
                self.rect.move_ip(0, -12)
                temp_center = self.rect.center
                self.surf = pygame.transform.rotate(self.original_surf, 18).convert_alpha()
                self.rect = self.surf.get_rect()
                self.rect.center = temp_center
                
def start_screen():
    font = pygame.font.Font(None, 74)
    text = font.render(str("'S' TO PLAY"), 1, white)
    screen.blit(text, (250,270))
    
def game_over(score):
    font = pygame.font.Font(None, 74)
    font2 = pygame.font.Font(None, 50)
    text = font.render(str("GAME OVER"), 1, white)
    text_score = font2.render(str("Score: " + str(score)), 1, white)
    screen.blit(text, (225,270))
    screen.blit(text_score, (315,350))
                         
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

bkcolor = (85,45,72)
black = (0,0,0)
white = (255,255,255)

pygame.init()     

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))# Fill background

bird = Bird()
 
#backround image
grass = pygame.image.load("grass.png").convert()
 
#sound
crash_sound = pygame.mixer.Sound("jump_01.wav")
woosh = pygame.mixer.Sound("woosh.wav")

#Sprite group
pipe_group = pygame.sprite.Group()
top_pipe_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(bird)

# Create a custom event for adding a new enemy
ADDPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPIPE, 2500)
  
#game clock
clock = pygame.time.Clock()


def game_loop():
    running = True
    not_paused = True
    start = False
    score = 0
    while running == True:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_p:
                    not_paused = False
                if event.key == K_r:
                    not_paused = True
                if event.key == K_SPACE:
                    pygame.mixer.Sound.play(woosh)
                    pygame.mixer.music.stop()
                if event.key == K_s:
                    start = True
                if event.key == K_n and not_paused == False:
                    bird.rect.center = (80, 250)
                    score = 0
                    for entity in pipe_group:
                        entity.kill()
                    not_paused = True
                                        
            elif event.type == ADDPIPE and not_paused == True and start == True:
                # Create the new pipe and add it to sprite groups
                rand_int = random.randint(250,500)
                #add pipes
                new_pipe = Pipe(rand_int)
                new_pipe_d = Pipe_d(rand_int - 170)
                #add pipes to groups
                pipe_group.add(new_pipe,new_pipe_d)
                all_sprites.add(new_pipe,new_pipe_d)
                top_pipe_group.add(new_pipe_d)
                
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        bird.update(pressed_keys)
        
        
        if not_paused == True:
            
            #move bird
            if start == True:
                bird.fly(pressed_keys)
        
            #add background
            screen.fill(white)
            screen.blit(grass, [0, 0])
            
            #start screen
            if start == False:                
                start_screen()
                
            # Draw all sprites
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
        
            for entity in pipe_group:
                entity.attack()
                
            #bird bottom boundaries
            if bird.rect.top > 545:
                not_paused = False
                game_over(score)
                
            #update score and play sound effect
            for entity in top_pipe_group:
                if entity.rect.left == 25:
                    score += 1 
                    pygame.mixer.Sound.play(crash_sound)
                    pygame.mixer.music.stop()
 
            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(bird, pipe_group):
                not_paused = False
                game_over(score)
                
             #Display scores:
            font = pygame.font.Font(None, 74)
            text = font.render(str(score), 1, white)
            screen.blit(text, (25,10))
            
            #update display 
            pygame.display.update()
                
            clock.tick(60)

game_loop()
pygame.quit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    