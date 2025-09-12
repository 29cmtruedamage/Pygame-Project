import pygame
from src.utils import resource_path
import random
import time
from enum import Enum
pygame.init()
class opponend_Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        paddleSize = (30, 120)
        darkBlue = (16, 78, 139)
        self.image = pygame.Surface((paddleSize))
        self.image.fill(darkBlue)
        paddleRect = self.image.get_rect(center = (910, 300)) 
        self.paddleRectDefPos = paddleRect.center
        self.rect = paddleRect
        self.speed = 7
        
    def opponend_movementControl(self, ball):
        upperBorder = 30
        downBorder = 574
        borderWhenToStop = 450
        ball_y = ball.sprite.rect.center[1]
        ball_x = ball.sprite.rect.center[0]
        self_y = self.rect.center[1]
        
        if ball_y >= self_y and self.rect.bottom <= downBorder and ball_x > borderWhenToStop: 
            self.rect.y += self.speed
        if ball_y <= self.rect.center[1] and self.rect.top >= upperBorder and ball_x > borderWhenToStop: 
            self.rect.y -= self.speed
    
    def update(self, ball):
        self.opponend_movementControl(ball)
            
    def opponend_resetPaddles(self):
            self.rect.center = self.paddleRectDefPos 
            
class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddleType: str):
        super().__init__()
        paddleSize = (30, 120)
        darkBlue = (16, 78, 139)
        self.image = pygame.Surface((paddleSize))
        self.image.fill(darkBlue)
        
        if paddleType == 'player1':
            paddleRect = self.image.get_rect(center = (90, 300))
            MovementUP = pygame.K_w
            MovementDOWN = pygame.K_s
            self.paddleRectDefPos = paddleRect.center
        if paddleType == 'player2':
            paddleRect = self.image.get_rect(center = (910, 300)) 
            MovementUP = pygame.K_UP
            MovementDOWN = pygame.K_DOWN
            self.paddleRectDefPos = paddleRect.center
            
        self.rect = paddleRect
        self.UP = MovementUP
        self.DOWN = MovementDOWN
        self.speed = 7
        
      
        
    def movementControl(self):
        keys = pygame.key.get_pressed()
        upperBorder = 30
        downBorder = 574
        if keys[self.UP] and self.rect.top >= upperBorder:
            self.rect.y -= self.speed
        if keys[self.DOWN] and self.rect.bottom <= downBorder:
            self.rect.y += self.speed
    
    def update(self):
        self.movementControl()
    
    def resetPaddles(self):
            self.rect.center = self.paddleRectDefPos 
            

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/ball.png')), 0, 0.14)
        self.rect = self.image.get_rect(center = (500, 300))
        
        self.x_speed = 4
        self.y_speed = 4
        
    def ballMovement(self):
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        
    def resetBall(self):
        self.rect.center = (500, 300)
        self.x_speed = random.choice([4, -4])
        self.y_speed = random.choice([4, -4])
        
        
    def update(self):
        self.ballMovement()
        
        
def collisionHandling(ball, paddle1, paddle2, topBorder, bottomBorder):
    x_speed_increase = 1.05 
    y_speed_increase = 1.025
    def handle_paddle_collision(ball, paddle):
        if not ball.rect.colliderect(paddle.rect):
            return
        dx_left = abs(ball.rect.right - paddle.rect.left)
        dx_right = abs(ball.rect.left - paddle.rect.right)
        dy_top = abs(ball.rect.bottom - paddle.rect.top)  
        dy_bottom = abs(ball.rect.top - paddle.rect.bottom) 

        
        min_dist = min(dx_left, dx_right, dy_top, dy_bottom)

        if min_dist == dx_left:
            ball.x_speed = -abs(ball.x_speed * x_speed_increase)
        elif min_dist == dx_right:
            ball.x_speed = abs(ball.x_speed * x_speed_increase)
        elif min_dist == dy_top:  
            ball.y_speed = -abs(ball.y_speed -3)
        elif min_dist == dy_bottom: 
            ball.y_speed = abs(ball.y_speed + 3)

    handle_paddle_collision(ball.sprite, paddle1.sprite)
    handle_paddle_collision(ball.sprite, paddle2.sprite)
    if ball.sprite.rect.colliderect(topBorder):
        ball.sprite.y_speed = abs(ball.sprite.y_speed * y_speed_increase)
        
        
    if ball.sprite.rect.colliderect(bottomBorder):
        ball.sprite.y_speed = -abs(ball.sprite.y_speed * y_speed_increase)
        
            
