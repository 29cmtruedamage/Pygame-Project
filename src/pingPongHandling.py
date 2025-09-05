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
            

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/ball.png')), 0, 0.14)
        self.rect = self.image.get_rect(center = (500, 300))
        self.extraSpeed = 1
        self.x_speed = 3 
        self.y_speed = 3
        
    def ballMovement(self):
        self.rect.x += self.x_speed * self.extraSpeed
        self.rect.y += self.y_speed * self.extraSpeed
        
    def extraSpeedHandling(self):
        self.extraSpeed += 0.001
    def resetBall(self):
        self.rect.center = (500, 300)
        self.x_speed = random.choice([3, -3])
        self.y_speed = random.choice([3, -3])
        self.extraSpeed = 1
        
    def update(self):
        self.ballMovement()
        self.extraSpeedHandling()
    
def collisionHandling(ball, paddle1, paddle2, topBorder, bottomBorder):
    def handle_paddle_collision(ball, paddle):
        if not ball.rect.colliderect(paddle.rect):
            return
        dx_left = abs(ball.rect.right - paddle.rect.left)
        dx_right = abs(ball.rect.left - paddle.rect.right)
        dy_top = abs(ball.rect.bottom - paddle.rect.top)  
        dy_bottom = abs(ball.rect.top - paddle.rect.bottom) 

        
        min_dist = min(dx_left, dx_right, dy_top, dy_bottom)

        if min_dist == dx_left:
            ball.x_speed = -abs(ball.x_speed)
        elif min_dist == dx_right:
            ball.x_speed = abs(ball.x_speed)
        elif min_dist == dy_top:  
            ball.y_speed = -abs(ball.y_speed -3)
        elif min_dist == dy_bottom: 
            ball.y_speed = abs(ball.y_speed + 3)

    handle_paddle_collision(ball.sprite, paddle1.sprite)
    handle_paddle_collision(ball.sprite, paddle2.sprite)
    if ball.sprite.rect.colliderect(topBorder):
        ball.sprite.y_speed = abs(ball.sprite.y_speed)
    if ball.sprite.rect.colliderect(bottomBorder):
        ball.sprite.y_speed = -abs(ball.sprite.y_speed)

            
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
        
        
def pongGameOverScreen(screen, score1, score2):
    if score1 == 5:
        winner = "Player 1"
    if score2 == 5:
        winner = "Player 2"
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

