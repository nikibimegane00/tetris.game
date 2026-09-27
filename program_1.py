import pyxel                                                                                          
import random                                                                                         
                                                                                                         
                                                                                          
W = 160                                                                                               
H = 320                                                                                               
                                                                                                         
pyxel.init(W, H, title="block blast")                                                                 
pyxel.load("my_resource.pyxres")                                                                      
                                                                                                         
                                                             
COLS = 8                                                                                              
ROWS = 8                                                                                              
CELL = 20                                                                                             
OFF_X = (W - COLS * CELL) // 2   # 0                                                                  
OFF_Y = 18                                                                                            
                                                                                                         
                                                           
SHAPES = {                                                                                            
   "dot":  [(0, 0)],                                   
   "h2":   [(0, 0), (1, 0)],                                                             
   "h3":   [(0, 0), (1, 0), (2, 0)],                                                   
   "v2":   [(0, 0), (0, 1)],                                                                
   "v3":   [(0, 0), (0, 1), (0, 2)],                                                         
   "sq2":  [(0, 0), (1, 0), (0, 1), (1, 1)],                                                 
   "r3x2": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)],                                
   "r2x3": [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)],                                  
   "sq3":  [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1),                                          
            (0, 2), (1, 2), (2, 2)],                                                       
}                                                                                                     
                                                                                                         
SHAPE_COLOR = {                                                                                       
   "dot": 7, "h2": 14, "h3": 8, "v2": 9, "v3": 11,                                                   
   "sq2": 12, "r3x2": 10, "r2x3": 3, "sq3": 6,                                                       
}                                                                                                     
                                                                                                         
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]                                               
                                                                                                         
score = 0                                                                                             
game_over = False                                                                                     
candidates = []                                                               
selected = 0                                                        
piece_x = 0                                                         
piece_y = 0                                                                                           
                                                                                                         
                                                                                                         
def shape_size(name):                                                                                 
    cells = SHAPES[name]                                                                              
    w = max(cx for cx, _ in cells) + 1                                                                
    h = max(cy for _, cy in cells) + 1                                                                
    return w, h                                                                                       
                                                                                                         
                                                                                                         
def make_candidates():                                                                                
    names = list(SHAPES.keys())                                                                       
    return [random.choice(names) for _ in range(3)]                                                   
                                                                                                         
                                                                                                         
def recenter():                                                                                       
    global piece_x, piece_y                                                                           
    w, h = shape_size(candidates[selected])                                                           
    piece_x = (COLS - w) // 2                                                                         
    piece_y = (ROWS - h) // 2                                                                         
                                                                                                         
                                                                                                         
def reset_game():                                                                                     
    global board, score, game_over, candidates, selected, used                                           
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]                                           
    score = 0                                                                                         
    game_over = False                                                                                 
    candidates = make_candidates()
    used = [False, False, False]                                                                    
    selected = 0                                                                                      
    recenter()                                                                                        
                                                                                                         
                                                                                                         
def can_place(x, y):                                                                                  
    for cx, cy in SHAPES[candidates[selected]]:                                                       
        nx = x + cx                                                                                   
        ny = y + cy                                                                                   
        if not (0 <= nx < COLS and 0 <= ny < ROWS):                                                   
            return False                                                                              
        if board[ny][nx] != 0:                                                                        
            return False                                                                              
    return True                                                                                       
                                                                                                         
                                                                                                         
def can_place_anywhere(name):                                                                         
    cells = SHAPES[name]                                                                              
    for y in range(ROWS):                                                                             
        for x in range(COLS):                                                                         
            ok = True                                                                                 
            for cx, cy in cells:                                                                      
                nx = x + cx                                                                           
                ny = y + cy                                                                           
                if not (0 <= nx < COLS and 0 <= ny < ROWS):                                           
                    ok = False                                                                        
                    break                                                                             
                if board[ny][nx] != 0:                                                                
                    ok = False                                                                        
                    break                                                                             
            if ok:                                                                                    
                return True                                                                           
    return False                                                                                      
                                                                                                         
                                                                                                         
def clear_full_lines():                                                                               
    global score                                                                                      
    full_rows = [y for y in range(ROWS) if all(board[y][x] != 0 for x in range(COLS))]                
    full_cols = [x for x in range(COLS) if all(board[y][x] != 0 for y in range(ROWS))]                
    for y in full_rows:                                                                               
        for x in range(COLS):                                                                         
            board[y][x] = 0                                                                           
    for x in full_cols:                                                                               
        for y in range(ROWS):                                                                         
            board[y][x] = 0                                                                           
    score += (len(full_rows) + len(full_cols)) * 100                                                  
                                                                                                         
                                                                                                         
def place_piece():                                                                                    
    global candidates, selected, game_over, used                                                          
    color = SHAPE_COLOR[candidates[selected]]                                                         
    for cx, cy in SHAPES[candidates[selected]]:                                                       
        board[piece_y + cy][piece_x + cx] = color                                                     
    clear_full_lines()                                                                                                                                                          
    
    used[selected] = True
    
    if all(used):                                                                           
           candidates = make_candidates()                                                    
           used = [False, False, False]                                                          
           selected = 0                                                                                                  
           recenter()                                                                                                    
    else:                                                                                   
        selected = next(i for i in range(3) if not used[i])                                                           
        recenter()                                                                                                    
                                                                                                                         
    remaining = [name for i, name in enumerate(candidates) if not used[i]]                                            
    if remaining and not any(can_place_anywhere(name) for name in remaining):                                         
        game_over = True                                                                
                                                           
                                                                                                         
                                                                                                         
