import pygame
from sys import exit
import random
import menuHandling as mh
import jumpAndRunHandling as jar
import pygame.docs
import time

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
    startScreenState = True
    menu_state = False 
    jumpAndRun_state = False
    
    
    #Sounds
    gameOverSound = pygame.mixer.Sound('environment/audios/GameOverSound.mp3')
    gameOverSound.set_volume(0.5)
    
    gameStartSound = pygame.mixer.Sound('environment/audios/GameStartSound.mp3')
    gameStartSound.set_volume(0.5)
    
    jumpSound = pygame.mixer.Sound('environment/audios/jumpSound.mp3')
    jumpSound.set_volume(0.5)
    
    menuMusik = pygame.mixer.Sound('environment/audios/MenuBackgroundMusik.mp3')
    menuMusik.set_volume(0.5)
    
    jarMusik = pygame.mixer.Sound('environment/audios/JumpAndRunBM.mp3')
    jarMusik.set_volume(0.5)
    
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
                #startScreen
                if startScreenState == True:
                    menuMusik.play()     
                    startScreenState = False    
                    menu_state = True 
                    print("StartScreen") 
                
                #menuScreen
                elif menu_state:
                    if mh.defaultVektor_rect_Game1.collidepoint(mouse_pos):
                        menu_state = False
                        jumpAndRun_state = True
                        menuMusik.stop()
                        gameStartSound.play()
                        time.sleep(0.2)
                        jarMusik.play()
                    #For next Games
                    # if mh.defaultVektor_rect_Game2.collidepoint(mouse_pos):
                    #     #doSth
                    # if mh.defaultVektor_rect_Game3.collidepoint(mouse_pos):
                    #     #doSth
                    # if mh.defaultVektor_rect_Game4.collidepoint(mouse_pos):
                    #     #doSth
                    
                

            
            #KeyDown Hanlding
            if event.type == pygame.KEYDOWN:
                
                #menuState
                if menu_state and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                
                #jarState
                elif jumpAndRun_state and event.key == pygame.K_ESCAPE:
                    jumpAndRun_state = False
                    menu_state = True
                    jarMusik.stop()
                    menuMusik.play()
        
        
        
                     
        if startScreenState:
            screen.fill((10,100,200))
            print("StartSCreen")
                 
        #menu-handling
        if menu_state:
            #KeyDown event handling
            
            print("Menu")
            
            mh.menu_mainMenuPicScreening()
            mh.menu_defaultVektorScreening()
            mh.menu_vektorScreening()
            
        if jumpAndRun_state:
            #KeyDown event handling
            
            screen.fill((0,0,0))        
            
            print("mmmm")
        
        
        #essentials
        clock.tick(60)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
