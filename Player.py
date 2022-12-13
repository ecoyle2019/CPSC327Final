
import random


class Player:
    def __init__(self, name, side=None, pieces=None):
        self.name = name
        self.side = side
        self.pieces = pieces
        self.type = "Human"
    def get_move(self):
        pass

class RandomPlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.type = "Random"
    
    def get_move(self, possible_moves):
        return random.choice(possible_moves)


class HeuristicPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Heuristic"


    # def get_possible_moves(self, worker):
    #     poss_rows = [worker.row - 1, worker.row, worker.row + 1]
    #     poss_cols = [worker.col - 1, worker.col, worker.col + 1]


    #     poss_moves = list(itertools.product(poss_rows, poss_cols))

    #     for m in poss_moves:
    #         if m[0] > 5 or m[1] > 5:
    #             poss_moves.remove(m)

    #     return poss_moves
    
    def get_move(self, possible_moves):
        # return self.find_best_move(possible_moves)

        # directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        # possible_moves = self.game.get_sub_scores() # get sub-scores for all possible moves
        # move = self.game.players[self.game.turn % 2].find_best_move(possible_moves)
        # worker_to_move = move[0]
        # new_row = move[1][0]
        # new_col = move[1][1]

        # self.game.select_worker(worker_to_move.name)
        # worker_to_move.move_to(new_row, new_col)
        # build_dir = random.choice(directions)
        
        # worker = best_move[0]
        best_move = self.find_best_move(possible_moves)
        worker = best_move[0]
        orig_row = worker.row
        orig_col = worker.col

        new_row = best_move[1][0]
        new_col = best_move[1][1]

        # (1, 3) -> (2, 2): diff = -1, 1
        row_diff = orig_row - new_row
        col_diff = orig_col - new_col

        if row_diff == 1 and col_diff == -1:
            return 'sw'
        elif row_diff == 1 and col_diff == 1:
            return 'se'
        elif row_diff == -1 and col_diff == -1:
            return 'nw'
        elif row_diff == -1 and col_diff == 1:
            return 'ne'
        elif row_diff == 0 and col_diff == -1:
            return 'w'
        elif row_diff == 0 and col_diff == 1:
            return 'e'
        elif row_diff == 1 and col_diff == 0:
            return 's'
        elif row_diff == -1 and col_diff == 0:
            return 'n'
        

    

    def find_best_move(self, possible_moves):
        '''Find move with highest heuristic score. Ties are decided randomly'''

       
        # c1, c2, c3 = 3, 2, 1 # score weights

        w1_moves = possible_moves[0]
        w2_moves = possible_moves[1]

        # if max w1_moves > max w2_moves: move worker1 -- if tied, random, else: move worker2

        w1_sub_scores = list(w1_moves.values())
        w2_sub_scores = list(w2_moves.values())
        w1_scores = []
        w2_scores = []

        for w1 in w1_sub_scores:
            w1_scores.append(sum(w1))

        for w2 in w2_sub_scores:
            w2_scores.append(sum(w2))

        w1_max = max(w1_scores)
        w2_max = max(w2_scores)

        max_score = max(w1_max, w2_max)

        max_move_one = []
        max_move_two = []
        

        for w1 in w1_moves:
            if sum(w1_moves.get(w1)) == max_score:
                max_move_one.append(w1)

        for w2 in w2_moves:
            if(sum(w2_moves.get(w2))) == max_score:
                max_move_two.append(w2)

        max_moves = [max_move_one, max_move_two]

        if len(max_move_one) == 0:
            worker = self.pieces[1]
            moves = max_move_two
        elif len(max_move_two) == 0:
            worker = self.pieces[0]
            moves = max_move_one
        else:
            worker_num = random.randint(0, 1)
            worker = self.pieces[worker_num]
            moves = max_moves[worker_num]

        best = [worker, moves[random.randrange(len(moves))]]
        return best

