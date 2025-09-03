import pygame
from src.utils import resource_path
import random
import time
pygame.init()

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
        if keys[self.UP] and self.rect.top >= 30:
            self.rect.y -= self.speed
        if keys[self.DOWN] and self.rect.bottom <= 574:
            self.rect.y += self.speed
    
    def update(self):
        self.movementControl()
    
    def resetPaddles(self):
            self.rect.center = self.paddleRectDefPos 
            
def drawPongScreen(screen, BackgroundColour, BorderColour):
    screen.fill(BackgroundColour)
    whichPlay_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 30)
    whichPlay_p1 = whichPlay_font.render("Player 1", True, 'Black')
    whichPlay_p2 = whichPlay_font.render("Player 2", True, 'Black')
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
    ball = pygame.draw.circle(screen, 'Black', tupel, 40)
    return ball
     
def ballManagement(ball, paddle1_rect, paddle2_rect, topBorderRect, bottomBorderRect, x_movement, y_movement, sound):
    if ball.colliderect(paddle1_rect) or ball.colliderect(paddle2_rect):
        x_movement = -x_movement
        sound.play()
    if ball.colliderect(topBorderRect) or ball.colliderect(bottomBorderRect): 
        y_movement = -y_movement
        sound.play()
    return x_movement, y_movement

def resetGame(ball_x_pos, ball_y_pos, paddle1, paddle2, score1, score2):
    ball_x_pos = 500
    ball_y_pos = 300
    paddle1.sprite.resetPaddles()
    paddle2.sprite.resetPaddles()
    score1 = 0
    score2 = 0
    return ball_x_pos, ball_y_pos, score1, score2


def goalManagement(ball, scoreP1, scoreP2, ball_x_pos, ball_y_pos, paddle1, paddle2, ball_x_speed, ball_y_speed, goal: bool, sound):
    if ball.left <= 50:
        scoreP1 += 1
        sound.play()
    if ball.right >= 950:
        scoreP2 += 1
        sound.play()
    if ball.left <= 50 or ball.right >= 950:
        ball_x_pos = 500
        ball_y_pos = 300
        paddle1.sprite.resetPaddles()
        paddle2.sprite.resetPaddles()
        ball_x_speed = random.choice([5, -5])
        ball_y_speed = random.choice([5, -5])
        goal = True
    else: goal = False
    return scoreP1, scoreP2, ball_x_pos, ball_y_pos, ball_x_speed, ball_y_speed, goal


def checkWin(gameState, score1, score2):
    gameState = True
    if score1 == 5 or score2 == 5:
        gameState = False
    return gameState
        
        
def pongGameOverScreen(screen, score1, score2):
    if score1 == 5:
        winner = "Player 2"
    if score2 == 5:
        winner = "Player 1"
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
        
def extraSpeed(goal, extraSpeed):
    if goal == False:
        extraSpeed += 0.00001
    if goal == True:
        extraSpeed = 0
    return extraSpeed

