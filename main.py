
import pygame
import sys
import random
import math


# Установка размеров окна
WIDTH, HEIGHT = 800, 600

s = 1
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

all_vertices = []
vertices = []  # Список вершин
lines = []
chisla = []
start_pos = (0, 0)
directions = {}  # Словарь для хранения направлений на каждой линии
ch = {}
spis = []

font_name = pygame.font.match_font('arial')
chislo = [0]

# Основной цикл игры
running = True

def draw_text(surf, text, size, x, y, COLOR):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_arrow(x, y, angle, color):
    arrow_length = 15
    base_width = 7.5

    arrow_points = [
        (x + arrow_length * math.cos(angle), y + arrow_length * math.sin(angle)),
        (x + arrow_length * math.cos(angle + 2.5), y + arrow_length * math.sin(angle + 2.5)),
        (x + base_width * math.cos(angle + math.pi), y + base_width * math.sin(angle + math.pi)),
        (x + arrow_length * math.cos(angle - 2.5), y + arrow_length * math.sin(angle - 2.5))
    ]
    pygame.draw.polygon(screen, color, arrow_points)

def get_angle(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                directions[start_pos] = "left"
            elif event.key == pygame.K_RIGHT:
                directions[start_pos] = "right"
            elif event.key == pygame.K_RETURN:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            chisla.append(random.randint(1, 50))
            x, y = event.pos
            els = list(ch.items())

            vertex_clicked = False
            l = -1
            for vertex in vertices:
                l+=1
                if math.sqrt((vertex[0] - x) **2 + (vertex[1] - y) **2) < 50:
                    x, y = vertex
                    spis.append(ch[(x,y)])
                    all_vertices.append((x, y))
                    lines.append((start_pos, (x + 15, y + 15)))
                    vertex_clicked = True
                    break

            if not vertex_clicked:
                vertices.append((x - 15, y - 15))
                all_vertices.append((x - 15, y - 15))
                chislo.append(chislo[-1]+1)
                if len(ch) > 0:
                    ch[(x-15, y-15)] = els[-1][1]+1
                else: ch[(x-15, y-15)] = 1
                spis.append(ch[(x-15, y-15)])
            if start_pos != (0, 0) and not vertex_clicked:
                lines.append((start_pos, (x, y)))
            if vertex_clicked:
                start_pos = (x + 15, y + 15)
            else:
                start_pos = (x, y)
            if len(directions.values()) != len(all_vertices) - 1:
                directions[all_vertices[-1]] = 0
            if len(all_vertices) >= 2:
                if all_vertices[-1] == all_vertices[-2]:
                    directions[all_vertices[-1]+(s,s)] = 0
                    s+=1

    screen.fill(WHITE)
    for vertex in vertices:
        screen.blit(img, vertex)
    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 5)

        if line[0] in directions:
            if directions[line[0]] == "right":
                angle = get_angle(line[0], line[1])
                draw_arrow(line[1][0], line[1][1], angle, RED)
            elif directions[line[0]] == "left":
                angle = get_angle(line[1], line[0])
                draw_arrow(line[0][0], line[0][1], angle, BLUE)

    for vertex in range(1, len(all_vertices)):
        draw_text(screen, str(chisla[vertex - 1]), 30, ((all_vertices[vertex - 1][0] + all_vertices[vertex][0]) // 2),
                  ((all_vertices[vertex - 1][1] + all_vertices[vertex][1]) // 2), RED)
        draw_text(screen, str(spis[vertex-1]), 25, all_vertices[vertex-1][0]+18, all_vertices[vertex-1][1]+6, BLACK)

    pygame.display.flip()



# Создание матрицы смежности
INF = float('inf')
graph = [[float('inf')for _ in range(len(vertices))] for _ in range(len(vertices))]


els1 = (list(directions.values()))


for i in range(1, len(spis)):
    if spis[i] == spis[i-1]:
        graph[spis[i]-1][spis[i-1]-1] = chisla[i-1]
    if els1[i-1] == 'right':
        graph[spis[i-1]-1][spis[i]-1] = chisla[i-1]
    elif els1[i-1] == 'left':
        graph[spis[i]-1][spis[i-1]-1] = chisla[i-1]
    elif els1[i-1] == 0:
        graph[spis[i-1]-1][spis[i]-1] = chisla[i-1]
        graph[spis[i]-1][spis[i-1]-1] = chisla[i-1]
for i in graph:
    print(*i)











pygame.quit()
sys.exit()