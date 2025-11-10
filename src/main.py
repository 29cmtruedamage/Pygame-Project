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

class GameStates():
    def __init__(self):
        self.startScreenState = True
        self.menu_state = False 
        self.pause_state = False
        
        self.jumpAndRun_state = False
        self.jumpAndRun_GameOnState = False
        self.jumpAndRun_GameOverState = False
        #self.speedUp = False
        
        self.PongGameChooseGameMode_state = False
        
        self.PongGame1p_state = False
        self.PongGame1p_GameOnState = False
        self.PongGame1p_GameOverState = False
        self.PongGame1p_Tutorial_Screen = False
        
        self.PongGame2p_state = False
        self.PongGame2p_GameOnState = False
        self.PongGame2p_GameOverState = False
        self.PongGame2p_Tutorial_Screen = False
        
        
        
        self.GameStatesList = ["jumpAndRun_state", "jumpAndRun_GameOnState", "jumpAndRun_GameOverState",
                               "PongGame1p_state", "PongGame1p_GameOnState", "PongGame1p_GameOverState",
                               "PongGame2p_state", "PongGame2p_GameOnState", "PongGame2p_GameOverState"]
#time variables
#startTime = 0
def main():
    #state-deklarations
    state = GameStates()
    pressed = False
    
    #new Self-defined USEREVENTS
    timeToSpawnObstacle = 2000
    obstacleSpawnTimer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacleSpawnTimer, timeToSpawnObstacle)
    
    timeToSpawnObstacle_speedUp = 770
    obstacleSpawnTimer_speedUp = pygame.USEREVENT + 2
    pygame.time.set_timer(obstacleSpawnTimer_speedUp, timeToSpawnObstacle_speedUp)
    
    firstLevel = 100
    secondLevel = 150
    speedUp = False
        
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
    lastMeasuredTime = 0
    #score
    highScore = 0
    score = 0
    #DECLARING OBJECTS
    #declaring player and obstacles -Jump and Run
    player = pygame.sprite.GroupSingle()
    player.add(jar.Player())
    
    obstacle_group = pygame.sprite.Group()
    #declaring paddles -PingPong
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
    def resetJar():
        global backgroundSpeed, undergroundSpeed, speedUp, score
        jar.environmentReset(environmentRectList)
        backgroundSpeed = 1
        undergroundSpeed = 4
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
                if state.startScreenState == True:
                    menuMusik.play(10)     
                    state.startScreenState = False    
                    state.menu_state = True 
                    print("StartScreen") 
                
                #menuScreen
                elif state.menu_state:
                    if mh.defaultVektor_rect_Game1.collidepoint(mouse_pos): #Jump And Run
                        state.menu_state = False
                        state.jumpAndRun_state = True
                        state.jumpAndRun_GameOnState = True
                        state.jumpAndRun_GameOverState = False
                        menuMusik.stop()
                        gameStartSound.play()
                        time.sleep(0.2)
                        jarMusik.play(10)
                        startTime = pygame.time.get_ticks()
                        obstacle_group.empty()
                    #For next Games
                    if mh.defaultVektor_rect_Game2.collidepoint(mouse_pos): #PingPong 
                        state.menu_state = False
                        state.PongGameChooseGameMode_state = True
                        pp.chooseGamemodeScreen(screen, mouse_pos)
                    #Template
                    # if mh.defaultVektor_rect_Game3.collidepoint(mouse_pos): 
                        # do sth
                    # if mh.defaultVektor_rect_Game4.collidepoint(mouse_pos):
                        # do Sth
                
                #pause state handling    
                if state.pause_state:    
                    state.pause_state, state.GameStatesList = mh.pauseResumeHandling(state, mouse_pos, state.pause_state, state.GameStatesList)
                    if state.jumpAndRun_GameOnState: 
                        lastMeasuredTime = (pygame.time.get_ticks() - lastMeasuredTime)
                        startTime += lastMeasuredTime
                        
                    state.pause_state, state.GameStatesList, state.menu_state = mh.pauseBacktomenuHandling(state, mouse_pos, state.pause_state, state.GameStatesList)
                    if state.menu_state == True:
                        pongGameBM.stop()
                        jarMusik.stop()
                        menuMusik.play(15)
                        jar.environmentReset(environmentRectList)
                        backgroundSpeed = 1
                        undergroundSpeed = 4
                        player.sprite.playerReset()
                        speedUp = False
                        score = 0
                        obstacle_group.empty()
                        scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                #PongGame
                elif state.PongGameChooseGameMode_state:
                    state.PongGameChooseGameMode_state, state.PongGame1p_Tutorial_Screen, state.PongGame2p_Tutorial_Screen = pp.chooseGamemodeCollisionHandling(
                                                                                                                screen=screen,
                                                                                                                mouse_pos=mouse_pos,
                                                                                                                ChooseGameScreenState=state.PongGameChooseGameMode_state,
                                                                                                                gameMode1=state.PongGame1p_Tutorial_Screen,
                                                                                                                gameMode2=state.PongGame2p_Tutorial_Screen) 
                    
                elif state.PongGame2p_Tutorial_Screen:
                    state.PongGame2p_Tutorial_Screen = False
                    state.PongGame2p_state = True
                    state.PongGame2p_GameOnState = True
                    
                    menuMusik.stop()
                    gameStartSound.play()
                    time.sleep(0.2)
                    pongGameBM.play(15)      
                   
                        
                elif state.PongGame1p_Tutorial_Screen: 
                    state.PongGame1p_Tutorial_Screen = False
                    state.PongGame1p_state = True
                    state.PongGame1p_GameOnState = True
                    
                    menuMusik.stop()
                    gameStartSound.play()
                    time.sleep(0.2)
                    pongGameBM.play(15)  
                    
            #KeyDown Hanlding
            if event.type == pygame.KEYDOWN:
                
                #menuState
                if state.menu_state and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                
                #Jump And Run
                elif state.jumpAndRun_state:
                    if event.key == pygame.K_ESCAPE:
                        if state.jumpAndRun_GameOnState:
                            state.jumpAndRun_GameOnState = False
                            lastMeasuredTime = pygame.time.get_ticks()
                            state.pause_state = True
                            mh.pauseScreen(mouse_pos, mh.pause_DefVektorList, mh.pause_vektor_map)
                        if state.jumpAndRun_GameOverState:
                            state.jumpAndRun_state = False
                            state.jumpAndRun_GameOverState = False
                            state.menu_state = True
                            menuMusik.play(15)
                            
                    if state.jumpAndRun_GameOnState == False and state.jumpAndRun_GameOverState == True:
                        if event.key == pygame.K_RETURN: #Return = EnterTaste
                            state.jumpAndRun_GameOnState = True     
                            state.jumpAndRun_GameOverState = False
                            startTime = pygame.time.get_ticks()
                            jarMusik.play(15)
                
                #PongGame
                elif state.PongGameChooseGameMode_state:
                    if event.key == pygame.K_ESCAPE:
                        state.PongGameChooseGameMode_state = False
                        state.menu_state = True
                #PongGame 1
                elif state.PongGame1p_state:
                    if state.PongGame1p_GameOnState and event.key == pygame.K_ESCAPE:
                        state.PongGame1p_GameOnState = False
                        state.pause_state = True
                    
                    if state.PongGame1p_GameOverState == True:
                        if event.key == pygame.K_RETURN:
                            state.PongGame1p_GameOnState = True
                            state.PongGame1p_GameOverState = False
                            pongGameWinner.stop()
                            pongGameBM.play(15)
                            scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                        if event.key == pygame.K_ESCAPE:
                            state.PongGame1p_GameOnState = False
                            state.PongGame1p_GameOverState = False
                            state.PongGame1p_state = False
                            state.menu_state = True
                            pongGameBM.stop()
                            pongGameWinner.stop()
                            menuMusik.play(15)
                            jar.environmentReset(environmentRectList)   
                            
                #PongGame 2
                elif state.PongGame2p_state:
                    if event.key == pygame.K_ESCAPE and state.PongGame2p_GameOnState:
                        state.PongGame2p_GameOnState = False
                        state.pause_state = True
                        
                    if state.PongGame2p_GameOverState == True:
                        if event.key == pygame.K_RETURN: #Enter Taste
                            state.PongGame2p_GameOnState = True
                            state.PongGame2p_GameOverState = False
                            pongGameWinner.stop()
                            pongGameBM.play(15)
                            scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                        if event.key == pygame.K_ESCAPE:
                            state.PongGame2p_GameOnState = False
                            state.PongGame2p_GameOverState = False
                            state.PongGame2p_state = False
                            state.menu_state = True
                            pongGameBM.stop()
                            pongGameWinner.stop()
                            menuMusik.play(15)
                            jar.environmentReset(environmentRectList) 
                            
            #specific event Types:
            if state.jumpAndRun_GameOnState and not speedUp:
                if event.type == obstacleSpawnTimer and score < firstLevel:
                    obstacle_group.add(jar.Obstacle(random.choice(['bird','tree1','tree2','bird','tree1','tree2','tree3','mushroom'])))
                if score > secondLevel: 
                    speedUp = True
                    player.sprite.playerSpeedUp()
                    backgroundSpeed = 3
                    undergroundSpeed = 12
            if state.jumpAndRun_GameOnState and speedUp:
                if event.type == obstacleSpawnTimer_speedUp:
                    obstacle_group.add(jar.Obstacle(random.choice(['bird','tree1','tree2','bird','tree1','tree2','tree3','mushroom'])))
                    jar.obstacle_SpeedUp(obstacle_group)
                    
                    
        #State Handling
        #startScreen Handling
        if state.startScreenState:
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
        
        #pauseScreenHandling
        if state.pause_state:
            mh.pauseScreen(mouse_pos, mh.pause_DefVektorList, mh.pause_vektor_map)

        
        #menu-handling
        if state.menu_state:
            #KeyDown event handling
            
            #print("Menu")
            
            mh.menu_mainMenuPicScreening()
            mh.menu_defaultVektorScreening(mouse_pos, mh.menu_defaultVektorRectList)
            mh.menu_vektorScreening(mh.menu_vektorMap)
            
        if state.jumpAndRun_state:
            #KeyDown event handling
            if state.jumpAndRun_GameOnState:
                
                jar.drawEnvironment(screen, background_image, underground_image, 
                                    environmentRectList)
                jar.manageEnvironment(environmentRectList, backgroundSpeed, undergroundSpeed)
                score = jar.drawScore(screen, startTime, highScore=highScore)
                #print("GAME ONNNN")
                highScore = jar.checkHighscore(highScore, score)
                player.draw(screen)
                player.update()
                obstacle_group.draw(screen)
                obstacle_group.update()
                lastScore = score
                state.jumpAndRun_GameOnState, state.jumpAndRun_GameOverState= jar.collisionCheck(player, obstacle_group, gameOverSound)
                
            if state.jumpAndRun_GameOverState == True:
                jar.gameOverScreen(screen, lastScore)
                backgroundSpeed = 1
                undergroundSpeed = 4
                jar.environmentReset(environmentRectList)
                player.sprite.playerReset()
                speedUp = False
                score = 0
                obstacle_group.empty()
                print("Game Over")
                jarMusik.stop()
        
        #Pong Game Handling
        if state.PongGameChooseGameMode_state:
            pp.chooseGamemodeScreen(screen, mouse_pos)
            
        if state.PongGame1p_state:
            if state.PongGame1p_GameOnState:
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
                state.PongGame1p_GameOverState = pp.checkWin(state.PongGame1p_GameOnState, scoreP1, scoreP2)
                if state.PongGame1p_GameOverState: state.PongGame1p_GameOnState = False
                
            if state.PongGame1p_GameOverState == True:
                pongGameBM.stop()
                pongGameWinner.play(15)
                pp.pongGameOverScreen(screen, scoreP1, scoreP2, gameMode='1p')
                scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                
        if state.PongGame2p_state:
            if state.PongGame2p_GameOnState:
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
                state.PongGame2p_GameOverState = pp.checkWin(state.PongGame2p_GameOnState, scoreP1, scoreP2)
                if state.PongGame2p_GameOverState: state.PongGame2p_GameOnState = False
            
            if state.PongGame2p_GameOverState == True:
                pongGameBM.stop()
                pongGameWinner.play(1)
                pp.pongGameOverScreen(screen, scoreP1, scoreP2, gameMode='2p')
                scoreP1, scoreP2 = pp.resetGameCompletely(ball, paddle1, paddle2, scoreP1, scoreP2)
                
        #essentials
        clock.tick(80)
        pygame.display.update()
        
if __name__ == "__main__":
    main()
