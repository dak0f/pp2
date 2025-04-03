import pygame
import random
import time

# Инициализация pygame
pygame.init()

# Цвета
gray = (119, 118, 110)
black = (0, 0, 0)
red = (255, 0, 0)

# Размеры экрана
display_width = 800
display_height = 600

# Создание окна игры
gamedisplays = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()

# Загрузка изображений
carimg = pygame.image.load('car1.jpg')
backgroundpic = pygame.image.load("grass.jpg")
yellow_strip = pygame.image.load("yellow_strip.jpg")
strip = pygame.image.load("strip.jpg")

# Создание монетки (если нет изображения)
coin_img = pygame.Surface((30, 30))
coin_img.fill((255, 215, 0))  # Золотой цвет
pygame.draw.circle(coin_img, (255, 255, 0), (15, 15), 15)

# Параметры машины
car_width = 56
car_height = 100

def car(x, y):
    gamedisplays.blit(carimg, (x, y))

def obstacle(obs_startx, obs_starty, obs):
    # В этой упрощенной версии используем одно изображение для всех препятствий
    obs_pic = pygame.image.load("car2.jpg")
    gamedisplays.blit(obs_pic, (obs_startx, obs_starty))

def draw_coins(coins):
    for coin in coins:
        gamedisplays.blit(coin_img, (coin[0], coin[1]))

def show_score(score, coins_collected):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render("Score: " + str(score), True, black)
    coins_text = font.render("Coins: " + str(coins_collected), True, (255, 215, 0))
    gamedisplays.blit(score_text, (0, 30))
    gamedisplays.blit(coins_text, (0, 70))

def crash():
    font = pygame.font.SysFont(None, 80)
    text = font.render("Game Over!", True, red)
    gamedisplays.blit(text, (display_width/2 - 150, display_height/2 - 50))
    pygame.display.update()
    time.sleep(3)
    game_loop()

def game_loop():
    # Позиция машины
    x = display_width * 0.45
    y = display_height * 0.8
    x_change = 0
    
    # Параметры препятствий
    obstacle_speed = 8
    obs_startx = random.randrange(200, display_width - 200)
    obs_starty = -600
    obs_width = 56
    obs_height = 100
    
    # Монетки
    coins = []
    coins_collected = 0
    
    # Счет
    score = 0
    
    # Фон
    y2 = 0
    
    game_exit = False
    
    while not game_exit:
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
        
        x += x_change
        
        # Отрисовка фона
        gamedisplays.fill(gray)
        gamedisplays.blit(backgroundpic, (0, y2))
        gamedisplays.blit(backgroundpic, (0, y2 - display_height))
        gamedisplays.blit(backgroundpic, (700, y2))
        gamedisplays.blit(backgroundpic, (700, y2 - display_height))
        
        # Дорожная разметка
        gamedisplays.blit(yellow_strip, (400, y2))
        gamedisplays.blit(yellow_strip, (400, y2 - display_height))
        gamedisplays.blit(strip, (120, y2))
        gamedisplays.blit(strip, (680, y2))
        
        y2 += obstacle_speed
        if y2 > display_height:
            y2 = 0
        
        # Спавн монеток
        if random.random() < 0.02:  # 2% шанс появления монетки каждый кадр
            coins.append([random.randrange(150, display_width - 150), -30])
        
        # Обновление позиций монеток
        for coin in coins[:]:
            coin[1] += obstacle_speed / 2
            
            # Проверка столкновения с монеткой
            if (x < coin[0] + 30 and x + car_width > coin[0] and
                y < coin[1] + 30 and y + car_height > coin[1]):
                coins.remove(coin)
                coins_collected += 1
                score += 5
            elif coin[1] > display_height:  # Удаляем монетки за экраном
                coins.remove(coin)
        
        # Отрисовка монеток
        draw_coins(coins)
        
        # Препятствия
        obs_starty += obstacle_speed
        obstacle(obs_startx, obs_starty, 0)
        
        # Если препятствие уехало за экран
        if obs_starty > display_height:
            obs_starty = -obs_height
            obs_startx = random.randrange(150, display_width - 150)
            score += 1
        
        # Отрисовка машины
        car(x, y)
        
        # Отображение счета
        show_score(score, coins_collected)
        
        # Границы дороги
        if x < 120 or x > display_width - 120 - car_width:
            crash()
        
        # Столкновение с препятствием
        if y < obs_starty + obs_height:
            if (x > obs_startx and x < obs_startx + obs_width or
                x + car_width > obs_startx and x + car_width < obs_startx + obs_width):
                crash()
        
        pygame.display.update()
        clock.tick(60)

# Запуск игры
game_loop()
# pygame.quit()
quit()