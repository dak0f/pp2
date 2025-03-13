import pygame
from datetime import datetime
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2
RADIUS = H_HEIGHT - 50
RADIUS_ARK = RADIUS + 8

# Установка видеорежима (окна Pygame)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock with Music and Ball")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 25
ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Start at the center of the screen
ball_speed = 20

# Music player properties
music_files = ["forclock.mp3"]  # Add more files if needed
current_track = 0
pygame.mixer.music.load(music_files[current_track])

# Clock properties
font = pygame.font.SysFont('Verdana', 60)
number_font = pygame.font.SysFont('Verdana', 40)  # Шрифт для цифр на часах
img = pygame.image.load('2.png').convert_alpha()  # Загружаем изображение после установки видеорежима
bg = pygame.image.load('gojo.png').convert()
bg_rect = bg.get_rect(center=(H_WIDTH, H_HEIGHT))

# Load and scale clock hands
min_hand = pygame.image.load('minute.png').convert_alpha()
sec_hand = pygame.image.load('second.png').convert_alpha()
min_hand = pygame.transform.scale(min_hand, (50, 300))  # Размер минутной стрелки
sec_hand = pygame.transform.scale(sec_hand, (40, 350))  # Размер секундной стрелки

def blit_rotate_centered(surf, image, center_pos, angle):
    """Функция для вращения изображения вокруг центра."""
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=center_pos)  # Вращение вокруг центра
    surf.blit(rotated_image, rotated_rect)

def draw_numbers(surf, font):
    """Функция для отрисовки цифр на циферблате."""
    for number in range(1, 13):
        angle = math.radians(-90 + 30 * number)  # Угол для каждой цифры
        x = H_WIDTH + 0.8 * RADIUS * math.cos(angle)  # Позиция X
        y = H_HEIGHT + 0.8 * RADIUS * math.sin(angle)  # Позиция Y
        number_text = font.render(str(number), True, pygame.Color('white'))
        number_rect = number_text.get_rect(center=(x, y))
        surf.blit(number_text, number_rect)

# Function to play music
def play_music():
    pygame.mixer.music.play()

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()

# Function to play next track
def next_track():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    pygame.mixer.music.load(music_files[current_track])
    play_music()

# Function to play previous track
def previous_track():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    pygame.mixer.music.load(music_files[current_track])
    play_music()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls for music player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                play_music()
            elif event.key == pygame.K_s:  # Stop
                stop_music()
            elif event.key == pygame.K_n:  # Next track
                next_track()
            elif event.key == pygame.K_b:  # Previous track
                previous_track()

            # Keyboard controls for ball movement
            if event.key == pygame.K_UP:
                ball_y = max(ball_y - ball_speed, ball_radius)  # Move up, ensure it doesn't go off the screen
            elif event.key == pygame.K_DOWN:
                ball_y = min(ball_y + ball_speed, HEIGHT - ball_radius)  # Move down
            elif event.key == pygame.K_LEFT:
                ball_x = max(ball_x - ball_speed, ball_radius)  # Move left
            elif event.key == pygame.K_RIGHT:
                ball_x = min(ball_x + ball_speed, WIDTH - ball_radius)  # Move right

    # Draw background
    screen.fill(WHITE)
    screen.blit(bg, bg_rect)
    screen.blit(img, (0, 0))

    # Get current time
    t = datetime.now()
    minute, second = t.minute, t.second
    microsecond = t.microsecond

    # Углы для стрелок
    min_angle = -((minute + second / 60) * 6)  # Минутная стрелка
    sec_angle = -((second + microsecond / 1000000) * 6)  # Секундная стрелка

    # Рисуем стрелки, вращая их из центра
    blit_rotate_centered(screen, min_hand, (H_WIDTH, H_HEIGHT), min_angle)
    blit_rotate_centered(screen, sec_hand, (H_WIDTH, H_HEIGHT), sec_angle)

    # Рисуем центр часов
    pygame.draw.circle(screen, pygame.Color('white'), (H_WIDTH, H_HEIGHT), 8)

    # Отрисовываем цифры на циферблате
    draw_numbers(screen, number_font)

    # Отображаем текущее время
    time_render = font.render(f'{t:%H:%M:%S}', True, pygame.Color('forestgreen'), pygame.Color('orange'))
    screen.blit(time_render, (0, 0))

    # Рисуем дугу для секундной стрелки
    sec_angle_rad = -math.radians(sec_angle) + math.pi / 2
    pygame.draw.arc(screen, pygame.Color('magenta'),
                    (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK),
                    math.pi / 2, sec_angle_rad, 8)

    # Рисуем красный шар
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()