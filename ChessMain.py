""" 
This is our main driver file. It will be responsible for handling user input and displaying the current game State object
"""

import pygame as p
import ChessEngine 

WIDTH = HEIGHT = 512
DIMENSION = 8 #dimension of a chessboard is 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  #for animations later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main to reduces lags.
"""
def loadImages():
    #pygame.image.load() — loads an image file from disk and turns it into a pygame Surface object
    #IMAGES["wp"] = p.image.load("images/wp.png") #writing this 12times might be too much. We will do a loop.
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "wp", "bp", "bR", "bN", "bB", "bQ", "bK"] 
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES["wp"]' 
    #p.transform.scale() fixes that by resizing the loaded image to a specific size — in this case (SQ_SIZE, SQ_SIZE)

"""
The main driver. This will handle user input and update the graphics.
"""

def main():
    p.init() #p.init() initializes pygame itself — it sets up all the internal modules pygame
    screen = p.display.set_mode((WIDTH, HEIGHT)) #p.display.set_mode() tells pygame "open a window of this size" 
    clock = p.time.Clock() #This creates a Clock object, which pygame uses to control timing
    screen.fill(p.Color("white")) #This fills the entire window with a solid color — here, white
    gs = ChessEngine.Gamestate() #gs = ChessEngine.Gamestate() creates an actual instance of your GameState class
    loadImages() #Do this once, before the while loop
    running = True
    sqSelected = () #no square is select initially (tuple: (row, col))
    playerClick = [] #keep track of player clicks (two tuples : [(6, 4), (4,4)])
    while running:
        for e in p.event.get(): #p.event.get collects everything that happens — every key press, mouse click, window close button click — into a list of "events."
            if e.type == p.QUIT: #is the current event specifically a request to quit?
                running = False 
            elif e.rtpe == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) = loc of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked a square twice
                    sqSelected = () #deselect
                    playerClick = [] #clear player clicks
                else:
                    

        drawGameState(screen, gs)
        clock.tick(MAX_FPS) #Uses the Clock object to pause the loop just enough so it doesn't run faster than MAX_FPS
        p.display.flip() #p.display.flip() is what actually pushes everything you've drawn onto the visible window

"""
Responsible for all the graphics within a current game
"""
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces on top of those squares

"""
Draw the squares on the board. We need to draw the screen before the pieces.
The top left square is always light. It is true from both perspectives.

if (r + c) % 2 == 0:
    color = colors[0]
else:
    color = colors[1]
Chess boards alternate colors based on whether the sum of the row and column is even or odd: 
square (0,0) → sum is 0 → even → color index 0 
Square (0,1) → sum is 1 → odd → color index 1


for example, when r=2 and c=3, you get p.Rect(192, 128, 64, 64) — a 64x64 square starting 192 pixels from the left and 128 pixels from the top. 
Multiply that by all 64 combinations of r and c in the nested loop, and you get every square of the board positioned correctly

"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



"""
Draw the pieces on the board. Using the current GameState.board

blit is the pygame function that actually draws (copies) one image onto another surface at a specific position
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece =  board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

