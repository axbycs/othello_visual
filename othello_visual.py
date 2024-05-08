import pygame
import math

pygame.init()


# Classes
class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def is_placed_here(self, x, y):
        return self.x == x and self.y == y

    def to_coordinates(self):
        return [self.x, self.y]

    def change_piece(self, color):
        self.color = color


class ValidPlay:
    def __init__(self, x, y, coordinates):
        self.x = x
        self.y = y
        self.coordinates = coordinates

    def is_placed_here(self, x, y):
        return self.x == x and self.y == y


# Global variables
BOARD_SIZE = 8
BLOCK_SIZE = 100
SCREEN_HEIGHT = BLOCK_SIZE * BOARD_SIZE
SCREEN_WIDTH = SCREEN_HEIGHT + 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GRID_COLOR = (51, 51, 51)
BACKGROUND_COLOR = (8, 148, 100, 0)
PLAYER_A = (255, 255, 255)
PLAYER_B = (0, 0, 0)
PIECE_RADIUS = 45

PIECES = []
VALID_PLAYS = []
TURN = PLAYER_B

PIECES.append(Piece(4, 4, PLAYER_A))
PIECES.append(Piece(5, 5, PLAYER_A))
PIECES.append(Piece(4, 5, PLAYER_B))
PIECES.append(Piece(5, 4, PLAYER_B))


def valid_plays(turn):
    turn_pieces = []
    not_turn_pieces = []
    blank_spaces = []
    for piece in PIECES:
        if piece.color == turn:
            turn_pieces.append(piece.to_coordinates())
        else:
            not_turn_pieces.append(piece.to_coordinates())
    for x in range(1, BOARD_SIZE + 1):
        for y in range(1, BOARD_SIZE + 1):
            if [x, y] not in turn_pieces and [x, y] not in not_turn_pieces:
                blank_spaces.append([x, y])
    for piece in turn_pieces:
        for space in blank_spaces:
            is_edible, coordinates = can_eat(
                piece[0], piece[1], space[0], space[1], not_turn_pieces
            )
            if is_edible:
                VALID_PLAYS.append(ValidPlay(space[0], space[1], coordinates))


def can_eat(x1, y1, x2, y2, not_turn_pieces):
    is_edible = True
    coordinates = []
    if x1 == x2 or y1 == y2 or abs(y2 - y1) == abs(x2 - x1):
        coordinates = generate_coordinates(x1, x2, y1, y2)
    if len(coordinates) > 0:
        for coor in coordinates:
            if coor not in not_turn_pieces:
                is_edible = False
    else:
        is_edible = False
    return is_edible, coordinates


def generate_coordinates(x1, x2, y1, y2):
    coordinates = []
    x_step = 0
    y_step = 0
    diff = abs(x1 - x2)
    if diff == 0:
        diff = abs(y1 - y2)
    if x1 - x2 > 0:
        x_step = -1
    elif x1 - x2 < 0:
        x_step = 1
    if y1 - y2 > 0:
        y_step = -1
    elif y1 - y2 < 0:
        y_step = 1
    x_aux = x1
    y_aux = y1
    for i in range(diff - 1):
        x_aux += x_step
        y_aux += y_step
        coordinates.append([x_aux, y_aux])
    return coordinates


def eat_pieces(x, y, turn):
    global PIECES
    coordinates_of_pieces_to_change = []
    for v in VALID_PLAYS:
        if v.is_placed_here(x, y):
            coordinates_of_pieces_to_change += v.coordinates
    for p in PIECES:
        for c in coordinates_of_pieces_to_change:
            if p.x == c[0] and p.y == c[1]:
                p.change_piece(turn)
    PIECES.append(Piece(x, y, turn))


def end_game(made_a_play_last_turn):
    if len(VALID_PLAYS) == 0 and not made_a_play_last_turn:
        a_pieces = []
        b_pieces = []
        for piece in PIECES:
            if piece.color == PLAYER_A:
                a_pieces.append(piece)
            else:
                b_pieces.append(piece)
        # REDO
        return True
    else:
        return False


def game_engine(x, y):
    # Initial state
    global VALID_PLAYS
    global PIECES
    made_a_play_last_turn = True
    
    # Bucle engine
    while not end_game(made_a_play_last_turn):
        if len(VALID_PLAYS) > 0:
            found = False
            for v in VALID_PLAYS:
                if v.is_placed_here(x, y):
                    found = True
            if found:
                eat_pieces(x, y, turn)
                VALID_PLAYS = []
                made_a_play_last_turn = True
                if turn == PLAYER_A:
                    turn = PLAYER_B
                else:
                    turn = PLAYER_A
        else:
            made_a_play_last_turn = False
            if turn == PLAYER_A:
                turn = PLAYER_B
            else:
                turn = PLAYER_A
        valid_plays(turn)


def draw_grid():
    for x in range(0, BOARD_SIZE * BLOCK_SIZE, BLOCK_SIZE):
        for y in range(0, BOARD_SIZE * BLOCK_SIZE, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            for p in PIECES:
                if math.ceil(x / BLOCK_SIZE) == p.x and math.ceil(y / BLOCK_SIZE) == p.y:
                    pygame.draw.circle(screen, p.color, (x - (BLOCK_SIZE/2), y - (BLOCK_SIZE/2)), PIECE_RADIUS)
            for v in VALID_PLAYS:
                if math.ceil(x / BLOCK_SIZE) == v.x and math.ceil(y / BLOCK_SIZE) == v.y:
                    pygame.draw.circle(screen, TURN, (x - (BLOCK_SIZE/2), y - (BLOCK_SIZE/2)), PIECE_RADIUS, width=2)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def draw_counter():
    pass

def get_grid_coords(pos):
    x = math.ceil(pos[0] / BLOCK_SIZE)
    y = math.ceil(pos[1] / BLOCK_SIZE)
    return [x, y]


run = True
while run:
    valid_plays(TURN)
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # print(get_grid_coords(pos))
    pygame.display.update()

pygame.quit()
