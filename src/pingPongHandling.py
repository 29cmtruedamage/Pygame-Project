import pygame


pygame.init()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddleType):
        super().__init__
        paddleSize = (30, 120)
        darkBlue = (16, 78, 139)
        playerPaddle_image= pygame.Surface((paddleSize))
        playerPaddle_image.fill(darkBlue)
        
        if paddleType == 'player1':
            paddleRect = playerPaddle_image.get_rect(center = (130, 300))
            MovementUP = pygame.K_w
            MovementDOWN = pygame.K_s
        if paddleType == 'player2':
            paddleRect = playerPaddle_image.get_rect(center = (870, 300)) 
            MovementUP = pygame.K_UP
            MovementDOWN = pygame.K_DOWN
            
        self.rect = paddleRect
        self.UP = MovementUP
        self.DOWN = MovementDOWN
        self.speed = 10
        
    def movementControl(self):
        keys = pygame.key.get_pressed()
        if keys[self.UP] and self.rect.top <= 20:
            self.rect.center -= self.speed
        if keys[self.DOWN] and self.rect.bottom >= 540:
            self.rect.center += self.speed
    
