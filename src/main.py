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

#time variables
#startTime = 0
def main():
    #state-deklarations
    startScreenState = True
    menu_state = False 
    
    jumpAndRun_state = False
    jumpAndRun_GameOnState = False
    speedUp = False
    
    PongGame_state = False
    PongGame_GameOnState = False
    
    #new Self-defined USEREVENTS
    timeToSpawnObstacle = 2000
    obstacleSpawnTimer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacleSpawnTimer, timeToSpawnObstacle)
    
    timeToSpawnObstacle_speedUp = 800
    obstacleSpawnTimer_speedUp = pygame.USEREVENT + 2
    pygame.time.set_timer(obstacleSpawnTimer_speedUp, timeToSpawnObstacle_speedUp)
    
    firstLevel = 100
    secondLevel = 150
    
    #Background
    background_image = mh.background_image
    background_rect1 = mh.background_rect
    background_rect2 = background_image.get_rect(center = (1500, 300))
    #Underground
    underground_image = pygame.transform.scale(pygame.image.load('environment/graphics/Untergrund.png'), 
                                               (1050, 250)).convert_alpha()
    underground_rect1 = underground_image.get_rect(midtop = (500, 500))
    underground_rect2 = underground_image.get_rect(midtop = (1500, 500))
    backgroundSpeed = 1
    undergroundSpeed = 4
    environmentRectList = [background_rect1, background_rect2, 
                            underground_rect1, underground_rect2]
    
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
    
    pongBallSound = pygame.mixer.Sound('environment/audios/BallSound.mp3')
    pongBallSound.set_volume(0.5)
    
    pongGameBM = pygame.mixer.Sound('environment/audios/PongGameBM.mp3')
    pongGameBM.set_volume(0.5)
    
    #helper variables
    #time
    currentTime = pygame.time.get_ticks()
    startTime = 0
    #score
    highScore = 0
    score = 0
    #declaring player and obstacles
    player = pygame.sprite.GroupSingle()
    player.add(jar.Player())
    
    obstacle_group = pygame.sprite.Group()
    
    def jarGameOver():
        global backgroundSpeed, undergroundSpeed, speedUp, score
        jar.gameOverScreen(screen)
        backgroundSpeed = 1
        undergroundSpeed = 4
        jar.environmentReset(environmentRectList)
        player.sprite.playerReset()
        speedUp = False
        score = 0
        obstacle_group.empty()
        print("Game Over")
        jarMusik.stop()
        
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
                    menuMusik.play(10)     
                    startScreenState = False    
                    menu_state = True 
                    print("StartScreen") 
                
                #menuScreen
                elif menu_state:
                    if mh.defaultVektor_rect_Game1.collidepoint(mouse_pos):
                        menu_state = False
                        jumpAndRun_state = True
                        jumpAndRun_GameOnState = True
                        menuMusik.stop()
                        gameStartSound.play()
                        time.sleep(0.2)
                        jarMusik.play(10)
                        startTime = pygame.time.get_ticks()
                        obstacle_group.empty()
                    #For next Games
                    if mh.defaultVektor_rect_Game2.collidepoint(mouse_pos):
                        menu_state = False
                        PongGame_state = True
                        menuMusik.stop()
                        gameStartSound.play()
                        time.sleep(0.2)
                        pongGameBM.play(15)
                        screen.fill((0,0,0))
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
                elif jumpAndRun_state:
                    if event.key == pygame.K_ESCAPE:
                        jumpAndRun_state = False
                        jumpAndRun_GameOnState = False
                        speedUp = False
                        menu_state = True
                        jar.environmentReset(environmentRectList)
                        player.sprite.playerReset()
                        jarMusik.stop()
                        menuMusik.play(15)
                        
                            
                    if jumpAndRun_GameOnState == False:
                        if event.key == pygame.K_RETURN: #Return = EnterTaste
                            jumpAndRun_GameOnState = True     
                            startTime = pygame.time.get_ticks()
                            jarMusik.play(15)
                            
                elif PongGame_state:
                    if event.key == pygame.K_ESCAPE:
                        PongGame_state = False
                        menu_state = True
                        jar.environmentReset(environmentRectList)
                        pongGameBM.stop()
                        menuMusik.play(15)
            #specific event Types:
            if jumpAndRun_GameOnState and not speedUp:
                if event.type == obstacleSpawnTimer and score < firstLevel:
                    obstacle_group.add(jar.Obstacle(random.choice(['bird','tree1','tree2','bird','tree1','tree2','tree3','mushroom'])))
                if score > secondLevel: 
                    speedUp = True
                    player.sprite.playerSpeedUp()
                    backgroundSpeed = 3
                    undergroundSpeed = 12
            if speedUp:
                if event.type == obstacleSpawnTimer_speedUp:
                    obstacle_group.add(jar.Obstacle(random.choice(['bird','tree1','tree2','bird','tree1','tree2','tree3','mushroom'])))
                    jar.obstacle_SpeedUp(obstacle_group)
                    
                    
        #State Handling
        # 
                     
        if startScreenState:
            screen.fill((10,100,200))
            print("StartSCreen")
                 
        #menu-handling
        if menu_state:
            #KeyDown event handling
            
            print("Menu")
            
            mh.menu_mainMenuPicScreening()
            mh.menu_defaultVektorScreening(mouse_pos)
            mh.menu_vektorScreening()
            
        if jumpAndRun_state:
            #KeyDown event handling
            if jumpAndRun_GameOnState:
                
                jar.drawEnvironment(screen, background_image, underground_image, 
                                    environmentRectList)
                jar.manageEnvironment(environmentRectList, backgroundSpeed, undergroundSpeed)
                score = jar.drawScore(screen, startTime, highScore=highScore)
                print("GAME ONNNN")
                highScore = jar.checkHighscore(highScore, score)
                player.draw(screen)
                player.update()
                obstacle_group.draw(screen)
                obstacle_group.update()
                jumpAndRun_GameOnState = jar.collisionCheck(player, obstacle_group, gameOverSound)
                
            else:
                jar.gameOverScreen(screen)
                backgroundSpeed = 1
                undergroundSpeed = 4
                jar.environmentReset(environmentRectList)
                player.sprite.playerReset()
                speedUp = False
                score = 0
                obstacle_group.empty()
                print("Game Over")
                jarMusik.stop()
        
                
                
        #essentials
        clock.tick(80)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
