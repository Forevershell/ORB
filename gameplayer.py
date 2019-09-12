import pygame
import gamebullet
import math

size=25

def realround(n):
    if n>0:
        if n%1>=0.5:
            return int(n+1)
        else:
            return int(n)
    else:
        if abs(n%1)>=0.5:
            return -int(abs(n)+1)
    return int(n)

#player class
class Player():
    def __init__(self,x,y,angle,moveFactor,shootFactor):
        self.x=x
        self.y=y
        self.angle=angle
        self.bullets=[]
        self.angV=math.pi/20
        self.shotTimer=0
        self.shot=False
        self.shootFactor=shootFactor
        self.moveTimer=0
        self.moved=False
        self.moveFactor=moveFactor
        self.health=100
        self.streak=0
        self.score=0
        self.god=False
        self.godTimer=0
        self.level=1
    
    #movement
    def mUp(self):
        self.x=realround(self.x+math.cos(self.angle))
        self.y=realround(self.y-math.sin(self.angle))
    
    def mDown(self):
        self.x=realround(self.x-math.cos(self.angle))
        self.y=realround(self.y+math.sin(self.angle))
    
    def mRight(self):
        self.x=realround(self.x+math.cos(self.angle-math.pi/2))
        self.y=realround(self.y-math.sin(self.angle-math.pi/2))
    
    def mLeft(self):
        self.x=realround(self.x+math.cos(self.angle+math.pi/2))
        self.y=realround(self.y-math.sin(self.angle+math.pi/2))
    
    #turn
    def tRight(self):
        self.angle-=self.angV
    
    def tLeft(self):
        self.angle+=self.angV
        
    def getPos(self):
        return (self.x,self.y)
    
    def shoot(self):
        self.bullets.append(gamebullet.Bullet(int((self.x+0.5)*size),int((self.y+0.5)*size),self.angle))
        self.shot=True
    
    def timerIncrease(self):
        if self.moved:
            self.moveTimer+=1
        if self.moveTimer%self.moveFactor==0:
            self.move=False
            self.moveTimer=0
        if self.shot:
            self.shotTimer+=1
        if self.shotTimer%self.shootFactor==0:
            self.shot=False
            self.shotTimer=0
            
    def draw(self,surface,size,color,gameH):
        #Drawing the player
        pygame.draw.rect(surface,color,(self.x*size,self.y*size+gameH,size,size))
        #Drawing the cannon
        lineI=((self.x+0.5)*size,(self.y+0.5)*size+gameH)
        lineF=((self.x+0.5)*size+(math.cos(self.angle))*size,\
            (self.y+0.5)*size-(math.sin(self.angle))*size+gameH)
        pygame.draw.line(surface,color,lineI,lineF,5)
        