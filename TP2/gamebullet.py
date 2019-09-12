import pygame
import math
import gameenemy

#bullet class
class Bullet():
    def __init__(self,x,y,angle):
        self.x=x
        self.y=y
        self.angle=angle
        self.vel=24
        self.rad=5
        
    def moveBullet(self):
        self.x+=int((math.cos(self.angle))*self.vel)
        self.y-=int((math.sin(self.angle))*self.vel)
        
    def checkOut(self,size,width,height,board):
        if self.x+self.rad>=width-size:
            return True
        elif self.x-self.rad<=size:
            return True
        elif self.y+self.rad>=height-size:
            return True
        elif self.y-self.rad<=size:
            return True
        elif board[self.y//size][self.x//size]==1:
            return True
        return False
        
    def checkHit(self,enemy,size):
        if isinstance(enemy,gameenemy.Enemy):
            top=enemy.y*size
            bot=(enemy.y+1)*size
            left=enemy.x*size
            right=(enemy.x+1)*size
            if left-self.rad<=self.x<=right+self.rad and top<=self.y<=bot:
                return True
            elif top-self.rad<=self.y<=bot+self.rad and left<=self.x<=right:
                return True
        return False
        
    def __repr__(self):
        return str((self.x,self.y))

    def draw(self,surface,color):
        pygame.draw.circle(surface,color,(self.x,self.y),self.rad)