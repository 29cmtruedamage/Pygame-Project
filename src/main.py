import pygame
from sys import exit
import random

import pygame.docs

#inital declarations
pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multigame World")
clock = pygame.time.Clock()
gameStatus = True







#game loop
while gameStatus:
    
    for event in pygame.event.get(): 
        #Quit-Event Handling
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    
    
    
    
    
    
    
    pygame.display.update()