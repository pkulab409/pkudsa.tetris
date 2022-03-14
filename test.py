import block


def testBlock():
    for i in range(7):
        for j in range(4):
            table = [[0 for col in range(5)] for row in range(5)]
            testBlock = block.block.offsetTable[i][j]
            if i == 0:
                for k in range(4):
                    pos = testBlock[k]
                    table[2 - pos[1]][pos[0] + 2] = 1
            else:
                for k in range(4):
                    pos = testBlock[k]
                    table[1 - pos[1]][pos[0] + 1] = 1
            for c0 in range(5):
                for c1 in range(5):
                    print(table[c0][c1], end="")
                print("\n", end="")
            print("\n", end="")


testBlock()
