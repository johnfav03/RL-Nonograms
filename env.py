class nonogram:

    import numpy as np
    # cannibalized
    def __init__(self, data):
        self.reset()
        self.name = data[name]
        self.htmap = data[htmap]
        self.image = data[image]

    # cannibalized - parameterizable
    def reset(self):
        print("Board Reset")
        self.turns = 0
        self.board = np.full((10,10), -1)  ## Create board with all blank boxes in a shape of (9,9,9)
                                        ## For 9 Row, 9 Column, and 9 available numbers
                                        ## Created an array for numbers instead inputing number value there. Because it may give network a feel like there is a connection between each numbers, which is not.
                                        ## If no number selected n = [0,0,0,0,0,0,0,0,0]
                                        ## If any number selected n[x] = 1 where x is the selected number
                                        # jf: Seems to be using hot encoding to recognize numbers as symbols instead of numbers, using an array of size 1-n containing 0s or 1s in place of a 1-n value
                                            # could be super useful - circle back to this ^^ chance of drastic efficacy increase
                                            # i think i might want the numbers to be significant due to heatmap generation, but unsure
        self.done = False
        return self.board

    # cannibalized
    def display(self):
        # list comp and ternary op to create a visual string for board instead of nums
        vis = np.array([('■' if (i == 1) else ' ' for i in row) for row in self.board])
        str = '\n'.join(' '.join(row) for row in vis)
        print(str)

    # cannabalized
    def step(self, inp):
        # init reward and subtract 1 for turn
        self.reward = -1
        self.turns += 1
        # array of 3 vals: row, column, "move"
        row = inp[0]
        col = inp[1]
        val = inp[2]
        toggle = True
        end = False
        corr = True
        # check that row, col, and val are permited
        if (row < 0 or row > 9) or (col < 0 or col > 9) or (val != 1 and val != 0):
            print("Wrong Range")
            # if wrong input dec reward by 200
            self.reward -= 200    
            toggle = False
        # check that a move hasn't been made on that square
        if (self.board[row, col] != -1):
            print("Already Placed")
            # if tile already used dec reward by 200
            self.reward -= 200
            toggle = False
        else:
            # sel = np.zeros(9)
            # sel[val-1] = 1
            sel = val
            if (val != self.image[row, col]):
                # if the val isn't same as solution, dec reward by 50
                corr = False
                self.reward -= 50
            if toggle == True:
                print(f"{'Right' if corr else 'Wrong'}: {val} @ {col},{row}")
                self.board[row,col] = val
                self.display()
            # end the game if all tiles have been used
            if -1 not in self.board:
                end = True
            # jf: big debate - try for most complete in 100 turns or least turns to complete fully?
            if self.turns > 150:
                end = True
                self.reward -= 1000
            if end:
                # If the game won the reward increased by 1000
                self.done = True
                self.reward += 1000
        return (self.board, self.reward, self.done)