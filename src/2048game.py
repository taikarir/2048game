# Author: Tai Karir
# Date: 09/03/2020
# Email: tai.karir@gmail.com

import random
import curses
import math
import time
#starts a new window in curses
stdscr=curses.initscr()
win=curses.newwin(24,80,0,0)
curses.noecho()
curses.cbreak()
curses.curs_set(False)
curses.start_color()
win.keypad(True)
#initializes the color pairs to be used in the number tiles
curses.init_pair(7,curses.COLOR_BLACK,curses.COLOR_BLACK)
curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_YELLOW)
curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_RED)
curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_GREEN)
curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_BLUE)
curses.init_pair(6,curses.COLOR_WHITE,curses.COLOR_MAGENTA)
#coding for the grid
grid=[[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
      [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]]
#coding for the 2048 decoration
deco=[[0,1,1,1,0,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,1,0],
      [1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,0,1],
      [0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,0,1],
      [0,0,1,0,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,1,1,0],
      [0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1],
      [1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1],
      [1,1,1,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,1,0]]
#what numbers are in which rows and columns
row1=[0,0,0,0]
row2=[0,0,0,0]
row3=[0,0,0,0]
row4=[0,0,0,0]
rows=[row1,row2,row3,row4]
#the player's score
score=0
#the color of a certain tile
xcolor=0
#gameOver=1 when no moves can be made
gameOver=0
#this function draws the board based on the current position of the tiles
def drawBoard():
    win.clear()
    #draws the grid
    for i in range(0,len(grid)):
        for j in range(0,len(grid[i])):
            if grid[i][j]==1:
                win.addstr(i,j,"+")
            elif grid[i][j]==2:
                win.addstr(i,j,"-")
            elif grid[i][j]==3:
                win.addstr(i,j,"|")
    #draws all the tiles
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            #decides the color pair for the tile based on the number
            if rows[i][j]>0:
                xcolor=int(math.log2(rows[i][j]))
                if xcolor>6:
                    xcolor=6
            else:
                xcolor=7
            #colors in the tile based on the number
            for k in range(0,2):
                for l in range(0,4):
                    win.addstr(1+i*2+k,1+j*4+l," ",curses.color_pair(xcolor))
            win.addstr(1+i*2,1+j*4,str(rows[i][j]),curses.color_pair(xcolor))
    win.addstr(15,0,"Press x to exit")
    win.addstr(1,20,"Arrow keys to move")
    win.addstr(13,0,"Score: {}".format(score))
    if gameOver==1:
        win.addstr(12,24,"GAMEOVER")
    #draws the decoration
    for i in range(0,len(deco)):
        for j in range(0,len(deco[i])):
            if deco[i][j]==1:
                win.addstr(4+i,24+j,"#")
    win.refresh()
#this function adds a tile to the board
def addTile():
    empty=[]
    #choosing a random value for the new tile
    newtile=random.randrange(0,10)
    if newtile==9:
        newtile=4
    else:
        newtile=2
    #finding an empty space to place the tile
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            if rows[i][j]==0:
                empty.append([i,j])
    #placing the tile
    if len(empty)>1:
        x=random.randrange(len(empty)-1)
        rows[empty[x][0]][empty[x][1]]=newtile
    elif len(empty)==1:
        rows[empty[0][0]][empty[0][1]]=newtile
#this function detects whether a move can be made or not
def endGame():
    z=1
    for i in range(0,len(rows)):
        for j in range(0,len(rows[i])):
            if rows[i][j]>0 and i>0:
                if rows[i-1][j]==rows[i][j] or rows[i-1][j]==0:
                    z=0
            if rows[i][j]>0 and j>0:
                if rows[i][j-1]==rows[i][j] or rows[i][j-1]==0:
                    z=0
            if rows[i][j]>0 and i<3:
                if rows[i+1][j]==rows[i][j] or rows[i+1][j]==0:
                    z=0
            if rows[i][j]>0 and j<3:
                if rows[i][j+1]==rows[i][j] or rows[i][j+1]==0:
                    z=0
    #if a move can be made, returns 0; else, returns 1
    return z
#this function moves all the tiles based on wihch key the player pressed
def move(d,score=score,gameOver=gameOver):
    #this variable changes to 1 if a move is made
    y=0
    #this variable records which tiles have already combined this turn
    combined=[]
    x=0
    #moves the tiles in the direction of the key press 3 times, to ensure they slide as far as possible
    while x<3:
        combine=1
        #waits for a bit so the tiles appear to "slide"
        time.sleep(0.03)
        if d=="w":
            #moves all the tiles up
            for i in range(0,len(rows)):
                for j in range(0,len(rows[i])):
                    if rows[i][j]>0 and i>0:
                        #combines two adjacent tiles if they have the same value
                        if rows[i-1][j]>0:
                            if rows[i-1][j]==rows[i][j]:
                                #a tile cannot combine twice in a move
                                for p in combined:
                                    if (p[0]==i or p[0]==i-1) and p[1]==j:
                                        combine=0
                                if combine==1:
                                    y=1
                                    rows[i-1][j]=2*rows[i][j]
                                    score=score+rows[i][j]
                                    rows[i][j]=0
                                    combined.append([i-1,j])
                        #moves the tile
                        else:
                            y=1
                            for p in range(0,len(combined)):
                                if combined[p][0]==i and combined[p][1]==j:
                                    combined[p][0]==i-1
                            rows[i-1][j]=rows[i][j]
                            rows[i][j]=0
        elif d=="a":
            #moves all the tiles left
            for i in range(0,len(rows)):
                for j in range(0,len(rows[i])):
                    if rows[i][j]>0 and j>0:
                        if rows[i][j-1]>0:
                            if rows[i][j-1]==rows[i][j]:
                                for p in combined:
                                    if (p[1]==j or p[1]==j-1) and p[0]==i:
                                        combine=0
                                if combine==1:
                                    y=1
                                    rows[i][j-1]=2*rows[i][j]
                                    score=score+rows[i][j]
                                    rows[i][j]=0
                                    combined.append([i,j-1])
                        else:
                            y=1
                            for p in range(0,len(combined)):
                                if combined[p][0]==i and combined[p][1]==j:
                                    combined[p][1]=j-1
                            rows[i][j-1]=rows[i][j]
                            rows[i][j]=0
        elif d=="s":
            #moves all the tiles down
            for i in range(len(rows)-1,-1,-1):
                for j in range(0,len(rows[i])):
                    if rows[i][j]>0 and i<3:
                        if rows[i+1][j]>0:
                            if rows[i+1][j]==rows[i][j]:
                                for p in combined:
                                    if (p[0]==i or p[0]==i+1) and p[1]==j:
                                        combine=0
                                if combine==1:
                                    y=1
                                    rows[i+1][j]=2*rows[i][j]
                                    score=score+rows[i][j]
                                    rows[i][j]=0
                                    combined.append([i+1,j])
                        else:
                            y=1
                            for p in range(0,len(combined)):
                                if combined[p][0]==i and combined[p][1]==j:
                                    combined[p][0]=i+1
                            rows[i+1][j]=rows[i][j]
                            rows[i][j]=0
        elif d=="d":
            #moves all the tiles right
            for i in range(0,len(rows)):
                for j in range(len(rows[i])-1,-1,-1):
                    if rows[i][j]>0 and j<3:
                        if rows[i][j+1]>0:
                            if rows[i][j+1]==rows[i][j]:
                                for p in combined:
                                    if (p[1]==j or p[1]==j+1) and p[0]==i:
                                        combine=0
                                if combine==1:
                                    y=1
                                    rows[i][j+1]=2*rows[i][j]
                                    score=score+rows[i][j]
                                    rows[i][j]=0
                                    combined.append([i,j+1])
                        else:
                            y=1
                            for p in range(0,len(combined)):
                                if combined[p][0]==i and combined[p][1]==j:
                                    combined[p][1]=j+1
                            rows[i][j+1]=rows[i][j]
                            rows[i][j]=0
        x+=1
        drawBoard()
    #if a move was made, then add a tile
    if y==1:
        addTile()
    drawBoard()
    #the game is over when no moves can be made
    gameOver=endGame()
    return score,gameOver
#starts the game off with 2 tiles
addTile()
addTile()
drawBoard()
while True:
    drawBoard()
    #finds which key the player pressed
    key=win.getch()
    if key==curses.KEY_UP:
        score,gameOver=move("w",score,gameOver)
    elif key==curses.KEY_DOWN:
        score,gameOver=move("s",score,gameOver)
    elif key==curses.KEY_LEFT:
        score,gameOver=move("a",score,gameOver)
    elif key==curses.KEY_RIGHT:
        score,gameOver=move("d",score,gameOver)
    #ends the program if the player pressed "x"
    if key==120:
        break
    time.sleep(0.1)
curses.nocbreak()
curses.echo()
curses.curs_set(True)
win.keypad(False)
curses.endwin()
