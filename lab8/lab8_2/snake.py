import pygame
import random
import time

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score and level display
font = pygame.font.SysFont('arial', 20)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Start at center
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        self.level = 1
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Check for self-collision
        if new_head in self.positions[1:]:
            return True  # Game over
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False  # Game continues
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        self.level = 1
    
    def render(self, surface):
        for i, p in enumerate(self.positions):
            # Head is green, body is blue
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Border

class Food:
    def __init__(self, snake_positions):
        self.position = (0, 0)
        self.randomize_position(snake_positions)
    
    def randomize_position(self, snake_positions):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                            random.randint(0, GRID_HEIGHT - 1))
            # Make sure food doesn't spawn on snake or walls
            if self.position not in snake_positions:
                break
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

def show_info(surface, score, level):
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    surface.blit(score_text, (5, 5))
    surface.blit(level_text, (5, 30))

def game_over_screen(surface, score):
    surface.fill(WHITE)
    game_over_font = pygame.font.SysFont('arial', 50)
    score_font = pygame.font.SysFont('arial', 30)
    
    game_over_text = game_over_font.render("Game Over!", True, RED)
    score_text = score_font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to restart or Q to quit", True, BLACK)
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart
                if event.key == pygame.K_q:
                    return False  # Quit
    return False

def main():
    snake = Snake()
    food = Food(snake.positions)
    running = True
    
    while running:
        # Event handling
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
        
        # Game logic
        game_over = snake.update()
        
        # Check if snake hit the wall (optional - depends on game design)
        # head = snake.get_head_position()
        # if head[0] == 0 or head[0] == GRID_WIDTH-1 or head[1] == 0 or head[1] == GRID_HEIGHT-1:
        #     game_over = True
        
        if game_over:
            if game_over_screen(screen, snake.score):
                snake.reset()
                food.randomize_position(snake.positions)
                continue
            else:
                break
        
        # Check if snake ate food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            
            # Level up every 3 foods
            if snake.score % 3 == 0:
                snake.level += 1
                global FPS
                FPS += 2  # Increase speed
            
            food.randomize_position(snake.positions)
        
        # Drawing
        screen.fill(WHITE)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        show_info(screen, snake.score, snake.level)
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()