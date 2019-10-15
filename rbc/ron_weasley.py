import chess.engine
import random
from reconchess import *

import os, sys

# TODO debug
import logging, time

STOCKFISH_ENV_VAR = 'STOCKFISH_EXECUTABLE'

DEBUG_TURN_COUNT = 1 # 9999

class RonWeasley(Player):

    def __init__(self):
        '''
        Constructor
        '''

        #'''
        # trout bot

        self.board = None
        self.color = None
        self.my_piece_captured_square = None

        # make sure stockfish environment variable exists
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

        #'''

        # define values to rank potential captures
        self.capture_value = {}
        self.capture_value[chess.KING]   = 9999
        self.capture_value[chess.QUEEN]  = 9
        self.capture_value[chess.ROOK]   = 7
        self.capture_value[chess.BISHOP] = 3
        self.capture_value[chess.KNIGHT] = 3
        self.capture_value[chess.PAWN]   = 1

        logging.basicConfig(filename='ron_weasley.log', format='%(levelname)-10s%(message)s', level=logging.INFO)
        logging.info("Let's play chess!")


    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):
        '''
        Handles game start

        :param color: the color of this player's pieces
        :type color: chess.Color
        :param board: the initial state of the board
        :type board: chess.Board
        :param opponent_name: this player's opponent's name
        :type opponent_name: str
        '''

        self.board = board
        self.color = color
        self.my_piece_captured_square = None

        self.first_turn = True
        self.turn_num = 1
        self.move_map = {}

        # freshness is within the range [0, 1]
        # with 1 being fresh and 0 being stale
        self.freshness = []
        for i in range(64):
            self.freshness.append(1)

        # tracks the number of moves that end within each square
        self.num_endpoints = [0 for x in range(63)]

        if self.color == chess.WHITE:
            logging.info('I am Ron Weasley, playing as WHITE\n')
        else:
            logging.info('I am Ron Weasley, playing as BLACK\n')

        logging.info('Starting board:\n{}\n'.format(self.board))

        self.log_freshness_array()

        # create all the possible sense grids and store them for quick access
        self.store_sense_grids()

        '''
        #self.board.set_piece_at(24, chess.Piece(chess.KNIGHT, chess.WHITE))
        #print('{}\n'.format(self.board))
        #print(self.print_current_player())

        print('Available moves for current player:')
        print('{}\n'.format(list(self.board.legal_moves)))

        #print(board.piece_at(0))
        #print(board.piece_at(16))
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(0)], chess.RANK_NAMES[chess.square_rank(sense_actions[0])]))
        '''


    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        '''
        '''

        #logging.info('Handling opponent move result')

        '''
        # trout bot

        # if the opponent captured our piece, remove it from our board.
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            self.board.remove_piece_at(capture_square)

        '''


        #'''
        #self.print_current_player()

        # if the opponent captured our piece, remove it from our board.
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            logging.info('My piece was captured! {} at {}'.format(self.board.piece_at(capture_square), capture_square)) 
            self.board.remove_piece_at(capture_square)
            logging.info('Updated board:\n{}\n'.format(self.board))

            # TODO check what pieces might have been the attacker
            self.freshness[capture_square] = 0
        #'''


    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> \
            Optional[Square]:

        #logging.info('Choosing sense')
        #self.print_current_player()

        '''
        # trout bot

        # if our piece was just captured, sense where it was captured
        if self.my_piece_captured_square:
            sense_choice = self.my_piece_captured_square
            logging.info('Sense choice: {}'.format(sense_choice))
            return sense_choice

        self.sense_choice = random.choice(sense_actions)
        logging.info('Sense choice: {}'.format(sense_choice))
        '''

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

        # never choose a border square to sense - it reduces the number of squares you can see
        sense_idxs = sense_actions[9:15] + sense_actions[17:23] + sense_actions[25:31] + \
                sense_actions[33:39] + sense_actions[41:47] + sense_actions[49:54]
        sense_squares = [self.idx_to_space_name(x) for x in sense_idxs]

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
        
        logging.info('Best sense options ({}): {}'.format(max_score, sense_options))
        logging.info('Sense choice: {}'.format(self.sense_choice))

        end_time = time.time()
        #logging.info('Intermediate time (scoring squares): {}'.format(mid_time2 - mid_time1))
        #logging.info('Sense time taken: {}'.format(end_time - start_time))

        #logging.info('')

        return self.sense_choice


    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        '''
        Handles the result of the sense action from the game engine

        :param sense_result: current status of the chosen sense grid
        :type sense_result: array of chess.Square
        '''

        #logging.info('Handling sense result')
        #self.print_current_player()

        new_board = self.board.copy()

        sense_result = sorted(sense_result, key=lambda score: score[0])
        printable_sense_result = []
        for x in sense_result:
            if x[1] is None:
                printable_sense_result.append('_')
            else:
                printable_sense_result.append(x[1].symbol())

        str = 'Sense result:\n'
        str += '{:<2s}{:<2s}{:<2s}\n'.format(printable_sense_result[6], printable_sense_result[7], printable_sense_result[8])
        str += '{:<2s}{:<2s}{:<2s}\n'.format(printable_sense_result[3], printable_sense_result[4], printable_sense_result[5])
        str += '{:<2s}{:<2s}{:<2s}\n'.format(printable_sense_result[0], printable_sense_result[1], printable_sense_result[2])
        logging.info(str)

        sense_grid = [x[0] for x in sense_result]

        has_board_changed = False
        move_detected = False
        move_from_loc = None
        move_to_loc = None

        changed_squares = []

        # TODO: can detect multiple pieces moving with a sense
        # example:
        # sense 19 early in the game, detect both:
        #   pawn moving from 9->10
        #   queen moving from 3->9
        # need to detect both of those moves and react accordingly

        # determine what changed before and after the sense
        for space, piece in sense_result:
            current_piece = self.board.piece_at(space)

            if current_piece != piece:
                has_board_changed = True

            if current_piece is None and piece is not None:
                move_to_loc = space
            elif current_piece is not None and piece is None:
                move_from_loc = space

            new_board.set_piece_at(space, piece)
            #changed_squares.append((space, piece))

        if has_board_changed and move_from_loc is not None and move_to_loc is not None:
            from_piece = self.board.piece_at(move_from_loc)
            to_piece = self.board.piece_at(move_to_loc)
            
            if from_piece is not None and to_piece is not None and from_piece.piece_type != to_piece.piece_type:
                logging.info('Detected two moves in one sense! {} at {} is gone and {} at {} is new'.format(
                    self.board.piece_at(move_from_loc), move_from_loc, self.board.piece_at(move_to_loc), move_to_loc))

        if has_board_changed:
            logging.info('Sense has detected a board change! {} -> {}'.format(move_from_loc, move_to_loc))
            #logging.info('Sense has detected a board change! {}'.format(changed_squares)

            potential_moves = []

            if move_from_loc is not None and move_to_loc is not None:
                potential_moves = [chess.Move(move_from_loc, move_to_loc)]
            elif move_from_loc is None:
                for move in self.board.legal_moves:
                    if move.to_square == move_to_loc and new_board.piece_at(move_to_loc) == self.board.piece_at(move.from_square):
                        potential_moves.append(chess.Move(move.from_square, move_to_loc))
            elif move_to_loc is None:
                for move in self.board.legal_moves:
                    if move.from_square == move_from_loc and move.to_square not in sense_result:
                        potential_moves.append(chess.Move(move_from_loc, move.to_square))

            logging.info('Potential moves: {}\n'.format(potential_moves))

            if len(potential_moves) == 1:
                move = potential_moves[0]
                self.decrease_freshness(sense_grid)

                potential_move = chess.Move(move.from_square, move.to_square)

                #if potential_move in self.board.legal_moves:
                self.board.set_piece_at(move.to_square, self.board.piece_at(move.from_square))
                self.board.remove_piece_at(move.from_square)
                #self.board.push(potential_move)

                #else:
                #    self.board.push(chess.Move.null())

                self.reset_freshness_for_move(move, self.board.piece_at(move.to_square))

            else:
                if len(potential_moves) == 0:
                    logging.info('No potential moves detected!')
                else:
                    logging.info('More than one potential move detected!')

                self.decrease_freshness(sense_grid)

                # decrease the freshness extra for any potential starting location
                for move in potential_moves:
                    self.decrease_freshness_for_square(move.from_square)

                # update the spaces in the sense result given the information we know
                for space, piece in sense_result:
                    current_piece = self.board.piece_at(space)

                    if current_piece != piece:
                        self.board.set_piece_at(space, piece)

                '''
                # TODO search for the piece type that appeared in the sense square
                # and set their freshness values to 0

                #self.board.push(chess.Move.null())
                '''

            self.log_freshness_array()

        # no board changes
        else:
            logging.info('No detected board changes\n')
            self.decrease_freshness(sense_grid)
            

        #'''
        # trout bot

        # add the pieces in the sense result to our board
        for square, piece in sense_result:
            self.board.set_piece_at(square, piece)

        if has_board_changed:
            logging.info('Updated board:\n{}\n'.format(self.board))
            
        self.board.push(chess.Move.null())

        return
        #'''

        '''
        if has_board_changed:

        else:
            print('No change detected!!\n')
            self.reset_freshness(sense_grid)
            self.decrease_freshness(sense_grid)
            #self.board.push(chess.Move.null())

        self.board.push(chess.Move.null())
        self.first_turn = False
        self.turn_num += 1
        '''


    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        '''
        Chooses the chess move to perform

        :param move_actions: list of possible moves for this player
        :type move_actions: list of chess.Move
        :param seconds_left: seconds left to make a move
        :type seconds_left: float
        :return: a move (chess.Move) to perform
        '''

        # prevents crashes TODO may be fixed with removal of trout bot code
        if self.board.turn != self.color:
            return None

        #logging.info('Choosing move')
        #self.print_current_player()

        # determine which pieces can be captured 
        attacks = []

        for attacked_square in range(64):
            piece = self.board.piece_at(attacked_square)

            # only concerned with squares with enemy pieces
            if piece is not None and piece.color is not self.color:

                for attack in self.board.attackers(self.color, attacked_square):
                    attacks.append((attack, attacked_square, self.capture_value[piece.piece_type]))

        # sort attacks by the value of the captured piece
        attacks = sorted(attacks, key=lambda x: x[2], reverse=True)

        if len(attacks) > 0:
            logging.info('Potential attacks:')
            for attack in attacks:
                logging.info('\t{} -> {} ({})'.format(attack[0], attack[1], attack[2]))

        # if we might be able to take the king, try to
        '''
        if attacks[0][2] == self.capture_value[chess.KING]:
            return chess.Move(attacks[0][0], attacks[0][1])
        '''

        #'''
        enemy_king_square = self.board.king(not self.color)
        if enemy_king_square:
            # if there are any ally pieces that can take king, execute one of those moves
            enemy_king_attackers = self.board.attackers(self.color, enemy_king_square)
            if enemy_king_attackers:
                attacker_square = enemy_king_attackers.pop()
                return chess.Move(attacker_square, enemy_king_square)
        #'''

        # otherwise, try to move with the stockfish chess engine
        try:
            self.board.turn = self.color
            self.board.clear_stack()
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))

            logging.info('Chosen move: {} -> {}'.format(result.move.from_square, result.move.to_square))

            # check if the proposed move

            return result.move

        except (chess.engine.EngineError, chess.engine.EngineTerminatedError) as e:
            logging.error('Engine bad state at "{}"'.format(self.board.fen()))

        #logging.info('')

        # if all else fails, do a random move
        return random.choice(move_actions)


    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        '''
        Handles the result of this player's move 

        :param requested_move: the move returned by this player in choose_move()
        :type requested_move: chess.Move
        :param taken_move: the move actually performed by the player (may be different if this \
                player's piece ran into the opponent's piece by accident)
        :type taken_move: chess.Move
        :param captured_opponent_piece: the piece the opponent captured (if a capture occurred)
        :type captured_opponent_piece: bool
        ;param capture_square: the square where the opponent captured this player's piece (if a capture occurred)
        :type capture_square: chess.Square
        '''

        #logging.info('Handling move result')
        #self.print_current_player()

        # TODO compare taken_move to requested_move

        # if a move was executed, apply it to our board
        if taken_move is not None:
            #self.board.set_piece_at(taken_move.to_square, self.board.piece_at(taken_move.from_square))
            #self.remove_piece_at(taken_move.from_square)
            #self.board.push(chess.Move.null())

            logging.info('Taken move: {} -> {}'.format(taken_move.from_square, taken_move.to_square))

            if captured_opponent_piece:
                piece_captured = self.board.piece_at(capture_square)

            self.board.push(taken_move)

            if captured_opponent_piece:
                logging.info('Captured {} with {} at {}!!'.format(piece_captured, self.board.piece_at(capture_square), capture_square))

            logging.info('Updated board:\n{}\n'.format(self.board))

            # reset the freshness of the squares along the piece's path
            self.reset_freshness_for_move(taken_move, self.board.piece_at(taken_move.to_square))

            self.log_freshness_array()

        else:
            logging.error('Illegal move! {} -> {}'.format(requested_move.from_square, requested_move.to_square))

            requested_move_piece = self.board.piece_at(requested_move.from_square).piece_type

            # pawn tried to capture diagonally but there was no piece there
            if requested_move_piece == chess.PAWN:
                self.freshness[self.board.piece_at(requested_move.to_square)] = 0
                logging.info('Tried to move a pawn to {s}. Reset freshness at {s}'.format(s=requested_move.to_square()))

            self.board.push(chess.Move.null())

        #logging.info('')


    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        try:
            # if the engine is already terminated then this call will throw an exception
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass


    def reset_freshness(self, sense_grid):
        '''
        Resets freshness for any square just sensed

        :param sense_grid: the 3x3 sense grid just seen
        :type sense_grid: an array of chess.Square (max length 9)
        '''
        #logging.info('Resetting freshness for sense grid: {}'.format(sense_grid))

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

        #logging.info('Path: {}'.format(path))

        for square_idx in path:
            if square_idx > len(self.freshness):
                logging.error('Out of bounds for freshness array! {}'.format(square_idx))
            else:
                if square_idx >= len(self.freshness):
                    logging.error('Out of bounds for freshness array! {}'.format(square_idx))
                else:
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
        
        #logging.info('Determining path from {} to {} with piece {}'.format(start, end, piece))

        same_column = chess.square_file(start) == chess.square_file(end)
        same_row = chess.square_rank(start) == chess.square_rank(end)

        # knights jump over pieces so their path is only the start and end
        if piece.piece_type == chess.KNIGHT:
            #logging.info('Knight')
            path = [start, end]

        # for non knight pieces the path is every square in between start and end
        else:

            # moving vertically
            if same_column:
                #logging.info('Same column')
                step = 8

            # moving horizontally
            elif same_row:
                #logging.info('Same row')
                step = 1

            # moving diagonally
            else:
                #logging.info('Diagonal')
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

        if self.freshness[square_idx] < 0:
            self.freshness[square_idx] = 0


    def decrease_freshness(self, sense_grid):
        '''
        Decreases freshness for squares not in the sense grid and \
                for all squares that do not contain your own pieces

        :param sense_grid: the 3x3 sense grid just seen
        :type sense_grid: an array of chess.Square (max length 9)
        '''

        stale_points = []

        # determine the start and end points for the opponent's moves
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

        #logging.info('Decreasing freshness for {}'.format(sorted(stale_points)))

        '''
        # decrease the freshness for any potential endpoint
        for square_idx in stale_points:
            piece = self.board.piece_at(square_idx)

            # don't decrease freshness if your own piece is on the square
            if piece is None or piece.color != self.color:
                self.freshness[square_idx] -= 0.1
        '''

        # TODO don't decrease freshness if a piece can't be moved (totally blocked)
        # the next turn, any blocked pieces will have a freshness less than one
        # and at that point the previously blocked piece should have its
        # freshness decreased

        for square_idx in range(len(self.freshness)):

            # don't decrease freshness if the square is in the sense grid
            if square_idx in sense_grid:
                continue

            piece = self.board.piece_at(square_idx)

            # don't decrease freshness if your own piece is on the square
            if piece is None or piece.color != self.color:
                self.freshness[square_idx] -= 0.1

                if self.freshness[square_idx] < 0:
                    self.freshness[square_idx] = 0

        self.reset_freshness(sense_grid)

        self.log_freshness_array()


    def log_freshness_array(self):
        '''
        Prints the freshness board to the console:
        '''

        str = 'Freshness array:\n'

        for row_num in reversed(range(8)):
            row = [self.freshness[x] for x in range(row_num * 8, (row_num + 1) * 8)]
            str += '{:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d} {:<3d}\n'.format(\
                int(row[0]*10), 
                int(row[1]*10), 
                int(row[2]*10), 
                int(row[3]*10), 
                int(row[4]*10), 
                int(row[5]*10), 
                int(row[6]*10), 
                int(row[7]*10)) 

        #logging.info(str)


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


    def store_sense_grids(self):
        '''
        Creates all sense grids and stores them in a map 
        for faster access time
        '''

        self.sense_grids = []

        # get the sense grid for each possible sense square on the board
        for center_square in range(64):
            self.sense_grids.append(self.get_sense_grid(center_square))
            #logging.info('Sense grid for center {}: {}'.format(center_square, self.sense_grids[center_square]))


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

        #logging.info('Forming sense grid for {} (col {}, row {})'.format(sense_square, col_num, row_num))

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

        #logging.info('Sense grid: {}'.format(sense_zone))

        return sense_zone


    def score_sense_square(self, sense_square):
        '''
        Scores the potential of using the sense option on a given square

        :param sense_square: the square to test
        :type sense_square: int (0-63)
        :return: an integer score of the sense option (a higher integer is a better square to sense)
        '''
        sense_score = 0
        sense_grid = self.sense_grids[sense_square]
        
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

            if num_potential_moves == 0:
                percent_contained = 0
            else:
                percent_contained = float(num_endpoints_in_grid) / float(num_potential_moves)
            
            sense_score = sense_score + percent_contained

        #end_time = time.time()

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
            logging.info('Current player: WHITE')
        else:
            logging.info('Current player: BLACK')


