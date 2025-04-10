import pygame
import random
import time

# Initialize pygame
pygame.init()

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Game configuration constants
WIDTH, HEIGHT = 600, 600          # Game window dimensions
GRID_SIZE = 20                     # Size of each grid cell
GRID_WIDTH = WIDTH // GRID_SIZE    # Number of grid cells horizontally
GRID_HEIGHT = HEIGHT // GRID_SIZE  # Number of grid cells vertically
FPS = 10                           # Initial frames per second (game speed)

# Movement directions (x, y coordinates)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Food type configurations
FOOD_TYPES = [
    # Normal food (most common, no timer)
    {"color": RED, "weight": 1, "lifetime": None, "spawn_chance": 70},
    # Bonus food (medium value, disappears after 8 seconds)
    {"color": YELLOW, "weight": 2, "lifetime": 8, "spawn_chance": 20},
    # Premium food (high value, disappears quickly after 5 seconds)
    {"color": PURPLE, "weight": 3, "lifetime": 5, "spawn_chance": 10}
]

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Snake Game")
clock = pygame.time.Clock()

# Font setup for UI elements
font = pygame.font.SysFont('arial', 20)

class Snake:
    """Class representing the snake player"""
    
    def __init__(self):
        """Initialize snake with default starting position and properties"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # Center position
        self.direction = RIGHT      # Initial movement direction
        self.length = 1             # Starting length
        self.score = 0              # Player score
        self.level = 1              # Current level
        
    def get_head_position(self):
        """Return the current position of the snake's head"""
        return self.positions[0]
    
    def update(self):
        """
        Update snake position based on current direction
        Returns True if game over (collision), False otherwise
        """
        head = self.get_head_position()
        x, y = self.direction
        # Calculate new head position with wrap-around at screen edges
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Check for self-collision (game over condition)
        if new_head in self.positions[1:]:
            return True
        
        # Move snake by adding new head position
        self.positions.insert(0, new_head)
        # Remove tail segment if not growing
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return False
    
    def reset(self):
        """Reset snake to initial state for new game"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
        self.level = 1
    
    def render(self, surface):
        """Draw the snake on the game surface"""
        for i, p in enumerate(self.positions):
            # Head is green, body segments are blue
            color = GREEN if i == 0 else BLUE
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), 
                             (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Add border

class Food:
    """Class representing the food items"""
    
    def __init__(self, snake_positions):
        """
        Initialize food with random position and type
        snake_positions: list of positions to avoid when spawning
        """
        self.position = (0, 0)
        self.type = None
        self.spawn_time = 0
        self.randomize_position(snake_positions)
    
    def randomize_position(self, snake_positions):
        """Place food at random position not occupied by snake"""
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                           random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break
        
        # Choose food type weighted by spawn_chance values
        weights = [ft["spawn_chance"] for ft in FOOD_TYPES]
        self.type = random.choices(FOOD_TYPES, weights=weights)[0]
        self.spawn_time = time.time()  # Record spawn time for timed foods
    
    def should_disappear(self):
        """Check if timed food should disappear based on elapsed time"""
        if self.type["lifetime"] is None:
            return False  # Permanent food doesn't disappear
        return (time.time() - self.spawn_time) > self.type["lifetime"]
    
    def render(self, surface):
        """Draw food on game surface with appropriate color and timer"""
        rect = pygame.Rect((self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE), 
                         (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.type["color"], rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Add border
        
        # Display countdown for timed foods
        if self.type["lifetime"] is not None:
            remaining = max(0, self.type["lifetime"] - (time.time() - self.spawn_time))
            timer_text = font.render(f"{int(remaining)}", True, BLACK)
            surface.blit(timer_text, (rect.x + 5, rect.y + 2))

def draw_grid(surface):
    """Draw the background grid lines"""
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # Grid lines

def show_game_info(surface, score, level):
    """Display score and level information in the game UI"""
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    surface.blit(score_text, (5, 5))
    surface.blit(level_text, (5, 30))

def show_game_over(surface, score):
    """
    Display game over screen and handle restart/quit options
    Returns True if player wants to restart, False to quit
    """
    surface.fill(WHITE)
    
    # Create text surfaces
    game_over_font = pygame.font.SysFont('arial', 50)
    score_font = pygame.font.SysFont('arial', 30)
    
    game_over_text = game_over_font.render("Game Over!", True, RED)
    score_text = score_font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to restart or Q to quit", True, BLACK)
    
    # Position and draw text elements
    surface.blit(game_over_text, 
                (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    surface.blit(score_text, 
                (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    surface.blit(restart_text, 
                (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.update()
    
    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
                if event.key == pygame.K_q:
                    return False  # Quit game

def main():
    """Main game loop and logic"""
    
    # Initialize game objects
    snake = Snake()
    food = Food(snake.positions)
    running = True
    
    while running:
        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Change direction with arrow keys (no 180-degree turns)
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
        
        # Update snake position and check for collisions
        game_over = snake.update()
        
        if game_over:
            # Show game over screen and handle restart/quit
            if show_game_over(screen, snake.score):
                snake.reset()
                food.randomize_position(snake.positions)
                continue
            else:
                break
        
        # Check if current food should disappear (timed foods)
        if food.should_disappear():
            food.randomize_position(snake.positions)
        
        # Check if snake ate food
        if snake.get_head_position() == food.position:
            # Increase length and score based on food type
            snake.length += food.type["weight"]
            snake.score += food.type["weight"]
            
            # Level up every 5 points
            if snake.score // 5 > snake.level - 1:
                snake.level += 1
                global FPS
                FPS += 2  # Increase game speed
            
            # Spawn new food
            food.randomize_position(snake.positions)
        
        # Render game frame
        screen.fill(WHITE)
        draw_grid(screen)
        snake.render(screen)
        food.render(screen)
        show_game_info(screen, snake.score, snake.level)
        
        pygame.display.update()
        clock.tick(FPS)  # Control game speed
    
    pygame.quit()

if __name__ == "__main__":
    main()