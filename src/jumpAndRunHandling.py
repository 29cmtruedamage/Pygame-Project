import pygame
from random import randint
from src.utils import resource_path
#from menuHandling import vektor_font
#constants
#import menuHandling as mh

pygame.init()
colourGreen = (0, 139, 69)
colourBeige = (255,222,173)

generalSpeed = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_x = 150
        self.player_y = 512
        coordinate_Player = (self.player_x, self.player_y)
        playerScale = 0.2
        playerRun1 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/RunAnimation/PlayerRun1.png')), 0, playerScale).convert_alpha()
        playerRun2  = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/RunAnimation/PlayerRun2.png')), 0, playerScale).convert_alpha()
        playerRun3  = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/RunAnimation/PlayerRun3.png')), 0, playerScale).convert_alpha()
        playerRun4 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/RunAnimation/PlayerRun4.png')), 0, playerScale).convert_alpha()
        playerRun5 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/RunAnimation/PlayerRun5.png')), 0, playerScale).convert_alpha()
        player_rec = playerRun1.get_rect(midbottom = coordinate_Player)
        playerStanding = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/PlayerStanding.png')), 0, playerScale).convert_alpha()
        playerJump = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/characters/PlayerJump.png')), 0, playerScale).convert_alpha()

        self.animationList = [playerRun1, playerRun2, playerRun3, 
                              playerRun4, playerRun5]
        self.playerJump = playerJump
        self.playerStanding = playerStanding
        self.index = 0
        self.image = self.animationList[self.index]
        self.rect = player_rec
        self.hitbox = self.rect.inflate(-120, -50)
        
        self.jumpSound = pygame.mixer.Sound(resource_path('environment/audios/jumpSound.mp3'))
        self.jumpSound.set_volume(0.5)
        self.gravity = 0
        self.jumpHeight = -12
        self.playerSpeed = 0.1
        self.gravitySpeed = 0.33
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = self.jumpHeight
            self.jumpSound.play()
            
    def playerJumpHandling(self):
        self.gravity += self.gravitySpeed
        self.rect.y += self.gravity
        if self.rect.bottom >= self.player_y:
            self.rect.bottom = self.player_y
        
    def playerAnimation(self):
        if self.rect.bottom != self.player_y:
            self.image = self.playerJump
        else:
            self.index += self.playerSpeed
            self.index = self.index % len(self.animationList)
            helperIndex = self.index
            self.image = self.animationList[int(helperIndex)]
            
    def playerReset(self):
        self.rect.bottom = self.player_y
        self.gravity = 0
        self.playerSpeed = 0.1
        self.gravitySpeed = 0.33
        
    def playerSpeedUp(self):
        self.playerSpeed = 0.3
        self.gravitySpeed = 0.5
    def update(self):
        self.playerInput()
        self.playerJumpHandling()
        self.playerAnimation()
        self.hitbox.center = self.rect.center
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        y_pos_trees = 500
        treeScale = 0.35
        birdScale = 0.1
        mushroomScale = 0.5
        if type == 'bird':
            
            bird1_def = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Bird/Vogel1.png')).convert_alpha(), 0, birdScale)
            bird1 = pygame.transform.flip(bird1_def, True, False)
            bird2_def = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Bird/Vogel2.png')).convert_alpha(), 0, birdScale)
            bird2 = pygame.transform.flip(bird2_def, True, False)
            bird3_def = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Bird/Vogel3.png')).convert_alpha(), 0, birdScale)
            bird3 = pygame.transform.flip(bird3_def, True, False)
            
            self.frames = [bird1, bird2, bird3]
            y_pos = 350
        if type == 'tree1':
            tree1 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Tree_1.png')).convert_alpha(), 0, treeScale)
            self.frames = [tree1]
            y_pos = y_pos_trees
        if type == 'tree2':
            tree2 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Tree_2.png')).convert_alpha(), 0, treeScale)
            self.frames = [tree2]
            y_pos = y_pos_trees
        if type == 'tree3':
            tree3 = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Tree_3.png')).convert_alpha(), 0, treeScale)
            self.frames = [tree3]
            y_pos = y_pos_trees
        if type == 'mushroom':
            mushroom = pygame.transform.rotozoom(pygame.image.load(resource_path('environment/obstacles/Mushroom_2.png')).convert_alpha(), 0, mushroomScale)
            self.frames = [mushroom]
            y_pos = y_pos_trees
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(1100, 1300), y_pos))
        self.obstacleSpeed = 4 
        
    def animation_state(self):
        self.animation_index += 0.1 
        self.animation_index = self.animation_index % len(self.frames)
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
        if self.rect.x <= -100: 
             self.kill()
    
    def obstacleSpeedUp(self):
        self.obstacleSpeed = 12
        
    def obstacleReset(self):
        self.obstacleSpeed = 4 #Ursprungswert 
        
    def update(self):
        self.animation_state()
        self.rect.x -= self.obstacleSpeed
        self.destroy()


