import pyxel
import random

#画面サイズ
W = 160
H = 320

fall_timer = 0
FALL_SPEED = 15


pyxel.init(W, H, title="Tetris")

pyxel.load("my_resource.pyxres")
COLS = 10
ROWS = 20
CELL = 16
OFF_X = 0
OFF_Y = 0

TETROMINO = {"I": [(0, 0), (1, 0), (2, 0), (3, 0)],                                                                            
             "O": [(0, 0), (1, 0), (0, 1), (1, 1)],                                                                            
             "T": [(0, 0), (1, 0), (2, 0), (1, 1)],                                                                            
             "S": [(1, 0), (2, 0), (0, 1), (1, 1)],                                                                            
             "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],                                                                            
             "J": [(0, 0), (0, 1), (1, 1), (2, 1)],                                                                            
             "L": [(2, 0), (0, 1), (1, 1), (2, 1)],}    

PIECE_COLOR = {"I": 12,                                                                                        
               "O": 10,   
               "T": 13,                                                                                                
               "S": 11,                                                                                                
               "Z": 8,                                                                                                   
               "J": 1,                                                                                           
               "L": 9,}        

current_type = random.choice(list(TETROMINO.keys()))                                                                  
current_x = 3                                                                                
current_y = 0                                

board = [[0 for _ in range(COLS)]for _ in range(ROWS)]

def update():
    pass
        
def draw_block(bx, by, color):                                                                                                                                                                  
       pyxel.rect(OFF_X + bx * CELL, OFF_Y + by * CELL, CELL - 1, CELL - 1, color)                                       
                                                                                                                         
def draw():                                                                                                           
       pyxel.cls(0)                                                                                                      
                                                                                                                                                                                                                        
       for y in range(ROWS + 1):                                                                                         
           pyxel.line(OFF_X, OFF_Y + y * CELL, OFF_X + COLS * CELL, OFF_Y + y * CELL, 5)                                 
       for x in range(COLS + 1):                                                                                         
           pyxel.line(OFF_X + x * CELL, OFF_Y, OFF_X + x * CELL, OFF_Y + ROWS * CELL, 5)                                 
                                                                                                                                                                                                     
       for cx, cy in TETROMINO[current_type]:                                                                            
           draw_block(current_x + cx, current_y + cy, PIECE_COLOR[current_type])                                         
                        
                         
                         
    
        
pyxel.run(update, draw)