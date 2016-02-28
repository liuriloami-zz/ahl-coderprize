import random
import copy
import time
from hexplode import algo_player

explode = {}

def isEnemy(player, player_id, board):
    return player is not None and player is not player_id

def getCountdown(tile_id, board):
    tile = board[tile_id]
    if (tile["player"] is None):
        return len(tile["neighbours"])
    else:
        return len(tile["neighbours"]) - tile["counters"]

def getEnemyCountdown(tile_id, player_id, board):
    tile = board[tile_id]
    minCountdown = 7
    for neighbourId in tile["neighbours"]:
        if (isEnemy(board[neighbourId]["player"], player_id, board)):
            minCountdown = min(minCountdown, getCountdown(neighbourId, board))
    return minCountdown

@algo_player(name="Liuri Loami 18 - Extreme 2",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):

    priority = 0
    bestCountdown = 7
    bestNbrs = 7
    bestRiskDiff = 7
    bestCells = []

    ## Mark vulnerable tiles
    for tile_id, tile in board.items():
        if (isEnemy(tile["player"], player_id, board) and getCountdown(tile_id, board) == 1):
            for neighbour_id in tile["neighbours"]:
                if ("enemies" not in board[neighbour_id]):
                    board[neighbour_id]["enemies"] = 1
                else:
                    board[neighbour_id]["enemies"] += 1

    for tile_id, tile in board.items():

        ## If it is an enemy, skip it
        if (isEnemy(tile["player"], player_id, board)):
            continue

        ## Calculate everything
        countdown = getCountdown(tile_id, board)
        enemyCountdown = getEnemyCountdown(tile_id, player_id, board)
        advantage = enemyCountdown - countdown
        neighbours = len(tile["neighbours"])

        ## Priority 1: Player tile with advantage = 0
        if (tile["player"] is player_id and advantage == 0):
            if (priority != 1):
                bestCountdown = 7
            priority = 1
            if (countdown < bestCountdown):
                bestCountdown = countdown
                bestCells = []
                bestCells.append(tile_id)
            elif (countdown == bestCountdown):
                bestCells.append(tile_id)

        if (priority == 1):
            continue

        ## Priority 2: Empty tile with advantage >= 0
        if (tile["player"] is None and enemyCountdown < 7 and advantage >= 0):
            if (priority != 2):
                bestCountdown = 7
            priority = 2
            if (countdown < bestCountdown):
                bestCountdown = countdown
                bestCells = []
                bestCells.append(tile_id)
            elif (countdown == bestCountdown):
                bestCells.append(tile_id)

        if (priority == 2):
            continue

        ## Calculate the max risk
        risk = 7
        for neighbour_id in tile["neighbours"]:
            if ("enemies" in board[neighbour_id]):
                risk = min(risk, getCountdown(neighbour_id, board) - board[neighbour_id]["enemies"])

        ## Priority 3: Player tile with vulnerable neighbours that could represent some risk
        if (tile["player"] is player_id):
            riskDiff = countdown - risk
            if (riskDiff >= 0):
                priority = 3
                if (riskDiff > bestRiskDiff):
                    bestRiskDiff = riskDiff
                    bestCells = []
                    bestCells.append(tile_id)
                elif (riskDiff == bestRiskDiff):
                    bestCells.append(tile_id)

        if (priority == 3):
            continue

        ## Priority 4: Empty cell, with no enemies nor vulnerable neighbours with some risk
        if (tile["player"] is None and enemyCountdown == 7 and neighbours <= risk):
            priority = 4
            if (neighbours < bestNbrs):
                bestNbrs = neighbours
                bestCells = []
                bestCells.append(tile_id)
            elif (neighbours == bestNbrs):
                bestCells.append(tile_id)

        if (priority == 4):
            continue

        ## Priority 5: Player tile with advantage > 0 and the biggest countdown
        if (tile["player"] is player_id and advantage >= 0):
            if (priority != 5):
                bestCountdown = 7
            priority = 5
            if (countdown < bestCountdown):
                bestCountdown = countdown
                bestCells = []
                bestCells.append(tile_id)
            elif (countdown == bestCountdown):
                bestCells.append(tile_id)

        if (priority == 5):
            continue

    ## Priority 6: Anyone
    if (len(bestCells) == 0):
        for tile_id, tile in board.items():
            if tile["player"] is None or tile["player"] == player_id:
                bestCells.append(tile_id)

    return random.choice(bestCells)
