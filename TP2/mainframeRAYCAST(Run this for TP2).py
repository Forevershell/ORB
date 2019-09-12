#mainframeTest
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
#basic colors
red=(255,0,0)
blue=(0,0,255)
yellow=(255,255,0)
green=(0,255,0)
purple=(255,0,255)
orange=(255,128,0)
white=(255,255,255)

#shades
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
game=pygame.display.set_mode((1000,400))
pygame.display.set_caption("Game")
timeCount=0

#screen parameters get
screenW=game.get_width()
screenH=game.get_height()

#init
interval=200
sInterval=screenW//interval
FOV=math.pi/4
depth=20

##Redraw
def redrawPhaseI(p1,enemies):
    game.fill((255,255,255))
    myfont = pygame.font.SysFont('Futura', 30)
    textsurface = myfont.render('uwu Press P to Play uwu', False, (0, 0, 0))
    offsetW=textsurface.get_width()/2
    offsetH=textsurface.get_height()/2
    game.blit(textsurface,(screenW/2-offsetW,screenH/2-offsetH))
    pygame.display.update()

def redrawPhaseIII(p1,enemies):
    game.fill(darkest)
    myfont = pygame.font.SysFont('Futura', 30)
    textsurface = myfont.render('Uwu ded >.<', False, lightest)
    offset1W=textsurface.get_width()/2
    offset1H=textsurface.get_height()/2
    game.blit(textsurface,(screenW/2-offset1W,screenH/3-offset1H))
    textsurface2 = myfont.render('Press r to restart or q to quit', True, lightest)
    offset2W=textsurface2.get_width()/2
    offset2H=textsurface2.get_height()/2
    game.blit(textsurface2,(screenW/2-offset2W,2*screenH/3-offset2H))
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

def getColorDist(distance,color):
    result=[]
    for base in color:
        base-=100
        result.append((base/(distance+1))+100)
    return tuple(result)
    
def drawEnemyRect(printDistance,distance):
    rWidth=((screenW*3/2)/(distance*1.5+1))
    rHeight=((screenW*5/2)/(distance*1.5+1))
    pygame.draw.rect(game,getColorDist(distance,red),\
    (screenW/2+printDistance-rWidth/2,screenH/2-rHeight/2,rWidth,rHeight))

def drawBulletCirc(printDistance,distance):
    distance=int(distance)
    radius=1.5*(screenH/4)/(distance+1)
    pygame.draw.circle(game,getColorDist(distance,orange),\
    (int(screenW/2+printDistance),int(screenH/2)),int(radius))
    
def drawEnemy(enemy,player):
    #establishing enemy's angle relative to player
    enemyA=math.atan2((player.y-enemy.y),(enemy.x-player.x))
    #establishing angles on a 2pi polar plane
    playerAngle=0
    enemyAngle=0
    if player.angle>0:
        playerAngle=player.angle%(2*math.pi)
    else:
        playerAngle=2*math.pi-(abs(player.angle)%(2*math.pi))
    if enemyA>0:
        enemyAngle=enemyA%(2*math.pi)
    else:
        enemyAngle=2*math.pi-(abs(enemyA)%(2*math.pi))
    aDistance=playerAngle-enemyAngle
    dDistance=math.sqrt((enemy.x-player.x)**2+(enemy.y-player.y)**2)
    if abs(aDistance)<(FOV/2):
        printDistance=((aDistance/FOV)*screenW)
        drawEnemyRect(printDistance,dDistance)
        
def drawBullet(bullet,player):
    bulletX=(bullet.x-size/2)/25
    bulletY=(bullet.y-size/2)/25
    #establishing bullet's angle relative to player
    bulletA=math.atan2((player.y-bulletY),(bulletX-player.x))
    #establishing angles on a 2pi polar plane
    playerAngle=0
    bulletAngle=0
    if player.angle>0:
        playerAngle=player.angle%(2*math.pi)
    else:
        playerAngle=2*math.pi-(abs(player.angle)%(2*math.pi))
    if bulletA>0:
        bulletAngle=bulletA%(2*math.pi)
    else:
        bulletAngle=2*math.pi-(abs(bulletA)%(2*math.pi))
    aDistance=playerAngle-bulletAngle
    dDistance=math.sqrt((bulletX-player.x)**2+(bulletY-player.y)**2)
    if abs(aDistance)<(FOV/2):
        printDistance=(aDistance/FOV)*screenW
        drawBulletCirc(printDistance,dDistance)
        
        

