import random

class AllScoresNegativeError(Exception):
    pass



class NoPossibleMoves(Exception):
    """No possible moves can be made by this worker"""
    pass



class Strategy:
    game = None

    def select_worker(self, pieces):
        pass
    def select_move(self, worker):
        pass
    def select_build(self, worker):
        pass
    def print_action(self, worker, move_dir, build_dir):
        pass
    def convert_from_rc_to_dir(self, orig_row, orig_col, new_row, new_col):
        row_diff = orig_row - new_row
        col_diff = orig_col - new_col
        move_direction = ""
        if row_diff == -1 and col_diff == -1:
            move_direction = 'se'
        elif row_diff == -1 and col_diff == 1:
            move_direction = 'sw'
        elif row_diff == 1 and col_diff == -1:
            move_direction = 'ne'
        elif row_diff == 1 and col_diff == 1:
            move_direction = 'nw'
        elif row_diff == 0 and col_diff == -1:
            move_direction = 'e'
        elif row_diff == 0 and col_diff == 1:
            move_direction = 'w'
        elif row_diff == -1 and col_diff == 0:
            move_direction = 's'
        elif row_diff == 1 and col_diff == 0:
            move_direction = 'n'

        return move_direction
class InputStrategy(Strategy):
    def select_worker(self, pieces):
        return input("Select a worker to move\n")
    def select_move(self, worker):
        return input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
    def select_build(self, worker):
        return input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
    def print_action(self, worker, move_dir, build_dir):
        print(f"", end = "")

class RandomStrategy(Strategy):
    def select_worker(self, pieces):
        worker = random.choice(pieces)
        if len(Strategy.game.get_possible_moves(worker)) == 0:
            for p in pieces:
                if p != worker:
                    worker = p
            if len(Strategy.game.get_possible_moves(worker)) == 0:
                raise NoPossibleMoves

        return worker.name

    def select_move(self, worker):
        moves = Strategy.game.get_possible_moves(worker)
        move_choice = random.choice(moves)
        move_dir = self.convert_from_rc_to_dir(worker.row, worker.col, move_choice[0], move_choice[1])
        return move_dir

    def select_build(self, worker):
        builds = Strategy.game.get_possible_builds(worker)
        build_choice = random.choice(builds)
        build_dir = self.convert_from_rc_to_dir(worker.row, worker.col, build_choice[0], build_choice[1])
        return build_dir

    def print_action(self, worker, move_dir, build_dir):
        print(f"{worker},{move_dir},{build_dir}")

    

class HeuristicStrategy(Strategy):
    #def __init__(self, name):
        #super().__init__(name)
        #self.type = "Heuristic"


    # def get_possible_moves(self, worker):
    #     poss_rows = [worker.row - 1, worker.row, worker.row + 1]
    #     poss_cols = [worker.col - 1, worker.col, worker.col + 1]


    #     poss_moves = list(itertools.product(poss_rows, poss_cols))

    #     for m in poss_moves:
    #         if m[0] > 5 or m[1] > 5:
    #             poss_moves.remove(m)

    #     return poss_moves
    

    def select_move(self, worker):
        return self.move_direction

    def select_worker(self, pieces):
        
        # worker = best_move[0]
        possible_moves = Strategy.game.get_sub_scores()
        best_move = self.find_best_move(possible_moves, pieces)
        worker = best_move[0]
        orig_row = worker.row
        orig_col = worker.col
        new_row = best_move[1][0]
        new_col = best_move[1][1]
        self.move_direction = self.convert_from_rc_to_dir(orig_row, orig_col, new_row, new_col)
        #print(f"Row: {new_row}\n")
        #print(f"Col: {new_col}\n")

        # (1, 3) -> (2, 2): diff = -1, 1

        
        return worker.name
        
    def select_build(self, worker):
        builds = Strategy.game.get_possible_builds(worker)
        build_choice = random.choice(builds)
        build_dir = self.convert_from_rc_to_dir(worker.row, worker.col, build_choice[0], build_choice[1])
        return build_dir
    
    def print_action(self, worker, move_dir, build_dir):
        print(f"{worker},{move_dir},{build_dir}")
    

    def find_best_move(self, possible_moves, pieces):
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

        if len(w1_scores) > 0:
            w1_max = max(w1_scores)
        else:
            w1_max = -1

        if len(w2_scores) > 0:
            w2_max = max(w2_scores)
        else:
            w2_max = -1

        if w1_max == -1 and w2_max == -1:
            raise AllScoresNegativeError

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
            worker = pieces[1]
            moves = max_move_two
        elif len(max_move_two) == 0:
            worker = pieces[0]
            moves = max_move_one
        else:
            worker_num = random.randint(0, 1)
            worker = pieces[worker_num]
            moves = max_moves[worker_num]

        best = [worker, moves[random.randrange(len(moves))]]
        return best
