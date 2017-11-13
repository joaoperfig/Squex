# chr(9617) chr(9618) chr(9619) chr(9608)

class Piece:
    def __init__(self):
        self._status = 0 #0-no piece, 1-player 1, 2-player 2
        
    def isempty(self):
        return self._status == 0
    
    def play(self, playn):
        self._status = playn
    
    def play1(self):
        self._status = 1
        
    def play2(self):
        self._status = 2
        
    def __repr__(self):
        if self._status == 0:
            return " "
        elif self._status == 1:
            return chr(9617)
        elif self._status == 2:
            return chr(9608)
        else:
            return "?"
            

class Board:
    def __init__(self, lines, cols):
        self._l = lines
        self._c = cols
        self._content = () #lines by cols matrix
        self._diagonals = () #lines-1 by cols-1 matrix
        for i in range(lines):
            line = ()
            for j in range(cols):
                line = line + (Piece(),)
            self._content = self._content + (line,)
        for i in range(lines-1):
            diagoline = ()
            for j in range(cols-1):
                diagoline = diagoline + (Piece(),)
            self._diagonals = self._diagonals + (diagoline,)
        
    def show(self):
        string = "    "
        for j in range(self._c):
            string = string +(2-len(str(j)))*" "+str(j)+" "
        print(string)
        print("   "+chr(9484)+"-"*((self._c*3)-1)+chr(9488))
        for i in range(self._l):
            string = (2-len(str(i)))*" "+str(i)+" |"
            for j in range(self._c):
                string = string + str(self._content[i][j]) + str(self._content[i][j])+ "|"
            print(string)
            if i != self._l-1:
                string="   |--"
                for j in range(self._c-1):
                    thisdig = str(self._diagonals[i][j])
                    if thisdig == " ":
                        thisdig = "+"
                    string = string + thisdig + "--"
                string = string + "|"
                print(string)
        print("   "+chr(9492)+"-"*((self._c*3)-1)+chr(9496))
        
    def getneighbors(self, l, c):
        neigh = ((l-1,c-1), (l-1,c), (l-1,c+1), (l,c-1), (l,c+1), (l+1,c-1), (l+1,c), (l+1,c+1))
        res = ()
        for n in neigh:
            if (n[0]>=0) and (n[1]>=0) and (n[0]<self._l) and (n[1]<self._c):
                res = res + (n,)
        return res
    
    def getc(self, l, c):
        return self._content[l][c]._status
    
    def getd(self, l, c):
        return self._diagonals[l][c]._status

    def play1(self, l, c):
        self.play(1, l, c)
        
    def play2(self, l, c):
        self.play(2, l, c)
        
    def play(self, player, l, c):
        if not self._content[l][c].isempty():
            print("Trying to play on non empty space, continuing anyway")
        self._content[l][c].play(player)
        neigh = self.getneighbors(l, c)
        for n in neigh:
            if (self.getc(n[0], n[1]) == player) and (n[0]!=l) and (n[1]!=c):
                mid = (int(((n[0]+l)/2)-0.5),int(((n[1]+c)/2)-0.5))
                if self.getd(mid[0], mid[1]) == 0:
                    self._diagonals[mid[0]][mid[1]].play(player)
        
        
def multiplayer():
    board = Board(10,10)
    while True:
        board.show()
        while True:
            print("Player1 please input line and column (L C)")
            res = input(">")
            res = str.split(res)
            res = (eval(res[0]),eval(res[1]))
            if board._content[res[0]][res[1]].isempty():
                board.play1(res[0],res[1])
                break
        board.show()
        while True:
            print("Player2 please input line and column (L C)")
            res = input(">")
            res = str.split(res)
            res = (eval(res[0]),eval(res[1]))
            if board._content[res[0]][res[1]].isempty():
                board.play2(res[0],res[1])  
                break
            
def player2verticalconnectivity(board):
    
    def findjoined(b, current, old):
        found = False
        for c in current:
            for n in b.getneighbors(c[0], c[1]):
                if b.getc(n[0], n[1]) == 2: #see if belongs to player 2
                    if (n[0]==c[0]) or (n[1]==c[1]) or (b.getd(int(((n[0]+c[0])/2)-0.5),int(((n[1]+c[1])/2)-0.5)) == 2): #if it is diagonal, need middle piece
                        if (not n in current) and (not n in old):
                            current = current + (n,) #is adjacent, adds to current
                            found = True
        
        
    
    cost = 0
    old = ()
    current = ()
    for i in range(board._c):
        current = current + ((-1, i)) #imaginary line of placed pieces above the board
    