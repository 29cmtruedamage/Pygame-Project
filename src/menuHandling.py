import pygame
from main import screen

pygame.init() 
#Constants
LightGrey = (230, 230, 230)
DarkGrey =  (130, 130, 130)
Pink = (233, 128, 128)
Blue = (10, 100, 200)

# coordinate_vektor1 = (280, 300)
# coordinate_vektor2 = (280, 450)
# coordinate_vektor3 = (720, 300)
# coordinate_vektor4 = (720, 450)
coordinate_vektor1 = (500, 280)
coordinate_vektor2 = (500, 380)
coordinate_vektor3 = (500, 480)
coordinate_vektor4 = (720, 450)
coordinate_mainMenu = (500, 100)
coordinate_chooseAgame = (500, 200)
coordinate_backgroundCenter = (500, 300)
defaultVektorGröße = 75
vektorGröße = 40
mainMenuPicGröße = 175
chooseAgameGröße = 30

#Background initialisieren
background_image = pygame.transform.scale(pygame.image.load('environment/graphics/BG.png'), (1000, 600)).convert()
background_rect = background_image.get_rect(center = coordinate_backgroundCenter)

#Game-UI Vektors initialisieren
defaultVektor_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', defaultVektorGröße)
defaultVektor_text = defaultVektor_font.render("Platzhalter", True, 'Black')



defaultVektor_rect_Game1 = defaultVektor_text.get_rect(center = coordinate_vektor1)
defaultVektor_rect_Game2 = defaultVektor_text.get_rect(center = coordinate_vektor2)
defaultVektor_rect_Game3 = defaultVektor_text.get_rect(center = coordinate_vektor3)
defaultVektor_rect_Game4 = defaultVektor_text.get_rect(center = coordinate_vektor4)
# -> screen.blit(Vektor1, defaultVektor_rect_Game1)

vektor_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', vektorGröße)
vektor_GameText1 = vektor_font.render("Jump and Run", True, 'Black')
vektor_GameText2 = vektor_font.render(" PingPong ", True, 'Black')
vektor_GameText3 = vektor_font.render("Special-Game", True, 'Black')
vektor_GameText4 = vektor_font.render("Tik-Tak-Toe ", True, 'Black')


vektor_rect1 = vektor_GameText1.get_rect(center = coordinate_vektor1)
vektor_rect2 = vektor_GameText2.get_rect(center = coordinate_vektor2)
vektor_rect3 = vektor_GameText3.get_rect(center = coordinate_vektor3)
vektor_rect4 = vektor_GameText4.get_rect(center = coordinate_vektor4)

menu_vektorMap = {
    vektor_GameText1: vektor_rect1,
    vektor_GameText2: vektor_rect2,
    vektor_GameText3: vektor_rect3,
    #vektor_GameText4: vektor_rect4
}

menu_defaultVektorRectList = [defaultVektor_rect_Game1, 
                              defaultVektor_rect_Game2, 
                              defaultVektor_rect_Game3, 
                              #defaultVektor_rect_Game4
                              ]

mainMenuPic_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', mainMenuPicGröße)
mainMenuPic_text = mainMenuPic_font.render("Menu", False, Pink)
mainMenuPic_rect = mainMenuPic_text.get_rect(center = coordinate_mainMenu)

chooseAgame_font = pygame.font.Font('environment/textStyles/textStyle1.ttf', chooseAgameGröße)
chooseAgame_text = chooseAgame_font.render("choose a game...", True, Pink)
chooseAgame_rect = chooseAgame_text.get_rect(center = coordinate_chooseAgame)

#funktionen für screen
# def checkColl(mouse_pos):
#     global screen
#     for vektor in menu_defaultVektorRectList:
#         if vektor.collidepoint(mouse_pos):
#             pygame.draw.rect(screen, DarkGrey, vektor, 0, 50)
#         else:
#             pygame.draw.rect(screen, LightGrey, vektor, 0, 50)
            
def menu_defaultVektorScreening(mouse_pos):
    global screen
    for vektor in menu_defaultVektorRectList:
        if vektor.collidepoint(mouse_pos):
            pygame.draw.rect(screen, DarkGrey, vektor, 0, 50)
        else:
            pygame.draw.rect(screen, LightGrey, vektor, 0, 50)
        
def menu_vektorScreening():
    for key in menu_vektorMap:
        screen.blit(key, menu_vektorMap[key])

def menu_mainMenuPicScreening():
    screen.blit(background_image, background_rect)
    screen.blit(mainMenuPic_text, mainMenuPic_rect)
    screen.blit(chooseAgame_text, chooseAgame_rect)
    
