#mainframeTest
#Project Map Based Pygame
import pygame
import math
#custom imports
import gameplayer
import gameboard
import gameenemy
import gameimages

pygame.init()
pygame.font.init()
clock=pygame.time.Clock()

#game init
game=pygame.display.set_mode((1200,700))
pygame.display.set_caption("")
timeCount=0

#screen parameters
screenW=game.get_width()
screenH=game.get_height()

#game parameters
gameW=1200
gameH=450

#board inits
board=gameboard.Board()
rows=board.rows
cols=board.cols
size=board.size
printSize=board.printSize

#rayCast init
interval=200
sInterval=screenW//interval
FOV=math.pi/3
depth=18

##Color Functions
#wallcolors hsva
wallcolor1=(350,100,0,100)
wallcolor2=(160,50,0,100)

#basic colors rgb
white=(255,255,255)

#UI colors
uiBackground=(23, 43, 42)
textColor=(255, 170, 170)

#Map colors
mapBackground=(212, 106, 106)
enemyColor=(178,34,34)

#Ray Caster
groundColorDark=(97, 56, 56)
groundColorLight=(159, 91, 91)

def getColor(row,col):
    tile=board.store[row][col]
    #tile is empty
    if tile==0:
        return mapBackground
    #tile is wall
    else:
        return uiBackground

def getColorDist(distance,color):
    resColor=pygame.Color("red")
    result=list(color)
    result[2]=int(100-75*(distance/rows))
    resColor.hsva=(tuple(result))
    return resColor

##Helpers
def sortEnemies(enemies,player):
    for x in range(len(enemies)):
        for y in range(x,len(enemies)):
            if enemies[x].distance(player)<enemies[y].distance(player):
                enemies.insert(y,enemies.pop(x))

##Redraw
def redrawPhaseI(p1,enemies):
    game.fill(white)
    myfont = pygame.font.SysFont('Futura', 30)
    textsurface = myfont.render('uwu Press P to Play uwu', False, uiBackground)
    offsetW=textsurface.get_width()/2
    offsetH=textsurface.get_height()/2
    game.blit(textsurface,(screenW/2-offsetW,screenH/2-offsetH))
    pygame.display.update()
    
def redrawPhaseII(p1,enemies):
    rayCast(p1,enemies)
    pygame.draw.rect(game,uiBackground,(0,450,1200,250))
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(game,getColor(row,col),\
            (col*printSize,row*printSize+gameH,printSize,printSize))
    p1.draw(game,printSize,uiBackground,gameH)
    for enemy in enemies:
        enemy.draw(game,printSize,enemyColor,gameH)
    myfont = pygame.font.SysFont('Futura', 30)
    textsurface = myfont.render('Health '+str(p1.health), False, textColor)
    offsetW=textsurface.get_width()/2
    offsetH=textsurface.get_height()/2
    textsurface2 = myfont.render('Streak '+str(p1.streak), False, textColor)
    offsetW2=textsurface2.get_width()/2
    offsetH2=textsurface2.get_height()/2
    game.blit(textsurface,(1000-offsetW,2*screenH/3-offsetH))
    game.blit(textsurface2,(1000-offsetW2,3*screenH/4-offsetH2))
    if p1.god:
        textsurface3 = myfont.render("God Mode Activated", False, textColor)
        offsetW3=textsurface3.get_width()/2
        offsetH3=textsurface3.get_height()/2
        game.blit(textsurface3,(gameW/2-offsetW3,2*screenH/3-offsetH3))
    textsurface4 = myfont.render('Level '+str(p1.level), False, textColor)
    offsetW4=textsurface4.get_width()/2
    offsetH4=textsurface4.get_height()/2
    game.blit(textsurface4,(1000-offsetW4,4*screenH/5-offsetH4))
    textsurface5 = myfont.render('Score '+str(p1.score), False, textColor)
    offsetW5=textsurface5.get_width()/2
    offsetH5=textsurface5.get_height()/2
    game.blit(textsurface5,(1000-offsetW5,5*screenH/6-offsetH5))
    gameimages.drawHandAnim(game,p1)
    pygame.display.update()

