from hexplode import algo_player

def criticality (tile_id, board):
    return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, board):
    val = 7
    for neighbourId in board[tile_id]["neighbours"]:    
        if (board[neighbourId]["player"] is not None):
            val = min(val, criticality(neighbourId, board))
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

def avoider (player_id, board):
    mostCrit = 7
    mostNbrs = 0
    bestCell = "None"

    for tile_id, tile in board.items():
        neighbours = len(tile["neighbours"])
        if (tile["player"] == player_id):
            crit = criticality(tile_id, board)
            vul = vulnerability(tile_id, board)
            if (crit > vul):
                continue
            if (crit < mostCrit and crit > 1):
                mostCrit = crit
                mostNbrs = neighbours
                bestCell = tile_id
            elif (crit == mostCrit and neighbours > mostNbrs):
                mostNbrs = neighbours
                bestCell = tile_id
        elif (tile["player"] is None):
            if (neighbours < mostCrit):
                mostCrit = neighbours
                mostNbrs = neighbours
                bestCell = tile_id
    
    if (bestCell != "None"):
        return bestCell
    else:
        return exploder(player_id,board)

@algo_player(name="Liuri Loami 3 - Avoider",
             description="liuriloami@gmail.com")
def liurioami1(board, game_id, player_id):
    val = avoider(player_id, board)
    return val
