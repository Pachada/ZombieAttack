#Daniel Trejo González
#30/11/2020
#Dado un Grid de 20 x 20 con paredes, zombies, personal y ventantas, hacer una visualicación de como
#trabajoders se mueven a la salida y los zombies se mueven aleatoriamente e infectan personas

import pygame
import math
from queue import PriorityQueue
import random


WIDTH = 600
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Ataque zombie en Atomic Labs")

RED = (255, 0, 0)       #close
GREEN = (0, 255, 0)     #zombie
BLUE = (0, 0, 255)      #human
YELLOW = (255, 255, 0)  #open
WHITE = (255, 255, 255) #empty
BLACK = (0, 0, 0)       #wall    
PURPLE = (128, 0, 128)  
ORANGE = (255, 165 ,0)  
GREY = (128, 128, 128)  
TURQUOISE = (64, 224, 208) #exit 

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_wall(self):
        return self.color == BLACK
    
    def is_zombie(self):
        return self.color == GREEN
    
    def is_human(self):
        return self.color == BLUE
    
    def is_exit(self):
        return self.color == TURQUOISE
    
    def is_window(self):
        return self.color == ORANGE
    
    def is_close(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == YELLOW
    
    def make_wall(self):
        self.color = BLACK
    
    def make_zombie(self):
        self.color = GREEN
    
    def make_human(self):
        self.color = BLUE
    
    def make_exit(self):
        self.color = TURQUOISE
    
    def make_close(self):
        self.color = RED
    
    def make_open(self):
        self.color = YELLOW

    def make_window(self):
        self.color = ORANGE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # MOVING DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

#Create the rows and nodes
def make_grid(rows, width):
    zombie_count = 0
    zombie_one = zombie_spawn_location()
    zombie_two = zombie_spawn_location()
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            # Make the external walls
            if i == 0 or j == 0 or i == rows - 1 or j == rows - 1:
                node.make_wall()
            
            # Make iner walls
            if(check_if_internal_wall(i, j)):
                node.make_wall()
            
            # Make Windows
            if (j == 0 and (i == 3 or i == 4 or i == 5 or i == 6 or i == 13 or i == 14 or i == 15 or i == 16)):
                node.make_window()

            # Make the exit
            if i == rows - 1 and (j == 18 or j == 17 or j == 16 or j == 15 ):
                node.make_exit()
            grid[i].append(node)

            # Make humans
            if check_if_human(i, j):
                node.make_human()
            
            # Make zombies
            if node.is_window() and zombie_count < 2:
                if i == zombie_one or i == zombie_two:
                    zombie_count += 1
                    node.make_zombie()


            
    return grid 

def zombie_spawn_location() -> int:
    if (random.randrange(0,2) == 0):
        return random.randrange(3, 7)
    return random.randrange(13, 17)

def check_if_internal_wall(i, j):
    internal_walls = [[2,4], [3,4], [4,4], [5,4], [6,4], [7,4], [10,4], [11,4], [12,4], [13,4], [14,4], [15,4], [16,4],
    [13,5], [13,6], [13,7], [1,10], [2,10], [3,10], [4,10], [5,10], [6,10], [7,10],[8,10], [12,10], [13,10], [14,10], [15,10], [16,10],
    [17,10], [18,10], [2,12], [3,12], [4,12], [5,12], [6,12], [7,12], [12,12], [12,13], [12,14], [12,15], [16,12], [16,13], [16,14], 
    [16,15],[2,16], [3,16], [4,16], [5,16], [6,16], [7,16] ]
    
    return [i, j] in internal_walls

def check_if_human(i, j):
    humans = [[9,1], [3,3], [6,3], [11,3], [15,3], [4, 5], [16, 6], [2, 7], [7, 7], [3, 8], [17,8], [11,9], [13,12], [3,13], [17,13],
    [6,14], [10,15], [3,17], [7,17], [13,17]]

    return [i, j] in humans


#We draw the lines of the squares to make it look like a grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#Draw all
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

#Distancia de p1 al p2, usando Manhattan distance   f(n) = h(n) + g(n)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def recontruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#A* Pathfindig algorithm 
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            recontruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True        # Make path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_close()

    return False


def main(win, width):
    grid = make_grid(ROWS, width)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main(WIN, WIDTH)