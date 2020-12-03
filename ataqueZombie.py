#Daniel Trejo González
#30/11/2020
#Dado un Grid de 20 x 20 con paredes, zombies, personal y ventantas, hacer una visualicación de como
#trabajoders se mueven a la salida y los zombies se mueven aleatoriamente e infectan personas

import pygame
from queue import PriorityQueue
import time
import random
from random  import randrange


WIDTH = 600
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, WIDTH))
GRID = None
EXITS = []
iteration_count = 1
zombie_count = 0
humans_count = 20
saved_humans = 0

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
        self.path = []
        self.infected = False
        self.time_for_zombie = 2
        self.just_moved = False
    
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
    
    def is_open(self):
        return self.color == YELLOW

    def is_infected(self):
        return self.infected
    
    def make_wall(self):
        self.color = BLACK
    
    def make_zombie(self):
        self.make_infected()
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
    
    def make_path(self):
        self.color = PURPLE
    
    def make_infected(self):
        self.infected = True

    def check_if_already_zombie(self):
        global zombie_count
        global humans_count
        if self.time_for_zombie == 0:
            self.make_zombie()
            zombie_count += 1
            humans_count -= 1
            return True
        else:
            self.time_for_zombie -= 1
            return False
    
    def set_time_for_zombie(self, x):
        self.time_for_zombie = x
    
    def pass_infection(self, node):
        node.make_infected()
        node.set_time_for_zombie(self.time_for_zombie)

    def reset(self):
        self.color = WHITE
        self.time_for_zombie = 2
        self.infected = False
        self.path = []
        self.just_moved = False

    def set_path(self,path):
        self.path = path

    def add_to_path(self,node):
        self.path.insert(0,node)

    def get_neighbors(self):
        return self.neighbors

    def just_move_last_iteration(self):
        self.just_moved = True
    
    def zombie_attack(self):
        self.update_neighbors(GRID)
        for neighbor in self.neighbors:
            if neighbor.is_human() and not neighbor.is_infected():
                neighbor.make_infected()
                print(f"Human infected at x: {neighbor.get_pos()[0]}, y: {neighbor.get_pos()[1]}")

    def move(self):
        if self.just_moved:
            self.just_moved = False
            return
        
        if self.is_human():
            if self.is_infected():
                if self.check_if_already_zombie():
                    return
            
            global saved_humans
            global humans_count       
            if self in EXITS:
                saved_humans += 1
                humans_count -= 1
                print(f"Human saved at x: {self.get_pos()[0]}, y: {self.get_pos()[1]}")
                self.reset()
                self.make_exit()
                return

            if (len(self.path) == 0):
                print(f"Human saved at x: {self.get_pos()[0]}, y: {self.get_pos()[1]}")
                saved_humans += 1
                humans_count -= 1
                self.reset()
                return
            
            
            if (len(self.path)> 2):
                if not self.path[1].is_human() and not self.path[1].is_zombie():
                    self.path.pop(0)
            if not self.path[0].is_human() and not self.path[0].is_zombie():
                new_position = self.path.pop(0)
                new_position.set_path(self.path)
                new_position.make_human()
                new_position.just_move_last_iteration()
                if self.is_infected():
                    new_position.make_infected()
                    new_position.set_time_for_zombie(self.time_for_zombie)
                self.reset()
        
        elif self.is_zombie():
            self.zombie_attack()
            steps = 0
            new_position = self
            last_position = self

            while steps != 4:
                new_position.update_neighbors(GRID)
                move = randrange(0, len(new_position.neighbors))
                new_position_temp = new_position.neighbors[move]
                if not new_position_temp.is_human() and not new_position_temp == last_position:
                    steps += 1
                    new_position.reset()
                    new_position = new_position_temp

            new_position.make_zombie()
            new_position.just_move_last_iteration()
            new_position.zombie_attack()

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall() and not grid[self.row + 1][self.col].is_window() and not grid[self.row + 1][self.col].is_zombie(): # MOVING DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall() and not grid[self.row - 1][self.col].is_window() and not grid[self.row - 1][self.col].is_zombie(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall() and not grid[self.row][self.col + 1].is_window() and not grid[self.row][self.col + 1].is_zombie(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall() and not grid[self.row][self.col - 1].is_window() and not grid[self.row][self.col - 1].is_zombie(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

#Create the rows and nodes
def make_grid(rows, width):
    global zombie_count
    zombie_one = 0
    zombie_two = 0
    while zombie_one == zombie_two:
        zombie_one = zombie_spawn_location()
        zombie_two = zombie_spawn_location()
    grid = []
    gap = width // rows
    global EXITS
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
                EXITS.append(node)

            # Make humans
            if check_if_human(i, j):
                node.make_human()
            
            # Make zombies
            if node.is_window() and zombie_count < 2:
                if i == zombie_one or i == zombie_two:
                    zombie_count += 1
                    node.make_zombie()
                    print(f"Zombie enter from window x: {i}, y: {j}")

            grid[i].append(node)
            
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

def recontruct_path(start, came_from, current):
    while current in came_from:
        current = came_from[current]
        start.add_to_path(current)

#A* Pathfindig algorithm 
def algorithm(grid, start, end):
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
            recontruct_path(start, came_from, end)
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

    return False


def main(win, width):
    global GRID
    name = "ATAQUE ZOMBIE EN ATOMIC LABS"
    print(f"\n{name:*^60}")
    grid = make_grid(ROWS, width)
    GRID = grid

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    for row in grid:
        for node in row:
            exit = randrange(0, len(EXITS))
            if node.is_human():
                algorithm(grid, node, EXITS[exit])
                
    run = True
    global iteration_count
    file = open("InfoAtaqueZombie.txt", "w+")
    while humans_count > 0 and run:
        time.sleep(1)  #Aquí se puede cambiar la velocidad con la que se ve cada Frame
        draw(win, grid, ROWS, width)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for row in grid:
            for node in row:
                if node.is_human() or node.is_zombie():
                    node.move()
        
        file.write(f"\nIteration num: {iteration_count} | Zombies: {zombie_count} | Humans at the office: {humans_count} | Humans saved: {saved_humans}")
        iteration_count += 1

    print(f"Iteration num: {iteration_count} | Zombies: {zombie_count} | Humans at the office: {humans_count} | Humans saved: {saved_humans}")            
    file.close()
    pygame.quit()

if __name__ == '__main__':
    main(WIN, WIDTH)
