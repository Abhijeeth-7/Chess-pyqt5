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
    checked=''
  
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
       
    # def flipBoard(self):       
    #     if board[i][j]!=None and board[9-i][j]!=None:
    #         ui_board[i][j].setPixmap(QPixmap("imgs/"+board[9-i][j].image+str(board[9-i][j].team)+".png"))
    #         ui_board[9-i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
    #     elif board[i][j]!=None:
    #         ui_board[9-i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
    #         ui_board[i][j].setPixmap(QPixmap("imgs/blank.png"))
    #     elif board[9-i][j]!=None:
    #         ui_board[i][j].setPixmap(QPixmap("imgs/"+board[9-i][j].image+str(board[9-i][j].team)+".png"))
    #         ui_board[9-i][j].setPixmap(QPixmap("imgs/blank.png"))
    #     else:
    #         ui_board[9-i][j].setPixmap(QPixmap("imgs/blank.png"))
    #         ui_board[i][j].setPixmap(QPixmap("imgs/blank.png"))
    
    # def isUnderCheck(self,x,y):
    #     threats = list()
    #     check = False
    #     king = board[x][y]
    #     print("king at :",x,y,flush=True)
    #     for x,y in king.bounds:
    #         if (x,y)!=king.getPosition():
    #             threats.append(self.isUnderThreat(x,y,king))
    #         else:
    #             threats.append(0)           
    #     for i in range(len(threats)):
    #         if board[king.bounds[i][0]][king.bounds[i][1]]==None and threats[i]==1:
    #             check = True            
    #     if check:#and not self.canEscape(threats,king):
    #         king.check = True
    #     else:
    #         king.check = False
    #     return check
        
    # def isUnderThreat(self,x,y,king):
    #     row_bound, col_bound = x, y
    #     i,j = king.getPosition()
    #     row_inc = x-i
    #     col_inc = y-j
    #     x, y = i, j      
    #     while king.inBounds(x+row_inc,y+col_inc) and (board[x][y]==None or (x,y)==(i,j)):
    #         x, y = x+row_inc, y+col_inc           
    #     if board[x][y]!=None and board[x][y].team!=king.team:
    #         if board[x][y].inRange((row_bound,col_bound),board[x][y].bounds):
    #             return 1
    #     return 0
    
    # def changeColor(self,Flag,x,y,px,py):
    #     if Flag:
    #         ui_board[x][y].setStyleSheet("background-color: rgb(217, 61, 26)")
    #     else:
    #         if self.i%2==1:
    #             if self.j%2==1:
    #                 ui_board[x][y].setStyleSheet("background-color: rgb(153, 92, 7);")
    #             else:
    #                 ui_board[x][y].setStyleSheet("background-color: rgb(255, 217, 151);")
    #         else:
    #             if self.j%2==0:
    #                 ui_board[x][y].setStyleSheet("background-color: rgb(153, 92, 7);")
    #             else:
    #                 ui_board[x][y].setStyleSheet("background-color: rgb(255, 217, 151);")  
    
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
        white_queen=Queen(8,4,1)
        black_queen=Queen(1,5,2)
        self.white_king=King(8,5,1)
        self.black_king=King(1,4,2)
        self.kx += [8,1]
        self.ky += [5,4]
        board[1] = [None,black_rook[0],black_knight[0],black_bishop[0],self.black_king,black_queen,black_bishop[1],black_knight[1],black_rook[1]]
        board[2] = black_pawn
        board[7] = white_pawn
        board[8] = [None,white_rook[0],white_knight[0],white_bishop[0],white_queen,self.white_king,white_bishop[1],white_knight[1],white_rook[1]]
        
        for i in range(1,9):
            for j in range(1,9):
                if board[i][j]!=None:
                    board[i][j].updateBounds(board[i][j].bounds)
                    if board[i][j].image=='king':
                        print(board[i][j].bounds)
        
    def setUpPngs(self):
        for i in range(1,9):
            for j in range(1,9):
                if board[i][j]!=None:
                    ui_board[i][j].setPixmap(QPixmap("imgs/"+board[i][j].image+str(board[i][j].team)+".png"))
    
    def captureClicks(self,objname,team):
        x,y=int(objname[1]),int(objname[2])
        if board[x][y]!=None:
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
    
    def move(self,obj1,obj2,team):
        x1,y1=obj1
        x2,y2=obj2
        if board[x1][y1].team==self.team and (board[x1][y1].validate((x2,y2))):
            board[x1][y1].setPosition((x2,y2))
            board[x2][y2] = copy.copy(board[x1][y1])
            board[x1][y1] = None
            board[x2][y2].updateBounds(board[x2][y2].bounds)
            ui_board[x2][y2].setPixmap(QPixmap("imgs/"+board[x2][y2].image+str(board[x2][y2].team)+".png"))
            ui_board[x1][y1].setPixmap(QPixmap("imgs/blank.png"))
            return True
        return False
       
        
    # def wins(self):
    #     winning_team = self.isTimeout()
    #     if winning_team==1:
    #         print("white wins")
    #     elif winning_team==2:
    #         print("black wins")
            
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
                self.bounds=[(x+1,y),(self.i+2,self.j)]
            else:
                self.bounds=[(x-1,y),(self.i-2,self.j)]
                
        if self.inBounds(x+k,y) and board[x+k][y]==None:
            self.bounds+=[(x+k,y)]
            
        if self.inBounds(x+k,y+k) and board[x+k][y+k]!=None and not self.issameTeam(board[x+k][y+k]):
            self.bounds+=[(x+k,y+k)]
            
        if self.inBounds(x+k,y-k) and board[x+k][y-k]!=None and not self.issameTeam(board[x+k][y-k]):
            self.bounds+=[(x+k,y-k)]
