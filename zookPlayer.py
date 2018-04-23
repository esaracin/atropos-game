import sys
import copy

# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
msg = "Given board " + sys.argv[1] + "\n"
# msg = "[32][133][3332][13233][313332][1130223][30112222][1212121]LastPlay:(1,1,2,5)"
sys.stderr.write(msg)



#parse the input string, i.e., argv[1]
 
#perform intelligent search to determine the next move

#print to stdout for AtroposGame
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.

def all_open_pos(board):

    open_pos = []
    for i in range(len(board)):
        curr = len(board) - 1 - i
        contents = board[curr][0]

        left_d = 0
        right_d = len(contents) - 1

        for position in contents:
            if position == '0':
                to_add = ('0', i, left_d, right_d)
                open_pos.append(to_add)

            left_d += 1
            right_d -= 1

    return open_pos


def get_successors(board, prev_move):

    open_pos = []
    if prev_move == 'null':
        open_pos = all_open_pos(board)
    else:
        neighbors = get_neighbors(board, prev_move)
        # print("neighbors:", neighbors)
    
        for neighbor in neighbors:
            if neighbor[0] == '0':
                open_pos.append(neighbor)

        if len(open_pos) == 0:
            open_pos = all_open_pos(board)
            # print("open positions:", open_pos)
    
    succ = []
    for position in open_pos:
        for color in ['1', '2', '3']:
            move = (color, position[1], position[2], position[3])
            succ.append((apply_move(board, move), move))

    return succ



def apply_move(board, move):
    new_board = copy.deepcopy(board)
    row = new_board[-1 - move[1]]
    new_row = row[0][:move[2]] + move[0] + row[0][move[2] + 1:] 
    row[0] = new_row


    return new_board


def is_loss(neighbors, color):
    other_colors = ""
    if color == "1":
        other_colors = "23"
    elif color == "2":
        other_colors = "13"
    else:
        other_colors = "12"
    
    for i in range(len(neighbors) - 1):
        if (neighbors[i][0] in other_colors and neighbors[i+1][0] in \
        other_colors) and neighbors[i][0] != neighbors[i+1][0]:
            return True


    return False



def evaluate(board, prev_move, turn):
    neighbors = get_neighbors(board, prev_move)

    if is_loss(neighbors, prev_move[0]):
        if not turn:
            return float("inf")
        else:
            return float("-inf")

    # Get count of open neighbors
    count = 0
    for neighbor in neighbors:
        if neighbor[0] == '0':
            count += 1
    
    return -count


def get_neighbors(board, position):
    
    neighbors = []

    neighbors.append(get_checker(board, position[1], position[2] - 1, \
                                 position[3] + 1))

    neighbors.append(get_checker(board, position[1] + 1, position[2] - 1, \
                                 position[3]))

    neighbors.append(get_checker(board, position[1] + 1, position[2], \
                                 position[3] - 1))

    neighbors.append(get_checker(board, position[1], position[2] + 1, \
                                 position[3] - 1))

    neighbors.append(get_checker(board, position[1] - 1, position[2] + 1, \
                                 position[3]))

    neighbors.append(get_checker(board, position[1] - 1, position[2], \
                                 position[3] + 1))


    return neighbors
    


def get_checker(board, height, left_dist, right_dist):
    row = board[-1 - height]
    if height == 0:
        return (row[0][left_dist - 1], height, left_dist, right_dist)
    else: 
        return (row[0][left_dist], height, left_dist, right_dist)


def process_board(board):
    ind = board.index('L')

    if 'null' in board[ind + 9:]:
        prev_move = 'null'
    else:
        prev_move = eval(board[ind + 9:])

    
    board = eval(('[' + board[:ind] + ']').replace('][', '],['))

    for row in range(len(board)):
        board[row][0] = str(board[row][0])

    return board, prev_move




def next_move(board, depth, prev_move, turn):
    if depth == 0:
        return evaluate(board, prev_move, turn), prev_move

    successors = get_successors(board, prev_move)
    # print("successors:", successors)
    # print("board:", board)


    scores = []
    for succ_board, move in successors:
        # We don't want to check the next move of a board that's already lost
        if is_loss(get_neighbors(succ_board, move), move[0]):
            if not turn:
                score = float("inf")
            else:
                score = float("-inf")
        else:
            score, _ = next_move(succ_board, depth -1, move, not turn)

        scores.append([score, move])


    if len(scores) == 0:
        return evaluate(board, prev_move, turn), prev_move

    if turn:
        return max(scores)
    else:
        return min(scores)



board, prev_move = process_board(sys.argv[1])
# board, prev_move = process_board(msg)
_, move = next_move(board, 3, prev_move, True)

color = int(move[0])
move = (color, move[1], move[2], move[3])

sys.stdout.write(str(move));
