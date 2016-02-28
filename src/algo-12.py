import time
import copy
from hexplode import algo_player

def criticality (tile_id, board):
    if (board[tile_id]["player"] is None):
        return 7
    return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, player_id, board):
    vul = 7
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] is not None and board[neighbourId]["player"] != player_id):
            vul = min(vul, criticality(neighbourId, board))
    return vul

def winCount (rec, isHead, checkedTiles, dangers, tile_id, player_id, enemy_id, board):
    
    if (tile_id in checkedTiles): 
        return 1
    checkedTiles.append(tile_id)
    
    oldPlayer =  board[tile_id]["player"]
    board[tile_id]["player"] = player_id
    
    count = 0
    if (oldPlayer != player_id):
        count += 1
    
    
    if (oldPlayer is None):
        board[tile_id]["counters"] = 1
        return count
        
    if (criticality(tile_id, board) != 1):
        for neighbourId in board[tile_id]["neighbours"]:
            if (criticality(neighbourId, board) == 1):
                dangers.append(neighbourId)
        board[tile_id]["counters"] += 1
        return count
                
    for neighbourId in board[tile_id]["neighbours"]:
        count += winCount(rec, False, checkedTiles, dangers, neighbourId, player_id, enemy_id, board)
    
    if (isHead and rec > 0):
        maxLoss = -1000
        for tile_id in dangers:
            if (tile_id not in checkedTiles):
                list1 = []
                list2 = []
                newBoard = copy.deepcopy(board)
                maxLoss = max(maxLoss, winCount(rec-1, True, list1, 
                                            list2, tile_id, enemy_id, 
                                            player_id, newBoard))
        
    return count
    
def isTileSafe(tile_id, player_id, board):
    for neighbourId in board[tile_id]["neighbours"]:
        if (board[neighbourId]["player"] != player_id):
            return False
    return True
    
@algo_player(name="Liuri Loami 11 - Ultimate 7",
             description="liuriloami@gmail.com")
def liuriloami(board, game_id, player_id):
    enemy_id = None
    corner = False
    critical = False
    exploding = False
    bestCorner = 4
    bestWin = -100.0
    bestCell = None
    bestCrit = 7
    
    for tile_id, tile in board.items():
        player = tile["player"]
        if (player is not None and player is not player_id):
            enemy_id = player
            break
            
    for tile_id, tile in board.items():
        vul = vulnerability(tile_id, player_id, board)
        crit = criticality(tile_id, board)
        neighbours = len(tile["neighbours"])
        
        ## Corner, if not vulnerable
        if (tile["player"] is None and neighbours < bestCorner and vul > 3 and isTileSafe(tile_id, player_id, board) is False):
            corner = True
            bestCorner = neighbours
            bestCell = tile_id
            
        ## If a corner was chosen, forget about the rest
        if (corner):
            continue
            
        if (tile["player"] == player_id):
            
            # If it is safe, avoid it
            if (isTileSafe(tile_id, player_id, board) is True):
                continue
            
            #Search for the biggest explosion
            checkedTiles = []
            dangers = []
            boardCopy = copy.deepcopy(board)
            win = winCount(1, True, checkedTiles, dangers, tile_id, player_id, enemy_id, boardCopy)
                
            # If enemy is about to explode, explode first
            if (crit == 1 and vul == 1 and win > 0):
                bestCell = tile_id
                bestWin = win
                critical = True
                
            if (critical):
                continue
                    
            if (crit == 1 and win > bestWin):
                bestWin = win
                bestCell = tile_id
                exploding = True
                
            if (exploding is False and vul >= crit):
                if (-1*(vul-crit) > bestWin):
                    bestWin = -1*(vul-crit)
                    bestCell = tile_id
                if (-1*(vul-crit) == bestWin and win > bestWin):
                    bestWin = -1*(vul-crit)
                    bestCell = tile_id
                
   # If a tile was chosen, return if
    if (bestCell is not None):
        return bestCell
        
   # If not, return a random tile
    for tile_id, tile in board.items():
        if (tile["player"] == player_id):
            return tile_id
