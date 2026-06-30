"""
This class is responsible for storing all the informaiton abou the current state of a game.
It will also be responsible for determining the valid state of a moove.
It will also keep a moove log.
"""

class Gamestate():
    def __init__(self):
        #board is an 8x8 2d list, each element is made of 2 characters
        #the first character represents the color of the piece, 'b' or 'w'
        #the second characters represents the type of the piece, 'K', 'R', 'B','N' or 'p'
        #"--" represents an empty cell with no piece.
        self.board = [
             ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], #The first letter represents the colour, the second the piece
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],#bp = blackpawns for exemple
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"],
             ["--", "--", "--", "--", "--", "--", "--", "--"], #two dashes represent an empty cell
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]] #White pieces
        
        self.whiteToMove = True
        self.moveLog = []


        