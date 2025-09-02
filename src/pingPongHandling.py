import pygame


pygame.init()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, paddleType: str):
        super().__init__()
        paddleSize = (30, 120)
        darkBlue = (16, 78, 139)
        self.image = pygame.Surface((paddleSize))
        self.image.fill(darkBlue)
        
        if paddleType == 'player1':
            paddleRect = self.image.get_rect(center = (130, 300))
            MovementUP = pygame.K_w
            MovementDOWN = pygame.K_s
            self.paddleRectDefPos = paddleRect.center
        if paddleType == 'player2':
            paddleRect = self.image.get_rect(center = (870, 300)) 
            MovementUP = pygame.K_UP
            MovementDOWN = pygame.K_DOWN
            self.paddleRectDefPos = paddleRect.center
            
        self.rect = paddleRect
        self.UP = MovementUP
        self.DOWN = MovementDOWN
        self.speed = 10
        
      
        
    def movementControl(self):
        keys = pygame.key.get_pressed()
        if keys[self.UP] and self.rect.top >= 20:
            self.rect.y -= self.speed
        if keys[self.DOWN] and self.rect.bottom <= 580:
            self.rect.y += self.speed
    
    def update(self):
        self.movementControl()
    
    def resetPaddles(self):
            self.rect.center = self.paddleRectDefPos 