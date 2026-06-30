""" 
This is our main driver file. It will be responsible for handling user input and displaying the current game State object
"""

import pygame as p
from Chess import ChessEngine #Go into a folder/package called Chess, and from there, import the file ChessEngine.py as a whole module.

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
    while running:
        for e in p.event.get(): #p.event.get collects everything that happens — every key press, mouse click, window close button click — into a list of "events."
            if e.type == p.QUIT: #is the current event specifically a request to quit?
                running = False 
        
        clock.tick(MAX_FPS) #Uses the Clock object to pause the loop just enough so it doesn't run faster than MAX_FPS
        p.display.flip() #p.display.flip() is what actually pushes everything you've drawn onto the visible window



if __name__ == "__main__":
    main()

