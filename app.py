"""This is a simple implementation of Conway's Game of Life.
The rules are simple:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction."""

import pygame
import random

pygame.init()

# constants
WIDTH = 800
HEIGHT = 800
FPS = 60
CELL_SIZE = 10
CELLS_WIDE = WIDTH // CELL_SIZE
CELLS_HIGH = HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)

# set up the drawing window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# draw the grid
def draw_grid(positions):

    for position in positions:
        col, row = position
        # we need to figure out the actual position in pixels using col and row
        top_left = (col * CELL_SIZE, row * CELL_SIZE)
        pygame.draw.rect(screen, GREEN, (top_left, (CELL_SIZE, CELL_SIZE)))

    for row in range(CELLS_HIGH):
        pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))
    for col in range(CELLS_WIDE):
        pygame.draw.line(screen, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT))

def adjust_grid(positions):
    # only look at cells that could poteniallly change status
    all_neighbours = set()
    new_positions = set()

    # check alive cells to determine if they live or die
    for position in positions:
        neighbours = get_neighbours(position)
        all_neighbours.update(neighbours)

        # keep only alive neighbours
        neighbours = list(filter(lambda x: x in positions, neighbours))
        # if there is 2 or 3 alive neighbours, keep cell alive to next round
        if len(neighbours) == 2 or len(neighbours) == 3:
            new_positions.add(position)

    # check dead cells to determine if they come to life
    for position in all_neighbours:
        neighbours = get_neighbours(position)
        # keep only alive neighbours
        neighbours = list(filter(lambda x: x in positions, neighbours))

        # if there is 3 alive neighbours, bring cell to life
        if len(neighbours) == 3:
            new_positions.add(position)
    
    return new_positions

def get_neighbours(position):
    # get all eight neighbours of a cell
    x ,y = position
    neighbours = []

    for dx in [-1, 0, 1]:
        # check if x is out of bounds
        if x + dx < 0 or x + dx > CELLS_WIDE:
            continue 
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > CELLS_HIGH:
                continue
            if dx == dy == 0:
                continue
            neighbours.append((x + dx, y + dy))
    return neighbours
# generate random positions
def gen(num:int):
    # generate that many random col and row positions return as a set
    return set([(random.randrange(0, CELLS_WIDE), random.randrange(0, CELLS_HIGH)) for _ in range(num)])
# main loop
def main():
    running = True
    playing = False
    count = 0 
    frequency = 30

    positions = set()
    # positions.add((0,0))
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
        if count >= frequency:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # check if mouse clicked, if true add position to set
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                # translate x adn y to col and row
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if (col, row) in positions:
                    positions.remove((col, row))
                else:
                    positions.add((col, row))
            if event.type == pygame.KEYDOWN:
            # check key pressed for clear, generate and pause
                if event.key == pygame.K_c:
                    positions.clear()
                    playing = False
                    count = 0
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 7) * CELLS_WIDE)
                if event.key == pygame.K_SPACE:
                    playing = not playing
        # backgroun color
        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
