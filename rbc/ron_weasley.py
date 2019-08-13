import random
from reconchess import *

import os, sys

# TODO debug
import time

class RonWeasley(Player):

    def __init__(self):
        '''
        Constructor
        '''

        '''
        # make sure stockfish environment variable exists
        print(os.environ)
        if STOCKFISH_ENV_VAR not in os.environ:
            raise KeyError(
                'TroutBot requires an environment variable called "{}" pointing to the Stockfish executable'.format(
                    STOCKFISH_ENV_VAR))

        # make sure there is actually a file
        stockfish_path = os.environ[STOCKFISH_ENV_VAR]
        if not os.path.exists(stockfish_path):
            raise ValueError('No stockfish executable found at "{}"'.format(stockfish_path))

        # initialize the stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        '''
        pass


    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):

        self.first_turn = True
        self.color = color
        self.board = board

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

        if (board.turn == chess.WHITE):
            print('Current player: WHITE\n')
        else:
            print('Current player: BLACK\n')

        print('Available moves for current player:')
        #for move in board.legal_moves:
        #    print(move)
        print(list(self.board.legal_moves))
        print()
        print(self.board.move_stack)
        print()

        #print(board.piece_at(0))
        #print(board.piece_at(16))
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(0)], chess.RANK_NAMES[chess.square_rank(sense_actions[0])]))


    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        pass


    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> \
            Optional[Square]:

        start_time = time.time()

        # TODO
        self.sense_choice = random.choice(sense_actions)

        # never choose a border square to sense - it reduces the number of squares you can see
        sense_idxs = sense_actions[9:15] + sense_actions[17:23] + sense_actions[25:31] + \
                sense_actions[33:39] + sense_actions[41:47] + sense_actions[49:54]
        sense_squares = [self.idx_to_space_name(x) for x in sense_idxs]

        # TODO
        if not self.first_turn:
            return self.sense_choice

        # calculate the number of legal moves that end within each square
        self.num_endpoints = []
        for square_idx in range(64):
            self.num_endpoints.append(self.get_num_endpoints_in_square(square_idx))

        mid_time1 = time.time()

        # calculate a score for each square that indicates the viability for sensing there
        sense_scores = []
        for potential_sense_idx in sense_idxs:
            sense_score = self.score_sense_square(potential_sense_idx)
            sense_scores.append((potential_sense_idx, sense_score))

        mid_time2 = time.time()

        # sort the squares by their score to find the best ones to sense
        sense_scores = sorted(sense_scores, key=lambda score: score[1], reverse=True)

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

        new_board = self.board.copy()
        sense_grid = self.get_sense_grid(self.sense_choice)

        if self.first_turn:
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
                print('Sense has detected a board change!!')

                potential_moves = []
                if move_from_loc is None:
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
                    self.board.push(chess.Move(move.from_square, move.to_square))
                    self.reset_freshness(sense_grid)
                    print('Updated board:\n{}\n'.format(self.board))
                
                else:
                    print('More than one potential move detected!!')
                    print('Updated board:\n{}\n'.format(new_board))

            else:
                print('No change detected!!\n')
                self.reset_freshness(sense_grid)
                self.decrease_freshness(sense_grid)

            #self.first_turn = False


    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        return random.choice(move_actions + [None])


    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        pass


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


    def decrease_freshness(self, sense_grid):
        '''
        Decreases freshness for all squares not in the sense grid and \
                for all squares that do not contain your own pieces

        :param sense_grid: the 3x3 sense grid just seen
        :type sense_grid: an array of chess.Square (max length 9)
        '''

        for square_idx in range(64):
            if square_idx not in sense_grid:
                piece = self.board.piece_at(square_idx)
                if piece is None or piece.color != self.color:
                    self.freshness[square_idx] -= 0.1

        if self.first_turn:
            print('New freshness array: {}\n'.format(self.freshness))


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

            # increase score depending on how fresh/stale the square is
            elif self.freshness[square_idx] < 0.25:
                sense_score = sense_score + 2
            elif self.freshness[square_idx] < 0.5:
                sense_score = sense_score + 1
            elif self.freshness[square_idx] < 0.75:
                sense_score = sense_score + 0.5

            # increase the score based on the percentage of contained moves
            num_endpoints_in_grid = self.get_num_endpoints_in_grid(sense_grid)
            num_potential_moves = self.board.legal_moves.count()
            percent_contained = float(num_endpoints_in_grid) / float(num_potential_moves)
            sense_score = sense_score + percent_contained

        #end_time = time.time()

        #if self.first_turn:
        #    print('Time to score {}: {}'.format(sense_square, end_time - start_time))

        # TODO: incorporate probabilities of certain pieces in a given square?

        return sense_score


    def get_num_endpoints_in_square(self, square_idx):
        '''
        Determines the number of potential moves that end within a square

        :param square_idx: index of the square to check
        :type square_idx: int (0-63)
        :return: the number of legal moves for the current player that end in the given square
        '''
        num_endpoints = 0

        # iterate through all legal moves for the current player
        for move in self.board.legal_moves:

            # if the move ends in the given square, increase the counter
            if move.to_square == square_idx:
                num_endpoints = num_endpoints + 1

        return num_endpoints


    def get_num_endpoints_in_grid(self, sense_grid):
        '''
        Determines the number of potential moves that end within a sense grid

        :param sense_grid: an array of squares forming a 3x3 sense grid
        :type sense_grid: an array of maximum length 9
        :return: the number of legal moves for the current player that end in the given sense grid
        '''
        num_endpoints = 0

        # iterate through the counter for each square (previously calculated)
        for square_idx in sense_grid:
            num_endpoints = num_endpoints + self.get_num_endpoints_in_square(square_idx)

        return num_endpoints


    def is_piece_contained(self):
        '''
        Returns True if current location 
        '''
        return True




