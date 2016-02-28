import time
import copy
from hexplode import algo_player

def criticality (tile_id, board):
    if (board[tile_id]["player"] is None):
        return len(board[tile_id]["neighbours"])
    else:
        return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, player_id, board):
    vul = 7
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] is not None and board[neighbourId]["player"] != player_id):
            vul = min(vul, criticality(neighbourId, board))
    return vul

def winCount (checkedTiles, enemies, tile_id, player_id, board):
    
    if (tile_id in checkedTiles): 
        return 1
    checkedTiles.append(tile_id)
    
    if (board[tile_id]["player"] is None or criticality(tile_id, board) != 1):
        for neighbourId in board[tile_id]["neighbours"]:
            if (board[neighbourId]["player"] != player_id and board[neighbourId]["player"] is not None):
                if (neighbourId not in enemies):
                    enemies.append(neighbourId)
        if (board[tile_id]["player"] is not None and
            board[tile_id]["player"] != player_id):
            return 1
        else:
            return 0
        
    count = 0
    if (board[tile_id]["player"] != player_id):
        count += 1
        
    for neighbourId in board[tile_id]["neighbours"]:
        count += winCount(checkedTiles, enemies, neighbourId, player_id, board)
    return count
    
    
def lostCount(checkedTiles, losts, tile_id, player_id, board):
    
    if (tile_id in checkedTiles): 
        return 1
    checkedTiles.append(tile_id)
    
    if (board[tile_id]["player"] == player_id):
        losts.append(player_id)
        
    if (criticality(tile_id, board) == 1):
        for neighbourId in board[tile_id]["neighbours"]:
            lostCount(checkedTiles, losts, neighbourId, player_id, board)
    
    
def isTileSafe(tile_id, player_id, board):
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] != player_id):
            return False
    return True
    
@algo_player(name="Liuri Loami 5 - Ultimate 9",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):
    corner = False
    critical = False
    exploding = False
    bestCorner = 4
    bestWin = 0
    bestCell = None
    for tile_id, tile in board.items():
        vul = vulnerability(tile_id, player_id, board)
        crit = criticality(tile_id, board)
        neighbours = len(tile["neighbours"])
        
        ## Corner, if not vulnerable
        if (tile["player"] is None and neighbours < bestCorner and vul >= crit):
            corner = True
            bestCorner = neighbours
            bestCell = tile_id
            
        ## If a corner was chosen, forget about the rest
        if (corner):
            continue
            
        if (tile["player"] == player_id):
            
            # If it is safe, avoid it
            if (isTileSafe(tile_id, player_id, board) is True and crit > 1):
                continue
                
            #Search for the biggest explosion
            checkedTiles = []
            enemies = []
            losts = []
            boardCopy = copy.deepcopy(board)
            win = winCount(checkedTiles, enemies, tile_id, player_id, boardCopy)
            maxLose = 0
            for enemy_tile in enemies:
                enemyBoard = copy.deepcopy(board)
                tmpList = []
                lostCount(tmpList, losts, enemy_tile, player_id, enemyBoard) 
            win -= len(losts)
                    
            if (vul == crit and win > bestWin):
                bestWin = win
                bestCell = tile_id
                critical = True
                
            if (critical):
                continue
                
            if (crit == 1 and win > bestWin):
                bestWin = win
                bestCell = tile_id
                exploding = True
                
            if (exploding):
                continue
                
            if (win / max(1,vul-crit) > bestWin):
                bestWin = -1*(vul-crit)
                bestCell = tile_id
                
   # If a tile was chosen, return if
    if (bestCell is not None):
        return bestCell
        
   # If not, return a random tile
    for tile_id, tile in board.items():
        if (tile["player"] == player_id):
            return tile_id
