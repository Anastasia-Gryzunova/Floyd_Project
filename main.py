import pygame
import sys
import random
import math

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

# Загрузка картинок вершин
imge = pygame.image.load('vertex.png')
imge.set_colorkey((255, 255, 255))
img = pygame.transform.scale(imge, (40, 40))

imge1 = pygame.image.load('vertex2.png')
imge1.set_colorkey((255, 255, 255))
img1 = pygame.transform.scale(imge1, (38, 38))

imge2 = pygame.image.load('vertex3.png')
imge2.set_colorkey((255, 255, 255))
img2 = pygame.transform.scale(imge2, (37, 37))

# Установка необходимых словарей, списков и переменных
all_vertices = [] # Список всех вершин, т.е тех которые встречаются любое колв- раз
vertices = []  # Список вершин. Каждая вершина в данном списке уникальна.
lines = [] # Список ребер
chisla = [] # Список веса ребер
start_pos = (0, 0) # Последняя использованная вершина
directions = {}  # Словарь для хранения направлений для ребер
ch = {} # Словарь, где значение - вес ребер
spis = [] # Список для хранения направлений для ребер
font_name = pygame.font.match_font('arial')
chislo = [0] # Номера вершин
s = 1

# Основной цикл игры
running = True
# Функция отрисовки текста
def draw_text(surf, text, size, x, y, COLOR):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
# Функция отрисовки стрелки для ориентированного графа
def draw_arrow(a, b, angle, color):
    arrow_length = 15
    base_width = 7.5
    x = a
    y = b
    arrow_points = [
        (x + arrow_length * math.cos(angle), y + arrow_length * math.sin(angle)),
        (x + arrow_length * math.cos(angle + 2.5), y + arrow_length * math.sin(angle + 2.5)),
        (x + base_width * math.cos(angle + math.pi), y + base_width * math.sin(angle + math.pi)),
        (x + arrow_length * math.cos(angle - 2.5), y + arrow_length * math.sin(angle - 2.5))
    ]
    pygame.draw.polygon(screen, color, arrow_points)
