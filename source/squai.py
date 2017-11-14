from squex import *
import random
import copy
import time

maxdepth = 3
maxsons = 5
adjratio = 0.5
secratio = 0.8
farratio = 0.1

def expand(b, current): # get adjacent pieces for player2
    for c in current:
        for n in b.getneighbors(c[0], c[1]):
            if b.getc(n[0], n[1]) != 1: #checks if not belongs to player 1
                if (n[0]==c[0]) or (n[1]==c[1]) or (b.getd(int(((n[0]+c[0])/2)-0.5),int(((n[1]+c[1])/2)-0.5)) != 1): #if it is diagonal, needs free middle piece
                    if (not n in current):
                        current = current + (n,)      
    return current

def computeplayer2(board):
    return cp2aux(board, maxdepth, 2)[0]
    
def getown(board, player):
    res = ()                           
    for i in range(board._l):
        for j in range(board._c):
            if board.getc(i, j)==player:
                res = res + ((i, j),)
    return res
    
    
def cp2aux(board, remainder, player): # simulates best play for player (2 tries to minimize plays to win)   returns (board, score)
    if remainder == 0:
        #board.show()
        #print(player2verticalconnectivity(board), "\n")
        return (board, player2verticalconnectivity(board)) # reached max depth, return result
    
    if player == 1:
        other = 2
    else:
        other = 1
    if player == 1:
        delta = 0
    else:
        delta = 1
    
    own = getown(board, 2)                    #own pieces
    adjacent = expand(board, own)          #adjacent spaces
    seconds = expand(board, adjacent)      #adjacent to adjacent
    near = own + adjacent + seconds
    far = ()                               #all others
    for i in range(board._l):
        for j in range(board._c):
            if (not (i, j) in near) and (not board.getc(i, j)==1):
                far = far + ((i, j),)
    
    adjacent = random.sample(adjacent, int(len(adjacent)*adjratio))  # lists are shortened for time efficiency
    seconds = random.sample(seconds, int(len(seconds)*secratio))
    far = random.sample(far, int(len(far)*farratio))

    plays = adjacent+seconds+far
    random.shuffle(list(plays))
    plays = tuple(plays[:maxsons])
    
    boards = ()
    for p in plays:
        b = copy.deepcopy(board)
        b.play(player, p[0], p[1])
        boards = boards + (b,)
        
    reses = ()
    for b in boards:
        reses = reses + (cp2aux(b, remainder-delta, other)[1],)
        
    if player == 2: #player 2 tries to minimize
        mini = 100
        b = None
        for i in range(len(reses)):
            if reses[i]<mini:
                mini = reses[i]
                b = boards[i]
        return (b, mini)
    
    elif player == 1: #player 1 tries to maximize
        maxi = 0
        b = None
        for i in range(len(reses)):
            if reses[i]>maxi:
                maxi = reses[i]
                b = boards[i]
        return (b, maxi)
    
    else:
        print("ERROR")
        return (None, 50)
    
def singleplayer():
    board = Board(10,10)
    while True:
        board.show()
        while True:
            print("Please input line and column (L C)")
            res = input(">")
            res = str.split(res)
            res = (eval(res[0]),eval(res[1]))
            if board._content[res[0]][res[1]].isempty():
                board.play1(res[0],res[1])
                break
        board.show()
        print("Player2 is thinking...")
        start = time.time()
        board = computeplayer2(board)
        print("Decided after",time.time()-start,"seconds")
        
singleplayer()
        

                
        
        
        
