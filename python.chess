import pygame
import time
import sys

pygame.init()
WIDTH = 1000
HEIGHT = 900
WIN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Crazy Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

timer = pygame.time.Clock()
fps = 60
counter = 0
winner = ''
game_over = False

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight',
                 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight',
                 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []

## load images and adjust image size
dog = pygame.image.load('images/dog.png')
dog = pygame.transform.scale(dog, (95, 95))
chicken = pygame.image.load('images/chicken.png')
chicken = pygame.transform.scale(chicken, (95, 95))
w_rook = pygame.image.load('images/w_rook.png')
w_rook = pygame.transform.scale(w_rook, (85, 85))
w_knight = pygame.image.load('images/w_knight.png')
w_knight = pygame.transform.scale(w_knight, (85, 85))
w_bishop = pygame.image.load('images/w_bishop.png')
w_bishop = pygame.transform.scale(w_bishop, (85, 85))
w_king = pygame.image.load('images/w_king.png')
w_king = pygame.transform.scale(w_king, (95, 95))
w_queen = pygame.image.load('images/w_queen.png')
w_queen = pygame.transform.scale(w_queen, (85, 85))
w_pawn = pygame.image.load('images/w_pawn.png')
w_pawn = pygame.transform.scale(w_pawn, (65, 65))
w_images = [w_pawn, w_rook, w_knight, w_bishop, w_king, w_queen]
b_rook = pygame.image.load('images/b_rook.png')
b_rook = pygame.transform.scale(b_rook, (85, 85))
b_knight = pygame.image.load('images/b_knight.png')
b_knight = pygame.transform.scale(b_knight, (85, 85))
b_bishop = pygame.image.load('images/b_bishop.png')
b_bishop = pygame.transform.scale(b_bishop, (85, 85))
b_king = pygame.image.load('images/b_king.png')
b_king = pygame.transform.scale(b_king, (95, 95))
b_queen = pygame.image.load('images/b_queen.png')
b_queen = pygame.transform.scale(b_queen, (85, 85))
b_pawn = pygame.image.load('images/b_pawn.png')
b_pawn = pygame.transform.scale(b_pawn, (65, 65))
b_images = [b_pawn, b_rook, b_knight, b_bishop, b_king, b_queen]

piece_list = ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']

# draw main game board
def draw_board(board):
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(WIN, 'light gray', [600 - column * 200, row * 100, 100, 100])
        else:
            pygame.draw.rect(WIN, 'light gray', [700 - column * 200, row * 100, 100, 100])   
        pygame.draw.rect(WIN, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(WIN, 'red', [0, 800, WIDTH, 100], 5) # 5 is the border width of the rectangle
        pygame.draw.rect(WIN, 'red', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination',]
        WIN.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(WIN, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(WIN, 'black', (100 * i, 0), (100 * i, 800), 2)
        WIN.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))    

# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        if i != 3:
             WIN.blit(dog, (white_locations[i][0] * 100 + 3, white_locations[i][1] * 100 + 3))
        else:
            WIN.blit(w_king, (white_locations[i][0] * 100 + 3, white_locations[i][1] * 100 + 3))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(WIN, 'red', [white_locations[i][0]*100 + 1, white_locations[i][1]*100 + 1, 100, 100], 2)
    
    for i in range(len(black_pieces)):
        if i != 3:
             WIN.blit(chicken, (black_locations[i][0] * 100 + 3, black_locations[i][1] * 100 + 3))
        else:
             WIN.blit(b_king, (black_locations[i][0] * 100 + 3, black_locations[i][1] * 100 + 3))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(WIN, 'blue', [black_locations[i][0]*100 + 1, black_locations[i][1]*100 + 1, 100, 100], 2)

# function to check all pieces valid optiions on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        all_moves_list.append(moves_list)                    
    return all_moves_list

# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1]+1) not in white_locations and \
                (position[0], position[1]+1) not in black_locations and position[1]<7:
            moves_list.append((position[0], position[1]+1))
        if (position[0], position[1]+2) not in white_locations and \
                (position[0], position[1]+2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1]+2))
        if (position[0]+1, position[1]+1) in black_locations:
            moves_list.append((position[0]+1, position[1]+1))
        if (position[0]-1, position[1]+1) in black_locations:
            moves_list.append((position[0]-1, position[1]+1))
    else:
        if (position[0], position[1]-1) not in white_locations and \
                (position[0], position[1]-1) not in black_locations and position[1]>0:
            moves_list.append((position[0], position[1]-1))
        if (position[0], position[1]-2) not in white_locations and \
                (position[0], position[1]-2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1]-2))
        if (position[0]+1, position[1]-1) in white_locations:
            moves_list.append((position[0]+1, position[1]-1))
        if (position[0]-1, position[1]-1) in white_locations:
            moves_list.append((position[0]-1, position[1]-1))
    return moves_list

# check valid rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4): # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                   0 <= position [0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list                        

# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)    
    return moves_list

# check valid bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4): # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                   0 <= position [0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check valid queen moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list    

# check valid king moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)

    return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options        

# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(WIN, color, (moves[i][0]*100+50, moves[i][1]*100+50), 5)        

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        WIN.blit(b_images[index], (825, 5 + 50*i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        WIN.blit(w_images[index], (925, 5 + 50*i))

# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(WIN, 'dark red', [white_locations[king_index][0]*100 +1, 
                                                            white_locations[king_index][1]*100+1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(WIN, 'dark blue', [black_locations[king_index][0]*100 +1, 
                                                             black_locations[king_index][1]*100+1, 100, 100], 5)

def draw_game_over():
    pygame.draw.rect(WIN, 'black', [200, 200, 400, 70])
    WIN.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    WIN.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter +=1
    else:
        counter = 0    
    WIN.fill('dark gray')
    draw_board(WIN)
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                       turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                       black_piece = black_locations.index(click_coords)
                       captured_pieces_white.append(black_pieces[black_piece])
                       if black_pieces[black_piece] == 'king':
                           winner = 'white'
                       black_pieces.pop(black_piece)
                       black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                       turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight',
                                 'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight',
                                  'rook', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()                
    
    pygame.display.flip()
pygame.quit()


""" This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 800 x 800px
"""
pygame.display.set_caption("Two-player Chess game")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
