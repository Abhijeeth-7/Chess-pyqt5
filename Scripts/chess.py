# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 08:19:09 2020

@author: kanch
"""
from PyQt5.QtGui import QPixmap
import copy
from math import sqrt
board=[[None for j in range(9)]for i in range(9)]
    
class Chess:
    team=1
  
    def setPosition(self,loc):
        # print("position updated:")
        self.i=loc[0]
        self.j=loc[1]
                
    def getPosition(self):
        return (self.i,self.j)
    
    def issameTeam(self,obj):
        if obj==None or self==obj:
            return False
        if obj.team == self.team:
            return True
        else:
            return False
        
    def inBounds(self,i,j):
        if i>=1 and i<=8 and j>=1 and j<=8:
            return True
        return False
    
    def inRange(self,newloc,bounds):
        if self.image=='pawn':
            print(bounds,"newloc:",newloc)
            return (newloc in bounds)
        for i in range(0,len(bounds)//2+1,2):
            total_dist = sqrt((bounds[i][0]-bounds[i+1][0])**2+(bounds[i][1]-bounds[i+1][1])**2)
            dist1 = sqrt((bounds[i][0]-newloc[0])**2+(bounds[i][1]-newloc[1])**2)
            dist2 = sqrt((bounds[i+1][0]-newloc[0])**2+(bounds[i+1][1]-newloc[1])**2)
            if (total_dist*100)//1 == ((dist1+dist2)*100)//1:
                return True
        return False
        
    def validateD(self,loc):
        m11 = abs(self.i-loc[1])
        m12 = abs(self.j-loc[0])
        m21 = abs(self.i-loc[0])
        m22 = abs(self.j-loc[1])
        return m11==m12 or m21==m22
    
    def validateRC(self,loc):
        if (self.i==loc[0] or self.j==loc[1]):
            return True
        return False    
    
    def updateDiagBounds(self,bounds):
        bounds.clear()
        i,j=self.getPosition()
        while self.inBounds(i-1,j-1) and (board[i][j]==None or board[i][j]==self):
            i-=1
            j-=1
        if self.inBounds(i,j) and self.issameTeam(board[i][j]): i,j=i+1,j+1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        while self.inBounds(i+1,j+1) and  (board[i][j]==None or board[i][j]==self):
            if self.issameTeam(board[i+1][j+1]): break
            i+=1
            j+=1
        else:
            if self.inBounds(i,j) and self.issameTeam(board[i][j]): i,j=i-1,j-1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        while self.inBounds(i-1,j+1) and  (board[i][j]==None or board[i][j]==self):
            if self.issameTeam(board[i-1][j+1]): break
            i-=1
            j+=1
        else:
            if self.inBounds(i,j) and self.issameTeam(board[i][j]): i,j=i+1,j-1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        while self.inBounds(i+1,j-1) and (board[i][j]==None or board[i][j]==self):
            if self.issameTeam(board[i+1][j-1]): break
            i+=1
            j-=1
        else:
            if self.inBounds(i,j) and self.issameTeam(board[i][j]): i,j=i-1,j+1
        bounds.append((i,j))
    
    def updateRCBounds(self,bounds):
        bounds.clear()
        i,j=self.getPosition()
        i-=1    
        while self.inBounds(i,j) and board[i][j]==None:
            i-=1
        if self.inBounds(i,j) and self.issameTeam(board[i][j]): i=i+1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        i+=1
        while self.inBounds(i,j) and board[i][j]==None:
            i+=1
        if self.inBounds(i,j) and self.issameTeam(board[i][j]): i=i-1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        j-=1
        while self.inBounds(i,j) and board[i][j]==None:
            j-=1
        if self.inBounds(i,j) and self.issameTeam(board[i][j]): j=j+1
        bounds.append((i,j))
        
        i,j=self.getPosition()
        j+=1
        while self.inBounds(i,j) and board[i][j]==None:
            j+=1
        if self.inBounds(i,j) and self.issameTeam(board[i][j]): j=j-1
        bounds.append((i,j))
   
    # def canEscape(self,threats,king):
    #     bounds = king.bounds
    #     result = False
    #     for i in range(len(threats)):
    #         if threats[i]==0 and bounds[i]!=king.getPosition():
    #             obj = board[bounds[i][0]][bounds[i][1]]
    #             if obj!=None and obj.team == self.team:
    #                 result = result or False
    #                 continue
    #             result = result or True 
    #     return result
       
    
    def changeColor(self,Flag,x,y):
        if Flag:
            ui_board[x][y].setStyleSheet("""background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5,
                                         radius:0.5, fx:0.5, fy:0.5, stop:0.721591 rgba(255, 100, 100, 255),
                                         stop:0.8125 rgba(255, 255, 255, 255),
                                         stop:0.931818 rgba(255, 0, 0, 255));""")
        else:
            if x%2==1:
                if y%2==1:
                    ui_board[x][y].setStyleSheet("background-color: rgb(20, 138, 0);")
                else:
                    ui_board[x][y].setStyleSheet("background-color: rgb(187, 255, 171);")
            else:
                if y%2==0:
                    ui_board[x][y].setStyleSheet("background-color: rgb(20, 138, 0);")
                else:
                    ui_board[x][y].setStyleSheet("background-color: rgb(187, 255, 171);")  
    
    def isUnderCheck(self,x,y):
        king = board[x][y]
        
        Threat = False
        knightSquares = [
                            [x+2,y+1],[x+2,y-1],
                            [x-2,y+1],[x-2,y-1],
                            [x+1,y+2],[x-1,y+2],
                            [x+1,y-2],[x-1,y-2]
                        ]
        
        #checks for the threat to king from a Knight
        for xy in knightSquares:
            if self.inBounds(xy[0], xy[1]) and board[xy[0]][xy[1]]!=None:
                if board[xy[0]][xy[1]].image=="knight" and board[xy[0]][xy[1]].team!=king.team:
                    Threat = True
                    break

        if not Threat:
            #checking for threats in kings path    
            for bx,by in king.bounds:
                if (bx,by)!=king.getPosition():
                    if self.isUnderThreat(bx,by,king):
                        Threat = True
                        break
        
        self.changeColor(Threat, x, y)
        return Threat
        
    def isUnderThreat(self,x,y,king):
        
        king_rbound, king_cbound = x, y
        i,j = king.getPosition()
        row_inc = x-i
        col_inc = y-j
        x, y = i, j
        
        # keeps checking along the path x+row_inc and y+col_inc,
        # until we hit an object or until we go out of bounds.
        while king.inBounds(x+row_inc,y+col_inc) and (board[x][y]==None or (x,y)==(i,j)):
            x, y = x+row_inc, y+col_inc           
        
        #checking wether the last cell we stopped at ,is empty or not
        # if empty there is no threat from this path to the king, Hence return False
        # otherwise we check the object found is of opponents team or not, and can it reach(kill) the king?
        if board[x][y]!=None and board[x][y].team!=king.team:
            
            # Handling the case if pawn is foundin kings path
            if board[x][y].image=="pawn":
                x,y=board[x][y].getPosition()
                if king.team==1: inc = 1
                else: inc =-1
                return (king.getPosition() in ((x+inc,y-1),(x+inc,y+1)))
            
            #updating the bounds of the object to avoid anamolies
            board[x][y].updateBounds(board[x][y].bounds)
            if board[x][y].inRange((king_rbound,king_cbound),board[x][y].bounds):
                return True
        return False
    
    
    
class Game(Chess):
    
    def __init__(self,ui_obj,ui_b):
        global ui,ui_board,board,locs
        locs= list()
        ui = ui_obj
        ui_board = ui_b
        self.kx = list()
        self.ky = list()
        self.setUpBoard()
        self.setUpPngs()
        
    def setUpBoard(self):
        white_pawn=[None]
        black_pawn=[None]
        white_rook=[]
        white_knight=[]
        white_bishop=[]
        black_rook=[]
        black_knight=[]
        black_bishop=[]
        for i in range(1,9):
            white_pawn+=[Pawn(7,i,1)]
            black_pawn+=[Pawn(2,i,2)]
        for i in [1,8]:
            white_rook+=[Rook(8,i,1)]
            black_rook+=[Rook(1,i,2)]
        for i in [2,7]:
            white_knight+=[Knight(8,i,1)]
            black_knight+=[Knight(1,i,2)]
        for i in [3,6]:
            white_bishop+=[Bishop(8,i,1)]
            black_bishop+=[Bishop(1,i,2)]
        white_queen=Queen(8,5,1)
        black_queen=Queen(1,5,2)
        self.white_king=King(8,4,1)
        self.black_king=King(1,4,2)
        self.kx += [8,1]
        self.ky += [4,4]
        board[1] = [None,black_rook[0],black_knight[0],black_bishop[0],self.black_king,black_queen,black_bishop[1],black_knight[1],black_rook[1]]
        board[2] = black_pawn
        board[7] = white_pawn
        board[8] = [None,white_rook[0],white_knight[0],white_bishop[0],self.white_king,white_queen,white_bishop[1],white_knight[1],white_rook[1]]
        
        for i in range(1,9):
            for j in range(1,9):
                if board[i][j]!=None:
                    board[i][j].updateBounds(board[i][j].bounds)
        
    def setUpPngs(self):
        for i in range(1,9):
            for j in range(1,9):
                if board[i][j]!=None:
                    ui_board[i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
                    
    """
    def flipBoard(self,objname):
        i,j=int(objname[1]),int(objname[2])
        if board[i][j]!=None and board[9-i][j]!=None:
            ui_board[i][j].setPixmap(QPixmap("imgs/"+board[9-i][j].image+str(board[9-i][j].team)+".png"))
            ui_board[9-i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
        elif board[i][j]!=None:
            ui_board[9-i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
            ui_board[i][j].setPixmap(QPixmap("imgs/blank.png"))
        elif board[9-i][j]!=None:
            ui_board[i][j].setPixmap(QPixmap("imgs/"+board[9-i][j].image+str(board[9-i][j].team)+".png"))
            ui_board[9-i][j].setPixmap(QPixmap("imgs/blank.png"))
        else:
            ui_board[9-i][j].setPixmap(QPixmap("imgs/blank.png"))
            ui_board[i][j].setPixmap(QPixmap("imgs/blank.png"))
    """
    
    def captureClicks(self,objname,team):
        x,y=int(objname[1]),int(objname[2])
        if board[x][y]!=None:
            if team ==1:
                print("clikced on white",board[x][y].image,"\t team:",team)
                if locs==[] and board[x][y].team!=1:
                    return False
            else:
                print("clikced on black",board[x][y].image,"\t team:",team)
                if locs==[] and board[x][y].team!=2:
                    return False
            board[x][y].updateBounds(board[x][y].bounds)
            
        if len(locs)==2:
            locs.clear()
        if locs==[] and  board[x][y]!=None:
            locs.append((x,y))
        elif len(locs)==1 and locs[0]!=(x,y):
            locs.append((x,y))
            if board[x][y]!=None:
                if board[x][y].team==board[locs[0][0]][locs[0][1]].team:
                    locs.pop(0)
        if len(locs)==2 and locs[0]!=locs[1]:
            res = self.move(locs[0],locs[1],team)
            return res                  
    
    def move(self,click1,click2,team):
        x1,y1=click1
        x2,y2=click2
        obj1 = board[x1][y1]
        obj2 = board[x2][y2]
        # validating the players turn and also the move he is making
        if board[x1][y1].team==self.team and (board[x1][y1].validate((x2,y2))):
            
            #if king is being moved then update his coordinates in kx,ky variables, for keeping track of the king.
            if board[x1][y1].image == "king":
                self.changeColor(False,self.kx[team-1], self.ky[team-1])
                self.kx[team-1],self.ky[team-1]=(x2,y2)
            
            #perform the move on logic board(backend board)
            board[x2][y2] = copy.copy(board[x1][y1])
            board[x2][y2].setPosition((x2,y2))
            board[x2][y2].updateBounds(board[x2][y2].bounds)
            board[x1][y1] = None
            
            #check if the move has placed the king under check!?
            if self.isUnderCheck(self.kx[team-1],self.ky[team-1]):
                
                # case 1: if king is  moved and he is under check then move him back to his last location.
                if board[x2][y2].image == "king":
                    self.kx[team-1],self.ky[team-1]=(x1,y1)  
                
                # case 2: rolling back the changes, making this move puts the team's king under check!
                board[x1][y1] = obj1
                board[x2][y2] = obj2
                return False
            
            # writing the changes onto the UI board
            ui_board[x2][y2].setPixmap(QPixmap("imgs/"+board[x2][y2].image+str(board[x2][y2].team)+".png"))
            ui_board[x1][y1].setPixmap(QPixmap("imgs/blank.png"))
            
            self.isUnderCheck(self.kx[team%2], self.ky[team%2])
            
            return True
        return False
            
class Knight(Chess):   
    
    def __init__(self,row,col,team):
        self.team=team
        self.image="knight"
        self.i=row
        self.j=col
        self.bounds=[0]*8
        
    def validate(self,loc):
        if (loc in self.bounds) and not self.issameTeam(board[loc[0]][loc[1]]):
             return True
        return False
    
    def updateBounds(self,bounds):
        bounds.clear()
        i,j=self.getPosition()
        x=[2,2,-2,-2,1,-1,1,-1]
        y=[1,-1,1,-1,-2,-2,2,2]
        for k in range(8):
           bounds.append((i+x[k],j+y[k]))
         
class King(Chess):   

    def __init__(self,row,col,team):
        self.team=team
        self.image="king"
        self.i=row
        self.j=col
        self.check = False
        self.bounds = [0]*8
        
    def validate(self,loc):
        x,y=loc
        if not self.issameTeam(board[x][y]) and (loc in self.bounds):
            return True
        return False
    
    def updateBounds(self,bounds):
        self.i,self.j=self.getPosition()
        x,y=self.i,self.j
        bounds.clear()
        bounds += [(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1),(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
        for i in range(8):
            if not self.inBounds(bounds[i][0], bounds[i][1]):
                bounds[i]=(x,y)
    
class Queen(Chess):    
    def __init__(self,row,col,team):
        self.team=team
        self.image="queen"
        self.i=row
        self.j=col
        self.Diagbounds=[0]*4
        self.RCbounds=[0]*4
        self.bounds = self.Diagbounds+self.RCbounds
      
    def validate(self,loc):
        if (self.inRange(loc, self.bounds[:4]) or self.inRange(loc, self.bounds[4:]))\
            and (self.validateD(loc) or self.validateRC(loc)) and not self.issameTeam(board[loc[0]][loc[1]]):
            return True
        return False
    
    def updateBounds(self,bounds):
        self.updateDiagBounds(self.Diagbounds)
        self.updateRCBounds(self.RCbounds)
        self.bounds = self.Diagbounds+self.RCbounds
    
class Rook(Chess):
    def __init__(self,row,col,team):
        self.team=team
        self.image="rook"
        self.i=row
        self.j=col
        self.bounds=[0]*4
    
    def validate(self,loc):
        return (self.validateRC(loc) and self.inRange(loc,self.bounds)\
            and not self.issameTeam(board[loc[0]][loc[1]]))
    
    def updateBounds(self,bounds):
        self.updateRCBounds(bounds)
    
class Bishop(Chess):
    def __init__(self,row,col,team):
        self.team=team
        self.image="bishop"
        self.i=row
        self.j=col
        self.bounds=[0]*4
    
    def validate(self,loc):
        return (self.validateD(loc) and self.inRange(loc,self.bounds)\
                and not self.issameTeam(board[loc[0]][loc[1]]))
        
    def updateBounds(self,bounds):
        self.updateDiagBounds(bounds)

class Pawn(Chess):
    def __init__(self,row,col,team):
        self.team=team
        self.image="pawn"
        self.i=row
        self.j=col
        self.notmoved=True
        self.bounds=[]
    
    def validate(self,loc):
        if self.inRange(loc,self.bounds):
            self.notmoved=False
            return True
        return False
    
    def updateBounds(self,bounds):
        self.bounds.clear()
        x,y=self.getPosition()
        k=0
        if self.team==2:
            k=1
        else:
            k=-1
            
        if self.notmoved:
            if self.team==2:
                if board[x+1][y]==None:
                    self.bounds=[(x+1,y)]
                if board[x+2][y]==None:
                    self.bounds+=[(x+2,y)]
            else:
                  if board[x-1][y]==None:
                    self.bounds=[(x-1,y)]
                  if board[x-2][y]==None:
                    self.bounds+=[(x-2,y)]
            # print(self.bounds)

        if self.inBounds(x+k,y) and board[x+k][y]==None:
            self.bounds+=[(x+k,y)]
            
        if self.inBounds(x+k,y+k) and board[x+k][y+k]!=None and not self.issameTeam(board[x+k][y+k]):
            self.bounds+=[(x+k,y+k)]
            
        if self.inBounds(x+k,y-k) and board[x+k][y-k]!=None and not self.issameTeam(board[x+k][y-k]):
            self.bounds+=[(x+k,y-k)]
        print(self.bounds)
