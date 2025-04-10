import pygame
import pygame.gfxdraw
import sys
import math
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
pygame.display.set_caption("Advanced Paint with Shapes")

# Create drawing surface
drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

# Tools
PEN = 0
RECTANGLE = 1
CIRCLE = 2
ERASER = 3
SQUARE = 4
RIGHT_TRIANGLE = 5
EQUILATERAL_TRIANGLE = 6
RHOMBUS = 7
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
    """Draw all tool selection buttons in the UI"""
    # Button positions and labels
    tools = [
        (10, "Pen"), (100, "Rectangle"), (190, "Circle"), (280, "Eraser"),
        (370, "Square"), (460, "R-Triangle"), (550, "Eq-Triangle"), (640, "Rhombus")
    ]
    
    # Draw all buttons
    for i, (x_pos, label) in enumerate(tools):
        pygame.draw.rect(screen, (200, 200, 200), (x_pos, 10, 80, 30))
        if current_tool == i:  # Highlight current tool
            pygame.draw.rect(screen, (150, 150, 150), (x_pos, 10, 80, 30), 2)
        screen.blit(font.render(label, True, BLACK), (x_pos + 5, 15))

def draw_color_buttons():
    """Draw color selection buttons in the UI"""
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i * 40, 50, 30, 30))
        if color == current_color:  # Highlight selected color
            pygame.draw.rect(screen, WHITE, (10 + i * 40, 50, 30, 30), 2)

def draw_brush_size_controls():
    """Draw brush size controls in the UI"""
    # Size display
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (300, 55))
    
    # Increase/decrease buttons
    pygame.draw.rect(screen, (200, 200, 200), (370, 50, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), (405, 50, 30, 30))
    screen.blit(font.render("+", True, BLACK), (380, 50))
    screen.blit(font.render("-", True, BLACK), (415, 50))

def draw_preview():
    """Draw a preview of the current tool and color"""
    preview_pos = (WIDTH - 50, 40)
    preview_color = WHITE if current_tool == ERASER else current_color
    
    if current_tool == PEN:
        pygame.draw.circle(screen, preview_color, preview_pos, brush_size)
    elif current_tool == RECTANGLE:
        pygame.draw.rect(screen, preview_color, (preview_pos[0]-15, preview_pos[1]-10, 30, 20))
    elif current_tool == CIRCLE:
        pygame.draw.circle(screen, preview_color, preview_pos, 15)
    elif current_tool == SQUARE:
        pygame.draw.rect(screen, preview_color, (preview_pos[0]-15, preview_pos[1]-15, 30, 30))
    elif current_tool == RIGHT_TRIANGLE:
        points = [preview_pos, (preview_pos[0]+30, preview_pos[1]), (preview_pos[0], preview_pos[1]-30)]
        pygame.draw.polygon(screen, preview_color, points)
    elif current_tool == EQUILATERAL_TRIANGLE:
        height = 30 * math.sqrt(3) / 2
        points = [
            preview_pos,
            (preview_pos[0]+30, preview_pos[1]),
            (preview_pos[0]+15, preview_pos[1]-height)
        ]
        pygame.draw.polygon(screen, preview_color, points)
    elif current_tool == RHOMBUS:
        points = [
            (preview_pos[0], preview_pos[1]-15),
            (preview_pos[0]+15, preview_pos[1]),
            (preview_pos[0], preview_pos[1]+15),
            (preview_pos[0]-15, preview_pos[1])
        ]
        pygame.draw.polygon(screen, preview_color, points)
    
    # Add border for eraser preview
    if current_tool == ERASER:
        pygame.draw.circle(screen, BLACK, preview_pos, brush_size, 1)

def draw_help_text():
    """Draw help text at the bottom of the screen"""
    help_text = font.render("Press SPACE to clear canvas | Right-click to fill shapes", True, BLACK)
    screen.blit(help_text, (10, HEIGHT - 25))

def draw_rectangle(surface, color, start, end, width):
    """Draw a rectangle on the given surface"""
    rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]), 
                      abs(end[0] - start[0]), abs(end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, width)

def draw_square(surface, color, start, end, width):
    """Draw a square on the given surface (maintains equal width and height)"""
    size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    rect = pygame.Rect(
        start[0] if end[0] > start[0] else start[0] - size,
        start[1] if end[1] > start[1] else start[1] - size,
        size, size
    )
    pygame.draw.rect(surface, color, rect, width)

