#
# zookPlayer.py
#
# CS 440 PA 3
# Kylie Moses and Eli Saracino
#
# Intelligent player script for AtroposGame.
# Reads in board and last move string and determines and writes out next move string.
#


import sys
import copy

# print to stderr for debugging purposes
# remove all debugging statements before submitting your code
msg = "Given board " + sys.argv[1] + "\n"
# msg = "[32][133][3332][13233][313332][1130223][30112222][1212121]LastPlay:(1,1,2,5)"
sys.stderr.write(msg)

def all_open_pos(board):
    """
        Takes in a board and returns a list of all open positions on that board.
    """

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
    """
        Takes in a board and prev_move and returns a list of all possible successor boards.
    """

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
    """
        Takes in a board and move and returns a new deep copy of the passed in board
        with the move applied to it.
    """

    new_board = copy.deepcopy(board)
    row = new_board[-1 - move[1]]
    new_row = row[0][:move[2]] + move[0] + row[0][move[2] + 1:] 
    row[0] = new_row


    return new_board


def is_loss(neighbors, color):
    """
        Takes in a list of tuples (neighbors) and the color of the marker who has those neighbors, 
        and determines if the player who placed the marker with the passed in color has lost.
    """

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
    """
        Our static evaluator.
        Takes in a board, prev_move, and turn and determines the score of situation based
        on the prev_move on that board and whose turn it is. 
        Score is higher the fewer open positions there are left.
    """
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
    """
        Takes in a board and a position tuple of a marker and 
        returns a list of tuples representing that marker's neighbors.
    """
    
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
    """
        Takes in a board, height, left distance, and right distance
        of a marker on the board and returns the tuple representing that marker
        along with its color.
    """
    row = board[-1 - height]
    if height == 0:
        return (row[0][left_dist - 1], height, left_dist, right_dist)
    else: 
        return (row[0][left_dist], height, left_dist, right_dist)


def process_board(board):
    """
        Takes in the passed in board string and returns a 2D list of strings representing
        the board and a tuple representing the color and coordinates of the previous move on the board.
    """
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
    """
        Main player method that uses the minimax algorithm to determines the "best" next move of the player
        based on the passed in board and prev_move, with a given lookahead of depth.
        The turn parameter is used to determine whose "turn" it is during the recursive
        minimax algorithm.
    """

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


def main():
    board, prev_move = process_board(sys.argv[1])
    # board, prev_move = process_board(msg)
    _, move = next_move(board, 3, prev_move, True)

    color = int(move[0])
    move = (color, move[1], move[2], move[3])

    sys.stdout.write(str(move));
    

if __name__ == "__main__":main() ## with if
