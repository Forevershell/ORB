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
    
    return board
    
class Board:
    def __init__(self):
        self.size=25
        self.rows=20
        self.cols=20
        self.store=createBoard(self.rows,self.cols)