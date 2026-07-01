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

    """
    Takes a Move as a parameter and executes it (don't work for castling, pawn promotion and en passant)
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players

    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop() #pop() removes and returns the last item in the list
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns back

    """
    All moves considering checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we will not worry about checks

    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols given row
                turn = self.board[r][c][0] #Index [0] grabs the first character (the color). So turn is either 'w', 'b', or '-'
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #Index [1] grabs the type of the piece
                    if piece == 'p':
                        self.getPawnMoves(r,c , moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves
    """
    Get all the pawn moves for the pawns, and add those moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        pass

    """
    Get all the rook moves for the pawns, and add those moves to the list
    """
    def getRookMoves(self, r, c, moves):
        pass


class Move():
    # maps kets to values
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
     "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
     "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}





    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0] 
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    

    