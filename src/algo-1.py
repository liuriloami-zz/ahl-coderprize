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
    
def getVulnerability(tile_id, player_id, board):
    tile = board[tile_id]
    minCountdown = 7
    for neighbourId in tile["neighbours"]:
        countdown = getCountdown(neighbourId, board)
        if ("enemies" in board[neighbourId]):
            minCountdown = min(minCountdown, countdown - board[neighbourId]["enemies"])
        elif (isEnemy(board[neighbourId]["player"], player_id, board)):
            minCountdown = min(minCountdown, countdown)
    return minCountdown

@algo_player(name="Liuri Loami",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):
    
    priority = 0
    p1 = p2 = p3 = p4 = p5 = 7
    bestCell = None

    for tile_id, tile in board.items():
        if (isEnemy(tile["player"], player_id, board) and getCountdown(tile_id, board) == 1):
            for neighbourId in tile["neighbours"]:
                if ("enemies" not in board[neighbourId]):
                    board[neighbourId]["enemies"] = 1
                else:
                    board[neighbourId]["enemies"] += 1
    
    for tile_id, tile in board.items():

        if (isEnemy(tile["player"], player_id, board)):
            continue

        countdown = getCountdown(tile_id, board)
        enemyCountdown = getEnemyCountdown(tile_id, player_id, board)
        vulnerability = getVulnerability(tile_id, player_id, board)
        advantage = enemyCountdown - countdown
        advantage2 = vulnerability - countdown
        neighbours = len(tile["neighbours"])

        ## Priority 1: Advantage = 0 
        if (tile["player"] is player_id and advantage == 0):
            priority = 1  
            if (countdown < p1):
                p1 = countdown
                bestCell = tile_id
                
        if (priority == 1):
            continue
            
        ## Priority 2: Near an enemy, with some advantage
        if (tile["player"] is None and enemyCountdown < 7 and advantage >= 0):
            priority = 2
            if (advantage < p2):
                p2 = advantage
                bestCell = tile_id
                
        if (priority == 2):
            continue
            
        ## Priority 3: Without advantage, counting vulnerables
        if (tile["player"] is player_id and advantage >= 0 and advantage2 <= 0):
            priority = 3
            if (advantage2 < p3):
                p3 = advantage2
                bestCell = tile_id
                
        if (priority == 3):
            continue
            
        ## Priority 4: Corners
        if (tile["player"] is None and advantage >= 0):
            priority = 4
            if (neighbours < p4):
                p4 = neighbours 
                bestCell = tile_id 
                
        if (priority == 4):
            continue
            
        ## Priority 5: Exploder
        if (countdown < p5):
            p5 = countdown
            bestCell = tile_id
        
    return bestCell
