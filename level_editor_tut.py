import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 740
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16
MAX_COLS = 16
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 11
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll = 0
scroll_up_down = 0
scroll_speed = 1
x = 0
y = 0
scroll_x = 0
scroll_y = 0

left = 1
right = 1
up = 1
down =1

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

tileset_images = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tileset_images.append(img)

# define colours
GREEN = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0, 0, 0, 255)
GRAY = (131, 139, 139)

# define font
font = pygame.font.SysFont('Roboto', 30)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y, x_offset=0):
    img = font.render(text, True, text_col)
    screen.blit(img, (x + x_offset, y))


# create function for drawing background
def draw_bg():
    screen.fill(BLACK)

# draw grid
def draw_grid(scroll_x, scroll_y):
    # vertical lines (including new column)
    for c in range(left - 1, SCREEN_WIDTH // TILE_SIZE + right):
        pygame.draw.line(screen, GRAY, ((c * TILE_SIZE) - scroll_x, 0), ((c * TILE_SIZE) - scroll_x, SCREEN_HEIGHT))

    # horizontal lines
    for c in range(up, SCREEN_HEIGHT // TILE_SIZE + down):
        pygame.draw.line(screen, GRAY, (0, (c * TILE_SIZE) + scroll_y), (SCREEN_WIDTH, (c * TILE_SIZE) + scroll_y))


# function for drawing the world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, gid in enumerate(row):
            if gid >= 0:
                tile_img = tileset_images[gid]
                screen.blit(tile_img, (x * TILE_SIZE - scroll_x, y * TILE_SIZE + scroll_y))


# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0




run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid(scroll_x, scroll_y)
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 1, 1)
    draw_text(f'x{x}, y{y}', font, WHITE, 1, 30)
    #draw_text('Press q or a to change level', font, WHITE, 700, 500)



    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll the map
    if scroll_left == True:
        if scroll_x > 0:
            scroll_x -= 5 * scroll_speed
            left -= 1
    if scroll_right == True:
        scroll_x += 5 * scroll_speed
        right += 1
    if scroll_up == True:
        if scroll_y > 0:
            scroll_y += 5 * scroll_speed
            up -= 1
    if scroll_down == True:
        scroll_y -= 5 * scroll_speed
        down += 1

    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_x) // TILE_SIZE
    y = (pos[1] - scroll_y) // TILE_SIZE

    # check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if y >= 0 and y < len(world_data) and x >= 0 and x < len(world_data[y]):
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
            # check if the mouse pointer goes beyond the current level's boundaries
            if x >= MAX_COLS:
                # add a new column to world_data
                for row in world_data:
                    row.append(-1)
                MAX_COLS += 1

            if y >= ROWS:
                # add a new row to world_data
                new_row = [-1] * MAX_COLS
                world_data.append(new_row)
                ROWS += 1
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                level += 1
            if event.key == pygame.K_a and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            # save and load data
            if event.key == pygame.K_s and pygame.KMOD_CTRL:
                # save level data
                with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    for row in world_data:
                        writer.writerow(row)
            # load in level data
            if event.key == pygame.K_l:
                # reset scroll back to the start of the level
                scroll = 0
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile) - 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
