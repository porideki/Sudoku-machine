from board import Board
from dfs import dfs

class SearchProblem:
    '''探索問題を定義する抽象クラス'''
    def get_start_state(self):
        '''初期状態を返す関数'''
        raise NotImplementedError
    
    def next_states(self, state):
        '''与えられた状態 state から遷移できる状態のリストを返す関数'''
        raise NotImplementedError

    def is_goal(self, state):
        '''与えられた状態 state がゴールかどうかを True/False で返す関数'''
        raise NotImplementedError


class Sudoku(SearchProblem):
    def __init__(self, board):
        self.board = board
    
    def get_start_state(self):
        return self.board
    
    def is_goal(self, board):
        return board.filled() and board.verify()
 
    def next_states(self, board):
        import copy

        #候補表
        allowed_digits_table = [[0 for i in range(9)] for j in range(9)]
        for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
            allowed_digits_table[x][y] = board.get_allowed_digits(x, y)

        #精査
        while True: #do-while

            #更新前
            allowed_digits_table_b = copy.deepcopy(allowed_digits_table)
            
            #候補が1つのセルの座標リストの表
            confirmed_cell = []
            for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
                if len(allowed_digits_table[x][y]) == 1:
                    confirmed_cell += [(x, y)]

            #候補の除外
            for x, y in confirmed_cell: #(x, y): 候補が1つのセルの座標
                #エリア
                for (gx, gy) in [(3 * (x // 3) + (i // 3), 3 * (y // 3) + (i % 3)) for i in range(3 * 3)]:
                    if (gx, gy) != (x, y):
                        allowed_digits_table[gx][gy] = list(set(allowed_digits_table[gx][gy]) - set(allowed_digits_table[x][y]))
                
                for index in range(0, 9):
                    #行
                    if (x, index) != (x, y):
                        allowed_digits_table[x][index] = list(set(allowed_digits_table[x][index]) - set(allowed_digits_table[x][y]))
                    #列
                    if (index, y) != (x, y):
                        allowed_digits_table[index][y] = list(set(allowed_digits_table[index][y]) - set(allowed_digits_table[x][y]))
            
            if not(allowed_digits_table_b != allowed_digits_table):
                break
        
        #インスタンス生成
        next_boards = []
        for (x, y) in [(i // 9, i % 9) for i in range(9 * 9)]:
            for n in allowed_digits_table[x][y]:
                if board.data[x][y] == 0:
                    next_boards += [board.move(x, y, n)]

        return next_boards

if __name__ == '__main__':

    import time

    problem_data = \
        [[5, 3, 0, 0, 7, 0, 0, 0, 0],
         [6, 0, 0, 1, 9, 5, 0, 0, 0],
         [0, 9, 8, 0, 0, 0, 0, 6, 0],
         [8, 0, 0, 0, 6, 0, 0, 0, 3],
         [4, 0, 0, 8, 0, 3, 0, 0, 1],
         [7, 0, 0, 0, 2, 0, 0, 0, 6],
         [0, 6, 0, 0, 0, 0, 2, 8, 0],
         [0, 0, 0, 4, 1, 9, 0, 0, 5],
         [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    solution_data = \
        [[5, 3, 4, 6, 7, 8, 9, 1, 2],
         [6, 7, 2, 1, 9, 5, 3, 4, 8],
         [1, 9, 8, 3, 4, 2, 5, 6, 7],
         [8, 5, 9, 7, 6, 1, 4, 2, 3],
         [4, 2, 6, 8, 5, 3, 7, 9, 1],
         [7, 1, 3, 9, 2, 4, 8, 5, 6],
         [9, 6, 1, 5, 3, 7, 2, 8, 4],
         [2, 8, 7, 4, 1, 9, 6, 3, 5],
         [3, 4, 5, 2, 8, 6, 1, 7, 9]]

    start = time.time()

    board = Board(problem_data)
    sudoku = Sudoku(board)
    boards = dfs(sudoku)
    for i, board in enumerate(boards):
        print('\nSTEP %d' % i)
        print(board)
    assert boards[-1].data == solution_data

    print("\ncomplete({0}sec)".format(time.time() - start))
 
