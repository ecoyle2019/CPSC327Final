
# Heuristic will inherit from Player class
class Heuristic():

    def __init__(self):
        # add from Player.py
        pass

    def get_possible_move_scores(self):
        '''Given a possible move, return the sub-scores for that move'''
        # one idea for this is to keep track of the original row and column, and try moving to each possible position by calling worker.move_direction for all possible directions
        # after the worker is temporarily moved, call methods to get the scores then after storing the results in an array, reset the worker position to the start, and return the array
        # NOTE: it should also calculate the score for the current position: if the current position of a worker has a higher score than any possible moves, don't move that worker

        sub_scores = [self.get_height_score(), self.get_center_score(), self.get_distance_score()]
        return sub_scores


    def get_height_score(self):
        
        # row_idx = worker.row - 1
        # col_idx = worker.col - 1
        # return board[row_idx][col_idx].height
        
        pass

    def get_center_score(self):
        
        # center_score = 0

        # iterate through the worker's possible moves (do separately for each worker)
        #NOTE: this implementation works if we (*temporarily*) move to each possible position to calculate score
                        
        # if worker.row == 3 and worker.col == 3:
            # center_score += 2
        # if (worker.row in [2, 4]) and (worker.col in [2, 3, 4]):
            # center_score += 1
        # if worker.row == 3 and worker.col in [2, 4]:
            # center_score += 1
        # if worker.row in [1, 5] or worker.col in [1, 5]:
            # center_score += 0
        
        # return center_score
        pass

    def get_distance_score(self):

        # player_workers = [worker1, worker2]
        # opponent_workers = [worker1, worker2]

        # worker1_d1 = max( abs(player_workers[0].row - opponent_workers[0].row), abs(player_workers[0].col - opponent_workers[0].col))
        # worker1_d2 = max( abs(player_workers[0].row - opponent_workers[1].row), abs(player_workers[0].col - opponent_workers[1].col))

        # worker2_d1 = max( abs(player_workers[1].row - opponent_workers[0].row), abs(player_workers[1].col - opponent_workers[0].col))
        # worker2_d2 = max( abs(player_workers[1].row - opponent_workers[1].row), abs(player_workers[1].col - opponent_workers[1].col))

        # distance = min(worker1_d1, worker1_d2) + min(worker2_d1, worker2_d2)
        # distance_score = 8 - distance

        # return distance_score

        pass


    def get_sub_scores(self):
        '''Returns the sub-scores for each possible move'''
        # go through each possible move and call self.get_possible_move_scores, and store in a dictionary -- return the dictionary (will be used in get_move_score())

        pass

    def get_move_score(self):
        c1, c2, c3 = 3, 2, 1 # starting values -- experiment with different values

        # determine weights, then calculate
        pass