def redrawPhaseIII(p1,enemies):
    game.fill(uiBackground)
    myfont = pygame.font.SysFont('Futura', 30)
    textsurface = myfont.render('Uwu ded >.<', False, textColor)
    offset1W=textsurface.get_width()/2
    offset1H=textsurface.get_height()/2
    game.blit(textsurface,(screenW/2-offset1W,screenH/3-offset1H))
    textsurface2 = myfont.render('Press r to restart or q to quit', True, textColor)
    offset2W=textsurface2.get_width()/2
    offset2H=textsurface2.get_height()/2
    game.blit(textsurface2,(screenW/2-offset2W,2*screenH/3-offset2H))
    pygame.display.update()

##raycaster draw package
def drawEnemyRect(printDistance,distance):
    rWidth=int((gameW*2.5)/(distance*2+1))
    rHeight=int((gameW*3)/(distance*2+1))
    gameimages.makeEnemy(game,rWidth,rHeight,\
        (gameW/2+printDistance-rWidth/2,gameH/2-rHeight/2))

def drawBulletCirc(printDistance,distance):
    distance=int(distance)
    radius=(gameH/2)/(distance+1)
    gameimages.makeBullet(game,\
        (int(gameW/2+printDistance),int(gameH/2),int(radius)))
    
def drawEnemy(enemy,player):
    #establishing enemy's angle relative to player
    (realEnX,realEnY)=(enemy.x,enemy.y)
    enemyA=math.atan2((player.y-realEnY),(realEnX-player.x))
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
    dDistance=math.sqrt((realEnX-player.x)**2+(realEnY-player.y)**2)
    #wall collision
    behindWall=False
    #ray casting distance
    distance=0
    while distance<=dDistance:
        x=int(player.x+math.cos(enemyAngle)*distance+0.5)
        y=int(player.y-math.sin(enemyAngle)*distance+0.5)
        if board.store[y][x]!=0:
            behindWall=True
            break
        distance+=0.1
    #draw rectangles
    if not behindWall:
        if abs(aDistance)<(FOV/2):
            printDistance=((aDistance/FOV)*gameW)
            drawEnemyRect(printDistance,dDistance)
        if enemyAngle==2*math.pi:
            enemyAngle=0
            if abs(playerAngle)<(FOV/2):
                printDistance=(playerAngle/FOV)*gameW
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
    if abs(aDistance)<=(FOV/2):
        printDistance=(aDistance/FOV)*gameW
        drawBulletCirc(printDistance,dDistance)
    if playerAngle==2*math.pi:
        playerAngle=0
        aDistance=playerAngle-bulletAngle
        if abs(aDistance)<=(FOV/2):
            printDistance=(aDistance/FOV)*gameW
            drawBulletCirc(printDistance,dDistance)
        
##raycaster
def rayCast(p1,enemies):
    #Setting up Floor
    game.fill(white)
    pygame.draw.rect(game,groundColorDark,(0,0,gameW,gameH/2))
    #pygame.draw.rect(game,groundColorLight,(0,5*gameH/7,gameW,2*gameH/7))
    pygame.draw.rect(game,groundColorLight,(0,gameH/2,gameW,gameH/2))
    
    #initiating FOV
    rayAngle=(p1.angle+FOV/2)
    #Full Scaled
    #for x in range(0,gameW):
    #Interval Scaled
    for x in range(0,gameW,sInterval):
        #color changes based on surface detected
        colorInput=wallcolor1
        #Full Scaled
        #rayAngle-=(FOV/gameW)
        #Interval Scaled
        rayAngle-=(FOV/interval)
        
        distance=0
        hitWall=False
        
        eyeX=math.cos(rayAngle)
        eyeY=-math.sin(rayAngle)
        while not hitWall and distance<depth:
            offset=distance/size
            distance+=0.1
            testX=int(p1.x+eyeX*distance+0.5)
            testY=int(p1.y+eyeY*distance+0.5)
            
            if testX<0 or testX>cols or testY<0 or testY>rows:
                hitWall=True
                distance=depth
            else:
                if board.store[testY][testX]==1:
                    hitWall=True
                    colorInput=wallcolor2
                elif board.store[testY][testX]==2:
                    hitWall=True
                    colorInput=wallcolor1
                elif board.store[testY][testX]==3:
                    hitWall=True
        ceiling=(gameH/2)-(gameH/distance)
        floor=gameH-ceiling
        pygame.draw.line(game,getColorDist(distance,colorInput)\
            ,(x,ceiling),(x,floor),sInterval)

    #Lets GOOOOOOOOOOOOOOO        
    for enemy in enemies:
        drawEnemy(enemy,p1)
    
    for bullet in p1.bullets:
        drawBullet(bullet,p1)
        

