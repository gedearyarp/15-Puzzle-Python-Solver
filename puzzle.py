import queue
import os
import time        

class NodePuzzle:
    def __init__(self, parent, puzzle, empty_tile, f, g, level):
        self.parent = parent
        self.puzzle = puzzle
        self.empty_tile = empty_tile
        self.f = f
        self.g = g
        self.level = level

    def __lt__(self, next):
        return self.g + self.level <= next.g + next.level

def readPuzzle(file_name): 
    file_path = os.getcwd()
    file_path += f"//test//{file_name}"
    print(file_path)
    
    try:
        source = []
        with open(file_path) as f:
            lines = f.readlines()
            for line in lines:
                tiles = line.split()
                for tile in tiles:
                    source.append(int(tile))
        return tuple(source)
    except:
        print("File not found!")
        exit(0)
        
def isPossibleToSolve(puzzle) :
    plusOne = set([1, 3, 4, 6, 9, 11, 12, 14])
    kurang_sum = 0
    position = {}
    for i in range(16):
        position[puzzle[i]] = i

    for i in range(16):
        kurang_sum += kurang(i+1, puzzle, position)
        
    if(position[16] in plusOne):
        kurang_sum += 1
        
    print(f"Nilai KURANG => {kurang_sum}")
    
    if(kurang_sum%2 == 1):
        return False
    
    return True

def kurang(i, position):
    res = 0
    curPosition = position[i]
    for j in range(1, i):
        if position[j] > curPosition:
            res += 1
    return res

def nextPuzzle(source_puzzle, moves, costs_f):
    list_next_puzzle = []
    source_empty_tile = source_puzzle.empty_tile
    for move in moves[source_empty_tile]:    
        new_f = costs_f[move]
        new_g = source_puzzle.g
        if source_puzzle.puzzle[move] != move + 1:
            new_g -= 1
        if source_puzzle.puzzle[move] != source_empty_tile + 1:
            new_g += 1
            
        cur = list(source_puzzle.puzzle)
        cur[source_empty_tile] = cur[move]
        cur[move] = 16
        
        next_puzzle = NodePuzzle(source_puzzle, tuple(cur), move, new_f, new_g, source_puzzle.level + 1)
        list_next_puzzle.append(next_puzzle)
        
    return list_next_puzzle
    

def generateMove():
    moves = {}
    moves[0] = [1, 4]
    moves[1] = [0, 2, 5]
    moves[2] = [1, 3, 6]
    moves[3] = [2, 7]
    moves[4] = [0, 5, 8]
    moves[5] = [1, 4, 6, 9]
    moves[6] = [2, 5, 7, 10]
    moves[7] = [3, 6, 11]
    moves[8] = [4, 9, 12]
    moves[9] = [5, 8, 10, 13]
    moves[10] = [6, 9, 11, 14]
    moves[11] = [7, 10, 15]
    moves[12] = [8, 13]
    moves[13] = [9, 12, 14]
    moves[14] = [10, 13, 15]
    moves[15] = [11, 14]
    return moves  

def generateCostF(start):
    row_start = start//4
    col_start = start%4
    costs_f = []
    for i in range(16):
        row_i = i//4
        col_i = i%4
        costs_f.append(abs(row_start-row_i) + abs(col_start-col_i))
    return costs_f

def costG(puzzle):
    diff = 0
    for i in range(16):
        if puzzle[i] == 16:
            continue
        elif puzzle[i] != i+1:
            diff+=1
    return diff

def solvePuzzle(source):
    position = {}
    for i in range(16):
        position[source[i]] = i
    moves = generateMove()
    costs_f = generateCostF(position[16])
    
    source_puzzle = NodePuzzle(None, source, position[16], costs_f[position[16]], costG(source), 0)
    target = tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    visited = set()
    prio_queue = queue.PriorityQueue()

    if source == target:
        return source_puzzle
    
    visited.add(source)
    prio_queue.put(source_puzzle)

    while not prio_queue.empty():
        cur_puzzle = prio_queue.get()

        list_next_puzzle = nextPuzzle(cur_puzzle, moves, costs_f)
        for next_puzzle in list_next_puzzle:
            if next_puzzle.puzzle in visited:
                continue
            if next_puzzle.g == 0:
                return next_puzzle
            visited.add(next_puzzle.puzzle)
            prio_queue.put(next_puzzle)

if __name__ == "__main__" :
    fileName = str(input())
    source = readPuzzle(fileName)
    
    if not isPossibleToSolve(source):
        print("tidak mungkin selesai!")
    else :
        timeBefore = time.time()
        solved_node = solvePuzzle(source)
        timeAfter = time.time()
        print(f"Waktu: {timeAfter-timeBefore}")
        
        result_path = []
        print(solved_node.f)
        print(solved_node.g)
        while solved_node != None:
            result_path.append(solved_node.puzzle)
            solved_node = solved_node.parent
        
        for i in range(len(result_path)-1, -1, -1):
            for j in range(16):
                print(result_path[i][j], end=" ")
                if j%4 == 3:
                    print() 
            print() 
        
        print(len(result_path))
        
        timeAfter2 = time.time()
        print(f"Waktu: {timeAfter2-timeBefore}")