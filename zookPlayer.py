import sys
import copy
# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
#msg = "Given board " + sys.argv[1] + "\n";
msg = "[13][302][1003][31002][100003][3000002][121212]LastPlay:(1,3,1,3)"

#sys.stderr.write(msg);


#parse the input string, i.e., argv[1]

 
#perform intelligent search to determine the next move

#print to stdout for AtroposGame
#sys.stdout.write("(3,2,2,2)");
# As you can see Zook's algorithm is not very intelligent. He 
# will be disqualified.

def get_successors(board, prev_move):
    neighbors = get_neighbors(board, prev_move)
    
    open_pos = []
    for neighbor in neighbors:
        if neighbor[0] == '0':
            open_pos.append(neighbor)

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




def evaluate(board, prev_move):
    neighbors = get_neighbors(board, prev_move)

    # Get count of open neighbors
    count = 0
    for neighbor in neighbors:
        if neighbor[0] == '0':
            count += 1
    
    return count


def get_neighbors(board, position):
    
    neighbors = []
    neighbors.append(get_checker(board, position[1] + 1, position[2] - 1, \
                                 position[3]))

    neighbors.append(get_checker(board, position[1] + 1, position[2], \
                                 position[3] - 1))

    neighbors.append(get_checker(board, position[1], position[2] - 1, \
                                 position[3] + 1))

    neighbors.append(get_checker(board, position[1], position[2] + 1, \
                                 position[3] - 1))

    neighbors.append(get_checker(board, position[1] - 1, position[2], \
                                 position[3] + 1))

    neighbors.append(get_checker(board, position[1] - 1, position[2] +1, \
                                 position[3]))

    return neighbors
    


def get_checker(board, height, left_dist, right_dist):
    row = board[-1 - height]
    return (row[0][left_dist], height, left_dist, right_dist)


def process_board(board):
    ind = board.index('L')
    prev_move = eval(board[ind + 9:])
    
    board = eval(('[' + board[:ind] + ']').replace('][', '],['))

    for row in range(len(board)):
        board[row][0] = str(board[row][0])

    return board, prev_move




def next_move(board, depth, prev_move, turn):
    if depth == 0:
        return evaluate(board, prev_move), prev_move

    successors = get_successors(board, prev_move)

    scores = []
    for succ_board, move in successors:
        score, potential_move = next_move(succ_board, depth -1, move, not turn)
        scores.append([score, potential_move])

    if turn:
        return max(scores)
    else:
        return min(scores)

board, prev_move = process_board(msg)
print(get_successors(board, prev_move))
