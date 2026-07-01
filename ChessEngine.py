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
        
        self.moveFunctions = {'p': self.getPawnMoves,'R': self.getRookMoves,'N': self.getKnightMoves,'B': self.getBishopMoves,'Q': self.getQueenMoves,'K': self.getKingMoves}

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
                    self.moveFunctions[piece](r,c, moves) #calls the appropriate move function, based on piece type
        return moves
    """
    Get all the pawn moves for the pawns, and add those moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b': #enemy piece to capture to the left
                moves.append(Move((r, c),(r-1, c-1), self.board))
            if c+1 <= 7 and self.board[r-1][c+1][0] == 'b': #enemy piece to capture to the right
                moves.append(Move((r, c),(r-1, c+1), self.board))
       
        if not self.whiteToMove: #black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c), (r+1,c), self.board)) 
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r+2,c), self.board))
            if c-1 >= 0 and self.board[r+1][c-1][0] == "w": #enemy piece to capture to the left
                 moves.append(Move((r, c), (r+1,c-1), self.board))
            if c+1 <= 7 and self.board[r+1][c+1][0] == "w": #enemy piece to capture to the left
                 moves.append(Move((r, c), (r+1,c+1), self.board))

    """
    Get all the rook moves for the rooks, and add those moves to the list
    """
    def getRookMoves(self, r, c, moves):
        current_player = 'w' if self.whiteToMove else 'b'
        for i in range(1, 8-r): #vertical upward movement
            if self.board[r+i][c] == "--":
                moves.append(Move((r, c), (r+i,c), self.board))
            elif self.board[r+i][c][0] != current_player:
                moves.append(Move((r, c), (r+i,c), self.board))
                break
            else:
                break
        for i in range(1, r+1): #vertical downward movement
            if self.board[r-i][c] == "--":
                moves.append(Move((r, c), (r-i,c), self.board))
            elif self.board[r-i][c][0] != current_player:
                moves.append(Move((r, c), (r-i,c), self.board))
                break
            else:
                break
        for i in range(1, 8-c): #horizontal rightward movement
            if self.board[r][c+i] == "--":
                moves.append(Move((r, c), (r,c+i), self.board))
            elif self.board[r][c+i][0] != current_player:
                moves.append(Move((r, c), (r,c+i), self.board))
                break
            else:
                break
        for i in range(1, c+1): #horizontal leftward movement
            if self.board[r][c-i] == "--":
                moves.append(Move((r, c), (r,c-i), self.board))
            elif self.board[r][c-i][0] != current_player:
                moves.append(Move((r, c), (r,c-i), self.board))
                break
            else:
                break
    """
    Get all the knight moves for the knights, and add those moves to the list
    """
    def getKnightMoves(self, r, c, moves):
        directions = [(1, 2), (1, -2), (-1, -2), (-1, 2), (2, 1), (2, -1), (-2, -1), (-2, 1)]
        current_player = "w" if self.whiteToMove else "b"
        for direction in directions:
            if (0 <= r + direction[0] <= 7) and (0 <= c + direction[1] <= 7):
                if self.board[r + direction[0]][c + direction[1]] == "--":
                    moves.append(Move((r,c), (r + direction[0], c + direction[1]), self.board))
                elif self.board[r + direction[0]][c + direction[1]][0] != current_player:
                    moves.append(Move((r,c), (r + direction[0], c + direction[1]), self.board))
                

    """
    Get all the bishop moves for the bishops, and add those moves to the list
    """
    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        current_player = "w" if self.whiteToMove else "b"
        for dr, dc in directions:
            endRow, endCol = r + dr, c + dc
            for i in range(len(self.board)):
                if (0 <= endRow <= 7) and (0 <= endCol <= 7):
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.board[endRow][endCol][0] != current_player:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                endRow += dr
                endCol += dc
    
    """""
    Get all the queen moves for the queen, and add those moves to the list
    """
    def getQueenMoves(self, r, c, moves):
        pass

    """
    Get all the king moves for the king, and add those moves to the list
    """
    def getKingMoves(self, r, c, moves):
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
    overrides == to compare moveIDs instead of memory addresses
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    

    