def update():                                                                                         
    global selected, piece_x, piece_y                                                                 
    if game_over:                                                                                     
        if pyxel.btnp(pyxel.KEY_R):                                                                   
            reset_game()                                                                              
        return                                                                                        
                                                                                                                                                                            
    if pyxel.btnp(pyxel.KEY_1) and not used[0]:                                                                       
        selected = 0                                                                                  
        recenter()                                                                                    
    if pyxel.btnp(pyxel.KEY_2) and not used[1]:                                                                       
        selected = 1                                                                                  
        recenter()                                                                                    
    if pyxel.btnp(pyxel.KEY_3) and not used[2]:                                                                       
        selected = 2                                                                                  
        recenter()                                                                                    
                                                                                                                                                                                         
    if pyxel.btnp(pyxel.KEY_LEFT):                                                                    
        piece_x -= 1                                                                                  
    if pyxel.btnp(pyxel.KEY_RIGHT):                                                                   
        piece_x += 1                                                                                  
    if pyxel.btnp(pyxel.KEY_UP):                                                                      
        piece_y -= 1                                                                                  
    if pyxel.btnp(pyxel.KEY_DOWN):                                                                    
        piece_y += 1                                                                                  
                                                                                                                                                                          
    w, h = shape_size(candidates[selected])                                                           
    piece_x = max(0, min(piece_x, COLS - w))                                                          
    piece_y = max(0, min(piece_y, ROWS - h))                                                          
                                                                                                         
                                                                                                                                                                                          
    if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):                                    
        if can_place(piece_x, piece_y):                                                               
            place_piece()                                                                             
                                                                                                         
                                                                                                         
def draw_block(bx, by, color):                                                                        
    pyxel.rect(OFF_X + bx * CELL, OFF_Y + by * CELL, CELL - 1, CELL - 1, color)                       
                                                                                                         
                                                                                                         
def draw_candidate(i, name):                                                                          
    sx = 2 + i * 52                                                             
    sy = 200                                                                          
    sel = (i == selected)                                                                             
    color = SHAPE_COLOR[name]                                                                         
                                                                                                                                                            
    pyxel.rectb(sx, sy, 52, 78, 14 if sel else 5)                                                     
    pyxel.text(sx + 2, sy + 2, str(i + 1), 14 if sel else 7)                                          
                                                                                                                                                                                            
    cells = SHAPES[name]                                                                              
    w, h = shape_size(name)                                                                           
    p = 10                                                             
    cx0 = sx + (52 - w * p) // 2                                                                      
    cy0 = sy + 16 + (62 - h * p) // 2                                                                 
    for cx, cy in cells:                                                                              
        pyxel.rect(cx0 + cx * p, cy0 + cy * p, p - 1, p - 1, color)                                   
                                                                                                         
                                                                                                         
def draw():                                                                                           
    pyxel.cls(0)                                                                                      
                                                                                                                                                                                                   
    pyxel.text(4, 4, "SCORE", 7)                                                                      
    pyxel.text(4, 12, str(score), 10)                                                                 
                                                                                                                                                                                     
    for y in range(ROWS + 1):                                                                         
        pyxel.line(OFF_X, OFF_Y + y * CELL, OFF_X + COLS * CELL, OFF_Y + y * CELL, 5)                 
    for x in range(COLS + 1):                                                                         
        pyxel.line(OFF_X + x * CELL, OFF_Y, OFF_X + x * CELL, OFF_Y + ROWS * CELL, 5)                 
                                                                                                         
                                                                                                                                                                               
    for y in range(ROWS):                                                                             
        for x in range(COLS):                                                                         
            if board[y][x] != 0:                                                                      
                draw_block(x, y, board[y][x])                                                         
                                                                                                         
                                                                                                                                                         
    for cx, cy in SHAPES[candidates[selected]]:                                                       
        pyxel.rectb(OFF_X + (piece_x + cx) * CELL, OFF_Y + (piece_y + cy) * CELL,                     
                    CELL, CELL, SHAPE_COLOR[candidates[selected]])                                    
                                                                                                                                                                                           
    pyxel.text(4, 186, "1/2/3 えらぶ", 6)                                                             
    pyxel.text(86, 186, "SPACE おく", 6)                                                              
                                                                                                                                                                                             
    for i, name in enumerate(candidates):                                                             
        draw_candidate(i, name)                                                                       
                                                                                                         
                                                                                                                                                                                        
    if game_over:                                                                                     
        pyxel.rect(25, 70, 110, 55, 0)                                                                
        pyxel.rectb(25, 70, 110, 55, 8)                                                               
        pyxel.text(50, 82, "GAME OVER", 8)                                                            
        pyxel.text(38, 98, "SCORE: " + str(score), 7)                                                 
        pyxel.text(42, 110, "R: RESTART", 7)                                                          
                                                                                                         
                                                                                                         
reset_game()                                                                                          
pyxel.run(update, draw) 