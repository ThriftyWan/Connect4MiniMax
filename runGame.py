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
# The AI player (X) always goes first.
# Player 2 can be swapped for another AI or a human player.

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