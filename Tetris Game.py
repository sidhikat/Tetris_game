# Sidhika Tripathee
#andrewId: sidhikat
##Tetris Game
from tkinter import * 
import random
import copy
########
# Initializing data
#########
def init(data):
    #initializes dimensions
    data.rows=15
    data.cols= 10
    data.margin=10
    data.gameOver=False
    data.score=0
    # #cretes a 2D list
    data.emptyColor="white"
    data.board=[([data.emptyColor]*data.cols) for row in range(data.rows)]
    #creating seven different types of pieces
    iPiece = [
    [ True,  True,  True,  True]
    ]
  
    jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]
  
    lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]
  
    oPiece = [
    [ True, True],
    [ True, True]
    ]
  
    sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]
  
    tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ] 

    zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]
  
#initializes colors and pieces
    data.fallingPiece=[]
    data.fallingColor="white"
    data.fallingPieceRow=0
    data.fallingPieceCol=0
    tetrisPieces= [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    tetrisPieceColors= ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
#setting tetris pieces and tetris piece colors
    data.tetrisPieces= tetrisPieces
    data.tetrisPieceColors= tetrisPieceColors
    newFallingPiece(data)

#####
#creating board
######
#gets the coordinates for outer rectangle and inner rectangle of grid 
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)  
    
def mousePressed(event, data):
    pass

def keyPressed(event, data):
  # for now, for testing purposes, just choose a new falling piece
  # whenever ANY key is pressed!
  if(event.keysym == "Down"): moveFallingPiece(data,1,0)
  elif (event.keysym == "Right"): moveFallingPiece(data,0,1)
  elif(event.keysym == "Left"): moveFallingPiece(data,0,-1)
  elif(event.keysym =="Up"): rotateFallingPiece(data)
  elif(event.keysym=="r"): init(data)
  
def timerFired(data):
    
    if(not moveFallingPiece(data,1,0)):
        placeFallingPiece(data)
        removeFullRows(data)
        newFallingPiece(data)
        if(not fallingPieceIsLegal(data)):
            data.gameOver= True 

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    
def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas,data,row,col,data.board[row][col])
            

def drawCell(canvas, data, row, col, color="white"):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = .5 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill=color)
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)
    
####
#Falling tetris piece functions
#####

#postitions a random piece in the middle of the top row
def newFallingPiece(data):
    index= random.randint(0,len(data.tetrisPieces)-1)
    data.fallingPiece=data.tetrisPieces[index]
    data.fallingPieceColor=data.tetrisPieceColors[index]
    data.fallingPieceRow=0
    data.fallingPieceCol=data.cols//2-(len(data.fallingPiece[0])//2) #puts falling piece in middle of board
    
def drawFallingPiece(canvas, data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if(data.fallingPiece[row][col]):
                drawCell(canvas, data,data.fallingPieceRow +row, data.fallingPieceCol+col,data.fallingPieceColor )
            
def moveFallingPiece(data,drow,dcol):
    data.fallingPieceRow+=drow
    data.fallingPieceCol+=dcol
    if(not fallingPieceIsLegal(data)):
        data.fallingPieceRow-=drow
        data.fallingPieceCol-=dcol
        return False
    return True
    
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if(data.fallingPiece[row][col]):
                if( (data.fallingPieceRow<0) or ((row+data.fallingPieceRow)>=data.rows) or (col+data.fallingPieceCol)>=data.cols or (col+data.fallingPieceCol)<0): #checks to make sure piece doesn't move out of the board
                    return False
                if(not (data.board[row+data.fallingPieceRow][col+data.fallingPieceCol] == data.emptyColor)):#sees if there is another piece in that space
                    return False
    return True
             
def rotateFallingPiece(data):
    #set dimesions of falling piece to new variables
    originalShape=data.fallingPiece
    originalRow= data.fallingPieceRow
    originalCol= data.fallingPieceCol
    newX= data.fallingPieceRow
    newY= data.fallingPieceCol
    newRows= len(data.fallingPiece[0])
    newCols= len(data.fallingPiece)
    #calculating center
    oldCenterRow = data.fallingPieceRow + (len(data.fallingPiece)//2)
    oldCenterCol =  data.fallingPieceCol + (len(data.fallingPiece[0])//2)
    #creating new location based on the centers
    newX = -(newRows//2) + oldCenterRow 
    data.fallingPieceRow= newX
    newY= -(newCols//2)+ oldCenterCol
    data.fallingPieceCol =newY
    
    #adding new dimensions to new 2D list 
    newList = []
    for row in range(newRows):  
        newRow = []
        for col in range(newCols):
            oldRow = col #sets row as col
            oldCol= (len(data.fallingPiece[0]))-1 - row #sets col as num of cols-1 -row location of piece
            value = data.fallingPiece[oldRow][oldCol]
            newRow.append(value)
        newList.append(newRow)
        
    data.fallingPiece=newList
    
    #checks to see if rotatingPiece is legal
    if(not fallingPieceIsLegal(data)):
        data.fallingPiece=originalShape
        data.fallingPieceRow= originalRow
        data.fallingPieceCol= originalCol
        
#places the piece on the board when it reaches the bottom
def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if(data.fallingPiece[row][col]):
                data.board[data.fallingPieceRow+row][data.fallingPieceCol+col]= data.fallingPieceColor
                
#removes a row when it is completed
def removeFullRows(data):
    newRow=[([data.emptyColor]*data.cols) for row in range(data.rows)]
    newRowIndex=-1
    isFullRow=True
    fullRows=0 
    for row in range(-1,-(len(data.board))-1,-1):
        oldRow=copy.deepcopy(data.board[row]) #oldrow is the values on the board
        for col in range(len(data.board[0])):
            if(oldRow[col]== data.emptyColor):
                newRow[newRowIndex]= copy.deepcopy(oldRow) #adds oldrow to newrow if oldrow is not full
                isFullRow=False
        if(isFullRow):
            fullRows+=1 #number of fullRows that have been removed
        if(not isFullRow): 
            newRowIndex-=1
    data.score+= fullRows**2
    data.board=copy.deepcopy(newRow) #makes the board newRow board
    
#draws the Score on the board
def drawScore(data, canvas):
    
    canvas.create_text(data.width//5,data.height//15, fill="black", font="Times 15 bold",text="Score: "+str(data.score))
    
def redrawAll(canvas, data):
    if(data.gameOver): #checks to see if gameOver is True
        canvas.create_text(data.width//2,data.height//2,fill="darkblue",font="Times 20 italic bold",text=" Game OVER!\n Press 'r' to restart")
    
    else:
        drawGame(canvas, data)
        drawScore(data,canvas)
        drawFallingPiece(canvas,data)

####################################
# use the run function as-is
####################################

def run(width=500, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()  
    