def drawPongScreen(screen, BackgroundColour, BorderColour, gameMode):
    
    screen.fill(BackgroundColour)
    whichPlay_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 30)
    whichPlay_p1 = whichPlay_font.render("Player 1", True, 'Black')
    if gameMode == '2p': whichPlay_p2 = whichPlay_font.render("Player 2", True, 'Black') 
    else: whichPlay_p2 = whichPlay_font.render("Computer", True, 'Black')
    whichPlay_p1_rect = whichPlay_p1.get_rect(center = (100, 40))
    whichPlay_p2_rect = whichPlay_p2.get_rect(center = (900, 40))
    screen.blit(whichPlay_p1, whichPlay_p1_rect)
    screen.blit(whichPlay_p2, whichPlay_p2_rect)
    top_border = pygame.draw.line(screen, BorderColour, (0, 10), (1000, 10), 20)
    bottom_border = pygame.draw.line(screen, BorderColour, (0, 590), (1000, 590), 20)
    return top_border, bottom_border

def drawPongScore(screen, scoreP1, scoreP2):
    score_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 70)
    score_text = score_font.render(f"{scoreP1} - {scoreP2}", True, 'Black')
    score_rect = score_text.get_rect(center = (500, 50))
    screen.blit(score_text, score_rect)
    
#def checkScore(ballSurface)
def drawBall(screen, x, y):
    tupel = (x, y)
    ball = pygame.image.load(resource_path('environment/obstacles/ball.png'))
    return ball

def resetGamePerPoint(ball, paddle1, paddle2):
    ball.sprite.resetBall()
    paddle1.sprite.resetPaddles()
    paddle2.sprite.resetPaddles()

def resetGameCompletely(ball, paddle1, paddle2, score1, score2):
    ball.sprite.resetBall()
    paddle1.sprite.resetPaddles()
    paddle2.sprite.resetPaddles()
    score1 = 0
    score2 = 0
    return score1, score2

def goalManagament(ball, paddle1, paddle2, sound, score1, score2):
    scoreMade = False
    if ball.sprite.rect.left <= 30:
        score2 += 1
        scoreMade = True
    if ball.sprite.rect.right >= 970:
        score1 += 1
        scoreMade = True
    if scoreMade:
        sound.play()
        time.sleep(0.2)
        ball.sprite.resetBall()
        paddle1.sprite.resetPaddles()
        paddle2.sprite.resetPaddles()
    return score1, score2


def checkWin(gameState, score1, score2):
    gameState = True
    if score1 == 5 or score2 == 5:
        gameState = False
    return gameState
        
        
def pongGameOverScreen(screen, score1, score2, gameMode):
    if score1 == 5:
        winner = "Player 1"
    if score2 == 5:
        if gameMode == '2p': winner = "Player 2"
        else: winner = "Computer"
    if score1 == 5 or score2 == 5:
        screen.fill('Blue')
        winner_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 90)
        winner_text = winner_font.render(f"{winner} has Won!", True, 'White')
        winner_rect = winner_text.get_rect(center = (500, 200))
        
        playAgain_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 60)
        playAgain_text = playAgain_font.render("Press Enter to Restart, Press ESC to exit", True, 'White')
        playAgain_rect = playAgain_text.get_rect(center = (500, 350))
        
        screen.blit(winner_text, winner_rect)
        screen.blit(playAgain_text, playAgain_rect)

