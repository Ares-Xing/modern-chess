import pygame
import sys
import random

WIDTH, HEIGHT = 640, 640
SQ_SIZE = WIDTH // 8
FPS = 30

WHITE = (240, 240, 240)
BLACK = (40, 40, 40)
BLUE = (70, 130, 180)
GREEN = (60, 180, 75)
YELLOW = (255, 255, 150)
GREY = (150, 150, 150)

PIECE_TYPES = ["K", "Q", "R", "B", "N", "P"]
MORPH_TYPES = ["Q", "R", "B", "N", "P"]
PIECE_IMAGE_SIZE = int(SQ_SIZE * 1.0)
BACK_ROW_ORDER = ["R", "N", "B", "Q", "K", "B", "N", "R"]
PIECE_COUNTS = {"Q":1, "R":2, "B":2, "N":2, "P":8}

PIECE_SYMBOLS = {
    ("w", "K"): "♔", ("w", "Q"): "♕", ("w", "R"): "♖",
    ("w", "B"): "♗", ("w", "N"): "♘", ("w", "P"): "♙",
    ("b", "K"): "♚", ("b", "Q"): "♛", ("b", "R"): "♜",
    ("b", "B"): "♝", ("b", "N"): "♞", ("b", "P"): "♟",
}

def get_builtin_piece_images():
    pygame.font.init()
    font = pygame.font.SysFont("Apple Symbols", PIECE_IMAGE_SIZE)
    piece_images = {}
    for key, symbol in PIECE_SYMBOLS.items():
        surf = pygame.Surface((PIECE_IMAGE_SIZE, PIECE_IMAGE_SIZE), pygame.SRCALPHA)
        color = (0, 0, 0) if key[0] == "w" else (30, 30, 160)
        text_surface = font.render(symbol, True, color)
        rect = text_surface.get_rect(center=(PIECE_IMAGE_SIZE // 2, PIECE_IMAGE_SIZE // 2))
        surf.blit(text_surface, rect)
        piece_images[key] = surf
    return piece_images

class Piece:
    def __init__(self, color, name, image, start_pos=None):
        self.color = color
        self.name = name  # Actual type (after morph)
        self.revealed = False
        self.image = image
        self.start_pos = start_pos
        self.has_moved = False
        self.morph_pending = True if name != "K" else False  # King never morphs

    def __repr__(self):
        if self.revealed or self.name == "K":
            return f"{self.color}{self.name}"
        else:
            return "??"

class MorphCounter:
    """Tracks how many of each non-King piece for each color have been assigned."""
    def __init__(self):
        self.counts = {
            "w": {"Q":0, "R":0, "B":0, "N":0, "P":0},
            "b": {"Q":0, "R":0, "B":0, "N":0, "P":0}
        }
        self.max_counts = PIECE_COUNTS.copy()

    def add(self, color, kind):
        assert kind in self.max_counts
        self.counts[color][kind] += 1

    def can_assign(self, color, kind):
        return self.counts[color][kind] < self.max_counts[kind]

    def assign_random(self, color):
        """Randomly pick a type not exceeding the quota."""
        choices = [k for k in MORPH_TYPES if self.can_assign(color, k)]
        if not choices:
            # Should never happen if quota is maintained
            return "P"
        kind = random.choice(choices)
        self.add(color, kind)
        return kind

class JiangQiBoard:
    PIECES = [
        ("Q", 1), ("R", 2), ("B", 2), ("N", 2), ("P", 8)
    ]
    def __init__(self, piece_images):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "w"
        self.selected = None
        self.piece_images = piece_images
        self.captured_white = []
        self.captured_black = []
        self.game_over = False
        self.winner = None
        self.morph_counter = {"w": MorphCounter(), "b": MorphCounter()}
        self.init_pieces()

    def init_pieces(self):
        self.board[7][4] = Piece("w", "K", self.piece_images[("w", "K")], (7, 4))
        self.board[0][4] = Piece("b", "K", self.piece_images[("b", "K")], (0, 4))
        self.board[7][4].revealed = True
        self.board[0][4].revealed = True
        self.board[7][4].has_moved = False
        self.board[0][4].has_moved = False
        self.board[7][4].morph_pending = False
        self.board[0][4].morph_pending = False

        w_pool = []
        b_pool = []
        for name, count in self.PIECES:
            w_pool.extend([Piece("w", "?", None) for _ in range(count)])
            b_pool.extend([Piece("b", "?", None) for _ in range(count)])
        random.shuffle(w_pool)
        random.shuffle(b_pool)

        for col, name in enumerate(BACK_ROW_ORDER):
            if name == "K":
                continue
            # 白后排
            if w_pool:
                p = w_pool.pop()
                p.start_pos = (7, col)
                self.board[7][col] = p
            # 黑后排
            if b_pool:
                p = b_pool.pop()
                p.start_pos = (0, col)
                self.board[0][col] = p
        for col in range(8):
            if w_pool:
                p = w_pool.pop()
                p.start_pos = (6, col)
                self.board[6][col] = p
        for col in range(8):
            if b_pool:
                p = b_pool.pop()
                p.start_pos = (1, col)
                self.board[1][col] = p
        for row in range(2, 6):
            for col in range(8):
                self.board[row][col] = None

    def inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def move(self, from_pos, to_pos):
        if self.game_over:
            return False, "Game over"

        fx, fy = from_pos
        tx, ty = to_pos
        piece = self.board[fx][fy]
        if not piece:
            return False, "no pieces"
        if piece.color != self.turn:
            return False, "It's not your turn"
        dest = self.board[tx][ty]
        if dest and dest.color == self.turn:
            return False, "Can't capture your pieces"

        # Capture rule
        captured = None
        king_captured = False
        if dest and dest.color != piece.color:
            captured = dest
            if captured.name == "K":
                king_captured = True
                self.game_over = True
                self.winner = "White" if piece.color == "w" else "Black"
            if captured.color == "w":
                self.captured_white.append(self.reveal_identity_on_capture(captured, "w"))
            else:
                self.captured_black.append(self.reveal_identity_on_capture(captured, "b"))
            self.board[tx][ty] = None

        # Check valid move
        valid, reason = self.is_legal_move(piece, (fx, fy), (tx, ty), capture=bool(captured))
        if not valid:
            if captured:
                if captured.color == "w":
                    self.captured_white.pop()
                else:
                    self.captured_black.pop()
                self.board[tx][ty] = captured
            return False, reason

        # Finish movements
        self.board[tx][ty] = piece
        self.board[fx][fy] = None

        # Reveal pieces after the fir move
        if piece.morph_pending and not piece.has_moved:
            kind = self.morph_counter[piece.color].assign_random(piece.color)
            piece.name = kind
            piece.image = self.piece_images[(piece.color, kind)]
            piece.revealed = True
            piece.morph_pending = False
        elif not piece.revealed and piece.name != "K":
            piece.revealed = True
        piece.has_moved = True

        if king_captured:
            return True, f"{self.winner}Winer！"

        self.turn = "b" if self.turn == "w" else "w"
        return True, ""

    def is_legal_move(self, piece, from_pos, to_pos, capture=False):
        fx, fy = from_pos
        tx, ty = to_pos
        dx, dy = tx - fx, ty - fy
        abs_dx, abs_dy = abs(dx), abs(dy)

        if (fx, fy) == (tx, ty):
            return False, "Make a move"

        # First move：can capture any enemies
        if piece.morph_pending and not piece.has_moved:
            rule_name = self.get_square_rule(piece)
            return self.check_move_by_rule(rule_name, piece, from_pos, to_pos, ignore_target=True)
        # Reveal pieces
        return self.check_move_by_rule(piece.name, piece, from_pos, to_pos, ignore_target=False)

    def get_square_rule(self, piece):
        row, col = piece.start_pos
        if row not in [0, 1, 6, 7]:
            return "P"
        if row in [0, 7]:
            return BACK_ROW_ORDER[col]
        else:
            return "P"

    def check_move_by_rule(self, rule_name, piece, from_pos, to_pos, ignore_target=False):
        fx, fy = from_pos
        tx, ty = to_pos
        dx, dy = tx - fx, ty - fy
        abs_dx, abs_dy = abs(dx), abs(dy)
        dest = self.board[tx][ty]

        if ignore_target:
            if dest and dest.color == piece.color:
                return False, "Can't capture your pieces"
        else:
            if dest and dest.color == piece.color:
                return False, "Can't capture your pieces"

        if rule_name == "K":
            if max(abs_dx, abs_dy) == 1:
                return True, ""
            return False, "King only can move one grid"
        elif rule_name == "Q":
            if dx == 0 or dy == 0 or abs_dx == abs_dy:
                if not self.is_blocked(from_pos, to_pos):
                    return True, ""
                return False, "blocked"
            return False, "Queen's move not right"
        elif rule_name == "R":
            if dx == 0 or dy == 0:
                if not self.is_blocked(from_pos, to_pos):
                    return True, ""
                return False, "blocked"
            return False, "Rook's move not right'"
        elif rule_name == "B":
            if abs_dx == abs_dy:
                if not self.is_blocked(from_pos, to_pos):
                    return True, ""
                return False, "blocked"
            return False, "Bishop's move not right'"
        elif rule_name == "N":
            if (abs_dx, abs_dy) in [(2, 1), (1, 2)]:
                return True, ""
            return False, "Knight's move not right'"
        elif rule_name == "P":
            direction = -1 if piece.color == "w" else 1
            start_row = 6 if piece.color == "w" else 1
            # 直走
            if fy == ty and tx - fx == direction and (ignore_target or self.board[tx][ty] is None):
                return True, ""
            # 首次走两格
            if fy == ty and fx == start_row and tx - fx == 2 * direction and (ignore_target or (self.board[fx + direction][fy] is None and self.board[tx][ty] is None)):
                return True, ""
            # 吃子
            if abs(dy) == 1 and tx - fx == direction and (ignore_target or (self.board[tx][ty] is not None and self.board[tx][ty].color != piece.color)):
                return True, ""
            return False, "Pawn's move not right'"
        return False, "Invilid move"

    def is_blocked(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        dx, dy = tx - fx, ty - fy
        step_x = (dx > 0) - (dx < 0)
        step_y = (dy > 0) - (dy < 0)
        cur_x, cur_y = fx + step_x, fy + step_y
        while (cur_x, cur_y) != (tx, ty):
            if self.board[cur_x][cur_y] is not None:
                return True
            cur_x += step_x
            cur_y += step_y
        return False

    def reveal_identity_on_capture(self, piece, color):
        # If the captured piece is not yet assigned a type, assign it now (for display in capture area)
        if piece.morph_pending:
            kind = self.morph_counter[color].assign_random(color)
            piece.name = kind
            piece.image = self.piece_images[(color, kind)]
            piece.revealed = True
            piece.morph_pending = False
        else:
            piece.revealed = True
        return piece

def draw_board(screen, board: JiangQiBoard):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREY
            pygame.draw.rect(screen, color, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if board.selected == (row, col):
                pygame.draw.rect(screen, YELLOW, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)
            piece = board.board[row][col]
            if piece:
                if piece.revealed or piece.name == "K":
                    img = piece.image
                    rect = img.get_rect(center=(col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2))
                    screen.blit(img, rect)
                else:
                    pygame.draw.circle(screen, GREEN if piece.color == "w" else BLUE,
                                       (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2), SQ_SIZE // 3)

    # Captured pieces zone（white in left，black in right）
    y = HEIGHT - 80
    x_white = 10
    x_black = WIDTH - 10 - PIECE_IMAGE_SIZE
    for p in board.captured_white:
        screen.blit(p.image, (x_white, y))
        x_white += PIECE_IMAGE_SIZE // 2
    for p in board.captured_black:
        screen.blit(p.image, (x_black, y))
        x_black -= PIECE_IMAGE_SIZE // 2

def pos_from_mouse(pos):
    mx, my = pos
    return my // SQ_SIZE, mx // SQ_SIZE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Surprise Chess")
    font = pygame.font.SysFont("arial", SQ_SIZE // 2)
    clock = pygame.time.Clock()
    piece_images = get_builtin_piece_images()
    board = JiangQiBoard(piece_images)
    msg = ""
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        draw_board(screen, board)

        info_font = pygame.font.SysFont("arial", 22)
        if board.game_over:
            end_msg = f"Game over！{board.winner} Win！"
            msg_text = info_font.render(end_msg, True, (255, 0, 0))
            screen.blit(msg_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
        else:
            msg_text = info_font.render(msg, True, (200, 20, 20))
            screen.blit(msg_text, (10, HEIGHT - 30))
            turn_text = info_font.render("White's turn" if board.turn == "w" else "Black's turn", True, (30, 30, 200))
            screen.blit(turn_text, (WIDTH - 130, HEIGHT - 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not board.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pos_from_mouse(event.pos)
                if not board.inside(row, col): continue
                if board.selected is None:
                    piece = board.board[row][col]
                    if piece and piece.color == board.turn:
                        board.selected = (row, col)
                else:
                    from_pos = board.selected
                    to_pos = (row, col)
                    ok, reason = board.move(from_pos, to_pos)
                    if not ok:
                        msg = reason
                    else:
                        msg = ""
                    board.selected = None

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()