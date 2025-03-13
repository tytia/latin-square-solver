"""
The Latin Square problem solved with local search stochastic hill climbing.

Author: Terry Tian
"""

import numpy as np
from collections import Counter
from time import time

def generate_starting_square(n: int):
    square = np.array([np.arange(1, n + 1) for _ in range(n)])
    for row in square:
        np.random.shuffle(row)
    
    return square

def solve(n: int):
    sq = generate_starting_square(n)
    
    # create tables to store counts for numbers for each row and column
    rt = [] # row table
    ct = [Counter() for _ in range(n)] # column table
    for row in sq:
        rt.append(Counter(row))
        for i in range(n):
            ct[i][row[i]] += 1

    # create table to store every point's total collision count
    collision_table = np.zeros((n, n), dtype=int)
    for r in range(n):
        for c in range(n):
            collision_table[r][c] = rt[r][sq[r][c]] + ct[c][sq[r][c]] - 2 # -2 to remove self from collision count

    # swap the position with the most collisions into the position that yields the most global collision reduction until no collisions remain
    while np.any(collision_table):
        indexes = np.where(collision_table == np.max(collision_table)) # all positions with the most collisions
        i = np.random.randint(len(indexes[0])) # randomly choose starting point from all positions with the most collisions
        r0, c0 = indexes[0][i], indexes[1][i]
        origin_val = sq[r0][c0]
        br, bc = 0, 0 # best destination row and column for swap
        best_diff = n

        # find best swap target from chosen starting point
        for r in range(n):
            # don't consider the row if it already contains the origin value
            if (rt[r][origin_val] > 0 and r != r0) or (r == r0 and rt[r][origin_val] > 1):
                continue

            for c in range(n):
                # don't consider the column if it already contains the origin value
                if (ct[c][origin_val] > 0 and c != c0) or (c == c0 and ct[c][origin_val] > 1):
                    continue

                # resultant difference from moving the destination element to the origin point
                diff = rt[r0][sq[r][c]] + ct[c0][sq[r][c]] - int(r == r0 or c == c0) - collision_table[r][c]
                
                # add resultant difference from moving the origin element to the destination point
                diff += rt[r][sq[r0][c0]] + ct[c][sq[r0][c0]] - collision_table[r0][c0]

                if diff < best_diff:
                    best_diff = diff
                    br, bc = r, c
            
        sq[r0][c0], sq[br][bc] = sq[br][bc], sq[r0][c0]
        
        # update tables
        origin_val = sq[br][bc]
        dest_val = sq[r0][c0]
        rt[r0][dest_val] += 1
        ct[c0][dest_val] += 1
        rt[r0][origin_val] -= 1
        ct[c0][origin_val] -= 1

        rt[br][origin_val] += 1
        ct[bc][origin_val] += 1
        rt[br][dest_val] -= 1
        ct[bc][dest_val] -= 1
        
        for col in range(n):
            collision_table[r0][col] = rt[r0][sq[r0][col]] + ct[col][sq[r0][col]] - 2
        for row in range(n):
            collision_table[row][c0] = rt[row][sq[row][c0]] + ct[c0][sq[row][c0]] - 2
        
        if br != r0: # avoid re-updating the same row or column
            for col in range(n):
                collision_table[br][col] = rt[br][sq[br][col]] + ct[col][sq[br][col]] - 2
        
        if bc != c0:
            for row in range(n):
                collision_table[row][bc] = rt[row][sq[row][bc]] + ct[bc][sq[row][bc]] - 2

    return sq
        

if __name__ == "__main__":
    n = int(input("n: "))
    st = time()
    sq = solve(n)
    ed = time()

    print()
    for row in sq:
        print(*row)
    print(f"\nFinished in {ed - st}s.\n")