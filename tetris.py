import pygame
import random

# Game constants
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS

# Tetromino shapes with rotation states
SHAPES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1], [1, 1]]
    ],
    'T': [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]]
    ],
    'S': [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]]
    ],
    'Z': [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]]
    ],
    'J': [
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]]
    ],
    'L': [
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]]
    ]
}

# Colors for pieces
COLORS = {
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (240, 160, 0)
}

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.rotations = SHAPES[shape]
        self.rotation = 0
        self.x = COLUMNS // 2 - len(self.matrix()[0]) // 2
        self.y = 0

    def matrix(self):
        return self.rotations[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.rotations)
        if self.collides(0, 0):
            self.rotation = (self.rotation - 1) % len(self.rotations)

    def collides(self, dx, dy):
        for y, row in enumerate(self.matrix()):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.x + x + dx
                    ny = self.y + y + dy
                    if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                        return True
                    if ny >= 0 and board[ny][nx]:
                        return True
        return False

    def lock(self):
        for y, row in enumerate(self.matrix()):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    board[self.y + y][self.x + x] = self.shape

board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

current = Tetromino(random.choice(list(SHAPES.keys())))
fall_time = 0
fall_speed = 500  # milliseconds

running = True
while running:
    dt = clock.tick(60)
    fall_time += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not current.collides(-1, 0):
                current.x -= 1
            elif event.key == pygame.K_RIGHT and not current.collides(1, 0):
                current.x += 1
            elif event.key == pygame.K_DOWN and not current.collides(0, 1):
                current.y += 1
            elif event.key == pygame.K_UP:
                current.rotate()

    if fall_time >= fall_speed:
        fall_time = 0
        if not current.collides(0, 1):
            current.y += 1
        else:
            current.lock()
            lines_to_clear = [i for i, row in enumerate(board) if all(row)]
            for i in lines_to_clear:
                del board[i]
                board.insert(0, [None for _ in range(COLUMNS)])
            current = Tetromino(random.choice(list(SHAPES.keys())))
            if current.collides(0, 0):
                running = False

    window.fill((0, 0, 0))
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    window,
                    COLORS[cell],
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    for y, row in enumerate(current.matrix()):
        for x, cell in enumerate(row):
            if cell and current.y + y >= 0:
                pygame.draw.rect(
                    window,
                    COLORS[current.shape],
                    ((current.x + x) * CELL_SIZE, (current.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )
    pygame.display.flip()

pygame.quit()
