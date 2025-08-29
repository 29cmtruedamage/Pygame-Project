import pygame
from sys import exit
import random
import menuHandling as mh
import pygame.docs

#inital declarations
pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Multigame World")
clock = pygame.time.Clock()
gameStatus = True

def main():
    
    
   
    

    #state-deklarations
    menu_state = True
    jumpAndRun_state = False

    #helper variables
    
    
    
    #game loop
    while gameStatus:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get(): 
            #Quit-Event Handling
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #mouseDown event handling        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mh.defaultVektor_rect_Game1.collidepoint(mouse_pos):
                    menu_state = False
                    jumpAndRun_state = True
                         
        #menu-handling
        if menu_state:
            #KeyDown event handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("BBB")
                    pygame.quit()
                    exit()
                    

            mh.menu_mainMenuPicScreening()
            mh.menu_defaultVektorScreening()
            mh.menu_vektorScreening()
        
        if jumpAndRun_state:
            #KeyDown event handling
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    jumpAndRun_state = False
                    menu_state = True
                    print("aaa")
            screen.fill('Black')
        
        
        #essentials
        clock.tick(60)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
