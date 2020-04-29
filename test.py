"""list_line = []

with open("txt/Maze1.txt","r") as input_file:
    for every_line in input_file:
        list_of_elt_per_line = every_line.strip().split(' ')
        list_line.append(list_of_elt_per_line)       
print(list_line)

#Let's Build the Maze
line_count = 0
list_block = []
list_door = []
list_keys = []
list_ways = []
#position of an element in the Maze
x = 0
y = 0
for line in list_line:
    for elt in line:
        if elt == 's': #start
            start = Actor(maze_objects[elt])
            start.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
        elif elt == "1": #block
            block = Actor(maze_objects[elt])
            block.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_block.append(block)
        elif elt == "0":
            count_path += 1
            path = Actor(maze_objects[elt])
            path.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_ways.append(path)
        elif elt == "e":
            end = Actor(maze_objects[elt])
            end.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
        elif elt == "b":
            y_door = Actor(maze_objects[elt])
            y_door.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_door.append(y_door)
        elif elt == "a":
            y_key = Actor(maze_objects[elt])
            y_key.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_keys.append(y_key)
        elif elt == "i":
            b_door = Actor(maze_objects[elt])
            b_door.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_door.append(b_door)
        elif elt == "h":
            b_key = Actor(maze_objects[elt])
            b_key.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_keys.append(b_key)
        elif elt == "c":
            g_door = Actor(maze_objects[elt])
            g_door.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_door.append(g_door)
        elif elt == "d":
            g_key = Actor(maze_objects[elt])
            g_key.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_keys.append(g_key)
        elif elt == "g":
            r_door = Actor(maze_objects[elt])
            r_door.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_door.append(r_door)
        elif elt == "h":
            r_key = Actor(maze_objects[elt])
            r_key.topleft = PIXEL_IMAGE * x, PIXEL_IMAGE * y
            list_keys.append(r_key)

        y += 1
    x += 1
    """          
        

TILE_SIZE = 64
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8

tiles = ['path', 'block', 'reward']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

player = Actor("pacman", pos=(1 * TILE_SIZE, 1 * TILE_SIZE)) #, anchor=(0, 0),

def draw():
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
    player.draw()