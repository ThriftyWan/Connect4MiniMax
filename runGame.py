import board
import game
import player
import randomPlayer
import realPlayer
# Note that you can comment out the following if you don't want to seed the random player differently each run
from datetime import datetime
import time
import statistics
import os
from notifypy import Notify

# This script allows you to test your solution.
# Your coursework implementation must always be player 1.
# You should consider changing player 2 to use a minimax approach for evaluation.
# It is recommended that you also consider other game board sizes, and vary the number of pieces 
# that are required in a line to win. There are examples of the method calls to create such games
# commented out below.
#p1 = player.Player("X")

# Player 2 currently picks random moves and so, while player 2 is not very good, it does allow you to
# start testing your solution. Once you have something sensible, you should change player 2 to be more 
# intelligent. Note that you can specify a seed for the random player (currently the seed is '42'),
# which allows for testing in a consistent environment.
# Note that the following two lines seed the random player differently each run
#seed = datetime.now().timestamp()
#p2 = randomPlayer.RandomPlayer("O", seed)
# Instead of randomly seeding, you can comment out the following line to seed the random player and
# test with a consistent opponent
#p2 = randomPlayer.RandomPlayer("O", 42)
#p2 = realPlayer.RealPlayer("O")
#p2 = player.Player("O")
# The arguments to game.Game specify the two players, the number of rows, the number of columns
# and the number of pieces that need to be placed in a line in order to win.
# g = game.Game(p1, p2, 5, 6, 4)
# g = game.Game(p1, p2, 5, 6, 3)    
# g = game.Game(p1, p2, 4, 5, 3)
# g = game.Game(p1, p2, 4, 4, 4)
# g = game.Game(p1, p2, 4, 4, 3)
#g = game.Game(p1, p2, 4, 4, 3)

# You can pass 'True' to the playGame() method to test your alpha-beta pruning approach, i.e., to make
# player 1 use alpha-beta. If you want player 2 to use alpha-beta you will need to ensure 
# that you create player 2 accordingly. 
#g.playGame(False)
#g = game.Game(p1, p2, 4, 4, 3)
#g.playGame(False)

times = []
expanded = []
pruned = []

totalGames = 2

wins = 0
losses = 0
draws = 0

rows = 5
columns = 3
winNum = 3

startTime = time.time()
for i in range(0, totalGames):
    iterationStart = time.time()
    p1 = player.Player("X")
    seed = datetime.now().timestamp()
    p2 = randomPlayer.RandomPlayer("O", seed)
    g = game.Game(p1, p2, rows, columns, winNum)
    result = g.playGame(False)
    if result == 1:
        wins += 1
    elif result == -1:
        losses += 1
    else:
        draws += 1
    iterationTime = time.time() - iterationStart
    times.append(iterationTime)
    expanded.append(p1.numExpanded)
    pruned.append(p1.numPruned)

winrate = (wins / totalGames) * 100
totalTime = time.time() - startTime
meanTime = statistics.mean(times)
stdDeviationTime = statistics.stdev(times)
meanExpanded = statistics.mean(expanded)
stdDeviationExpanded = statistics.stdev(expanded)
meanPruned = statistics.mean(pruned)
stdDeviationPruned = statistics.stdev(pruned)
depth = p1.depth

print(f"\nGames run: {totalGames} \nRows: {rows}\nColumns: {columns} \nWin num: {winNum} \nDepth: {depth}\n")
print(f"Wins: {wins} \nLosses: {losses} \nDraws: {draws} \nWinrate: {winrate}\n")
print(f"Total Time: {totalTime} \nAverage Time: {meanTime} \nStandard Deviation Time: {stdDeviationTime}\n")
print(f"Average nodes expanded: {meanExpanded} \nStandard Deviation Nodes Expanded: {stdDeviationExpanded}\n")
print(f"Average Pruned: {meanPruned} \nStandard Deviation Pruned: {stdDeviationPruned}")

notification = Notify()
notification.title = "Finished test"
notification.message = "Successful"
notification.send()