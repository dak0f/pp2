import pygame
import random
import time

# Initialize pygame
pygame.init()

# Color definitions
GRAY = (119, 118, 110)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Screen dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Create game window
gamedisplays = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Enhanced Car Game")
clock = pygame.time.Clock()

# Load images (placeholder comments - replace with actual image paths)
carimg = pygame.image.load('car1.jpg')          # Player car image
backgroundpic = pygame.image.load("grass.jpg")  # Background image
yellow_strip = pygame.image.load("yellow_strip.jpg")  # Road markings
strip = pygame.image.load("strip.jpg")          # Side strips

# Coin types with different values and colors
COIN_TYPES = [
    {"color": BRONZE, "value": 1, "weight": 60},  # Common bronze coin (60% chance)
    {"color": SILVER, "value": 3, "weight": 30},   # Silver coin (30% chance)
    {"color": GOLD, "value": 5, "weight": 10}      # Rare gold coin (10% chance)
]

# Car parameters
CAR_WIDTH = 56
CAR_HEIGHT = 100

def create_coin_surface(color, size=30):
    """Create a coin surface with given color"""
    coin = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(coin, color, (size//2, size//2), size//2)
    pygame.draw.circle(coin, (255, 255, 0), (size//2, size//2), size//2 - 3)
    return coin

# Create coin images for each type
coin_images = {
    "bronze": create_coin_surface(BRONZE),
    "silver": create_coin_surface(SILVER),
    "gold": create_coin_surface(GOLD)
}

def car(x, y):
    """Draw player's car at specified position"""
    gamedisplays.blit(carimg, (x, y))

def obstacle(obs_startx, obs_starty, obs):
    """Draw obstacle car at specified position"""
    # In this simplified version we use one image for all obstacles
    obs_pic = pygame.image.load("car2.jpg")
    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))

def draw_coins(coins):
    """Draw all coins on the road"""
    for coin in coins:
        # coin[2] contains the type of coin ('bronze', 'silver', 'gold')
        gamedisplays.blit(coin_images[coin[2]], (coin[0], coin[1]))

def show_score(score, coins_collected, level):
    """Display score, coins collected and current level"""
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, BLACK)
    coins_text = font.render(f"Coins: {coins_collected}", True, GOLD)
    level_text = font.render(f"Level: {level}", True, RED)
    
    gamedisplays.blit(score_text, (0, 30))
    gamedisplays.blit(coins_text, (0, 70))
    gamedisplays.blit(level_text, (0, 110))

def crash():
    """Handle crash scenario and restart game"""
    font = pygame.font.SysFont(None, 80)
    text = font.render("Game Over!", True, RED)
    gamedisplays.blit(text, (DISPLAY_WIDTH/2 - 150, DISPLAY_HEIGHT/2 - 50))
    pygame.display.update()
    time.sleep(3)
    game_loop()

def game_loop():
    """Main game loop"""
    # Player car initial position
    x = DISPLAY_WIDTH * 0.45
    y = DISPLAY_HEIGHT * 0.8
    x_change = 0
    
    # Obstacle parameters
    base_obstacle_speed = 8
    obstacle_speed = base_obstacle_speed
    obs_startx = random.randrange(200, DISPLAY_WIDTH - 200)
    obs_starty = -600
    obs_width = 56
    obs_height = 100
    
    # Coin parameters
    coins = []  # Each coin: [x, y, type]
    coins_collected = 0
    coins_for_level_up = 10  # Need 10 coins to level up
    
    # Game stats
    score = 0
    level = 1
    
    # Background scrolling
    y2 = 0
    
    game_exit = False
    
    while not game_exit:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        # Update player position
        x += x_change
        
        # Draw background with scrolling effect
        gamedisplays.fill(GRAY)
        gamedisplays.blit(backgroundpic, (0, y2))
        gamedisplays.blit(backgroundpic, (0, y2 - DISPLAY_HEIGHT))
        gamedisplays.blit(backgroundpic, (700, y2))
        gamedisplays.blit(backgroundpic, (700, y2 - DISPLAY_HEIGHT))
        
        # Draw road markings
        gamedisplays.blit(yellow_strip, (400, y2))
        gamedisplays.blit(yellow_strip, (400, y2 - DISPLAY_HEIGHT))
        gamedisplays.blit(strip, (120, y2))
        gamedisplays.blit(strip, (680, y2))
        
        # Update background position
        y2 += obstacle_speed
        if y2 > DISPLAY_HEIGHT:
            y2 = 0
        
        # Spawn new coins randomly
        if random.random() < 0.02:  # 2% chance per frame
            # Choose coin type based on weights
            weights = [coin["weight"] for coin in COIN_TYPES]
            chosen_type = random.choices(["bronze", "silver", "gold"], weights=weights)[0]
            coins.append([random.randrange(150, DISPLAY_WIDTH - 150), -30, chosen_type])
        
        # Update coin positions and check collisions
        for coin in coins[:]:
            coin[1] += obstacle_speed / 2  # Coins move slower than cars
            
            # Check collision with player
            if (x < coin[0] + 30 and x + CAR_WIDTH > coin[0] and
                y < coin[1] + 30 and y + CAR_HEIGHT > coin[1]):
                coins.remove(coin)
                # Add score based on coin type
                if coin[2] == "bronze":
                    score += 1
                elif coin[2] == "silver":
                    score += 3
                else:  # gold
                    score += 5
                coins_collected += 1
                
                # Level up after collecting enough coins
                if coins_collected >= coins_for_level_up:
                    level += 1
                    coins_for_level_up += 10  # Need 10 more coins for next level
                    obstacle_speed += 1  # Increase enemy speed
                    base_obstacle_speed += 1  # Also increase base speed for restart consistency
            
            # Remove coins that go off screen
            elif coin[1] > DISPLAY_HEIGHT:
                coins.remove(coin)
        
        # Draw all coins
        draw_coins(coins)
        
        # Update and draw obstacle
        obs_starty += obstacle_speed
        obstacle(obs_startx, obs_starty, 0)
        
        # Respawn obstacle when it goes off screen
        if obs_starty > DISPLAY_HEIGHT:
            obs_starty = -obs_height
            obs_startx = random.randrange(150, DISPLAY_WIDTH - 150)
            score += 1
        
        # Draw player car
        car(x, y)
        
        # Display game info
        show_score(score, coins_collected, level)
        
        # Road boundary check
        if x < 120 or x > DISPLAY_WIDTH - 120 - CAR_WIDTH:
            crash()
        
        # Collision with obstacle
        if y < obs_starty + obs_height:
            if (x > obs_startx and x < obs_startx + obs_width or
                x + CAR_WIDTH > obs_startx and x + CAR_WIDTH < obs_startx + obs_width):
                crash()
        
        pygame.display.update()
        clock.tick(60)  # 60 FPS

# Start the game
game_loop()
pygame.quit()
quit()