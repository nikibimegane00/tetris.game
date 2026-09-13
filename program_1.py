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

def clear_lines():                                                                                                                                                        
       row = ROWS - 1                                                                                         
       while row >= 0:                                                                                        
           if all(board[row][col] != 0 for col in range(COLS)):                                                                                                
               for r in range(row, 0, -1):                                                                    
                   board[r] = board[r - 1][:]                                                                 
               board[0] = [0] * COLS                                                                          
           else:                                                                                              
               row -= 1  

def update():                                                                                              
       global current_x, current_y, fall_timer                                                                
                                                                                                                                                                                                        
       if pyxel.btnp(pyxel.KEY_LEFT) and can_move(-1, 0):                                                     
           current_x -= 1                                                                                     
       if pyxel.btnp(pyxel.KEY_RIGHT) and can_move(1, 0):                                                     
           current_x += 1                                                                                     
       if pyxel.btnp(pyxel.KEY_UP):                                                                           
           rotate_piece()                                                                                     
       if pyxel.btn(pyxel.KEY_DOWN) and can_move(0, 1):                                                       
           current_y += 1                                                                                     
                                                                                                                                                                                                 
       fall_timer += 1                                                                                        
       if fall_timer >= FALL_SPEED:                                                                           
           fall_timer = 0                                                                                     
           if can_move(0, 1):                                                                                 
               current_y += 1                                                                                 
           else:                                                                                              
               place_piece()                                                                                  
               clear_lines()                                                                                  
               new_piece()               
        
def draw_block(bx, by, color):                                                                                                                                                                  
       pyxel.rect(OFF_X + bx * CELL, OFF_Y + by * CELL, CELL - 1, CELL - 1, color)      
       
bag = []

def new_piece():                                                                                                                                                  
       global current_type, current_x, current_y, bag                                                            
       if not bag:
           bag = list(TETROMINO.keys())
           random.shuffle(bag)
       current_type = bag.pop()
       current_x = 3                                                                                          
       current_y = 0               
       
def can_move(dx, dy):                                                                                                                                               
       for cx, cy in TETROMINO[current_type]:                                                                 
           nx = current_x + cx + dx                                                                           
           ny = current_y + cy + dy                                                                           
           if not (0 <= nx < COLS):                                                  
               return False                                                                                   
           if ny >= ROWS:                                                              
               return False                                                                                   
           if ny >= 0 and board[ny][nx] != 0:                                  
               return False                                                                                   
       return True           

def rotate_piece():                                                                                                                                                
       cells = TETROMINO[current_type]                                                                        
       new_cells = [(-cy, cx) for cx, cy in cells]                                                                                                                   
       min_x = min(cx for cx, _ in new_cells)                                                                 
       min_y = min(cy for _, cy in new_cells)                                                                 
       new_cells = [(cx - min_x, cy - min_y) for cx, cy in new_cells]                                                                                                    
       for cx, cy in new_cells:                                                                               
           nx = current_x + cx                                                                                
           ny = current_y + cy                                                                                
           if not (0 <= nx < COLS) or ny >= ROWS or (ny >= 0 and board[ny][nx] != 0):                         
               return                                                                                         
       TETROMINO[current_type] = new_cells                                                                             
                                                                                                              
def place_piece():                                                                                                                                        
       for cx, cy in TETROMINO[current_type]:                                                                 
           by = current_y + cy                                                                                
           bx = current_x + cx                                                                                
           if by >= 0:                                                                                        
               board[by][bx] = PIECE_COLOR[current_type]                                                                                                                                          
                                                                                                                         
def draw():                                                                                                           
       pyxel.cls(0)                                                                                                      
                                                                                                                                                                                                                        
       for y in range(ROWS + 1):                                                                                         
           pyxel.line(OFF_X, OFF_Y + y * CELL, OFF_X + COLS * CELL, OFF_Y + y * CELL, 5)                                 
       for x in range(COLS + 1):                                                                                         
           pyxel.line(OFF_X + x * CELL, OFF_Y, OFF_X + x * CELL, OFF_Y + ROWS * CELL, 5)                                 
                                                                                                                                                                                                     
       for cx, cy in TETROMINO[current_type]:                                                                            
           draw_block(current_x + cx, current_y + cy, PIECE_COLOR[current_type]) 
        
       for y in range(ROWS):                                                                                  
                   for x in range(COLS):                                                                              
                       if board[y][x] != 0:                                                                           
                           draw_block(x, y, board[y][x])                                         
                        
                         
                         
    
        
pyxel.run(update, draw)