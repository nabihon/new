import pygame
import sys
import random
import time

# 초기화
pygame.init()
beep_sound = pygame.mixer.Sound("beep.wav")

# 화면 설정
GRID_WIDTH, GRID_HEIGHT = 10, 20
CELL_SIZE = 30
PREVIEW_CELL_SIZE = 20
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE + 100, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption('Tetris')

# 색상 정의
COLORS = [
    (255, 0, 0),  # 빨간색
    (0, 255, 0),  # 초록색
    (0, 0, 255),  # 파란색
    (255, 255, 0), # 노란색
    (255, 165, 0), # 주황색
    (128, 0, 128), # 보라색
    (0, 255, 255)  # 청록색
]

# 테트로미노 모양 정의
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((self.x + x) * CELL_SIZE, (self.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # 블록 경계선

    def draw_preview(self, offset_x, offset_y):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(offset_x + x * PREVIEW_CELL_SIZE, offset_y + y * PREVIEW_CELL_SIZE, PREVIEW_CELL_SIZE, PREVIEW_CELL_SIZE)
                    pygame.draw.rect(screen, self.color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # 블록 경계선

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = (0, 0, 0) if grid[y][x] == 0 else grid[y][x]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def check_collision(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (tetromino.x + x < 0 or tetromino.x + x >= GRID_WIDTH or
                    tetromino.y + y >= GRID_HEIGHT or grid[tetromino.y + y][tetromino.x + x] != 0):
                    return True
    return False

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def handle_input(tetromino, grid, last_key_press_time, key_delay):
    keys = pygame.key.get_pressed()
    current_time = time.time()
    
    if keys[pygame.K_LEFT]:
        if current_time - last_key_press_time['left'] > key_delay:
            tetromino.x -= 1
            if check_collision(tetromino, grid):
                tetromino.x += 1
            last_key_press_time['left'] = current_time

    if keys[pygame.K_RIGHT]:
        if current_time - last_key_press_time['right'] > key_delay:
            tetromino.x += 1
            if check_collision(tetromino, grid):
                tetromino.x -= 1
            last_key_press_time['right'] = current_time

    if keys[pygame.K_DOWN]:
        tetromino.y += 1
        if check_collision(tetromino, grid):
            tetromino.y -= 1

    if keys[pygame.K_UP]:
        if current_time - last_key_press_time['up'] > key_delay:
            tetromino.rotate()
            if check_collision(tetromino, grid):
                for _ in range(3):  # 회전이 안될 경우 원상태로 복구
                    tetromino.rotate()
            last_key_press_time['up'] = current_time

def clear_lines(grid):
    full_lines = [i for i, row in enumerate(grid) if all(row)]
    for i in full_lines:
        del grid[i]
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        beep_sound.play()

def main():
    clock = pygame.time.Clock()
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    current_tetromino = Tetromino()
    next_tetromino = Tetromino()  # 다음 테트로미노 생성
    fall_time = 0
    fall_speed = 0.3  # 도형이 내려오는 속도 조절
    last_key_press_time = {'left': 0, 'right': 0, 'down': 0, 'up': 0}
    key_delay = 0.2  # 키 입력 간의 최소 간격 (초)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 입력 처리
        handle_input(current_tetromino, grid, last_key_press_time, key_delay)

        # 도형 자동으로 내려오기
        fall_time += clock.get_rawtime() / 1000
        if fall_time >= fall_speed:
            current_tetromino.y += 1
            if check_collision(current_tetromino, grid):
                current_tetromino.y -= 1
                merge_tetromino(current_tetromino, grid)
                clear_lines(grid)
                current_tetromino = next_tetromino  # 다음 테트로미노로 전환
                next_tetromino = Tetromino()  # 새로운 다음 테트로미노 생성
            fall_time = 0

        screen.fill((0, 0, 0))
        draw_grid(grid)
        current_tetromino.draw()
        next_tetromino.draw_preview(GRID_WIDTH * CELL_SIZE + 20, 20)  # 다음 테트로미노 미리보기
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
