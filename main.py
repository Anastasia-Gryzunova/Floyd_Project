import pygame
import sys
import random
import math

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    pass

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

# Основной цикл игры
running = True
flag = False
vertices = []  # Список вершин
lines = []
vertex_clicked = False
start_pos = (0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Обработка нажатия левой кнопки мыши
            x, y = event.pos
            vertex_clicked = False
            for vertex in vertices:
                if math.sqrt((vertex[0]-x)**2 + (vertex[1]-y)**2) < 50:  # Расстояние для проверки клика
                    x, y = vertex  # Используем существующую точку
                    lines.append((start_pos, (x+15, y+15)))
                    vertex_clicked = True
                    break

            if not vertex_clicked:  # Добавляем новую вершину, только если точка не была найдена
                vertices.append((x-15, y-15))  # Добавление новой вершины при клике мышкой
            if start_pos != (0, 0) and not vertex_clicked:  # Если начальная точка уже установлена и мы не кликнули на существующую, добавляем линию
                lines.append((start_pos, (x, y)))
            if vertex_clicked:
                start_pos = (x+15, y+15)
            else:
                start_pos = (x, y)

    # Отрисовка
    screen.fill(WHITE)
    for vertex in vertices:
        screen.blit(img, vertex)
    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 5)
    pygame.display.flip()

pygame.quit()
sys.exit()