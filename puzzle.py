import numpy as np
import queue
import time
import os

class NodePuzzle:
    def __init__(self, parent, puzzle, empty_tile, f, g):
        self.parent = parent
        self.puzzle = puzzle
        self.empty_tile = empty_tile
        self.f = f
        self.g = g

    def __lt__(self, other):
        return self.f + self.g <= other.f + other.g

def readPuzzle(file_name): 
    file_path = os.getcwd()
    file_path += f"//test//{file_name}"
    
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
        
def nilaiKurang(puzzle) :
    plusOne = set([1, 3, 4, 6, 9, 11, 12, 14])
    nilai_kurang = 0
    position = findPosition(puzzle)
    
    for i in range(16):
        nilai_kurang += kurang(i+1, position)
    if position[16] in plusOne:
        nilai_kurang += 1
    return nilai_kurang

def kurang(i, position):
    res = 0
    curPosition = position[i]
    for j in range(1, i):
        if position[j] > curPosition:
            res += 1
    return res

def findPosition(puzzle):
    position = {}
    for i in range(16):
        position[puzzle[i]] = i
    return position

def nextPuzzle(source_puzzle, moves, visited):
    list_next_puzzle = []
    source_empty_tile = source_puzzle.empty_tile
    for move in moves[source_empty_tile]:
        cur_puzzle = list(source_puzzle.puzzle)
        cur_puzzle[source_empty_tile] = cur_puzzle[move]
        cur_puzzle[move] = 16
        cur_puzzle = tuple(cur_puzzle)
        
        if cur_puzzle in visited:
            continue

        new_g = source_puzzle.g
        if source_puzzle.puzzle[move] != move + 1:
            new_g -= 1
        if source_puzzle.puzzle[move] != source_empty_tile + 1:
            new_g += 1
        
        next_puzzle = NodePuzzle(source_puzzle, cur_puzzle, move, source_puzzle.f + 1, new_g)
        list_next_puzzle.append(next_puzzle)
    return list_next_puzzle

def costG(puzzle):
    diff = 0
    for i in range(16):
        if puzzle[i] == 16:
            continue
        elif puzzle[i] != i+1:
            diff+=1
    return diff

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

def solvePuzzle(source):
    position = findPosition(source)
    moves = generateMove()
    
    source_puzzle = NodePuzzle(None, source, position[16], 0, costG(source))
    visited = set()
    prio_queue = queue.PriorityQueue()
    total_simpul = 1

    if source_puzzle.g == 0:
        return tuple([source_puzzle, 0])
    
    visited.add(source)
    prio_queue.put(source_puzzle)
    while not prio_queue.empty():
        cur_puzzle = prio_queue.get()
        list_next_puzzle = nextPuzzle(cur_puzzle, moves, visited)
        for next_puzzle in list_next_puzzle:
            total_simpul += 1
            if next_puzzle.g == 0:
                return tuple([next_puzzle, total_simpul])
            visited.add(next_puzzle.puzzle)
            prio_queue.put(next_puzzle)

if __name__ == "__main__" :
    fileName = str(input())
    source = readPuzzle(fileName)
    nilai_kurang = nilaiKurang(source)
    
    if nilai_kurang%2:
        print(f"Nilai Kurang        = {nilai_kurang}")
        print("Impossible to Solve!")
    else :
        timeBefore = time.time()
        solve = solvePuzzle(source)
        solved_node = solve[0]
        total_simpul = solve[1]
        result_path = []
        timeAfter2 = time.time()
        
        while solved_node != None:
            result_path.append(solved_node.puzzle)
            solved_node = solved_node.parent
        
        for i in range(len(result_path)-1, -1, -1):
            print(np.array(result_path[i]).reshape(4,4), '\n')
        
        print(f"Nilai Kurang        = {nilai_kurang}")
        print(f"Total Langkah       = {len(result_path)-1} steps")
        print(f"Waktu               = {(timeAfter2-timeBefore)} s")
        print(f"Simpul Dibangkitkan = {total_simpul} simpul")