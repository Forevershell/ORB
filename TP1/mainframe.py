#Project Map Based Pygame
import pygame
import math
#custom imports
import gameplayer
import gameboard
import gameenemy

pygame.init()
pygame.font.init()

#temp variables to be implemented in classes

#colors
lightest=(89, 188, 202)
light=(51, 169, 185)
medium=(18, 155, 174)
dark=(2, 126, 143)
darkest=(2, 98, 111)
#enemy colors
colorE=(178,34,34)

#board inits
board=gameboard.Board()
rows=board.rows
cols=board.cols
size=board.size

#game init
game=pygame.display.set_mode((cols*size,rows*size))
pygame.display.set_caption("Game")
timeCount=0
phase=1

#player and enemy inits
p1=gameplayer.Player(cols//2,rows//2,math.pi/2)
enemies=[]
#screen parameters get
screenW=game.get_width()
screenH=game.get_height()


##Redraw
def redrawPhaseI():
    game.fill((255,255,255))
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Press P to Play', False, (0, 0, 0))
    game.blit(textsurface,(screenW/2,screenH/2))
    pygame.display.update()

def redrawPhaseII():
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(game,getColor(row,col),\
            (col*size,row*size,size,size))
    p1.draw(game,size,darkest)
    for bullet in p1.bullets:
        bullet.draw(game,medium)
    for enemy in enemies:
        enemy.draw(game,size,colorE)
    pygame.display.update()

def redrawPhaseIII():
    game.fill(darkest)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('You suck', False, lightest)
    game.blit(textsurface,(screenW/2,screenH/2))
    pygame.display.update()

##Helper Functions
def getColor(row,col):
    tile=board.store[row][col]
    #tile is empty
    if tile==0:
        return lightest
    #tile is wall
    else:
        return dark
        

##mainloop
run=True
timeCount=0
while run:
    pygame.time.delay(75)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    
    keys=pygame.key.get_pressed()
    
    ##Menu Phase
    if phase==1:
        if keys[pygame.K_p]:
            phase=2
        redrawPhaseI()
        
    ##Main Game Phase
    elif phase==2:
        #Movement
        oX,oY=p1.getPos()
        if keys[pygame.K_a] and oX>0:
            p1.mLeft()
            x,y=p1.getPos()
            if board.store[y][x]==1:
                p1.mRight()
        if keys[pygame.K_d] and oX<cols-1:
            p1.mRight()
            x,y=p1.getPos()
            if board.store[y][x]==1:
                p1.mLeft()
        if keys[pygame.K_w] and oY>0:
            p1.mUp()
            x,y=p1.getPos()
            if board.store[y][x]==1:
                p1.mDown()
        if keys[pygame.K_s] and oY<rows-1:
            p1.mDown()
            x,y=p1.getPos()
            if board.store[y][x]==1:
                p1.mUp()
        x,y=p1.getPos()
        board.store[oY][oX]=0
        
        #Turning
        if keys[pygame.K_LEFT]:
            p1.tLeft()
        if keys[pygame.K_RIGHT]:
            p1.tRight()
            
        #Shooting
        if keys[pygame.K_SPACE] and p1.shotTimer%10==0:
            p1.shoot()
        for bullet in p1.bullets:
            bullet.moveBullet()
            if bullet.checkOut(size,screenW,screenH,board.store):
                p1.bullets.remove(bullet)
            for enemy in enemies:
                if bullet.checkHit(enemy,size):
                    enemies.remove(enemy)
                    p1.bullets.remove(bullet)
                    break
                
        #Timer
        if timeCount%10==0:
            enemies.append(gameenemy.Enemy(board.store))
        for enemy in enemies:
            if enemy.collide(p1):
                phase=3
            if timeCount%3==0:
                enemy.move(p1,board.store)
        
        timeCount+=1
        p1.timerIncrease()
        redrawPhaseII()
    
    ##End Game Phase
    elif phase==3:
        if keys[pygame.K_p]:
            phase=1
            #reset()
        redrawPhaseIII()

pygame.quit()