##mainloop
def main():
    run=True
    timeCount=0
    phase=1
    
    #player and enemy inits
    p1=gameplayer.Player(cols//2,rows//2,math.pi/2)
    enemies=[]
    
    while run:
        pygame.time.delay(25)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        keys=pygame.key.get_pressed()
        
        ##Menu Phase
        if phase==1:
            if keys[pygame.K_p]:
                phase=2
            redrawPhaseI(p1,enemies)
            
        ##Main Game Phase
        elif phase==2:
            #Movement
            oX,oY=p1.getPos()
            if keys[pygame.K_a] and oX>0:
                p1.mLeft()
                x,y=p1.getPos()
                if board.store[y][x]!=0:
                    p1.mRight()
            if keys[pygame.K_d] and oX<cols-1:
                p1.mRight()
                x,y=p1.getPos()
                if board.store[y][x]!=0:
                    p1.mLeft()
            if keys[pygame.K_w] and oY>0:
                p1.mUp()
                x,y=p1.getPos()
                if board.store[y][x]!=0:
                    p1.mDown()
            if keys[pygame.K_s] and oY<rows-1:
                p1.mDown()
                x,y=p1.getPos()
                if board.store[y][x]!=0:
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
                if bullet.checkOut(size,cols*size,rows*size,board.store):
                    p1.bullets.remove(bullet)
                for enemy in enemies:
                    if bullet.checkHit(enemy,size):
                        enemies.remove(enemy)
                        p1.bullets.remove(bullet)
                        break
                    
            #Timer
            if timeCount%100==0:
                enemies.append(gameenemy.Enemy(board.store))
            for enemy in enemies:
                if enemy.collide(p1):
                    phase=3
                if timeCount%40==0:
                    enemy.move(p1,board.store)
            
            ###Ray Casting###
            #Setting up Floor
            game.fill(white)
            pygame.draw.rect(game,dark,(0,screenH/2,screenW,screenH/2))
            #pygame.draw.rect(game,medium,(0,5*screenH/7,screenW,2*screenH/7))
            pygame.draw.rect(game,medium,(0,7*screenH/8,screenW,1*screenH/8))
            
            #initiating FOV
            rayAngle=(p1.angle+FOV/2)
            #Full Scaled
            #for x in range(0,screenW):
            #Interval Scaled
            for x in range(0,screenW,sInterval):
                #color changes based on surface detected
                colorInput=purple
                
                #Full Scaled
                rayAngle-=(FOV/screenW)
                #Interval Scaled
                rayAngle-=(FOV/interval)
                
                distance=0
                hitWall=False
                
                eyeX=math.cos(rayAngle)
                eyeY=-math.sin(rayAngle)
                while not hitWall and distance<depth:
                    distance+=0.1
                    testX=int(p1.x+eyeX*distance)
                    testY=int(p1.y+eyeY*distance)
                    
                    if testX<0 or testX>cols or testY<0 or testY>rows:
                        hitWall=True
                        distance=depth
                    else:
                        if board.store[testY][testX]==1:
                            hitWall=True
                            colorInput=blue
                        elif board.store[testY][testX]==2:
                            hitWall=True
                            colorInput=purple
                        elif board.store[testY][testX]==3:
                            hitWall=True
                ceiling=(screenH/2)-(screenH/distance)
                floor=screenH-ceiling
                pygame.draw.line(game,getColorDist(distance,colorInput)\
                    ,(x,ceiling),(x,floor),sInterval)
    
            #Lets GOOOOOOOOOOOOOOO        
            for enemy in enemies[::-1]:
                drawEnemy(enemy,p1)
            
            for bullet in p1.bullets[::-1]:
                drawBullet(bullet,p1)
                
            pygame.display.update()
            
            timeCount+=1
            p1.timerIncrease()
        
        ##End Game Phase
        elif phase==3:
            if keys[pygame.K_r]:
                phase=1
                return True
            elif keys[pygame.K_q]:
                return False
            redrawPhaseIII(p1,enemies)
        
playAgain=True
while playAgain:
    playAgain=main()

pygame.quit()