import random
from reconchess import *

import sys

class RonWeasley(Player):
    def handle_game_start(self, color: Color, board: chess.Board, opponent_name: str):

        self.first_turn = True
        self.color = color
        self.board = board

        # freshness is within the range [0, 1]
        # with 1 being fresh and 0 being stale
        self.freshness = []
        for i in range(64):
            self.freshness.append(1)

        if self.color == chess.WHITE:
            print('I am Ron Weasley, playing as WHITE\n')
        else:
            print('I am Ron Weasley, playing as BLACK\n')

        print('{}\n'.format(self.board))
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece.color == self.color:
                print('{}: {} - my piece!'.format(i, piece))
            else:
                print('{}: {}'.format(i, piece))

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

        # never choose a border square to sense - it reduces the number of squares you can see
        sense_actions = sense_actions[9:15] + sense_actions[17:23] + sense_actions[25:31] + \
                sense_actions[33:39] + sense_actions[41:47] + sense_actions[49:54]
        sense_squares = [self.idx_to_space_name(x) for x in sense_actions]

        if self.first_turn:
            #print('Sense squares = {}'.format(sense_squares))
            print('Available moves for me:\n{}\n'.format(move_actions))
        #print('{}{}'.format(chess.FILE_NAMES[chess.square_file(sense_actions[1])], chess.RANK_NAMES[chess.square_rank(sense_actions[1])]))

        if self.first_turn:
            return 17
        else:
            return random.choice(sense_actions)


    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]):
        if self.first_turn:
            print('Sense result: {}\n'.format(sense_result))
            for space, piece in sense_result:
                self.board.set_piece_at(space, piece)
            print('Updated board:\n{}\n'.format(self.board))
            self.first_turn = False


    def choose_move(self, move_actions: List[chess.Move], seconds_left: float) -> Optional[chess.Move]:
        return random.choice(move_actions + [None])


    def handle_move_result(self, requested_move: Optional[chess.Move], taken_move: Optional[chess.Move],
                           captured_opponent_piece: bool, capture_square: Optional[Square]):
        pass


    def handle_game_end(self, winner_color: Optional[Color], win_reason: Optional[WinReason],
                        game_history: GameHistory):
        pass


    def decrease_freshness(self):
        '''
        '''
        pass


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


    def get_sense_square(self, sense_square):
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


    def is_piece_contained(self):
        '''
        Returns True if current location 
        '''
        return True




