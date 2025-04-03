import pygame
import pygame.gfxdraw
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint")

# Create drawing surface
drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

# Tools
PEN = 0
RECTANGLE = 1
CIRCLE = 2
ERASER = 3
current_tool = PEN

# Colors
colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]
current_color = BLACK
brush_size = 5

# Drawing state
drawing = False
start_pos = (0, 0)
last_pos = (0, 0)

# Font
font = pygame.font.SysFont('Arial', 16)

def draw_tool_buttons():
    # Draw tool selection buttons
    pygame.draw.rect(screen, (200, 200, 200), (10, 10, 80, 30))
    pygame.draw.rect(screen, (200, 200, 200), (100, 10, 80, 30))
    pygame.draw.rect(screen, (200, 200, 200), (190, 10, 80, 30))
    pygame.draw.rect(screen, (200, 200, 200), (280, 10, 80, 30))
    
    # Highlight current tool
    if current_tool == PEN:
        pygame.draw.rect(screen, (150, 150, 150), (10, 10, 80, 30), 2)
    elif current_tool == RECTANGLE:
        pygame.draw.rect(screen, (150, 150, 150), (100, 10, 80, 30), 2)
    elif current_tool == CIRCLE:
        pygame.draw.rect(screen, (150, 150, 150), (190, 10, 80, 30), 2)
    elif current_tool == ERASER:
        pygame.draw.rect(screen, (150, 150, 150), (280, 10, 80, 30), 2)
    
    # Tool labels
    pen_text = font.render("Pen", True, BLACK)
    rect_text = font.render("Rectangle", True, BLACK)
    circle_text = font.render("Circle", True, BLACK)
    eraser_text = font.render("Eraser", True, BLACK)
    
    screen.blit(pen_text, (20, 15))
    screen.blit(rect_text, (105, 15))
    screen.blit(circle_text, (200, 15))
    screen.blit(eraser_text, (290, 15))

def draw_color_buttons():
    # Draw color selection buttons
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (380 + i * 40, 10, 30, 30))
        if color == current_color:
            pygame.draw.rect(screen, WHITE, (380 + i * 40, 10, 30, 30), 2)

def draw_brush_size_controls():
    # Brush size label
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (660, 15))
    
    # Increase/decrease buttons
    pygame.draw.rect(screen, (200, 200, 200), (720, 10, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), (755, 10, 30, 30))
    
    plus_text = font.render("+", True, BLACK)
    minus_text = font.render("-", True, BLACK)
    
    screen.blit(plus_text, (730, 10))
    screen.blit(minus_text, (765, 10))

def draw_preview():
    # Draw preview of current tool/color
    if current_tool == PEN:
        pygame.draw.circle(screen, current_color, (WIDTH - 30, 25), brush_size)
    elif current_tool == RECTANGLE:
        pygame.draw.rect(screen, current_color, (WIDTH - 50, 10, 30, 20))
    elif current_tool == CIRCLE:
        pygame.draw.circle(screen, current_color, (WIDTH - 35, 20), 15)
    elif current_tool == ERASER:
        pygame.draw.circle(screen, WHITE, (WIDTH - 30, 25), brush_size)
        pygame.draw.circle(screen, BLACK, (WIDTH - 30, 25), brush_size, 1)

def draw_help_text():
    help_text = font.render("Press SPACE to clear canvas", True, BLACK)
    screen.blit(help_text, (10, HEIGHT - 25))

def draw_rectangle(surface, color, start, end, width):
    rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                      abs(end[0] - start[0]), abs(end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, width)

def draw_circle(surface, color, start, end, width):
    radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
    pygame.draw.circle(surface, color, start, radius, width)

def main():
    global current_tool, current_color, brush_size, drawing, start_pos, last_pos
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:  # Clear canvas
                    drawing_surface.fill(WHITE)
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos
                    
                    # Check if a tool button was clicked
                    if 10 <= event.pos[0] <= 90 and 10 <= event.pos[1] <= 40:
                        current_tool = PEN
                    elif 100 <= event.pos[0] <= 180 and 10 <= event.pos[1] <= 40:
                        current_tool = RECTANGLE
                    elif 190 <= event.pos[0] <= 270 and 10 <= event.pos[1] <= 40:
                        current_tool = CIRCLE
                    elif 280 <= event.pos[0] <= 360 and 10 <= event.pos[1] <= 40:
                        current_tool = ERASER
                    
                    # Check if a color button was clicked
                    for i in range(len(colors)):
                        if 380 + i * 40 <= event.pos[0] <= 410 + i * 40 and 10 <= event.pos[1] <= 40:
                            current_color = colors[i]
                    
                    # Check brush size controls
                    if 720 <= event.pos[0] <= 750 and 10 <= event.pos[1] <= 40:
                        brush_size = min(50, brush_size + 1)
                    elif 755 <= event.pos[0] <= 785 and 10 <= event.pos[1] <= 40:
                        brush_size = max(1, brush_size - 1)
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    
                    # Finalize shape drawing
                    if current_tool == RECTANGLE:
                        draw_rectangle(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == CIRCLE:
                        draw_circle(drawing_surface, current_color, start_pos, event.pos, brush_size)
            
            elif event.type == MOUSEMOTION and drawing:
                if current_tool == PEN:
                    pygame.draw.line(drawing_surface, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif current_tool == ERASER:
                    pygame.draw.line(drawing_surface, WHITE, last_pos, event_pos, brush_size)
                    last_pos = event.pos
        
        # Draw everything
        screen.fill(WHITE)
        screen.blit(drawing_surface, (0, 0))
        
        # Draw UI elements
        draw_tool_buttons()
        draw_color_buttons()
        draw_brush_size_controls()
        draw_preview()
        draw_help_text()
        
        # Draw preview of rectangle/circle while dragging
        if drawing and (current_tool == RECTANGLE or current_tool == CIRCLE):
            temp_surface = drawing_surface.copy()
            if current_tool == RECTANGLE:
                draw_rectangle(temp_surface, current_color, start_pos, pygame.mouse.get_pos(), brush_size)
            elif current_tool == CIRCLE:
                draw_circle(temp_surface, current_color, start_pos, pygame.mouse.get_pos(), brush_size)
            screen.blit(temp_surface, (0, 0))
        
        pygame.display.update()

if __name__ == "__main__":
    main()