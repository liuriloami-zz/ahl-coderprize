from hexplode import algo_player

def criticality (tile_id, board):
    return len(board[tile_id]["neighbours"]) - board[tile_id]["counters"]

def vulnerability (tile_id, board):
    val = 7
    for neighbourId in board[tile_id]["neighbours"]:    
        val = min(val, criticality(neighbourId, board))
    return val

def winCount (tile_id, player_id, board):
    if (board[tile_id]["player"] is None):
        board[tile_id]["counters"] = 1
    else:
        board[tile_id]["counters"] = int(board[tile_id]["counters"]) + 1
    if (criticality(tile_id, board) != 1):
        return 0
    count = 0
    if (board[tile_id]["player"] != player_id):
        board[tile_id]["player"] = player_id
        count += 1
    for neighbourId in board[tile_id]["neighbours"]:    
        count += winCount(neighbourId, player_id, board)
    return count
    
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
                
    if (minNbrs != maxNbrs and minNbrs != 7):
        return bestCell
    else:
        return exploder(player_id, board)

def gobbler(player_id, board):
    bestWin = 0
    bestCell = None
    for tile_id, tile in board.items():
        if (tile["player"] == player_id):
            newBoard = board
            win = winCount(tile_id, player_id, newBoard)
            if (win > bestWin):
                bestWin = win
                bestCell = tile_id
    if (bestWin > 0):
        return bestCell
    else:
        return exploder(player_id, board)

@algo_player(name="Liuri Loami 4 - Gobbler",
             description="liuriloami@gmail.com")
def liurioami1(board, game_id, player_id):
    val = gobbler(player_id, board)
    return val
