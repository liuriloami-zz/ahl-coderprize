from hexplode import algo_player

def criticality (tile_id, board):
    return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, board):
    tileCrit = criticality(tile_id)
    val = 0
    for neighbourId in board[tile_id]["neighbours"]:    
        val += tileCrit - criticality(neighbourId)
    return val

def exploder (player_id, board):
    mostCrit = 7
    bestNbrs = 0
    bestCell = "None"
    
    minNbrsVal = 7
    minNbrsCell = "None"

    for tile_id, tile in board.items():
        neighbours = len(tile["neighbours"])
        if tile["player"] is None: 
            if (neighbours < minNbrsVal):
                minNbrsCell = tile_id
                minNbrsVal = neighbours
        if tile["player"] == player_id:
            crit = criticality(tile_id, board)
            if (crit < mostCrit):
                mostCrit = crit
                bestNbrs = neighbours
                bestCell = tile_id
            elif (crit == mostCrit and neighbours > bestNbrs):
                bestNbrs = neighbours
                bestCell = tile_id
        
    if (bestCell != "None"):
        return bestCell
    else:
        return minNbrsCell

def loader (player_id, board):
    mostCrit = 7
    bestNbrs = 0
    bestCell = "None"

    for tile_id, tile in board.items():
        neighbours = len(tile["neighbours"])
        if tile["player"] == player_id:
            crit = criticality(tile_id, board)
            if (crit < mostCrit and crit > 1):
                mostCrit = crit
                bestNbrs = neighbours
                bestCell = tile_id
            elif (crit == mostCrit and neighbours > bestNbrs):
                bestNbrs = neighbours
                bestCell = tile_id
        elif tile["player"] is None:
            if (neighbours < mostCrit):
                mostCrit = neighbours
                bestNbrs = neighbours
                bestCell = tile_id
    if (bestCell != "None"):
        return bestCell
    else:
        return exploder(player_id, board)

def cornered (player_id, board):
    minNbrs = 7
    maxNbrs = -1
    bestCell = "None"

    for tile_id, tile in board.items():
        neighbours = len(tile["neighbours"])
        if tile["player"] is None:
            if (neighbours > maxNbrs):
                maxNbrs = neighbours
            if (neighbours < minNbrs):
                minNbrs = neighbours
                bestCell = tile_id
                
    if (minNbrs != maxNbrs and maxNbrs != -1):
        return bestCell
    else:
        return exploder(player_id, board)
    
@algo_player(name="Liuri Loami 6 - Cornered Exploder",
             description="liuriloami@gmail.com")
def liurioami1(board, game_id, player_id):
    val = cornered(player_id, board)
    return val
