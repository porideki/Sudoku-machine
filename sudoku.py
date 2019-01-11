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

        #置ける数リスト表
        allowed_digits_matrix = [[0 for i in range(9)] for j in range(9)]
        for x in range(0, 9):
            for y in range(0, 9):
                allowed_digits_matrix[x][y] = board.get_allowed_digits(x, y)

        '''
        print("before")
        for i in range(0, 9):
            print(allowed_digits_matrix[i])
        '''

        #精査
        '''
        allowed_digits_matrixから大きさが１のマス(候補の数が1種類しかないマス)を探し、座標をone_digit_cellに保存
        one_digit_cellから(x,y)に座標を一つずつ取り出す
            (x,y)が属するブロック・行・列の(x,y)を除く全てのマスの候補の数から(x,y)の候補の数を除外する
        上の処理をallowed_digits_matrixの更新が起こらなくなるまで繰り返す
        '''
        #cnt = 0
        while True:

            #print("{0}: ".format(cnt))

            #更新前
            allowed_digits_matrix_b = copy.deepcopy(allowed_digits_matrix)
            
            one_digit_cell = []
            for x in range(0, 9):
                for y in range(0, 9):
                    if len(allowed_digits_matrix[x][y]) == 1:
                        one_digit_cell += [(x, y)]
            '''
            for x,y in one_digit_cell:
                print("[{0}][{1}]: {2}".format(x, y, allowed_digits_matrix[x][y]))
            '''
            for x, y in one_digit_cell:
                #ブロック
                for lx in range(0, 3):
                    for ly in range(0, 3):
                        gx, gy = 3 * (x // 3) + lx, 3 * (y // 3) + ly
                        if (gx, gy) != (x, y):
                            allowed_digits_matrix[gx][gy] = list(set(allowed_digits_matrix[gx][gy]) - set(allowed_digits_matrix[x][y]))
                #行
                for gx in range(0, 9):
                    if (gx, y) != (x, y):
                        allowed_digits_matrix[gx][y] = list(set(allowed_digits_matrix[gx][y]) - set(allowed_digits_matrix[x][y]))
                #列
                for gy in range(0, 9):
                    if (x, gy) != (x, y):
                        allowed_digits_matrix[x][gy] = list(set(allowed_digits_matrix[x][gy]) - set(allowed_digits_matrix[x][y]))

            #cnt += 1
            
            if allowed_digits_matrix_b == allowed_digits_matrix:
                break
        '''
        print("after")
        for i in range(0, 9):
            print(allowed_digits_matrix[i])
        '''
        
        #インスタンス生成
        next_board = copy.deepcopy(board)
        for x in range(0, 9):
            for y in range(0, 9):
                if len(allowed_digits_matrix[x][y]) == 1:
                    next_board.data[x][y] = allowed_digits_matrix[x][y][0]

        #print(next_board)
        if next_board.filled():
            return [next_board]

        next_boards = []
        for x in range(0, 9):
            for y in range(0, 9):
                for n in allowed_digits_matrix[x][y]:
                    if next_board.data[x][y] == 0:
                        next_boards += [next_board.move(x, y, n)]

        return next_boards

if __name__ == '__main__':
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
    board = Board(problem_data)
    sudoku = Sudoku(board)
    #sudoku.next_states(board)
    
    boards = dfs(sudoku)
    for i, board in enumerate(boards):
        print('\nSTEP %d' % i)
        print(board)
    assert boards[-1].data == solution_data
    
