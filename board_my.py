class Board:
    def __init__(self, data):
        self.data = data

    def filled(self):
        '''全てのマスが埋まっているか'''
        isFilled = True
        for x in range(0, len(self.data)):
            for y in range(0, len(self.data[0])):
                isFilled &= self.data[x][y] != 0

        return isFilled

    def verify(self):
        '''ルールチェック'''
        isPass = True

        #ブロック
        for bx in range(0, 3):
            for by in range(0, 3):
                numcounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for x in range(0, 3):
                    for y in range(0, 3):
                        adress = {"x": 3 * bx + x, "y": 3 * by + y}  #実アドレス
                        numcounts[self.data[adress["x"]][adress["y"]]] += 1
                for i in range(0,9):
                    isPass &= numcounts[i] <= [8, 1, 1, 1, 1, 1, 1, 1, 1, 1][i]
                #print("{0}x{1} block: {2}".format(bx, by, numcounts))           
            
        #行
        for x in range(0, 9):
            numcounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for y in range(0, 9):
                numcounts[self.data[x][y]] += 1
            for i in range(0,9):
                isPass &= numcounts[i] <= [8, 1, 1, 1, 1, 1, 1, 1, 1, 1][i]
            #print("row {0}: {1}".format(x, numcounts))

        #列
        for y in range(0, 9):
            numcounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for x in range(0, 9):
                numcounts[self.data[x][y]] += 1
            for i in range(0,9):
                isPass &= numcounts[i] <= [8, 1, 1, 1, 1, 1, 1, 1, 1, 1][i]
            #print("column {0}: {1}".format(y, numcounts))

        return isPass

    def get_allowed_digits(self, x, y):
        '''置くことが出来る数字'''

        outlist = []

        #置けない
        if self.data[x][y] != 0:
            outlist = []
        else:
            #ブロック
            block = set()
            bx, by = (x // 3, y // 3)
            for lx in range(0, 3):
                for ly in range(0, 3):
                    adress = {"x": 3 * bx + lx, "y": 3 * by + ly}
                    block.add(self.data[adress["x"]][adress["y"]])
            block = set([1,2,3,4,5,6,7,8,9]) - block

            #行
            row = set()
            for ly in range(0, 9):
                row.add(self.data[x][ly])
            row = set([1,2,3,4,5,6,7,8,9]) - row

            #列
            column = set()
            for lx in range(0, 9):
                column.add(self.data[lx][y])
            column = set([1,2,3,4,5,6,7,8,9]) - column

            outlist = list(block & row & column)

        return outlist

    def move(self, x, y, d):
        assert self.data[x][y] == 0
        
        #リストコピー
        nextData = [[0 for y in range(9)] for x in range(9)]
        for (gx, gy) in [(i // 9, i % 9) for i in range(9 * 9)]:
            nextData[gx][gy] = self.data[gx][gy]
        
        nextData[x][y] = d

        return Board(nextData)

    def __str__(self):
        separator = '+---+---+---+'
        lines = [separator]
        for i in range(0, 9, 3):
            for j in range(i, i + 3):
                lines.append('|%d%d%d|%d%d%d|%d%d%d|' % tuple(self.data[j]))
            lines.append(separator)
        return '\n'.join(lines).replace('0', ' ')

if __name__ == '__main__':

    board = Board([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                   [6, 0, 0, 1, 9, 5, 0, 0, 0],
                   [0, 9, 8, 0, 0, 0, 0, 6, 0],
                   [8, 0, 0, 0, 6, 0, 0, 0, 3],
                   [4, 0, 0, 8, 0, 3, 0, 0, 1],
                   [7, 0, 0, 0, 2, 0, 0, 0, 6],
                   [0, 6, 0, 0, 0, 0, 2, 8, 0],
                   [0, 0, 0, 4, 1, 9, 0, 0, 5],
                   [0, 0, 0, 0, 8, 0, 0, 7, 9]])
    print(board)
    print(board.verify())
