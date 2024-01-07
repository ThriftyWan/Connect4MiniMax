import board


class RealPlayer:
    def __init__ (self, name):
        self.name = name

    def getMove(self, gameBoard):

        move = -1

        while(move < 0 or move > gameBoard.numColumns - 1 or gameBoard.colFills[move] >= gameBoard.numRows):
            move = int(input("Column to add piece: "))

        return move