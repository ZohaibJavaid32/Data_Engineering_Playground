import pygame
import random
import sys
import math


def main():
    pygame.init()
    pygame.display.set_caption('Snake')

    BLOCK = 20
    WIDTH = 30 * BLOCK
    HEIGHT = 20 * BLOCK
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    start_ticks = pygame.time.get_ticks()

    WHITE = (245, 245, 245)
    BLACK = (10, 10, 12)
    SNAKE_HEAD = (102, 255, 178)
    SNAKE_BODY = (31, 189, 120)
    FOOD_COLOR = (255, 102, 102)
    GRID_COLOR = (30, 30, 35)

    def draw_text(text, size, color, x, y):
        f = pygame.font.SysFont(None, size)
        surf = f.render(text, True, color)
        screen.blit(surf, (x, y))

    def spawn_food(snake):
        cols = WIDTH // BLOCK
        rows = HEIGHT // BLOCK
        while True:
            x = random.randrange(0, cols) * BLOCK
            y = random.randrange(0, rows) * BLOCK
            if (x, y) not in snake:
                return (x, y)

    def reset_game():
        cols = WIDTH // BLOCK
        rows = HEIGHT // BLOCK
        start_x = (cols // 2) * BLOCK
        start_y = (rows // 2) * BLOCK
        snake = [(start_x - i * BLOCK, start_y) for i in range(3)]
        direction = (BLOCK, 0)
        food = spawn_food(snake)
        score = 0
        return snake, direction, food, score

    snake, direction, food, score = reset_game()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != (0, BLOCK):
                        direction = (0, -BLOCK)
                elif event.key == pygame.K_DOWN:
                    if direction != (0, -BLOCK):
                        direction = (0, BLOCK)
                elif event.key == pygame.K_LEFT:
                    if direction != (BLOCK, 0):
                        direction = (-BLOCK, 0)
                elif event.key == pygame.K_RIGHT:
                    if direction != (-BLOCK, 0):
                        direction = (BLOCK, 0)
                elif event.key == pygame.K_SPACE and game_over:
                    snake, direction, food, score = reset_game()
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Wrap-around at edges instead of dying
            new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
            # Check self collision
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)
                else:
                    snake.pop()

        # gradient background
        for i in range(HEIGHT):
            t = i / HEIGHT
            r = int(12 + (24 - 12) * t)
            g = int(18 + (32 - 18) * t)
            b = int(30 + (48 - 30) * t)
            pygame.draw.line(screen, (r, g, b), (0, i), (WIDTH, i))

        # subtle grid
        for gx in range(0, WIDTH, BLOCK):
            pygame.draw.line(screen, GRID_COLOR, (gx, 0), (gx, HEIGHT), 1)
        for gy in range(0, HEIGHT, BLOCK):
            pygame.draw.line(screen, GRID_COLOR, (0, gy), (WIDTH, gy), 1)

        # draw pulsing food
        fx, fy = food
        t = (pygame.time.get_ticks() - start_ticks) / 400.0
        # gentler pulse around a smaller base size
        base = int(BLOCK * 0.6)
        pulse = 1 + 0.12 * math.sin(t)
        size = max(4, int(base * pulse))
        fx_center = fx + BLOCK // 2
        fy_center = fy + BLOCK // 2
        pygame.draw.circle(screen, (255, 200, 200), (fx_center, fy_center), size // 2 + 3)
        pygame.draw.circle(screen, FOOD_COLOR, (fx_center, fy_center), size // 2)

        # draw snake with rounded rects
        for i, (x, y) in enumerate(snake):
            rect = pygame.Rect(x + 2, y + 2, BLOCK - 4, BLOCK - 4)
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, (0, 0, 0, 40), rect.inflate(4, 4), border_radius=8)
            pygame.draw.rect(screen, color, rect, border_radius=8)

        draw_text(f'Score: {score}', 26, WHITE, 10, 10)

        if game_over:
            draw_text('GAME OVER', 50, (255, 120, 120), WIDTH // 2 - 120, HEIGHT // 2 - 40)
            draw_text('Press SPACE to play again or ESC to quit', 24, WHITE, WIDTH // 2 - 220, HEIGHT // 2 + 20)

        pygame.display.flip()
        clock.tick(15)


if __name__ == '__main__':
    main()
