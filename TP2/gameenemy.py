import pygame
import random
import math
import gameplayer
import backtracker

#enemy class
#multiple types of enemy
class Enemy():
    def __init__(self,board):
        space=[]
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col]==0:
                    space.append((col,row))
        self.x,self.y=random.choice(space)
        #self.x,self.y=(2,2)
            
    def collide(self,player):
        if isinstance(player,gameplayer.Player):
            (pX,pY)=(player.x,player.y)
            return (pX,pY)==(self.x,self.y)
        return False
    
    def move(self,player,board):
        if isinstance(player,gameplayer.Player):
            (pX,pY)=(player.x,player.y)
            if pX<self.x and board[self.y][self.x-1]==0:
                self.x-=1
            if pX>self.x and board[self.y][self.x+1]==0:
                self.x+=1
            if pY<self.y and board[self.y-1][self.x]==0:
                self.y-=1
            if pY>self.y and board[self.y+1][self.x]==0:
                self.y+=1
            
    def draw(self,surface,size,color):
        pygame.draw.rect(surface,color,(self.x*size,self.y*size,size,size))