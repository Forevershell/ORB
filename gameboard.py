#board

def createBoard(rows,cols):
    #Board is set in place, can change later based upon preferences
    board=[]
    for row in range(rows):
        board.append([])
        for col in range(cols):
            board[row].append(0)
            if row==0 or row==rows-1:
                board[row][col]=1
            if col==0 or col==cols-1:
                board[row][col]=2
    
    for i in range(4):
        board[5][i]=1
        board[5][i+8]=1
        board[5][i+16]=1
        board[20][i]=1
        board[20][i+8]=1
        board[20][i+16]=1
    
    for i in range(12):
        board[10][i]=1
        board[15][cols-1-i]=1
    
    for i in range(3):
        board[i+11][3]=2
        board[14-i][cols-4]=2
    
    return board
    
class Board:
    def __init__(self):
        self.size=25
        self.rows=26
        self.cols=20
        self.printSize=0
        if self.rows>self.cols:
            self.printSize=250//self.rows
        else:
            self.printSize=250//self.cols
        self.store=createBoard(self.rows,self.cols)