import pygame
import sys
import random
import math

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    WHITE = (255,163,251)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



# Установка размеров окна
WIDTH, HEIGHT = 800, 600

# Установка цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Генерация графа с помощью Pygame")
imge = pygame.image.load('vertex.png')
imge.set_colorkey((255, 255, 255))
img = pygame.transform.scale(imge, (40, 40))

# Цвета
WHITE = (230, 230, 250)
BLACK = (0, 0, 0)

# Основной цикл игры
running = True
flag = False
vertices = []  # Список вершин
lines = []
chisla = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Обработка нажатия левой кнопки мыши
            x, y = event.pos
            vertices.append((x-15, y-15))  # Добавление новой вершины при клике мышкой
            lines.append((x, y))
            chisla.append(random.randint(1, 50))

    # Отрисовка
    screen.fill(WHITE)
    for vertex in range(1, len(vertices)+1):
        screen.blit(img, vertices[vertex-1])
        if  vertex != len(vertices):
            pygame.draw.line(screen, BLACK, lines[vertex-1],  lines[vertex], 5)
            draw_text(screen, str(chisla[vertex-1]), 30, ((vertices[vertex-1][0]+vertices[vertex][0])//2), ((vertices[vertex-1][1]+vertices[vertex][1])//2))
    pygame.display.flip()

pygame.quit()
sys.exit()