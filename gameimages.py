#Images
import pygame
import os

def drawHandAnim(surface,p1):
    images=[pygame.image.load(os.path.join("images","Hand1.png")),\
        pygame.image.load(os.path.join("images","Hand2.png")),\
        pygame.image.load(os.path.join("images","Hand3.png")),\
        pygame.image.load(os.path.join("images","Hand4.png")),\
        pygame.image.load(os.path.join("images","Hand5.png"))]
    scaled=[]
    for image in images:
        scaled.append(pygame.transform.scale(image,(1200,450)))
    if p1.shotTimer<5:
        surface.blit(scaled[p1.shotTimer],(0,0))
    else:
        surface.blit(scaled[0],(0,0))
    
def makeBullet(surface,circle):
    x,y=circle[0],circle[1]
    radius=circle[2]
    image=pygame.image.load(os.path.join("images","bullet.png"))
    scaled=pygame.transform.scale(image,(radius*2,radius*2))
    surface.blit(scaled,(x-radius,y-radius))
    
def makeEnemy(surface,width,height,position):
    image=pygame.image.load(os.path.join("images","enemy.png"))
    scaled=pygame.transform.scale(image,(width,height))
    surface.blit(scaled,position)