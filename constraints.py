import csv

def label(line, arr):
    sum = 0
    seg = []
    for i in arr:
        if len(seg) != 0:
            seg.append(-1)
        for j in range(0, i):
            seg.append(1)
    rng = len(line) - len(seg) + 1
    for i in range(rng):
        for j in range(len(seg)):
            line[i+j] += (10*seg[j])/rng
    return line

def initGrid(sz):
    grid = []
    for i in range(sz):
        line = []
        for j in range(sz):
            line.append(0)
        grid.append(line)
    return grid

def buildGrid(grid, rows, cols):
    for i in range(len(grid)):
        grid[i] = label(grid[i], rows[i])
    for i in range(len(grid)):
        line = [0 for i in grid]
        line = label(line, cols[i])
        for j in range(len(line)):
            grid[j][i] += line[j]
    grid = [[max(round(j, 2), 0) for j in i] for i in grid]
    upper = len(grid)*2
    grid = [[(j/upper) for j in i] for i in grid]
    return grid

def saveGrid(grid, fname):
    with open(fname, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(grid)

if __name__ == "__main__":
    grid = initGrid(10)
    arr = [[[6, 2], [4, 4], [2, 6], [7], [0], [7], [0], [2, 6], [4, 4], [6, 2]], [[3, 3], [3, 3], [2, 2], [2, 1, 1, 2], [1, 2, 1, 1, 1], [1, 2, 1, 1, 1], [3, 1, 2], [3, 1, 2], [4, 1, 3], [4, 1, 3]]]									    
    rows = arr[0]
    cols = arr[1]
    grid = buildGrid(grid, rows, cols)
    saveGrid(grid, "grid.csv")