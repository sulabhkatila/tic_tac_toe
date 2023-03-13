import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_x = 0
    num_o = 0

    # Count how many moves X and O have made
    for i in board:
        for j in i:
            if j == "X":
                num_x +=1
            elif j == "O":
                num_o +=1

    if num_x == num_o:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Loop to search for available moves
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == None:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    column = action[1]
    dc_board = copy.deepcopy(board)

    # Check if the move is valid
    if dc_board[row][column] != None:
        raise Exception("Illegal Move")

    # Make the move
    dc_board[row][column] = player(board)

    return dc_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Horizontal 3 in a row
    for i in board:
        if i[0] != None:
            if i[0] == i[1]:
                if i[1] == i[2]:
                    return i[1]

    # Vertical 3 in a row
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != None:
                if board[i][j] == board[i+1][j]:
                    if board[i+2][j] == board[i+1][j]:
                        return board[i][j]
        break

    # Diagonal 3 in a row
    if board[1][1] != None:
        if board[0][0] == board[1][1]:
            if board[1][1] == board[2][2]:
                return board[1][1]

        if board[0][2] == board[1][1]:
            if board[1][1] == board[2][0]:
                return board[1][1]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check if any one got 3 in a row
    if winner(board) != None:
        return True

    # Check for empty spaces, and return false if found one
    for i in board:
        for j in i:
            if j == None:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Check for draw
    if not winner(board):
        return 0

    # Check if X won
    if winner(board) == "X":
        return 1

    # Check if O won
    if winner(board) == "O":
        return -1

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Check if the game has ended
    if terminal(board):
        return None

    # Check if it is X's turn
    elif player(board) == "X":

        all_moves = {}

        # Store all the possible moves with their values
        for action in actions(board):
            value = minvalue(result(board, action))
            all_moves[action] = value

        # Get the move with the highest value
        best_move = max(all_moves, key = all_moves.get)

        return best_move

    # Check if it is O's turn
    else:

        all_moves = {}

        # Store all the possible moves with their values
        for action in actions(board):
            value = maxvalue(result(board, action))
            all_moves[action] = value
        best_move = min(all_moves, key = all_moves.get)

        # Get the move with the lowest value
        return best_move


def maxvalue(board):
    """
    Returns the max value it can get in the current position
    """
    maxv = -math.inf
    if terminal(board):
        return utility(board)

    for action in actions(board):
        maxv = max(maxv, minvalue(result(board, action)))
    return maxv


def minvalue(board):
    """
    Returns the minimum value it can get in the current position
    """
    minv = math.inf
    if terminal(board):
        return utility(board)

    for action in actions(board):
        minv = min(minv, maxvalue(result(board, action)))
    return minv
