import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune 
		self.treeExpanded = False
		self.depth = -1
		self.transpositionTable = {}

	def getMove(self, gameBoard): #Returns a column

		if gameBoard.numColumns >= 5 and gameBoard.numRows >= 4:
			self.depth = 5

		def minimax(board, depth, maximisingPlayer):
			self.numExpanded += 1

			#Get the key for the gameboard as a string of the pieces
			boardList = []
			for row in range(0, board.numRows):
				for column in range(0, board.numColumns):
					boardList.append(board.checkSpace(row, column).value)
			key = "".join(boardList) #Key now contains the board as a string
			
			if key in self.transpositionTable:
				#print("Board found in table")
				return self.transpositionTable[key]
	

			if depth == 0 or board.checkWin() == True or board.checkFull() == True:
				#Evaluate the state
				#print(f"terminal state score: {self.evaluateState(board)}")
				return self.evaluateState(board), None

			#Get all valid moves
			columns = gameBoard.numColumns
			rows = gameBoard.numRows
			#Find valid columns by using colFills
			validColumns = list()
			orderedColumns = list()
			
			for i in range (columns):
				if board.colFills[i] < rows:
					validColumns.append(i)
					#If numRows = 2 then colFills can be either 0 or 1 so only add when colFills <
					


			if maximisingPlayer == True:
				maximumValue = float("-inf")
				bestMove = None
						
				for col in validColumns:
					validState = board.copy()
					validState.addPiece(col, self.name) #Add an "X" in each valid column
					newValue, _ = minimax(validState, depth - 1, False)
					if newValue > maximumValue:
						maximumValue = newValue
						bestMove = col
				result =  maximumValue, bestMove
			else:
				minimumValue = float("inf")
				bestMove = None

				for col in validColumns:
					validState = board.copy()
					validState.addPiece(col, "O") #Add an "O" in each valid column
					newValue, _ = minimax(validState, depth - 1, True)
					if newValue < minimumValue:
						minimumValue = newValue
						bestMove = col
				result = minimumValue, bestMove

			self.transpositionTable[key] = result
			return result

		evalScore, moveToMake = minimax(gameBoard, depth=self.depth, maximisingPlayer=True)
		#print(f"Evaluation Score for the chosen move: {evalScore}, Move Made: {moveToMake} \n")

		return moveToMake


	def getMoveAlphaBeta(self, gameBoard):

		def minimaxAlphaBeta(board, depth, alpha, beta, maximisingPlayer):
			self.numExpanded += 1

			#Get the key for the gameboard as a string of the pieces
			boardList = []
			for row in range(0, board.numRows):
				for column in range(0, board.numColumns):
					boardList.append(board.checkSpace(row, column).value)
			key = "".join(boardList) #Key now contains the board as a string
			
			if key in self.transpositionTable:
				#print(f"Board found in table: {self.transpositionTable[key]}")
				return self.transpositionTable[key]

			
			if depth == 0 or board.checkWin() == True or board.checkFull() == True:
				#Evaluate the state
				return self.evaluateState(board), None

			#Get all valid moves
			columns = gameBoard.numColumns
			rows = gameBoard.numRows
			#Find valid columns by using colFills
			validColumns = list()
			for i in range (columns):
				if board.colFills[i] < rows:
					validColumns.append(i)
					#If numRows = 2 then colFills can be either 0 or 1 so only add when colFills <

			if maximisingPlayer == True:
				maximumValue = float("-inf")
				bestMove = None
						
				for col in validColumns:
					validState = board.copy()
					validState.addPiece(col, self.name) #Add an "X" in each valid column
					newValue, _ = minimaxAlphaBeta(validState, depth - 1, alpha, beta, False)
					if newValue > maximumValue:
						maximumValue = newValue
						bestMove = col
					alpha = max(alpha, newValue)
					if beta <= alpha:
						self.numPruned += 1
						break
				result = maximumValue, bestMove
			else:
				minimumValue = float("inf")
				bestMove = None
 
				for col in validColumns:
					validState = board.copy()
					validState.addPiece(col, "O") #Add an "O" in each valid column
					newValue, _ = minimaxAlphaBeta(validState, depth - 1, alpha, beta, True)
					if newValue < minimumValue:
						minimumValue = newValue
						bestMove = col
					beta = min(beta, newValue)
					if beta <= alpha:
						self.numPruned += 1
						break
				result = minimumValue, bestMove

			self.transpositionTable[key] = result
			return result

		evalScore, moveToMake = minimaxAlphaBeta(gameBoard, depth=self.depth, alpha=float("-inf"), beta=float("inf"), maximisingPlayer=True)
		print(f"Evaluation Score for the chosen move: {evalScore}, Move Made: {moveToMake} \n")

		return moveToMake
	
	def evaluateState(self, gameBoard): #Testing for connect 4
		heur = 0
		heurScaling = 10 ** gameBoard.winNum - 1
		state = gameBoard.copy()
		flag = False

		if state.checkWin() == True and state.lastPlay[2] == self.name:
			heur = heurScaling * 10
			return heur
		elif state.checkWin() == True and state.lastPlay[2] == "O":
			heur = -(heurScaling * 10)
			return heur

		for row in range (0, state.numRows):
			for column in range(0, state.numColumns):

				for x in range(0, 4): #Loop through checking vertical, horizontal, positive diagonals and negative diagonal streaks
					playerStreak = 0
					opponentStreak = 0
					for i in range(0, state.winNum):
						try:
							if x == 0:
								if state.checkSpace(row + i, column).value == self.name:
									playerStreak += 1
								else:
									break
							elif x == 1:
								if state.checkSpace(row, column + i).value == self.name:
									playerStreak += 1
								else:
									break
							elif x == 2:
								if state.checkSpace(row + i, column + i).value == self.name:
									playerStreak += 1
								else:
									break
							elif x == 3:
								if state.checkSpace(row - i, column + i).value == self.name:
									playerStreak += 1
								else:
									break
						except IndexError:
							pass
						if playerStreak >= 2:
							heur += 10 ** (playerStreak - 1)

					for i in range(0, state.winNum):
						try:
							if x == 0:
								if state.checkSpace(row + i, column).value == "O":
									opponentStreak += 1
								else:
									break
							elif x == 1:
								if state.checkSpace(row, column + i).value == "O":
									opponentStreak += 1
								else:
									break
							elif x == 2:
								if state.checkSpace(row + i, column + i).value == "O":
									opponentStreak += 1
								else:
									break
							elif x == 3:
								if state.checkSpace(row - i, column + i).value == "O":
									opponentStreak += 1
								else:
									break
						except IndexError:
							pass
						if opponentStreak >= 2:
							heur -= 10 ** (opponentStreak - 1)
				
				#Alter the heuristic based on how close pieces are to the center
							
				if state.numColumns % 2 == 0:
					if column == state.numColumns / 2 or column == (state.numColumns / 2) - 1:
						if state.checkSpace(row, column).value == self.name:
							heur += 15
						elif state.checkSpace(row, column).value == "O":
							heur -= 15
				else:
					if column == (state.numColumns - 1) / 2:
						if state.checkSpace(row, column).value == self.name:
							heur += 30
						elif state.checkSpace(row, column).value == "O":
							heur -= 30
					

		#Check threats of states where the opponent can win, if there are 3 Os and 1 " " in a line there is a threat
		#for row in range(0, state.numRows):
			#for column in range(0, state.numColumns):
				OpponentCount = 0
				SpaceCount = 0
				for x in range (0, 4): #4 Directions to check in
					for i in range(0, state.winNum):
						try:
							if x == 0 and row < state.numRows - state.winNum + 1: #Check vertical opponent winning positions
								if state.checkSpace(row + i, column).value == "O":
									OpponentCount += 1
								elif state.checkSpace(row + i, column).value == " ":
									SpaceCount += 1
							elif x == 1 and column < state.numColumns - state.winNum + 1: #Check horizontals
								if state.checkSpace(row, column + i).value == "O":
									OpponentCount += 1
								elif state.colFills[column + i] == row:
									SpaceCount += 1
							elif x == 2 and row < state.numRows - state.winNum + 1 and column < state.numColumns - state.winNum + 1:
								if state.checkSpace(row + i, column + i).value == "O":
									OpponentCount += 1
								elif state.colFills[column + i] == row + i:
									SpaceCount += 1
							elif x == 3 and row >= state.winNum - 1 and column < state.numColumns - state.winNum + 1:
								if state.checkSpace(row - i, column + i).value == "O":
									OpponentCount += 1
								elif state.colFills[column + i] == row - i:
									SpaceCount += 1
						except IndexError:
							pass
					#print(f"Opponent count: {OpponentCount}, Spaces: {SpaceCount}")
					if OpponentCount == state.winNum - 1 and SpaceCount == 1:
						heur -= heurScaling #Opponent can win on their turn in this state
						flag = True
						OpponentCount = 0
						SpaceCount = 0
						break
					OpponentCount = 0
					SpaceCount = 0
				if flag == True:
					break
			if flag == True:
				break

		#Pieces in the center columns are strategically better so check the number of player and opponent pieces in the center columns
		#Perhaps assign the biggest values to those in the center most column then decrease the impact the further out 

		#print(f"heuristic: {heur}")
		return heur
	
	#Reason for many winning states detected is that checkWin() is used, change it to specifically look for horizontal streaks, vertical etc