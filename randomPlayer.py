import board
import random

# A simple player that chooses random moves, to help with (starting) testing. Once you have something
# sensible, you should use that instead of the random player.
class RandomPlayer:
	
    # The random player is used as a baseline opponent for testing the AI.
    # You can specify a seed for the random number generation so that you can test with a consistent environment.
    # If you want to seed the player differently each time, you can use something like the following (in
    # runGame)
    #       import datetime
    #       seed = datetime.now().timestamp()
    # to get a different seed each time.
	def __init__(self, name, seed=0):
		self.name = name
		self.randomGenerator = random.Random(seed)
	
    # Return a random column, checking that it is not full
	def getMove(self, gameBoard):
		maxCol = gameBoard.numColumns

		choice = self.randomGenerator.randint(0, maxCol-1)
    
		while gameBoard.colFills[choice] >= gameBoard.numRows:
			choice = self.randomGenerator.randint(0, maxCol-1)

		return choice