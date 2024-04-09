import math

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
    Author: Esam Alwaseem
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Author: Esam Alwaseem
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Author: Mohammed Haidous
    """
    # Check if the proposed move is to a cell that is not empty. If so, raise an exception.
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action.")
    
    # Create a deep copy of the board to avoid mutating the original board.
    new_board = [row[:] for row in board]
    
    # Apply the move to the copied board. The move is determined by the current player.
    new_board[action[0]][action[1]] = player(board)
    
    # Return the new board configuration after the move.
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Author: Esam Alwaseem
    """
    # Check rows, columns, and diagonals
    lines = [board[i] for i in range(3)] + [[board[i][j] for i in range(3)] for j in range(3)] + \
            [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    for line in lines:
        if line.count(line[0]) == 3 and line[0] is not None:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Author: Mohammed Haidous
    """
    if winner(board) is not None or all(all(cell is not None for cell in row) for row in board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Author: Mohammed Haidous
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Authors: Mohammed Haidous & Esam Alwaseem
    """
    # Base case: if the board is in a terminal state, return None as no more moves are possible.
    if terminal(board):
        return None

    def max_value(board):
        # Base case for max_value: if board is in a terminal state, return the utility of the board.
        if terminal(board):
            return utility(board)
        v = -math.inf  # Initialize v to negative infinity to ensure any utility is larger.
        for action in actions(board):
            # Recursively call min_value for the next state and update v to the maximum value found.
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        # Base case for min_value: if board is in a terminal state, return the utility of the board.
        if terminal(board):
            return utility(board)
        v = math.inf  # Initialize v to infinity to ensure any utility is smaller.
        for action in actions(board):
            # Recursively call max_value for the next state and update v to the minimum value found.
            v = min(v, max_value(result(board, action)))
        return v

    # Determine the current player and calculate the optimal move based on maximizing or minimizing utility.
    if player(board) == X:
        # For player X (maximizing player), find the action that leads to the highest value.
        value, move = max((min_value(result(board, action)), action) for action in actions(board))
    else:
        # For the minimizing player, find the action that leads to the lowest value.
        value, move = min((max_value(result(board, action)), action) for action in actions(board))
    # Return the optimal move for the current player.
    return move

