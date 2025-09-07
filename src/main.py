import pygame
from sys import exit
import random
from src import menuHandling as mh
from src import jumpAndRunHandling as jar
from src import pingPongHandling as pp
from src.utils import resource_path
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
    
    PongGame2p_state = False
    PongGame2p_GameOnState = False
    PongGame2p_Tutorial_Screen = False
    
    PongGame1p_state = False
    PongGame1p_GameOnState = False
    PongGame1p_Tutorial_Screen = False
    #new Self-defined USEREVENTS
    timeToSpawnObstacle = 2000
    obstacleSpawnTimer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacleSpawnTimer, timeToSpawnObstacle)
    
    timeToSpawnObstacle_speedUp = 770
    obstacleSpawnTimer_speedUp = pygame.USEREVENT + 2
    pygame.time.set_timer(obstacleSpawnTimer_speedUp, timeToSpawnObstacle_speedUp)
    
    firstLevel = 100
    secondLevel = 150
    
    #Background
    background_image = mh.background_image
    background_rect1 = mh.background_rect
    background_rect2 = background_image.get_rect(center = (1500, 300))
    #Underground
    underground_image = pygame.transform.scale(pygame.image.load(resource_path('environment/graphics/Untergrund.png')), 
                                               (1050, 250)).convert_alpha()
    underground_rect1 = underground_image.get_rect(midtop = (500, 500))
    underground_rect2 = underground_image.get_rect(midtop = (1500, 500))
    backgroundSpeed = 1
    undergroundSpeed = 4
    environmentRectList = [background_rect1, background_rect2, 
                            underground_rect1, underground_rect2]
    
    #Sounds
    gameOverSound = pygame.mixer.Sound(resource_path('environment/audios/GameOverSound.mp3'))
    gameOverSound.set_volume(0.5)
    
    gameStartSound = pygame.mixer.Sound(resource_path('environment/audios/GameStartSound.mp3'))
    gameStartSound.set_volume(0.5)
    
    jumpSound = pygame.mixer.Sound(resource_path('environment/audios/jumpSound.mp3'))
    jumpSound.set_volume(0.5)
    
    menuMusik = pygame.mixer.Sound(resource_path('environment/audios/MenuBackgroundMusik.mp3'))
    menuMusik.set_volume(0.5)
    
    jarMusik = pygame.mixer.Sound(resource_path('environment/audios/JumpAndRunBM.mp3'))
    jarMusik.set_volume(0.5)
    
    pongBallSound = pygame.mixer.Sound(resource_path('environment/audios/BallSound.mp3'))
    pongBallSound.set_volume(0.5)
    
    pongGameBM = pygame.mixer.Sound(resource_path('environment/audios/PongGameBM.mp3'))
    pongGameBM.set_volume(0.5)
    
    pongGameWinner = pygame.mixer.Sound(resource_path('environment/audios/PongGameWinner.mp3'))
    pongGameWinner.set_volume(0.3)
    
    pongPointSound = pygame.mixer.Sound(resource_path('environment/audios/PointSound.mp3'))
    pongPointSound.set_volume(0.6)
    
    #colours 
    LightBlue = (204, 235, 255)
    #helper variables
    #time
    currentTime = pygame.time.get_ticks()
    startTime = 0
    #score
    highScore = 0
    score = 0
    #DECLARING OBJECTS
    #declaring player and obstacles
    player = pygame.sprite.GroupSingle()
    player.add(jar.Player())
    
    obstacle_group = pygame.sprite.Group()
    #declaring paddles
    paddle1 = pygame.sprite.GroupSingle()
    paddle1.add(pp.Paddle('player1'))

    paddle2 = pygame.sprite.GroupSingle()
    paddle2.add(pp.Paddle('player2'))

    opponendPaddle = pygame.sprite.GroupSingle()
    opponendPaddle.add(pp.opponend_Paddle())
    ball = pygame.sprite.GroupSingle()
    ball.add(pp.Ball())
    
    #PongBall Coordinate
    scoreP1 = 0
    scoreP2 = 0
    goal = False
    # ball_image = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/ball.png')), 0, 0.14)
    # ball = ball_image.get_rect(center = (500, 300))
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
                    if mh.defaultVektor_rect_Game4.collidepoint(mouse_pos): #PingPong 2-PL
                        menu_state = False
                        PongGame2p_Tutorial_Screen = True
                        pp.PingPongTutorialScreen(screen, '2p')
                        
                        
                    if mh.defaultVektor_rect_Game3.collidepoint(mouse_pos): #PingPong 1-Pl
                        menu_state = False
                        PongGame1p_Tutorial_Screen = True
                        pp.PingPongTutorialScreen(screen, '1p')
                    # if mh.defaultVektor_rect_Game4.collidepoint(mouse_pos):
                    #     #doSth    
                    
                elif PongGame2p_Tutorial_Screen:
                    PongGame2p_Tutorial_Screen = False
                    PongGame2p_state = True
                    PongGame2p_GameOnState = True
                    menuMusik.stop()
                    gameStartSound.play()
                    time.sleep(0.2)
                    pongGameBM.play(15)      
                        
                elif PongGame1p_Tutorial_Screen: 
                    PongGame1p_Tutorial_Screen = False
                    PongGame1p_state = True
                    PongGame1p_GameOnState = True
                    
                    menuMusik.stop()
                    gameStartSound.play()
                    time.sleep(0.2)
                    pongGameBM.play(15)  
            

            
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
                elif PongGame1p_state:
                    if event.key == pygame.K_ESCAPE:
                        PongGame1p_state = False
                        menu_state = True
                        jar.environmentReset(environmentRectList)
                        
                        pongGameBM.stop()
                        pongGameWinner.stop()
                        menuMusik.play(15)
                        scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                    
                    if PongGame1p_GameOnState == False:
                        if event.key == pygame.K_RETURN:
                            PongGame1p_GameOnState = True
                            pongGameWinner.stop()
                            pongGameBM.play(15)
                            
                elif PongGame2p_state:
                    if event.key == pygame.K_ESCAPE:
                        PongGame2p_state = False
                        menu_state = True
                        jar.environmentReset(environmentRectList)
                        
                        pongGameBM.stop()
                        pongGameWinner.stop()
                        menuMusik.play(15)
                        scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                        
                    if PongGame2p_GameOnState == False:
                        if event.key == pygame.K_RETURN:
                            PongGame2p_GameOnState = True
                            pongGameWinner.stop()
                            pongGameBM.play(15)
                            
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
            text_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', 110)
            text2_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', 50)
            
            sign_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', 20)
            signt_text = sign_font.render("Made by Muhammed Emir Akgül", True, 'White')
            text_text1 = text_font.render("Welcome to this Game!", True, 'White')
            text_text2 = text2_font.render("Press anywhere with the mouse to start", True, 'White')
            text1_rect = text_text1.get_rect(center = (500, 270))
            text2_rect = text_text2.get_rect(center = (500, 400))
            sign_rect = signt_text.get_rect(center = (850, 30))
            screen.blit(text_text1, text1_rect)
            screen.blit(text_text2, text2_rect)
            screen.blit(signt_text, sign_rect)
            
            print("StartSCreen")
                 
        #menu-handling
        if menu_state:
            #KeyDown event handling
            
            #print("Menu")
            
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
        
        
        if PongGame1p_state:
            if PongGame1p_GameOnState:
                topBorder, bottomBorder = pp.drawPongScreen(screen, LightBlue, 'Black', gameMode='1p')
                paddle1.draw(screen)
                opponendPaddle.draw(screen)
                paddle1.update()
                opponendPaddle.update(ball)
                ball.draw(screen)
                ball.update()
                pp.collisionHandling(ball=ball, paddle1=paddle1, paddle2=opponendPaddle, topBorder=topBorder, bottomBorder=bottomBorder)
                if goal == True: time.sleep(0.4)
                scoreP1, scoreP2 = pp.goalManagament(ball, paddle1, paddle2, pongPointSound, scoreP1, scoreP2)
                
                pp.drawPongScore(screen, scoreP1, scoreP2)
                PongGame1p_GameOnState = pp.checkWin(PongGame1p_GameOnState, scoreP1, scoreP2)
            
            if PongGame1p_GameOnState == False:
                pongGameBM.stop()
                pongGameWinner.play(1)
                pp.pongGameOverScreen(screen, scoreP1, scoreP2, gameMode='1p')
                scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                
        if PongGame2p_state:
            if PongGame2p_GameOnState:
                topBorder, bottomBorder = pp.drawPongScreen(screen, LightBlue, 'Black', gameMode='2p')
                paddle1.draw(screen)
                paddle2.draw(screen)
                paddle1.update()
                paddle2.update()
                ball.draw(screen)
                ball.update()
                
                pp.collisionHandling(ball=ball, paddle1=paddle1, paddle2=paddle2, topBorder=topBorder, bottomBorder=bottomBorder)
                if goal == True: time.sleep(0.4)
                scoreP1, scoreP2 = pp.goalManagament(ball, paddle1, paddle2, pongPointSound, scoreP1, scoreP2)
                
                pp.drawPongScore(screen, scoreP1, scoreP2)
                PongGame2p_GameOnState = pp.checkWin(PongGame2p_GameOnState, scoreP1, scoreP2)
            
            if PongGame2p_GameOnState == False:
                pongGameBM.stop()
                pongGameWinner.play(1)
                pp.pongGameOverScreen(screen, scoreP1, scoreP2, gameMode='2p')
                scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                
        #essentials
        clock.tick(80)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
