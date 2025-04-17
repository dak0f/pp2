import pygame
import random
import time
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="snake_game",
    user="postgres",       # замени на своего юзера
    password="add20070701",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS game_records (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50),
    score INTEGER,
    level INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# Pygame init
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
YELLOW, PURPLE = (255, 255, 0), (128, 0, 128)
WIDTH, HEIGHT, GRID = 600, 600, 20
GRID_W, GRID_H = WIDTH // GRID, HEIGHT // GRID
FPS = 10
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
FOOD_TYPES = [
    {"color": RED, "weight": 1, "lifetime": None, "spawn_chance": 70},
    {"color": YELLOW, "weight": 2, "lifetime": 8, "spawn_chance": 20},
    {"color": PURPLE, "weight": 3, "lifetime": 5, "spawn_chance": 10}
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with PostgreSQL")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)

class Snake:
    def __init__(self):
        self.positions = [(GRID_W // 2, GRID_H // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        self.level = 1

    def get_head(self):
        return self.positions[0]

    def update(self):
        head = self.get_head()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_W, (head[1] + y) % GRID_H)
        if new_head in self.positions[1:]:
            return True
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return False

    def reset(self):
        self.__init__()

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect(p[0]*GRID, p[1]*GRID, GRID, GRID)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self, snake_pos):
        self.position = (0, 0)
        self.type = None
        self.spawn_time = 0
        self.spawn(snake_pos)

    def spawn(self, snake_pos):
        while True:
            self.position = (random.randint(0, GRID_W-1), random.randint(0, GRID_H-1))
            if self.position not in snake_pos:
                break
        weights = [f["spawn_chance"] for f in FOOD_TYPES]
        self.type = random.choices(FOOD_TYPES, weights=weights)[0]
        self.spawn_time = time.time()

    def expired(self):
        if self.type["lifetime"] is None:
            return False
        return (time.time() - self.spawn_time) > self.type["lifetime"]

    def render(self, surface):
        rect = pygame.Rect(self.position[0]*GRID, self.position[1]*GRID, GRID, GRID)
        pygame.draw.rect(surface, self.type["color"], rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        if self.type["lifetime"]:
            remaining = max(0, self.type["lifetime"] - (time.time() - self.spawn_time))
            txt = font.render(f"{int(remaining)}", True, BLACK)
            surface.blit(txt, (rect.x + 4, rect.y + 2))

def draw_grid(surface):
    for x in range(0, WIDTH, GRID):
        for y in range(0, HEIGHT, GRID):
            rect = pygame.Rect(x, y, GRID, GRID)
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

def draw_info(surface, score, level):
    surface.blit(font.render(f"Score: {score}", True, BLACK), (5, 5))
    surface.blit(font.render(f"Level: {level}", True, BLACK), (5, 30))

def draw_leaderboard(surface):
    cursor.execute("SELECT player_name, score FROM game_records ORDER BY score DESC LIMIT 5")
    records = cursor.fetchall()
    title = font.render("Top 5 Scores:", True, BLACK)
    surface.blit(title, (WIDTH - 180, 5))
    for i, (name, score) in enumerate(records):
        line = font.render(f"{i+1}. {name}: {score}", True, BLACK)
        surface.blit(line, (WIDTH - 180, 30 + i*25))

def game_over_screen(surface, score):
    surface.fill(WHITE)
    big_font = pygame.font.SysFont('arial', 40)
    game_over_text = big_font.render("Game Over!", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    prompt = font.render("Enter name: ", True, BLACK)
    surface.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 60))
    surface.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 - 20))
    surface.blit(prompt, (WIDTH//2 - 80, HEIGHT//2 + 20))
    pygame.display.update()

    name = ""
    typing = True
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15:
                    name += event.unicode
        surface.fill(WHITE)
        surface.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 60))
        surface.blit(score_text, (WIDTH//2 - 50, HEIGHT//2 - 20))
        surface.blit(prompt, (WIDTH//2 - 80, HEIGHT//2 + 20))
        input_text = font.render(name, True, BLUE)
        surface.blit(input_text, (WIDTH//2 + 20, HEIGHT//2 + 20))
        pygame.display.update()

def main():
    global FPS
    snake = Snake()
    food = Food(snake.positions)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        if snake.update():
            name = game_over_screen(screen, snake.score)
            if name:
                cursor.execute(
                    "INSERT INTO game_records (player_name, score, level) VALUES (%s, %s, %s)",
                    (name, snake.score, snake.level)
                )
                conn.commit()
                snake.reset()
                food.spawn(snake.positions)
                FPS = 10
                continue
            else:
                break

        if food.expired():
            food.spawn(snake.positions)

        if snake.get_head() == food.position:
            snake.length += food.type["weight"]
            snake.score += food.type["weight"]
            if snake.score // 5 > snake.level - 1:
                snake.level += 1
                FPS += 2
            food.spawn(snake.positions)

        screen.fill(WHITE)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        draw_info(screen, snake.score, snake.level)
        draw_leaderboard(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    conn.close()

if __name__ == "__main__":
    main()
