import pygame
import random
import math
import gameplayer

#enemy class
#multiple types of enemy
class Enemy():
    def __init__(self,board,player):
        space=[]
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col]==0 and (col,row)!=(player.x,player.y):
                    space.append((col,row))
        self.x,self.y=random.choice(space)
            
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
                
    def distance(self,player):
        return math.sqrt((self.x-player.x)**2+(self.y-player.y)**2)
        
    def __repr__(self):
        return str((self.x,self.y))
            
    def draw(self,surface,size,color,gameH):
        pygame.draw.rect(surface,color,(self.x*size,self.y*size+gameH,size,size))