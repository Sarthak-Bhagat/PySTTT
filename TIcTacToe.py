# TTT.py
import pygame as pg
from pygame.locals import *
import random
import time, os, sys
pg.init()


pg.font.init()


GRAY = [128,128,128]
RED = [255, 0, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
WEIRD_YELLOW = [255, 255, 153]
font = pg.font.SysFont(None, 175)
size = [600, 600]
fps = 60
pos = None

def Draw(turn,screen,board):
    screen.fill(WHITE)
    for i in range(1,4):
        pg.draw.line(screen,BLACK,(0, i*size[0]/3), (size[1], i*size[0]/3), 4)
        pg.draw.line(screen,BLACK,(i*size[0]/3, 0), (i*size[0]/3,size[0]) , 4)
    small_font = pg.font.SysFont(None, 75)
    text = small_font.render(str(turn)+'\'s turn', True, BLACK)  
    text_rect = text.get_rect()
    screen.blit(text, (210,620,text_rect[2],text_rect[3]))   
    for i in range(3):
        for j in range(3):
            if board[j][i] != 0:
                x_loc = i * (size[0]/3)
                x_loc = x_loc + size[0]/6
                y_loc = j * (size[0]/3)
                y_loc = y_loc + size[0]/6
                text = font.render(str(board[int(j)][int(i)]), True, BLACK) 
                text_rect = text.get_rect()    
                text_rect.centerx = x_loc    
                text_rect.centery = y_loc    
                screen.blit(text, (text_rect[0], text_rect[1], (size[0]/3 - 9 ), (size[1]/3 - 9 )))

    
        

def select(pos,turn,screen,board):
    width = size[0]/3
    x = (pos[0] // width) 
    y = (pos[1] // width)
    if board[int(y)][int(x)] != 0:
        main(turn,board)
    x_loc = x * (size[0]/3)
    x_loc = x_loc + size[0]/6
    y_loc = y * (size[0]/3)
    y_loc = y_loc + size[0]/6
    pg.draw.rect(screen, RED,((x*width)+5 , (y*width)+5, (size[0]/3 - 9 ), (size[1]/3 - 9 )), 4)
    text = font.render(str(turn), True, GRAY) 
    text_rect = text.get_rect()    
    text_rect.centerx = x_loc    
    text_rect.centery = y_loc    
    screen.blit(text, (text_rect[0], text_rect[1], (size[0]/3 - 9 ), (size[1]/3 - 9 )))
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if mouse_pos[1] < 600:
                    Draw(turn, screen,board)
                    select(mouse_pos,turn,screen,board)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    Write(pos,turn,screen,board)
        pg.display.update()
    pos = None    
    


def Write(pos,key,screen,board):
    width = size[0]/3
    x = (pos[0] // width) 
    y = (pos[1] // width) 
    x_loc = x * (size[0]/3)
    x_loc = x_loc + size[0]/6
    y_loc = y * (size[0]/3)
    y_loc = y_loc + size[0]/6
    board[int(y)][int(x)] = key
    text = font.render(str(board[int(y)][int(x)]), True, BLACK) 
    text_rect = text.get_rect()    
    text_rect.centerx = x_loc    
    text_rect.centery = y_loc    
    screen.blit(text, (text_rect[0], text_rect[1], (size[0]/3 - 9 ), (size[1]/3 - 9 )))
    pg.display.update()
    if key == 'O':
        key = 'X'
    elif key == 'X':
        key = 'O'
    main(key,board)


def main(turn,board):
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode([600, 680])
    screen.convert()
    pg.display.set_caption('Tic Tac Toe') #pylint: disable=undefined-variable
    mouse_pos = None
    pg.init()

    
    while True:
        Draw(turn,screen,board)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                return False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if mouse_pos[1] < 600:
                    select(mouse_pos,turn,screen,board)
            if check(board) != False:
                Game_Over(check(board))
                return False

        pg.display.update()
            
                

    pg.quit()
    sys.exit()


def Game_Over(Winner):
    os.environ['SDL_VIDEO_CENTERED'] = 'True'
    screen = pg.display.set_mode([300, 300])
    font = pg.font.SysFont(None, 45)
    board = [[0 for i in range(3)] for i in range(3)]
    while True:
        for event in pg.event.get():
            screen.fill(WHITE)
            text = font.render(Winner ,1,BLACK)
            text_rect = text.get_rect()
            text_rect.center = screen.get_rect().center
            screen.blit(text, text_rect)
            replay = font.render('Replay?',True,RED)
            replay_rect = replay.get_rect()
            replay_rect.centerx = screen.get_rect().centerx
            replay_rect.centery = screen.get_rect().centery+50
            button_replay = pg.Rect(replay_rect[0], replay_rect[1], (replay_rect[2]+10), (replay_rect[3]+10)) 
            pg.draw.rect(screen, WEIRD_YELLOW, button_replay)
            pg.draw.rect(screen, BLACK, button_replay, 3) 
            screen.blit(replay, (replay_rect[0]+5, replay_rect[1]+5))
            pg.display.update()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                return False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_replay.collidepoint(mouse_pos):
                    main('X',board)


def check(grid):
    #check column 
    for j in range(3):
        if grid[0][j] == grid[1][j] and grid[0][j] == grid[2][j] and grid[0][j] != 0:
            return (str(grid[0][j])+' Wins!')
    
    #check row
    
    for i in range(3):
        if grid[i][0] == grid[i][1] and grid[i][0] == grid[i][2] and grid[i][0] != 0:
            return (str(grid[i][0])+' Wins!')

    #check diag
    if grid[0][0] == grid[1][1] and grid[0][0] == grid[2][2] and grid[0][0] != 0:
        return (str(grid[0][0])+' Wins!')
    if grid[0][2] == grid[1][1] and grid[0][2] == grid[2][0] and grid[0][2] != 0:
        return (str(grid[0][2] )+' Wins!')
    #check for draw 
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                return False
    return 'Its a Draw'

    

def TTT():
    board = [[0 for i in range(3)] for i in range(3)]
    main('X',board)