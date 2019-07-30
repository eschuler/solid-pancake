import random
from reconchess import *

import sys

class SquareStruct:
    def __init__(self):
        self.possible_pieces = []   # ordered list of tuples
        self.staleness = 0
        self.changed_since_last_update = False

    def increase_staleness(self):
        '''
        Increases the staleness factor of a space
        '''

        # staleness is within the range [0, 1]
        # with 0 being fresh and 1 being stale

        # staleness should only increase if the square
        # is uncertain (i.e. multiple entries in possible_pieces)
        # so we need to track if possible_pieces has changed since
        # the last time this method was called
        pass


class RonWeasley(Player):
    def handle_game_start(self, color: Color, board: chess.Board):
        if color == chess.WHITE:
            print('I am Ron Weasley, playing as WHITE')
        else:
            print('I am Ron Weasley, playing as BLACK')

        self.first_turn = True

        self.current_board = []
        for i in range(63):
            self.current_board

        print(board)
        print(board.piece_at(0))
        print(board.piece_at(16))
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(0)], chess.RANK_NAMES[chess.square_rank(sense_actions[0])]))

    def handle_opponent_move_result(self, captured_my_piece: bool, capture_square: Optional[Square]):
        pass

    def choose_sense(self, sense_actions: List[Square], move_actions: List[chess.Move], seconds_left: float) -> \
            Optional[Square]:

        # never choose a border square to sense - it reduces the number of squares you can see
        sense_actions = sense_actions[9:15] + sense_actions[17:23] + sense_actions[25:31] + \
                sense_actions[33:39] + sense_actions[41:47] + sense_actions[49:54]
        sense_squares = [self.idx_to_space_name(x) for x in sense_actions]

        #print(sense_actions)
        if self.first_turn:
            print(sense_squares)
            print(move_actions)
            self.first_turn = False
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(sense_actions[1])], chess.RANK_NAMES[chess.square_rank(sense_actions[1])]))

        return random.choice(sense_actions)

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        pass

    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        return random.choice(move_actions + [None])

    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        pass

    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        pass

    def idx_to_space_name(self, idx):
        '''
        Converts a square index (0-63) to the square string ('a1', ..., 'h8')

        :param idx: square index (0-63)
        :type idx: int
        :return: the square string
        '''
        return chess.FILE_NAMES[chess.square_file(idx)] + chess.RANK_NAMES[chess.square_rank(idx)]


    def get_sense_square(self, sense_square):
        '''
        Returns an array of spaces contained within the 3x3 space surrounding a sense location

        :param sense_square: the square chosen for sensing
        :type sense_square: chess.Square (int enum)
        :return: an array of adjacent locations (up to 9 total)
        '''
        sense_


    def is_piece_contained(self):
        '''
        Returns True if current location 
        '''
        return True




