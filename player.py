import board
import random
import math

# Player implementation using minimax with and without alpha-beta pruning.
# Includes a transposition table to cache previously evaluated board states.
# The player always plays as "X" and moves first.
# getMove() uses plain minimax; getMoveAlphaBeta() uses minimax with alpha-beta pruning.
# Both methods return a column index (0-indexed) for the next move.
# Tracks nodes expanded and branches pruned for performance analysis.
class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 
		self.numPruned = 0 
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