def obstacle_SpeedUp(obstacle_group):
    for obstacle in obstacle_group:
        obstacle.obstacleSpeedUp()
        
def obstacle_Reset(obstacle_group):
    for obstacle in obstacle_group:
        obstacle.obstacleReset()

score_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 55)
highScore_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 40)

def drawScore(screen, startTime, highScore):
    currentScore = int((pygame.time.get_ticks() - startTime) / 100)
    score_text = score_font.render(f" Your Score: {currentScore} ", True, 'Black')
    highScore_text = highScore_font.render(f" HIGHSCORE: {highScore} ", False, 'Black')
    
    score_rect_Score = score_text.get_rect(center = (500, 150))
    score_rect_HighScore = highScore_text.get_rect(center = (500, 50))
    
    screen.blit(score_text, score_rect_Score)
    screen.blit(highScore_text, score_rect_HighScore)
    
    return currentScore

def checkHighscore(highScore, currentScore):
    if highScore >= currentScore:
        return highScore
    else: return currentScore
    
def environmentReset(rectList):
    rectList[0].center = (500, 300)
    rectList[1].center = (1500, 300)
    rectList[2].midtop = (500, 500)
    rectList[3].midtop = (1500, 500)

def drawEnvironment(screen, b_image, u_image, rectList):
    screen.blit(b_image, rectList[0])
    screen.blit(b_image, rectList[1])
    screen.blit(u_image, rectList[2])
    screen.blit(u_image, rectList[3])
    
#[b_rect1, b_rect2, u_rect1, u_rect2]
def manageEnvironment(rectList, backgroundSpeed, undergroundSpeed):
    rectList[0].x -= backgroundSpeed
    rectList[1].x -= backgroundSpeed
    
    rectList[2].x -= undergroundSpeed
    rectList[3].x -= undergroundSpeed
    
    for rect in rectList:
        if rect.right <= 12:
            rect.left = 1000
            
def collisionCheck(player, obstacle_group, gameOverSound):
    for obstacle_rect in obstacle_group:
        if player.sprite.hitbox.colliderect(obstacle_rect.rect):
            gameOverSound.play()
            return False, True
    return True, False

gameOverScreen_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 200)
gameOverPressEnter_font = pygame.font.Font(resource_path('environment/textStyles/textStyle1.ttf'), 50)
gameOverCenter = (500, 200)
gameOverPressEnterCenter = (500, 400)
returnBackMenuCenter = (500, 460)

def gameOverScreen(screen):
    gameOverScreen_text = gameOverScreen_font.render("GAME OVER", False, colourBeige)
    gameOverScreen_rect = gameOverScreen_text.get_rect(center = gameOverCenter)
    
    gameOverPressEnter_text = gameOverPressEnter_font.render("PRESS ENTER TO RESTART", True, colourBeige)
    gameOverPressEnter_rect = gameOverPressEnter_text.get_rect(center = gameOverPressEnterCenter)
    
    returnBackMenu_text = gameOverPressEnter_font.render("PRESS ESC TO RETURN TO MENU", True, colourBeige)
    returnBackMenu_rect = returnBackMenu_text.get_rect(center = returnBackMenuCenter)
    screen.fill(colourGreen)
    
    screen.blit(gameOverScreen_text, gameOverScreen_rect)
    screen.blit(gameOverPressEnter_text, gameOverPressEnter_rect)
    screen.blit(returnBackMenu_text, returnBackMenu_rect)
    


    