# Функция получения угла, при котором должна быть направлена стрелка
def get_angle(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])
# Основной цикл игры
while running:
    for event in pygame.event.get():
        # Выход, если нажата кнопка завершения программы
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        # Установка напрвления ребра
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                directions[start_pos] = "left"
            elif event.key == pygame.K_RIGHT:
                directions[start_pos] = "right"
            elif event.key == pygame.K_RETURN:
                running = False
        # Установка вершины
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            chisla.append(random.randint(-50, 50)) # Добавляем вес ребра (рандомно)
            x, y = event.pos # Сохраняем координаты точки
            els = list(ch.items())  # Преобразовываем els в список веса ребер
            vertex_clicked = False # Создаем вершину для проверки цикла, чтобы не рисовалась точка, если я нажала на уже существующую
            for vertex in vertices:
                if math.sqrt((vertex[0] - x) ** 2 + (vertex[1] - y) ** 2) < 50: # Проверка, что нажато пространство рядом с вершиной
                    x, y = vertex # Если да, то сохраннеая вершина равна той, рядом с которой мы нажали
                    spis.append(ch[(x, y)]) # Добавляем направление
                    all_vertices.append((x, y)) # Добавляем вершину в список всех вершин
                    lines.append((start_pos, (x + 15, y + 15))) # Добавляем ребро
                    vertex_clicked = True # Обозначим, что мы кликнули на ту вершину, которая уже была нажата
                    break

            # Если мы не нажимали на уже нажатую вершину
            if not vertex_clicked:
                vertices.append((x - 15, y - 15)) # Добавляем вершину в список уникальных вершин
                all_vertices.append((x - 15, y - 15)) # Добавляем вершину в список всех вершин
                chislo.append(chislo[-1] + 1) # Добавляем номер вершин
                # Проверка на то, первая эта вершина или нет
                if len(ch) > 0:
                    ch[(x - 15, y - 15)] = els[-1][1] + 1
                else:
                    ch[(x - 15, y - 15)] = 1
                spis.append(ch[(x - 15, y - 15)])

            if start_pos != (0, 0) and not vertex_clicked:
                lines.append((start_pos, (x, y))) # Добавляем ребро, если последняя вершина - не начальая
            if vertex_clicked:
                start_pos = (x + 15, y + 15) # Обозначаем последнюю вершину, если был цикл
            else:
                start_pos = (x, y) # Обозначаем последнюю вершину, если не было цикла

            # Если не кликнуты клавиши 'right' и 'left', то считается что по этому ребру можно пройти с двух сторон
            if len(directions.values()) != len(all_vertices) - 1:
                directions[all_vertices[-1]] = 0
            if len(all_vertices) >= 2:
                if all_vertices[-1] == all_vertices[-2]:
                    directions[all_vertices[-1]+(s, s)] = 0
                    s += 1
    # Отрисовка графа
    screen.fill(WHITE)
    # Отрисовка вершин
    for vertex in vertices:
        screen.blit(img, vertex)
    # Отрисовка ребер
    for line in lines:
        pygame.draw.line(screen, BLACK, line[0], line[1], 5)
        # Отрисовка стрелок в ориентированном графе
        if line[0] in directions:
            if directions[line[0]] == "right":
                angle = get_angle(line[0], line[1])
                draw_arrow(line[1][0], line[1][1], angle, RED)
            elif directions[line[0]] == "left":
                angle = get_angle(line[1], line[0])
                draw_arrow(line[0][0], line[0][1], angle, BLUE)
    # Отрисовка веса в графе и порядкового номера вершины
    for vertex in range(1, len(all_vertices)):
        draw_text(screen, str(chisla[vertex - 1]), 30, ((all_vertices[vertex - 1][0] + all_vertices[vertex][0]) // 2),
                  ((all_vertices[vertex - 1][1] + all_vertices[vertex][1]) // 2), RED)
        draw_text(screen, str(spis[vertex-1]), 25, all_vertices[vertex-1][0] + 18, all_vertices[vertex-1][1] + 6, BLACK)

    pygame.display.flip()
# Создание матрицы смежности
graph = [[float('inf') for _ in range(len(vertices))] for _ in range(len(vertices))]

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

INF = 99999
h = True
f = 600

def floyd_warshall(graph):
    # Алгоритм флойда и его визуализация
    V = len(graph)
    dist = [[0 if i == j else graph[i][j] if graph[i][j] != 0 else INF for j in range(V)] for i in range(V)]
    for k in range(V):
        for i in range(V):
            # Выделяем красным ту точку, которую рассматриваем, т.е заменяем изображение
            screen.blit(img1, (vertices[i][0], vertices[i][1]+2))
            draw_text(screen, str(spis[i]), 25, all_vertices[i][0] + 18,
                      all_vertices[i][1] + 6, BLACK)
            pygame.display.flip()
            pygame.time.wait(f)
            for j in range(V):
                if i!=j and i == k or i!=j and j==k:
                    # Если есть две различные точки, то выводим их красными (рассматриваем путь от i-ой к j-ой)
                    screen.blit(img1, (vertices[j][0], vertices[j][1]+2))
                    draw_text(screen, str(spis[j]), 25, all_vertices[j][0] + 18,
                              all_vertices[j][1] + 6, BLACK)
                    pygame.display.flip()
                    pygame.time.wait(f)
                    # Проверка, что существуют ребра между двумя точками
                    if (
                    (vertices[i][0] + 15, vertices[i][1] + 15), (vertices[j][0] + 15, vertices[j][1] + 15)) in lines or  ((vertices[j][0] + 15, vertices[j][1] + 15), (vertices[i][0] + 15, vertices[i][1] + 15)) in lines:



                        pygame.draw.line(screen, RED, (vertices[i][0] + 15, vertices[i][1]+15 ), (vertices[j][0] + 15, vertices[j][1]+15), 5)

                        pygame.display.flip()
                        pygame.time.wait(f)
                # Проверка, что взяли три различные точки, две из них делаем красными а однй зеленой. От красной до красной рассматриваем путь через зеленую
                if i!=j and i!=k and j!=k:

                    screen.blit(img2, vertices[k])
                    screen.blit(img1, (vertices[j][0], vertices[j][1]+2))
                    draw_text(screen, str(spis[k]), 25, all_vertices[k][0] + 18,
                              all_vertices[k][1] + 6, BLACK)
                    draw_text(screen, str(spis[j]), 25, all_vertices[j][0] + 18,
                              all_vertices[j][1] + 6, BLACK)
                    pygame.display.flip()
                    pygame.time.wait(f)
                    # Проверка, что существуют ребра между точкой из которой смотрим и проходим.
                    if (
                    (vertices[i][0] + 15, vertices[i][1] + 15), (vertices[k][0] + 15, vertices[k][1] + 15)) in lines and ((vertices[k][0]+15, vertices[k][1]+15), (vertices[j][0]+15, vertices[j][1]+15)) in lines or (
                    (vertices[k][0] + 15, vertices[k][1] + 15), (vertices[i][0] + 15, vertices[i][1] + 15)) in lines and ((vertices[j][0] + 15, vertices[j][1] + 15),(vertices[k][0] + 15, vertices[k][1] + 15)) in lines or (
                    (vertices[i][0] + 15, vertices[i][1] + 15), (vertices[k][0] + 15, vertices[k][1] + 15)) in lines and ((vertices[j][0]+15, vertices[j][1]+15), (vertices[k][0]+15, vertices[k][1]+15)) in lines or (
                    (vertices[k][0] + 15, vertices[k][1] + 15), (vertices[i][0] + 15, vertices[i][1] + 15)) in lines and ((vertices[k][0]+15, vertices[k][1]+15), (vertices[j][0]+15, vertices[j][1]+15)) in lines:




                        pygame.draw.line(screen, RED, (vertices[i][0] + 15, vertices[i][1]+15 ), (vertices[k][0] + 15, vertices[k][1]+15), 5)
                        pygame.draw.line(screen, RED, (vertices[k][0] + 15, vertices[k][1]+15 ), (vertices[j][0] + 15, vertices[j][1]+15), 5)


                        pygame.display.flip()

                        pygame.time.wait(f)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                print(
                    f"Шаг {k + 1}: Расстояние от вершины {i+1} до вершины {j+1} через вершину {k+1} равно {dist[i][j]}")
                # В коде ниже происходит все то же самое, только возвращается цвет точек и ребер, который был изначально
                if i != j and i != k and j != k:
                    screen.blit(img, vertices[k])
                    draw_text(screen, str(spis[k]), 25, all_vertices[k][0] + 18,
                              all_vertices[k][1] + 6, BLACK)
                    pygame.display.flip()

                    if (
                            (vertices[i][0] + 15, vertices[i][1] + 15),
                            (vertices[k][0] + 15, vertices[k][1] + 15)) in lines and (
                    (vertices[k][0] + 15, vertices[k][1] + 15),
                    (vertices[j][0] + 15, vertices[j][1] + 15)) in lines or (
                            (vertices[k][0] + 15, vertices[k][1] + 15),
                            (vertices[i][0] + 15, vertices[i][1] + 15)) in lines and (
                    (vertices[j][0] + 15, vertices[j][1] + 15),
                    (vertices[k][0] + 15, vertices[k][1] + 15)) in lines or (
                            (vertices[i][0] + 15, vertices[i][1] + 15),
                            (vertices[k][0] + 15, vertices[k][1] + 15)) in lines and (
                    (vertices[j][0] + 15, vertices[j][1] + 15),
                    (vertices[k][0] + 15, vertices[k][1] + 15)) in lines or (
                            (vertices[k][0] + 15, vertices[k][1] + 15),
                            (vertices[i][0] + 15, vertices[i][1] + 15)) in lines and (
                    (vertices[k][0] + 15, vertices[k][1] + 15), (vertices[j][0] + 15, vertices[j][1] + 15)) in lines:
                        pygame.draw.line(screen, BLACK, (vertices[i][0] + 15, vertices[i][1]+15 ), (vertices[k][0] + 15, vertices[k][1]+15), 5)
                        pygame.draw.line(screen, BLACK, (vertices[k][0] + 15, vertices[k][1]+15 ), (vertices[j][0] + 15, vertices[j][1]+15), 5)


                        pygame.display.flip()
                        pygame.time.wait(f)
                if i!=j:
                    screen.blit(img, vertices[j])
                    draw_text(screen, str(spis[j]), 25, all_vertices[j][0] + 18,
                              all_vertices[j][1] + 6, BLACK)
                    pygame.display.flip()
                    if (
                    (vertices[i][0] + 15, vertices[i][1] + 15), (vertices[j][0] + 15, vertices[j][1] + 15)) in lines or           ((vertices[j][0] + 15, vertices[j][1] + 15), (vertices[i][0] + 15, vertices[i][1] + 15)) in lines:

                        pygame.draw.line(screen, BLACK, (vertices[i][0] + 15, vertices[i][1]+15 ), (vertices[j][0] + 15, vertices[j][1]+15), 5)

                        pygame.display.flip()
                        pygame.time.wait(f)

            screen.blit(img, vertices[i])
            draw_text(screen, str(spis[i]), 25, all_vertices[i][0] + 18,
                      all_vertices[i][1] + 6, BLACK)
            pygame.display.flip()
            pygame.time.wait(f)

    return dist


result = floyd_warshall(graph)
print(lines, vertices)
# Отображаем итоговый результат
print("\nFinal result:")
for row in result:
    print(row)


pygame.quit()
sys.exit()