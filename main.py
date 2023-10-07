import pygame
import time
from random import *
from collections import deque


def draw_sqrs(count, height, width, separator, c1, c2, c3, c4, c_reg, lst):
    for row in range(count):
        y = row * height + (row + 1) * separator
        for col in range(count):
            x = col * width + (col + 1) * separator

            sqr_looking = lst[row][col]
            if sqr_looking == 1:
                sqr_color = c1
            elif sqr_looking == 2:
                sqr_color = c2
            elif sqr_looking == 3:
                sqr_color = c3
            elif sqr_looking == 4:
                sqr_color = c4
            else:
                sqr_color = c_reg

            pygame.draw.rect(display, sqr_color, (x, y, width, height))


def make_maze(count):
    """making starter list"""
    lst = [[0 if x % 2 == 0 and y % 2 == 0 else 3 for x in range(count)] for y in range(count)]
    visited = ((count + 1) // 2)**2

    print("--- %s maze was started to made seconds ---" % (time.time() - start_time))

    """maze making algoritm"""
    now_sqr = [0, 0]
    searched = list()
    searched.append(now_sqr)
    sqrs_deque = deque()
    while visited != 0:
        neighbors = [n for n in return_near(now_sqr[0], now_sqr[1], 2, count) if n not in searched]
        if len(neighbors) > 0:
            sqrs_deque.append(now_sqr)
            ran_neighbor = choice(neighbors)
            lst = destroy_wall(now_sqr[0], now_sqr[1], ran_neighbor[0], ran_neighbor[1], lst)
            now_sqr = ran_neighbor
            searched.append(now_sqr)
            visited -= 1
        elif len(sqrs_deque) > 0:
            now_sqr = sqrs_deque.pop()
        else:
            found = False
            ran_x = ran_y = 0
            while not found:
                ran_x, ran_y = randint(0, count - 1), randint(0, count - 1)
                if [ran_x, ran_y] not in searched and lst[ran_y][ran_x] == 0:
                    found = True
            now_sqr = [ran_x, ran_y]
            searched.append(now_sqr)
    return lst


def destroy_wall(x_start, y_start, x_way, y_way, lst):
    """finding wall x"""
    target_x = x_start
    if x_start > x_way:
        target_x = x_start - 1
    elif x_start < x_way:
        target_x = x_start + 1

    """finding wall y"""
    target_y = y_start
    if y_start > y_way:
        target_y = y_start - 1
    elif y_start < y_way:
        target_y = y_start + 1

    """destroying wall"""
    lst[target_y][target_x] = 0
    return lst


def return_near(x, y, k, count):
    return_list = []
    if 0 <= y - k <= count - 1 and 0 <= x <= count - 1:
        return_list.append([x, y - k])
    if 0 <= y <= count - 1 and 0 <= x + k <= count - 1:
        return_list.append([x + k, y])
    if 0 <= y + k <= count - 1 and 0 <= x <= count - 1:
        return_list.append([x, y + k])
    if 0 <= y <= count - 1 and 0 <= x - k <= count - 1:
        return_list.append([x - k, y])

    return tuple(return_list)


def find_way(queue, lst, count):
    searched = []
    parents = dict()
    parents[str([0, 0])] = None
    while True:
        now_sqr = queue.popleft()
        if now_sqr not in searched and lst[now_sqr[1]][now_sqr[0]] != 3:
            """creating parents list"""
            for n in return_near(now_sqr[0], now_sqr[1], 1, count):
                if str(n) not in parents:
                    if lst[n[1]][n[0]] != 3:
                        parents[str([n[0], n[1]])] = now_sqr

            if lst[now_sqr[1]][now_sqr[0]] == 1:
                """if found do this"""
                while now_sqr != [0, 1] and now_sqr != [1, 0]:
                    now_sqr = parents.get(str(now_sqr))
                    lst[now_sqr[1]][now_sqr[0]] = 2
                return lst

            if lst[now_sqr[1]][now_sqr[0]] == 0 or lst[now_sqr[1]][now_sqr[0]] == 4:
                """adding new sqrs to queue"""
                queue += return_near(now_sqr[0], now_sqr[1], 1, count)
                searched.append(now_sqr)


pygame.init()
start_time = time.time()

"""settings"""
maze_spawn = True

sqr_width = sqr_height = 15
sqr_count = 51
sep = 1

display_width = (sqr_width + sep) * sqr_count + sep
display_height = (sqr_height + sep) * sqr_count + sep
display_color = (150, 150, 150)


sqr_color_reg = (0, 0, 0)
sqr_color_active = (100, 0, 255)
sqr_color_way = (255, 255, 255)
sqr_color_wall = (0, 200, 0)
sqr_color_start = (255, 0, 0)

wall_coof = 0.2

"""display part"""
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pathfinder")
display.fill(display_color)

"""creating main massiv with numbers"""
if maze_spawn:
    sqrs = make_maze(sqr_count)
    print("--- %s maze was made seconds ---" % (time.time() - start_time))
else:
    sqrs = []
    for i in range(sqr_count):
        mas = []
        for j in range(sqr_count):
            if random() < wall_coof:
                mas.append(3)
            else:
                mas.append(0)
        sqrs.append(mas)

"""creating start sqr"""
sqrs[0][0] = 4
way_point = None

"""main game loop"""
in_game = True
while in_game:
    for event in pygame.event.get():
        """closing game"""
        if event.type == pygame.QUIT:
            in_game = False
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            """getting mouse pos"""
            x_mouse, y_mouse = pygame.mouse.get_pos()

            """finding position in sqrs from mouse pos"""
            column = x_mouse // (sep + sqr_width)
            row = y_mouse // (sep + sqr_height)

            """in not wall, create waypoint"""
            if sqrs[row][column] == 0:
                for i in range(sqr_count):
                    for j in range(sqr_count):
                        if sqrs[i][j] == 1 or sqrs[i][j] == 2:
                            sqrs[i][j] = 0

                sqrs[row][column] = 1
                search_queue = deque()
                search_queue.append([0, 0])
                try:
                    sqrs = find_way(search_queue, sqrs, sqr_count)
                except IndexError:
                    print('cant get to this place')

    """drawing sqrs"""
    draw_sqrs(sqr_count, sqr_height, sqr_width, sep,
              sqr_color_active,
              sqr_color_way,
              sqr_color_wall,
              sqr_color_start,
              sqr_color_reg,
              sqrs)

    pygame.display.update()

# some test here