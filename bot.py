from itertools import combinations, product
from random import choice

class TicTacToeBot:
    # Change this to "False" once you start implementing your bot
    isNew = False

    def __init__(self, config):
        self.player = config['player']
        if self.player == "x":
            self.bool = True
        elif self.player == "o":
            self.bool = False
        else:
            raise ValueError("player must be x or o")
        self.win_taunts = [
            "WOOHOO! I WIN!",
            "winner winner chicken dinner",
            "good game",
            "i can see you made a mistake. it's ok, we all do sometimes."
        ]
        self.loose_taunts = [
            "dang it",
            "welp, i made a mistake."
        ]
        self.draw_taunts = [
            "i guess a draw is ok",
            "if you're smart this will be a draw",
            "draw draw draw draw draw",
            "let's call it a draw, ok?"
        ]

    def can_win(self,my_spots,open_spots):
        """
        Determines if a player can win when their markers are at particular spots

        Parameters:
            my_spots: list
                coordinates of the player's markers
            open_spots: list
                coordinates of the open spots
        Returns
            can_win: bool
                indicates whether the player can win
            move: tuple or None
                Spot that would make a player win if possible.
                Otherwise, returns None
        """
        sides_sum = {1,3}
        def is_side(spot):
            return sum(spot) in sides_sum

        bad_triples = [ { (0,0), (1,2), (2,1) },
                        { (0,2), (1,0), (2,1) },
                        { (2,0), (0,1), (1,2) },
                        { (2,2), (0,1), (1,0) } ]
        
        for pair in combinations(my_spots,2):
            # find the complementary spot
            complement = ( -(pair[0][0] + pair[1][0]) % 3, -(pair[0][1] + pair[1][1]) % 3 )
            # if complementary spot filled, try next pair
            if complement not in open_spots:
                continue
            # if two spots are adjacent sides, move on
            if {pair[0],pair[1],complement} in bad_triples:
                continue
            else:
                return True, complement
            
        return False, None

    def get_curr_outcome(self,board,curr,level=0,verbose=False):
        """recursively solves tic tac toe"""
        # find open spots
        open_spots = []
        curr_spots = []
        other_spots = []
        for rownum,row in enumerate(board):
            for colnum, entry in enumerate(row):
                if entry == 'empty':
                    open_spots.append((rownum,colnum))
                elif entry == curr:
                    curr_spots.append((rownum,colnum))
                else:
                    other_spots.append((rownum,colnum))
        assert len(open_spots) + len(curr_spots) + len(other_spots) == 9

        # if current player can win, they do
        curr_can_win,winningmove = self.can_win(curr_spots,open_spots)
        if curr_can_win:
            # win by choosing winning move
            return 1, winningmove
        # if there's only one spot left, there's a draw
        elif len(open_spots) == 1:
            # draw by moving in only remaining open spot
            return 0, open_spots[0]
        # if the current player can't immediately win

        # what would the other player's outcome and move be if I made each move?
        currwin = []
        currdraw = []
        currloose = []
        for move in open_spots:
            new_board = [[entry for entry in row] for row in board]
            new_board[move[0]][move[1]] = curr
            if curr == "x":
                others_outcome = self.get_curr_outcome(new_board,"o",level=level+1)[0]
            elif curr == "o":
                others_outcome = self.get_curr_outcome(new_board,"x",level=level+1)[0]
            if others_outcome == 1:
                currloose.append(move)
            elif others_outcome == 0:
                currdraw.append(move)
            elif others_outcome == -1:
                currwin.append(move)
            else: 
                raise ValueError(f"other's outcome is {others_outcome}") 
        if level == 0 and verbose:
            print("win moves",currwin,"draw moves",currdraw,"loose moves",currloose,sep='\n')
        if len(currwin) > 0:
            #curr picks a winning move if possible
            return 1, choice(currwin)
        elif len(currdraw) > 0:
            #curr picks a draw move
            return 0, choice(currdraw)
        elif len(currloose) > 0:
            #curr looses
            return -1, choice(currloose)
        else:
            raise ValueError(f"current possible moves are \ncurrwin {currwin}\ncurrdraw {currdraw}\ncurrloose{currloose}")

    def move(self, board):
        outcome,move = self.get_curr_outcome(board,curr=self.player,verbose=True)
        # if outcome == 1:
        #     print(choice(self.win_taunts))
        # if outcome == 0:
        #     print(choice(self.draw_taunts))
        # if outcome == -1:
        #     print(choice(self.loose_taunts))
        return {"x": move[0], "y": move[1]}