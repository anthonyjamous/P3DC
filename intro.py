import pgzero, pgzrun

maze = []

PIXEL_IMAGE = 50
#it'll allow us to define the dimensions dynamically
NB_OF_ELEMENT_PER_LINE = 0

maze_objects = {
    "1" : "block",
    "0" : "path",
    "s" : "pacman",
    "e" : "reward",
    "b" : "yellow_door",
    "a" : "yellow_key",
    "i" : "blue_door",
    "h" : "blue_key",
    "c" : "green_door",
    "d" : "green_key",
    "g" : "red_door",
    "f" : "red_key"
    "2+": "range"
}

with open("txt/Maze1.txt","r") as input_file:
    for every_line in input_file:
        list_of_column_per_line = every_line.strip().split(' ')
        NB_OF_ELEMENT_PER_LINE = len(list_of_column_per_line)
        maze.append(list_of_column_per_line)       

#Now we can define the WIDTH and HEIGHT
WIDTH = PIXEL_IMAGE * NB_OF_ELEMENT_PER_LINE
HEIGHT = PIXEL_IMAGE * NB_OF_ELEMENT_PER_LINE

########################################################################################################
#  sprites
player = Actor(maze_objects["s"],anchor=(0,0))
enemy = Actor("ghost", anchor=(0,0), pos = (3* PIXEL_IMAGE, 6 * PIXEL_IMAGE))

#find the postion of player
for x in range(len(maze)):
    for y in range(len(maze[x])):
        if maze [x][y] == "s":
            player.pos = x*PIXEL_IMAGE, y*PIXEL_IMAGE





def draw():
    screen.clear()
    # Build the Maze
    #knowing that I used a dictionnary, I want to check the type of 
    #the sprite to be sure to insert the correct element  
    for line in range(len(maze)):
        for column in range(len(maze[line])):
            x = column * PIXEL_IMAGE
            y = line * PIXEL_IMAGE
            if maze[line][column] == "s": #start
                screen.blit(maze_objects["0"], (x, y))#fill with a path
            else: #fill the others element in the screen
                screen.blit(maze_objects[maze[line][column]], (x, y))
                
    player.draw()
    enemy.draw()

def on_key_down(key):

    row = int(player.y / PIXEL_IMAGE)
    column = int(player.x / PIXEL_IMAGE)
    if key == keys.UP:
        row = row - 1
    if key == keys.DOWN:
        row = row + 1
    if key == keys.LEFT:
        column = column - 1
    if key == keys.RIGHT:
        column = column + 1
    
    sprite = maze_objects[maze[row][column]]
    print(f'sprite found: {sprite}')

    if sprite == "path" or sprite == "pacman":
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x,y))
    elif sprite == "reward":
        player.x = column * PIXEL_IMAGE
        player.y = row * PIXEL_IMAGE
        print("You Reached the end")
        exit()
    else:
        pass

     

pgzrun.go()