def draw_circle(surface, color, start, end, width):
    """Draw a circle on the given surface"""
    radius = int(((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5)
    pygame.draw.circle(surface, color, start, radius, width)

def draw_right_triangle(surface, color, start, end, width):
    """Draw a right-angled triangle on the given surface"""
    points = [
        start,
        (end[0], start[1]),  # Right angle point
        (start[0], end[1])   # Completing the triangle
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_equilateral_triangle(surface, color, start, end, width):
    """Draw an equilateral triangle on the given surface"""
    side_length = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
    height = side_length * math.sqrt(3) / 2
    
    points = [
        start,
        (start[0] + side_length, start[1]),
        (start[0] + side_length/2, start[1] - height)
    ]
    pygame.draw.polygon(surface, color, points, width)

def draw_rhombus(surface, color, start, end, width):
    """Draw a rhombus on the given surface"""
    width_shape = abs(end[0] - start[0])
    height_shape = abs(end[1] - start[1])
    
    center_x = (start[0] + end[0]) / 2
    center_y = (start[1] + end[1]) / 2
    
    points = [
        (center_x, center_y - height_shape/2),  # Top
        (center_x + width_shape/2, center_y),   # Right
        (center_x, center_y + height_shape/2),  # Bottom
        (center_x - width_shape/2, center_y)    # Left
    ]
    pygame.draw.polygon(surface, color, points, width)

def handle_tool_selection(pos):
    """Check if a tool button was clicked and update current tool"""
    global current_tool
    tools_x = [10, 100, 190, 280, 370, 460, 550, 640]
    if 10 <= pos[1] <= 40:  # Check y-coordinate first
        for i, x in enumerate(tools_x):
            if x <= pos[0] <= x + 80:
                current_tool = i
                return True
    return False

def handle_color_selection(pos):
    """Check if a color button was clicked and update current color"""
    global current_color
    if 50 <= pos[1] <= 80:  # Color buttons y-range
        for i in range(len(colors)):
            if 10 + i * 40 <= pos[0] <= 40 + i * 40:
                current_color = colors[i]
                return True
    return False

def handle_brush_size_change(pos):
    """Check if brush size controls were clicked and update size"""
    global brush_size
    if 50 <= pos[1] <= 80:  # Size controls y-range
        if 370 <= pos[0] <= 400:  # Increase button
            brush_size = min(50, brush_size + 1)
            return True
        elif 405 <= pos[0] <= 435:  # Decrease button
            brush_size = max(1, brush_size - 1)
            return True
    return False

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
                    
                    # Check UI element clicks
                    handle_tool_selection(event.pos) or \
                    handle_color_selection(event.pos) or \
                    handle_brush_size_change(event.pos)
                
                elif event.button == 3:  # Right mouse button (fill shapes)
                    if current_tool in [RECTANGLE, CIRCLE, SQUARE, RIGHT_TRIANGLE, EQUILATERAL_TRIANGLE, RHOMBUS]:
                        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        if current_tool == RECTANGLE:
                            draw_rectangle(temp_surface, current_color, start_pos, last_pos, 0)
                        elif current_tool == CIRCLE:
                            draw_circle(temp_surface, current_color, start_pos, last_pos, 0)
                        elif current_tool == SQUARE:
                            draw_square(temp_surface, current_color, start_pos, last_pos, 0)
                        elif current_tool == RIGHT_TRIANGLE:
                            draw_right_triangle(temp_surface, current_color, start_pos, last_pos, 0)
                        elif current_tool == EQUILATERAL_TRIANGLE:
                            draw_equilateral_triangle(temp_surface, current_color, start_pos, last_pos, 0)
                        elif current_tool == RHOMBUS:
                            draw_rhombus(temp_surface, current_color, start_pos, last_pos, 0)
                        drawing_surface.blit(temp_surface, (0, 0))
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    
                    # Finalize shape drawing
                    if current_tool == RECTANGLE:
                        draw_rectangle(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == CIRCLE:
                        draw_circle(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == SQUARE:
                        draw_square(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == RIGHT_TRIANGLE:
                        draw_right_triangle(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == EQUILATERAL_TRIANGLE:
                        draw_equilateral_triangle(drawing_surface, current_color, start_pos, event.pos, brush_size)
                    elif current_tool == RHOMBUS:
                        draw_rhombus(drawing_surface, current_color, start_pos, event.pos, brush_size)
            
            elif event.type == MOUSEMOTION and drawing:
                if current_tool == PEN:
                    pygame.draw.line(drawing_surface, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif current_tool == ERASER:
                    pygame.draw.line(drawing_surface, WHITE, last_pos, event.pos, brush_size)
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
        
        # Draw shape preview while dragging
        if drawing and current_tool in [RECTANGLE, CIRCLE, SQUARE, RIGHT_TRIANGLE, EQUILATERAL_TRIANGLE, RHOMBUS]:
            temp_surface = drawing_surface.copy()
            mouse_pos = pygame.mouse.get_pos()
            
            if current_tool == RECTANGLE:
                draw_rectangle(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            elif current_tool == CIRCLE:
                draw_circle(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            elif current_tool == SQUARE:
                draw_square(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            elif current_tool == RIGHT_TRIANGLE:
                draw_right_triangle(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            elif current_tool == EQUILATERAL_TRIANGLE:
                draw_equilateral_triangle(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            elif current_tool == RHOMBUS:
                draw_rhombus(temp_surface, current_color, start_pos, mouse_pos, brush_size)
            
            screen.blit(temp_surface, (0, 0))
        
        pygame.display.update()

if __name__ == "__main__":
    main()