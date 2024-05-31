import pygame

pygame.init()

BLACK = (0, 0, 0)

height = 35
width = 35
bsize = 15
fps = 100


def distribute_down(grid, i, j):
    if grid[i+1][j] == -1:
        return
    
    if grid[i][j] + grid[i+1][j] <= 1:
        grid[i+1][j] += grid[i][j]
        grid[i][j] = 0
    else:
        grid[i][j] -= 1 - grid[i+1][j]
        grid[i+1][j] = 1
        distribute_sideways(grid, i, j)


def distribute_sideways(grid, i, j):
    modified = [j]
    if j+1 < len(grid[0]) and grid[i][j+1] != -1:
        modified.append(j+1)
    if j-1 >= 0 and grid[i][j-1] != -1:
        modified.append(j-1)

    avg = sum(map(lambda x: grid[i][x], modified)) / len(modified)
    for x in modified:
        grid[i][x] = avg


def move_water(grid, i, j):
    if i+1 >= len(grid):
        grid[i][j] = 0
    elif grid[i+1][j] != -1:
        distribute_down(grid, i, j)
    elif grid[i+1][j] == -1:
        distribute_sideways(grid, i, j)


def update(grid):
    for i in range(len(grid))[::-1]:
        for j in range(len(grid[0])):
            if grid[i][j] != -1:
                move_water(grid, i, j)


def render(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rect = (j*bsize, i*bsize, bsize, bsize)
            if grid[i][j] == -1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                intensity = round(255 - (grid[i][j] * 255))
                color = (intensity, intensity, 255)
                pygame.draw.rect(screen, color, rect)


def snap_to_grid(mouse_pos):
    j = mouse_pos[0] - (mouse_pos[0] % bsize)
    i = mouse_pos[1] - (mouse_pos[1] % bsize)
    return i // bsize, j // bsize


def generate_empty_grid():
    return [[0 for _ in range(width)] for _ in range(height)]


screen = pygame.display.set_mode([width*bsize, height*bsize])
pygame.display.set_caption('Waterfall Simulation')

clock = pygame.time.Clock()

grid = generate_empty_grid()
mode = 'ground'

done = False
mouse_down = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                grid = generate_empty_grid()
            
            if event.key == pygame.K_1:
                mode = 'erase'
            elif event.key == pygame.K_2:
                mode = 'water'
            elif event.key == pygame.K_3:
                mode = 'ground'

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    render(grid)
    update(grid)

    if mouse_down:
        i, j = snap_to_grid(pygame.mouse.get_pos())
        if mode == 'erase':
            grid[i][j] = 0
        elif mode == 'water':
            grid[i][j] = 1
        elif mode == 'ground':
            grid[i][j] = -1

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