##mainloop
def main():
    run=True
    timeCount=0
    phase=1
    
    #delay control and balance
    #Balance Control
    moveFactor=2
    shootFactor=10
    vampiricDelay=30
    
    #player and enemy inits
    p1=gameplayer.Player(cols//2,rows//2,math.pi/2,moveFactor,shootFactor)
    
    #Delay Control
    enemySpeedDelay=85
    enemySpawnDelay=108
    levelDelay=50
        
    enemies=[]
    
    while run:
        clock.tick(10)
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
            if p1.moveTimer%moveFactor==0:
                if keys[pygame.K_a] and oX>0:
                    p1.mLeft()
                    x,y=p1.getPos()
                    if board.store[y][x]!=0:
                        p1.mRight()
                    else:
                        p1.moved=True
                if keys[pygame.K_d] and oX<cols-1:
                    p1.mRight()
                    x,y=p1.getPos()
                    if board.store[y][x]!=0:
                        p1.mLeft()
                    else:
                        p1.moved=True
                if keys[pygame.K_w] and oY>0:
                    p1.mUp()
                    x,y=p1.getPos()
                    if board.store[y][x]!=0:
                        p1.mDown()
                    else:
                        p1.moved=True
                if keys[pygame.K_s] and oY<rows-1:
                    p1.mDown()
                    x,y=p1.getPos()
                    if board.store[y][x]!=0:
                        p1.mUp()
                    else:
                        p1.moved=True
            
            #Turning
            if keys[pygame.K_LEFT]:
                p1.tLeft()
            if keys[pygame.K_RIGHT]:
                p1.tRight()
                
            #Shooting
            if keys[pygame.K_SPACE] and p1.shotTimer%shootFactor==0:
                p1.shoot()
            for bullet in p1.bullets:
                bullet.moveBullet()
                if bullet.checkOut(size,cols*size,rows*size,board.store):
                    p1.bullets.remove(bullet)
                for enemy in enemies:
                    if bullet.checkHit(enemy,size):
                        enemies.remove(enemy)
                        p1.bullets.remove(bullet)
                        p1.score+=p1.level*(p1.streak+1)
                        p1.streak+=1
                        p1.health+=10
                        if p1.god==True:
                            p1.godTimer=0
                        break
                    
            ##God Mode
            if not p1.god and p1.streak>0 and p1.streak%3==0:
                p1.god=True
            
            if p1.god:
                moveFactor=1
                shootFactor=5
                p1.godTimer+=1
                p1.angV=math.pi/15
            else:
                moveFactor=2
                shootFactor=10
                p1.angV=math.pi/20
        
            if p1.godTimer>=20*p1.streak:
                p1.godTimer=0
                p1.god=False
                p1.streak+=1
                
            ##Timer
            if timeCount%enemySpawnDelay==0 and len(enemies)<=10:
                enemies.append(gameenemy.Enemy(board.store,p1))
                #Sorts enemies based on distances
                sortEnemies(enemies,p1)
                p1.score+=p1.level
            
            for enemy in enemies:
                if enemy.collide(p1):
                    p1.health-=20
                    p1.streak=0
                    enemies.remove(enemy)
                if timeCount%enemySpeedDelay==0:
                    enemy.move(p1,board.store)
            
            if timeCount%levelDelay==0:
                if enemySpeedDelay>5:
                    enemySpeedDelay-=10
                if enemySpawnDelay>8:
                    enemySpawnDelay-=10
                if vampiricDelay>5:
                    vampiricDelay-=5
                p1.level+=1
            
            if timeCount%vampiricDelay==0:
                p1.health-=1
            
            if p1.health<=0:
                phase=3
            
            redrawPhaseII(p1,enemies)
            
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