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

def simulateExplosion(tile_id, player_id, checkedTiles, board):
    if (tile_id in checkedTiles): 
        return 1
    checkedTiles.append(tile_id)
    
    oldPlayer = board[tile_id]["player"]
    countdown = getCountdown(tile_id, board)
    enemyCountdown = getEnemyCountdown(tile_id, player_id, board)
    
    board[tile_id]["player"] = player_id
    
    if (oldPlayer is None):
        board[tile_id]["counters"] = 1
        return 1
        
    if (countdown != 1):
        if (enemyCountdown == 1):
            if (countdown == 2):
                return -1000
            else:
                return 0
        board[tile_id]["counters"] += 1
        if (isEnemy(oldPlayer, player_id, board)):
            return 1
        else:
            return 0
        
    count = 0
    if (isEnemy(board[tile_id]["player"], player_id, board)):
        count += 1
        
    for neighbourId in board[tile_id]["neighbours"]:
        count += simulateExplosion(neighbourId, player_id, checkedTiles, board)
    return count



@algo_player(name="Liuri Loami 19 - Extreme",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):
    hasCritical = False
    hasCorner = False
    hasAdvantage = False
  
    criticalExplosion = -1000
    criticalCountdown = 7
    cornerNbrs = 4
    worseAdv = 7
    worseAdvExplosion = -1000
    
    bestCells = []
        
    for tile_id, tile in board.items():
 
        if (isEnemy(tile["player"], player_id, board)):
            continue
            
        countdown = getCountdown(tile_id, board)
        enemyCountdown = getEnemyCountdown(tile_id, player_id, board)
        advantage = enemyCountdown - countdown
        explosion = simulateExplosion(tile_id, player_id, [], copy.deepcopy(board))
        neighbours = len(tile["neighbours"])
        
        ## 1. Look for criticals
        if (advantage == 0 and (countdown < criticalCountdown or 
                                            (countdown == criticalCountdown and explosion > criticalExplosion))):
            criticalExplosion = explosion
            criticalCountdown = countdown
            bestCells = []
            bestCells.append(tile_id)
            hasCritical = True
        elif (advantage == 0 and countdown == criticalCountdown and explosion == criticalExplosion):
            bestCells.append(tile_id)
        
        if (hasCritical):
            continue
            
        ## 2. Look for corners
        if (tile["player"] is None and advantage >= 0):
            if (neighbours < cornerNbrs):
                cornerNbrs = neighbours
                bestCells = []
                bestCells.append(tile_id)
                hasCorner = True
            elif (neighbours == cornerNbrs):
                bestCells.append(tile_id)
            
        if (hasCorner):
            continue
        
        ## 3. Look for tiles almost in disavantage
        if (tile["player"] is player_id and advantage >= 0 and (advantage < worseAdv or (advantage == worseAdv and explosion > worseAdvExplosion))):
            worseAdv = advantage
            worseAdvExplosion = explosion
            bestCells = []
            bestCells.append(tile_id)
            hasAdvantage = True
        elif (tile["player"] is player_id and advantage == worseAdv and explosion == worseAdvExplosion):
            bestCells.append(tile_id)
            
        if (hasAdvantage):
            continue
         
    if (len(bestCells) == 0):
        for tile_id, tile in board.items():
            if tile["player"] is None or tile["player"] == player_id:
                bestCells.append(tile_id)
    return random.choice(bestCells)
