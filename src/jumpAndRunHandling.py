import pygame
from random import randint
#from menuHandling import vektor_font
#constants
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        coordinate_Player = (50, 500)
        playerScale = 0.5
        playerRun1 = pygame.transform.rotozoom(pygame.image.load('environment/characters/RunAnimation/PlayerRun1.png'), 0, playerScale).convert_alpha()
        playerRun2 = pygame.transform.rotozoom(pygame.image.load('environment/characters/RunAnimation/PlayerRun2.png'), 0, playerScale).convert_alpha()
        playerRun3 = pygame.transform.rotozoom(pygame.image.load('environment/characters/RunAnimation/PlayerRun3.png'), 0, playerScale).convert_alpha()
        playerRun4 = pygame.transform.rotozoom(pygame.image.load('environment/characters/RunAnimation/PlayerRun4.png'), 0, playerScale).convert_alpha()
        playerRun5 = pygame.transform.rotozoom(pygame.image.load('environment/characters/RunAnimation/PlayerRun5.png'), 0, playerScale).convert_alpha()
        player_rec = playerRun1.get_rect(center = coordinate_Player)
        playerStanding = pygame.transform.rotozoom(pygame.image.load('environment/characters/PlayerStanding.png'), 0, playerScale).convert_alpha()
        playerJump = pygame.transform.rotozoom(pygame.image.load('environment/characters/PlayerJump.png'), 0, playerScale).convert_alpha()

        self.animationList = [playerRun1, playerRun2, playerRun3, 
                              playerRun4, playerRun5]
        self.playerJump = playerJump
        self.playerStanding = playerStanding
        self.index = 0
        self.image = self.animationList[self.index]
        self.rect = player_rec
        
        self.jumpSound = pygame.mixer.Sound('environment/audios/jumpSound.mp3')
        self.jumpSound.set_volume(0.5)
        self.gravity = 0
        
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -20
            self.jumpSound.play()
            
    def playerJumpHandling(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500
        
    def playerAnimation(self):
        if self.rect.bottom != 500:
            self.image = self.playerJump
        else:
            self.index += 0.1
            self.index = self.index % len(self.animationList)
            self.image = self.animationList[int(self.index)]
            
    def update(self):
        self.playerInput()
        self.playerJumpHandling()
        self.playerAnimation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        y_pos_trees = 500
        
        if type == 'bird':
            birdScale = 0.5
            bird1 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Bird/Vogel1.png').convert_alpha(), 0, birdScale)
            bird2 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Bird/Vogel2.png').convert_alpha(), 0, birdScale)
            bird3 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Bird/Vogel3.png').convert_alpha(), 0, birdScale)
            
            self.frames = [bird1, bird2, bird3]
            y_pos = 300
        if type == 'tree1':
            tree1 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Tree_1.png').convert_alpha(), 0, treeScale)
            self.frames = [tree1]
            y_pos = y_pos_trees
        if type == 'tree2':
            tree2 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Tree_2.png').convert_alpha(), 0, treeScale)
            self.frames = [tree2]
            y_pos = y_pos_trees
        if type == 'tree3':
            tree3 = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Tree_3.png').convert_alpha(), 0, treeScale)
            self.frames = [tree3]
            y_pos = y_pos_trees
        if type == 'mushroom':
            mushroom = pygame.transform.rotozoom(pygame.image.load('environment/obstacles/Mushroom_2.png').convert_alpha(), 0, birdScale)
            self.frames = [mushroom]
            y_pos = y_pos_trees
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(mitbottom = (randint(1100, 1300), y_pos))
        
        
    def animation_state(self):
        self.animation_index += 0.1 
        self.animation_index = self.animation_index % len(self.frames)
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
            if self.rect.x <= -100: 
                self.kill()
                
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

score_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', 55)
highScore_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', 40)

def drawScore(screen, startTime, highScore):
    currentScore = int((pygame.time.get_ticks() - startTime) / 100)
    score_text = score_font.render(f"Your Score: {currentScore}", True, 'Black')
    highScore_text = highScore_font.render(f"HIGHSCORE: {highScore}", False, 'Black')
    
    score_rect_Score = score_text.get_rect(center = (500, 150))
    score_rect_HighScore = highScore_text.get_rect(center = (500, 50))
    
    screen.blit(score_text, score_rect_Score)
    screen.blit(highScore_text, score_rect_HighScore)
    
    return currentScore

def checkHighscore(highScore, currentScore):
    if highScore >= currentScore:
        return highScore
    else: return currentScore
    
def drawEnvironment(screen, background,background_rect, underground, underground_rect):
    screen.blit(background, background_rect)
    screen.blit(underground, underground_rect)