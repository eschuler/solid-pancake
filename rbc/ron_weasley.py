print('Importing chess.engine')
import chess.engine
print('Done importing chess.engine')
import random
from reconchess import *

import os, sys

# TODO debug
import time

STOCKFISH_ENV_VAR = 'STOCKFISH_EXECUTABLE'

DEBUG_TURN_COUNT = 9999

class RonWeasley(Player):

    def __init__(self):
        '''
        Constructor
        '''

        # make sure stockfish environment variable exists
        if STOCKFISH_ENV_VAR not in os.environ:
            raise KeyError(
                'RonWeasley requires an environment variable called "{}" pointing to the Stockfish executable'.format(
                    STOCKFISH_ENV_VAR))

        # make sure there is actually a file
        stockfish_path = os.environ[STOCKFISH_ENV_VAR]
        if not os.path.exists(stockfish_path):
            raise ValueError('No stockfish executable found at "{}"'.format(stockfish_path))

        # initialize the stockfish engine
        print('Waiting to initialize Stockfish engine')
        #self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.engine = None
        #print('Done initializing Stockfish engine')
        print('Stockfish not initialized')


    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):

        self.first_turn = True
        self.turn_num = 1
        self.color = color
        self.board = board
        self.move_map = {}

        # freshness is within the range [0, 1]
        # with 1 being fresh and 0 being stale
        self.freshness = []
        for i in range(64):
            self.freshness.append(1)

        # tracks the number of moves that end within each square
        self.num_endpoints = [0 for x in range(63)]

        if self.color == chess.WHITE:
            print('I am Ron Weasley, playing as WHITE\n')
        else:
            print('I am Ron Weasley, playing as BLACK\n')

        print('{}\n'.format(self.board))

        self.print_current_player()

        print('Available moves for current player:')
        print('{}\n'.format(list(self.board.legal_moves)))

        #print(board.piece_at(0))
        #print(board.piece_at(16))
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(0)], chess.RANK_NAMES[chess.square_rank(sense_actions[0])]))


    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        #print('In handle_opponent_move_result()')
        #self.print_current_player()
        pass


    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> \
            Optional[Square]:

        #print('In choose_sense()')
        #self.print_current_player()

        # parse potential opponent moves for information
        self.start_points = []
        self.end_points = {}
        self.move_map = {}
        for move in self.board.legal_moves:
            start_point = move.from_square
            end_point = move.to_square

            # store the start and end points in lists
            if start_point not in self.start_points:
                self.start_points.append(start_point)

            # store the end points as a dict with # occurrences
            if end_point not in self.end_points:
                self.end_points[end_point] = 1
            else:
                self.end_points[end_point] += 1

            # initialize a list in the move map if needed
            if start_point not in self.move_map.keys():
                self.move_map[start_point] = [start_point]

            # store the move mapping
            if end_point not in self.move_map[start_point]:
                self.move_map[start_point].append(end_point)

        start_time = time.time()

        # TODO
        self.sense_choice = random.choice(sense_actions)

        # never choose a border square to sense - it reduces the number of squares you can see
        sense_idxs = sense_actions[9:15] + sense_actions[17:23] + sense_actions[25:31] + \
                sense_actions[33:39] + sense_actions[41:47] + sense_actions[49:54]
        sense_squares = [self.idx_to_space_name(x) for x in sense_idxs]

        # TODO
        if not self.turn_num <= DEBUG_TURN_COUNT:
            return self.sense_choice

        mid_time1 = time.time()

        # calculate a score for each square that indicates the viability for sensing there
        sense_scores = []
        for potential_sense_idx in sense_idxs:
            sense_score = self.score_sense_square(potential_sense_idx)
            sense_scores.append((potential_sense_idx, sense_score))

        mid_time2 = time.time()

        # sort the squares by their score to find the best ones to sense
        sense_scores = sorted(sense_scores, key=lambda score: score[1], reverse=True)

        # TODO DEBUG
        #print('Top 5 sense options: {}'.format(sense_scores[:5]))

        max_score = sense_scores[0][1]
        sense_options = []

        # gather all the squares with the max score
        for score in sense_scores:
            if score[1] == max_score:
                sense_options.append(score[0])
            else:
                break

        self.sense_choice = random.choice(sense_options)

        print('Best sense options ({}): {}'.format(max_score, sense_options))
        print('Sense choice: {}'.format(self.sense_choice))

        end_time = time.time()
        #print('Intermediate time (scoring squares): {}'.format(mid_time2 - mid_time1))
        print('Sense time taken: {}'.format(end_time - start_time))
        print()

        return self.sense_choice


    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        '''
        Handles the result of the sense action from the game engine

        :param sense_result: current status of the chosen sense grid
        :type sense_result: array of chess.Square
        '''

        #print('In handle_sense_result()')
        #self.print_current_player()

        new_board = self.board.copy()
        sense_grid = self.get_sense_grid(self.sense_choice)

        if self.turn_num <= DEBUG_TURN_COUNT:
            has_board_changed = False
            move_detected = False
            move_from_loc = None
            move_to_loc = None

            print('Sense result: {}\n'.format(sense_result))
            for space, piece in sense_result:
                current_piece = self.board.piece_at(space)

                if current_piece != piece:
                    has_board_changed = True

                if current_piece is None and piece is not None:
                    move_to_loc = space
                elif current_piece is not None and piece is None:
                    move_from_loc = space

                new_board.set_piece_at(space, piece)

            if has_board_changed:
                print('Sense has detected a board change!! {} to {}'.format(move_from_loc, move_to_loc))

                potential_moves = []
                if move_from_loc is not None and move_to_loc is not None:
                    potential_moves = [chess.Move(move_from_loc, move_to_loc)]
                elif move_from_loc is None:
                    for move in self.board.legal_moves:
                        if move.to_square == move_to_loc and new_board.piece_at(move_to_loc) == self.board.piece_at(move.from_square):
                            potential_moves.append(chess.Move(move.from_square, move_to_loc))
                elif move_to_loc is None:
                    for move in self.board.legal_moves:
                        if move.from_square == move_from_loc:
                            potential_moves.append(chess.Move(move_from_loc, move.to_square))

                print('Potential moves: {}\n'.format(potential_moves))

                if len(potential_moves) == 1:
                    move = potential_moves[0]
                    self.reset_freshness(sense_grid)
                    self.decrease_freshness(sense_grid)
                    self.board.push(chess.Move(move.from_square, move.to_square))
                    self.reset_freshness_for_move(move, self.board.piece_at(move.to_square))
                
                else:
                    if len(potential_moves) == 0:
                        print('No potential moves detected!')
                    else:
                        print('More than one potential move detected!')

                    self.reset_freshness(sense_grid)
                    self.decrease_freshness(sense_grid)

                    # decrease the freshness extra for any potential starting location
                    #for move in potential_moves:
                    #    self.decrease_freshness(move.from_square)

                    self.board.push(chess.Move.null())

                print('Updated board:\n{}\n'.format(self.board))
                print('Updated freshness:')
                self.print_freshness_array()

            else:
                print('No change detected!!\n')
                self.reset_freshness(sense_grid)
                self.decrease_freshness(sense_grid)
                self.board.push(chess.Move.null())

        self.first_turn = False
        self.turn_num += 1


    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        '''
        Chooses the chess move to perform

        :param move_actions:
        :param seconds_left:
        :return: a move (chess.Move) to perform
        '''

        print('In choose_move()')
        self.print_current_player()

        enemy_king_square = self.board.king(not self.color)

        # if we might be able to take the king, try to
        '''
        if enemy_king_square:

            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)

            # if there are any ally pieces that can take king, execute one of those moves
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()

                move = chess.Move(attacker_square, enemy_king_square)
                print('I am making the move {} -> {}\n'.format(move.from_square, move.to_square))
                return move
        '''

        move = random.choice(list(self.board.legal_moves))

        if self.turn_num <= DEBUG_TURN_COUNT:

            print('Available moves for current player:')
            print('{}\n'.format(list(self.board.legal_moves)))

            print('Chosen move: {} ({}->{})\n'.format(move, move.from_square, move.to_square))

        if move not in move_actions:
            print('Error!! Move not in available moves {}'.format(move_actions))
            move = random.choice(move_actions)
            print('New chosen move: {} ({}->{})\n'.format(move, move.from_square, move.to_square))

        return move 


    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        '''
        '''

        print('In handle_move_result()')
        self.print_current_player()

        if taken_move is None:
            print('Illegal move!!\n')

        else:
            self.board.push(chess.Move(taken_move.from_square, taken_move.to_square))

            print('Updated board:\n{}\n'.format(self.board))

            # reset the freshness of the squares along the piece's path
            self.reset_freshness_for_move(taken_move, self.board.piece_at(taken_move.to_square))


    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        pass


    def reset_freshness(self, sense_grid):
        '''
        Resets freshness for any square just sensed

        :param sense_grid: the 3x3 sense grid just seen
        :type sense_grid: an array of chess.Square (max length 9)
        '''
        for square_idx in sense_grid:
            self.freshness[square_idx] = 1


    def reset_freshness_for_move(self, move, piece):
        '''
        Resets freshness for any square along the path
        that your piece just moved

        :param move: the move that you just took
        :type move: chess.Move
        :param piece: the piece that was just moved
        :type piece: chess.Piece
        '''

        path = self.get_path(move, piece)

        for square_idx in path:
            self.freshness[square_idx] = 1


    def get_path(self, move, piece):
        '''
        Gets the squares in the path for a given move

        :param move: the move that you just took
        :type move: chess.Move
        :param piece: the piece that was just moved
        :type piece: chess.Piece
        :return: a list of squares in the path (list of ints)
        '''

        path = []

        start = move.from_square
        end = move.to_square
        
        #print('Determining path from {} to {} with piece {}'.format(start, end, piece))

        same_column = chess.square_file(start) == chess.square_file(end)
        same_row = chess.square_rank(start) == chess.square_rank(end)

        # knights jump over pieces so their path is only the start and end
        if piece.piece_type == chess.KNIGHT:
            #print('Knight')
            path = [start, end]

        # for non knight pieces the path is every square in between start and end
        else:

            # moving vertically
            if same_column:
                #print('Same column')
                step = 8

            # moving horizontally
            elif same_row:
                #print('Same row')
                step = 1

            # moving diagonally
            else:
                #print('Diagonal')
                step = 9

            # moving down to board
            if start > end:
                step = step * -1

            # determine the path
            for i in range(start, end + step, step):
                path.append(i)

        return path


    def decrease_freshness_for_square(self, square_idx, decrease_amount=0.1):
        '''
        Decrease freshness for a given square

        :param square_idx: the index of the square to change (0-63)
        :type square_idx: int
        :param decrease_amount: the amount to decrease the freshness (default 0.1)
        :type decrease_amount: float
        '''
        self.freshness[square_idx] -= decrease_amount


    def decrease_freshness(self, sense_grid):
        '''
        Decreases freshness for squares not in the sense grid and \
                for all squares that do not contain your own pieces

        :param sense_grid: the 3x3 sense grid just seen
        :type sense_grid: an array of chess.Square (max length 9)
        '''

        stale_points = []

        # determine the start and end points for the opponent's moves
        '''
        for move in self.board.legal_moves:
            start_point = move.from_square
            end_point = move.to_square
            if not self.is_piece_contained(start_point, sense_grid):
                if start_point not in stale_points and start_point not in sense_grid:
                    stale_points.append(start_point)
                if end_point not in stale_points and end_point not in sense_grid:
                    stale_points.append(end_point)

        # also decrease the freshness of any squares that are not 100% fresh
        # ("compound uncertainty")
        for square_idx in range(len(self.freshness)):
            if square_idx not in stale_points and self.freshness[square_idx] < 1:
                stale_points.append(square_idx)

        print('Decreasing freshness for {}'.format(sorted(stale_points)))

        # decrease the freshness for any potential endpoint
        for square_idx in stale_points:
            piece = self.board.piece_at(square_idx)

            # don't decrease freshness if your own piece is on the square
            if piece is None or piece.color != self.color:
                self.freshness[square_idx] -= 0.1
        '''

        for square_idx in range(len(self.freshness)):

            # don't decrease freshness if the square is in the sense grid
            if square_idx in sense_grid:
                continue

            piece = self.board.piece_at(square_idx)

            # don't decrease freshness if your own piece is on the square
            if piece is None or piece.color != self.color:
                self.freshness[square_idx] -= 0.1


    def print_freshness_array(self):
        '''
        Prints the freshness board to the console:
        '''
        for row_num in reversed(range(8)):
            row = [self.freshness[x] for x in range(row_num * 8, (row_num + 1) * 8)]
            print('{:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d}'.format(\
                int(row[0]*10), 
                int(row[1]*10), 
                int(row[2]*10), 
                int(row[3]*10), 
                int(row[4]*10), 
                int(row[5]*10), 
                int(row[6]*10), 
                int(row[7]*10))) 

        print()


    def are_boards_matching(self, board1, board2):
        '''
        Returns True if boards are matching

        :param board1: first board to compare
        :type board1: chess.Board
        :param board2: second board to compare
        :type board2: chess.Board
        :return: True if boards match; False otherwise
        '''
        for i in range(64):
            if board1.piece_at(i) != board2.piece_at(i):
                return False
        return True


    def idx_to_space_name(self, idx):
        '''
        Converts a square index (0-63) to the square string ('a1', ..., 'h8')

        :param idx: square index (0-63)
        :type idx: int
        :return: the square string
        '''
        return chess.FILE_NAMES[chess.square_file(idx)] + chess.RANK_NAMES[chess.square_rank(idx)]


    def get_sense_grid(self, sense_square):
        '''
        Returns an array of spaces contained within the 3x3 space surrounding a sense location

        :param sense_square: the square chosen for sensing
        :type sense_square: chess.Square (int enum)
        :return: an array of adjacent locations (up to 9 total)
        '''
        sense_zone = []

        # calculate column and row number on the chess board
        col_num = sense_square % 8
        row_num = int(sense_square / 8)

        if row_num > 0:
            # lower left corner
            if col_num > 0:
                sense_zone.append(sense_square - 9)

            # lower middle
            sense_zone.append(sense_square - 8)

            # lower right corner
            if col_num < 7:
                sense_zone.append(sense_square - 7)

        # middle row left 
        if col_num > 0:
            sense_zone.append(sense_square - 1)

        # sense square
        sense_zone.append(sense_square)

        # middle row right
        if col_num < 7:
            sense_zone.append(sense_square + 1)

        if row_num < 7:
            # top left corner
            if col_num > 0:
                sense_zone.append(sense_square + 7)

            # top middle
            sense_zone.append(sense_square + 8)

            # top right corner
            if col_num < 7:
                sense_zone.append(sense_square + 9)

        return sense_zone


    def score_sense_square(self, sense_square):
        '''
        Scores the potential of using the sense option on a given square

        :param sense_square: the square to test
        :type sense_square: int (0-63)
        :return: an integer score of the sense option (a higher integer is a better square to sense)
        '''
        sense_score = 0
        sense_grid = self.get_sense_grid(sense_square)
        
        #start_time = time.time()

        for square_idx in sense_grid:

            piece = self.board.piece_at(square_idx)

            # decrease score if the grid contains your own piece
            if piece is not None and piece.color == self.color:
                sense_score = sense_score - 1

            # increase score more if the square is less fresh
            else:
                sense_score = sense_score + (1 - self.freshness[square_idx])

            # increase the score based on the percentage of contained moves
            num_endpoints_in_grid = self.get_num_endpoints_in_grid(sense_grid)
            num_potential_moves = self.board.legal_moves.count()
            percent_contained = float(num_endpoints_in_grid) / float(num_potential_moves)
            sense_score = sense_score + percent_contained

        #end_time = time.time()

        #if self.turn_num <= DEBUG_TURN_COUNT:
        #    print('Time to score {}: {}'.format(sense_square, end_time - start_time))

        # TODO: incorporate probabilities of certain pieces in a given square?

        return sense_score


    def get_num_endpoints_in_grid(self, sense_grid):
        '''
        Determines the number of potential moves that end within a sense grid

        :param sense_grid: an array of squares forming a 3x3 sense grid
        :type sense_grid: an array of ints (max length 9)
        :return: the number of legal moves for the current player that end in the given sense grid
        '''
        num_endpoints = 0

        # iterate through the counter for each square (previously calculated)
        for square_idx in sense_grid:
            if square_idx in self.end_points.keys():
                num_endpoints += self.end_points[square_idx]

        return num_endpoints


    def is_piece_contained(self, piece_location, sense_grid):
        '''
        Returns True if current location "contains" a piece

        :param piece_location: grid location of the piece to tets
        :type piece_location: int
        :param sense_grid: 3x3 grid of squares being sensed
        :type sense_grid: list of ints (max length 9)
        :return: True if the given piece is contained by the \
                given sense grid
        '''

        contained = False

        # perform containment checks
        if piece_location in self.move_map.keys():
           
            # get all potential endpoints for the given piece
            # (includes the start location)
            potential_endpoints = self.move_map[piece_location]

            # check if the sense grid contains the piece's start location
            start_point_in_grid = piece_location in sense_grid

            all_end_points_in_grid = True
            all_but_one_end_points_in_grid = True

            # check how many end points are within the sense grid
            for end_point in potential_endpoints:

                # ignore the start location for this part
                if end_point == piece_location:
                    continue

                # endpoint outside the sense grid
                if end_point not in sense_grid:

                    # first endpoint outside the sense grid
                    if all_end_points_in_grid:
                        all_end_points_in_grid = False

                    # second endpoint outside the sense grid
                    elif all_but_one_end_points_in_grid:
                        all_but_one_end_points_in_grid = False
                        break

            # the piece is contained if all end points are within the sense grid
            # or if the piece's start location is within the sense grid and all
            # but one endpoint is within the sense grid
            contained = all_end_points_in_grid or (all_but_one_end_points_in_grid and start_point_in_grid)

        # if there are no legal moves for the given piece, it is contained
        else:
            contained = True

        return contained


    def print_current_player(self):
        '''
        Displays the current player to the console
        '''
        if (self.board.turn == chess.WHITE):
            print('Current player: WHITE\n')
        else:
            print('Current player: BLACK\n')


