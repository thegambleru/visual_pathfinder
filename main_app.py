import pygame
import math
from queue import PriorityQueue


#Display resolution and window name

side = 800
win = pygame.display.set_mode((side,side))
pygame.display.set_caption("A* Visual Pathfinder")


#colors_list

red = (203,75,75)
green = (77,167,77)
white = (175,216,248)
black = (0,0,0)
purple = (148,64,237)
orange = (237,194,64)
grey = (128,128,128)
turq = (0,119,119)

class Node:
    def __init__(self,row,col,side,total_rows):
        self.row = row
        self.col = col
        self.x = row * side
        self.y = col * side
        self.color = white
        self.neighbors = []
        self.side = side
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col

    def visited(self):
        return self.color == red

    def open(self):
        return self.color == green

    def wall(self):
        return self.color == black

    def start(self):
        return self.color == orange

    def end(self):
        return self.color == turq

    def reset(self):
        self.color = white

    def to_visited(self):
        self.color = red

    def to_open(self):
        self.color = green

    def to_wall(self):
        self.color = black

    def to_start(self):
        self.color = orange

    def to_end(self):
        self.color = turq

    def to_path(self):
        self.color = purple

    def draw(self,win):
        pygame.draw.rect(win,self.color, (self.x,self.y,self.side,self.side) )

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].wall():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].wall():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].wall():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].wall():
            self.neighbors.append(grid[self.row][self.col - 1])



    def __lt__(self,other):
        return False


def her(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def path(via,current,draw):
    while current in via:
        current = via[current]
        current.to_path()
        draw()

def algorithm(draw,grid,start,end):
    count = 0 
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    via = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = her(start.get_pos(), end.get_pos() )

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path(via,end,draw)
            end.to_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                via[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + her(neighbor.get_pos(), end.get_pos() )
                if neighbor not in open_set_hash:
                    count += 1 
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.to_open()

        draw()

        if current != start:
            current.to_visited()

    return False


def make_grid(rows,side):
    grid = []
    gap = side // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def gridlines(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,grey, (0,i * gap), (width, i * gap) )
        for j in range(rows):
            pygame.draw.line(win,grey, (j * gap, 0), (j * gap, width) )

def draw(win,grid,rows,side):
    win.fill(white)

    for row in grid:
        for node in row:
            node.draw(win)

    gridlines(win,rows,side)

    pygame.display.update()

def get_click_pos(pos,rows,side):
    gap = side // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win,side):
    rows = 50
    grid = make_grid(rows, side)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,rows,side)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, rows, side)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.to_start()

                elif not end and node != start:
                    end = node
                    end.to_end()

                elif node != end and node != start:
                    node.to_wall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, rows, side)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None               
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win,grid,rows,side), grid, start, end)
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows,side)


    pygame.quit()


main(win,side)