vektorGröße = 60
vektor1center = (300, 350)
vektor2center = (700, 350)
LightGrey = (230, 230, 230)
DarkGrey =  (130, 130, 130)
# Defaultvektor_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 70)
# DefVek_text = Defaultvektor_font.render("  Platzhalter  ", False, 'Black')
vektor_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), vektorGröße)
vektor_GameText1 = vektor_font.render("    1-Player    ", True, 'Black')
vektor_GameText2 = vektor_font.render("    2-Players   ", True, 'Black')
Vektor_rect_Game1 = vektor_GameText1.get_rect(center = vektor1center)
Vektor_rect_Game2 = vektor_GameText2.get_rect(center = vektor2center)
VektorRectList = [Vektor_rect_Game1, Vektor_rect_Game2]

chooseGame_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), int(vektorGröße * 1.2))
chooseGame_text = chooseGame_font.render("choose a Game-mode", True, 'Black')
chooseGame_rect = chooseGame_text.get_rect(center = (500, 80))


returnMenu_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), vektorGröße)
returnMenu_text = returnMenu_font.render("Press ESC to return back to menu", True, 'Black')
returnMenu_rect = returnMenu_text.get_rect(center = (500, 180))
def chooseGamemodeScreen(screen, mouse_pos):
    def menu_defaultVektorScreening(screen, mouse_pos): #helper function
        for vektor in VektorRectList:
            if vektor.collidepoint(mouse_pos):
                pygame.draw.rect(screen, DarkGrey, vektor, 0, 50)
            else:
                pygame.draw.rect(screen, LightGrey, vektor, 0, 50)
    
    screen.fill('White')
    screen.blit(chooseGame_text, chooseGame_rect)
    screen.blit(returnMenu_text, returnMenu_rect)
    
    menu_defaultVektorScreening(screen, mouse_pos)
    screen.blit(vektor_GameText1, Vektor_rect_Game1)
    screen.blit(vektor_GameText2, Vektor_rect_Game2)
 
 
###   
class gameMode(Enum):
    one_player = 1
    two_players = 2
    
def chooseGamemodeCollisionHandling(screen, mouse_pos, ChooseGameScreenState: bool, gameMode1: bool, gameMode2: bool):
    if Vektor_rect_Game1.collidepoint(mouse_pos):
        gameMode1 = True
        ChooseGameScreenState = False
        PingPongTutorialScreen(screen, gameMode.one_player.value)
    elif Vektor_rect_Game2.collidepoint(mouse_pos):
        ChooseGameScreenState = False
        gameMode2 = True
        PingPongTutorialScreen(screen, gameMode.two_players.value)
    return ChooseGameScreenState, gameMode1, gameMode2
    
    
def PingPongTutorialScreen(screen, gameMode):
    if gameMode == 1:
        WASD_center = (500, 400)
    else: WASD_center = (250, 400)
    
    Pfeil_center = (750, 400)
    WASD = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/graphics/WASD-Tasten.jpeg')), 0, 0.7)
    Pfeiltasten = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/graphics/Pfeiltasten-Tasten.jpeg')), 0, 0.7)
    WASD_rect = WASD.get_rect(center = WASD_center)
    Pfeiltasten_rect = Pfeiltasten.get_rect(center = Pfeil_center)
    
    text_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 50)
    pressToContinue = text_font.render("Press anywhere with mouse to start", True, 'Black')
    player1_text = text_font.render("Player 1 controls with:", True, 'Black')
    player2_text = text_font.render("Player 2 controls with:", True, 'Black')
    
    pressToContinue_rect = pressToContinue.get_rect(center = (500, 40))
    player1_rect = player1_text.get_rect(center = (WASD_center[0], WASD_center[1] - 170))
    player2_rect = player1_text.get_rect(center = (Pfeil_center[0], Pfeil_center[1]- 170))
    
    
    screen.fill('White')
    screen.blit(pressToContinue, pressToContinue_rect)
    screen.blit(WASD, WASD_rect)
    screen.blit(player1_text, player1_rect)
    
    if gameMode == 2:
        screen.blit(Pfeiltasten, Pfeiltasten_rect)
        screen.blit(player2_text, player2_rect)
        pygame.draw.line(screen, 'Black', (500, 100), (500, 600))
