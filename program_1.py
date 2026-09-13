import pyxel
import random

#画面サイズ
W = 160
H = 320

fall_timer = 0
score = 0
game_over = False
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

board = [[0 for _ in range(COLS)]for _ in range(ROWS)]

def clear_lines():   
    global score                                                                                                                                                     
    row = ROWS - 1                                                                                         
    while row >= 0:                                                                                       
        if all(board[row][col] != 0 for col in range(COLS)):                                                                                                
            for r in range(row, 0, -1):                                                                    
                board[r] = board[r - 1][:]                                                                 
            board[0] = [0] * COLS   
            score += 100                                                                       
        else:                                                                                              
            row -= 1  

def update():                                                                                              
       global current_x, current_y, fall_timer, game_over
       if game_over:
           if pyxel.btnp(pyxel.KEY_R):
               reset_game()
           return                                                               
                                                                                                                                                                                                        
       if pyxel.btnp(pyxel.KEY_LEFT) and can_move(-1, 0):                                                     
           current_x -= 1                                                                                     
       if pyxel.btnp(pyxel.KEY_RIGHT) and can_move(1, 0):                                                     
           current_x += 1                                                                                     
       if pyxel.btnp(pyxel.KEY_UP):                                                                           
           rotate_piece()                                                                                     
       if pyxel.btnp(pyxel.KEY_DOWN) and can_move(0, 1):                                                       
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

def reset_game():                                                                       
       global board, bag, score, game_over, current_type, current_x, current_y, fall_timer                    
       board = [[0 for _ in range(COLS)] for _ in range(ROWS)]                                                
       bag = list(TETROMINO.keys())
       random.shuffle(bag)                                                                                    
       score = 0
       game_over = False
       fall_timer = 0
       current_type = bag.pop()                                                                               
       current_x = 3
       current_y = 0                                                                                          

def peek_next():                                                                                           
       global bag
       if not bag:
           bag = list(TETROMINO.keys())
           random.shuffle(bag)
       return bag[-1]                                                                                         

def new_piece():                                                                                                                                                  
       global current_type, current_x, current_y, bag, game_over                                                       
       if not bag:
           bag = list(TETROMINO.keys())
           random.shuffle(bag)
       current_type = bag.pop()
       current_x = 3                                                                                          
       current_y = 0 
       if not can_move(0, 0):                                         
           game_over = True                 
       
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
                           pyxel.text(4, 4, "SCORE", 7)
                           pyxel.text(4, 12, str(score), 7)
                           
                           nxt = peek_next()                                                                                      
                           pyxel.rect(W - 58, 4, 54, 38, 0)                                                                       
                           pyxel.rectb(W - 58, 4, 54, 38, 7)                                                                      
                           pyxel.text(W - 50, 6, "NEXT", 7)                                                                       
                           cells = TETROMINO[nxt]                                                                                 
                           min_x = min(cx for cx, _ in cells)                                                                     
                           min_y = min(cy for _, cy in cells)                                                                     
                           for cx, cy in cells:                                                                                  
                               pyxel.rect(W - 50 + (cx - min_x) * 8, 16 + (cy - min_y) * 8, 7, 7, PIECE_COLOR[nxt])  
                               
                               if game_over:                                                                                          
                                   pyxel.rect(25, 135, 110, 55, 0)                                                                    
                                   pyxel.rectb(25, 135, 110, 55, 8)                                                                   
                                   pyxel.text(58, 147, "GAME OVER", 8)                                                                
                                   pyxel.text(38, 163, "SCORE: " + str(score), 7)                                                     
                                   pyxel.text(42, 175, "R: RESTART", 7)  
                         
                         
    
reset_game()       
pyxel.run(update, draw)