import enum, time
import pgzrun, pgzero
######################

PIXEL_IMAGE = 50

#it'll allow us to define the dimensions dynamically
NB_OF_ELEMENT_PER_LINE = 0
NB_OF_ELEMENT_PER_COLUMN = 0
n = 0
F1_PRESSED = 0
ENDPOINT = 0
PLAYER_MOVE = 0

has_blue_key = 0
has_green_key = 0
has_red_key = 0
has_yellow_key = 0
game_over = 0
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
    "f" : "red_key",
    "r" : "pink_cell",
    "z" : "ghost"
}

LAST_X = 0  # stores the last value of x in the maze
LAST_Y = 0  # stores the last value of Y in the maze
START_X = 0  # stores the starting position x in the maze
START_Y = 0  # stores the starting position y in the maze
DESTINATION_X = 0  # stores the ending position x in the maze
DESTINATION_Y = 0  # stores the ending position y in the maze
maze = {}
positionssaved = []
shortestpath=[]

class Values(enum.Enum):
    MOVABLE = '0'
    WALL = '1'
    START = 's'
    END_POINT = 'e'
    RED_DOOR = 'g'
    RED_KEY = 'f'
    GREEN_DOOR = 'c'
    GREEN_KEY = 'd'
    BLUE_DOOR = 'i'
    BLUE_KEY = 'h'
    YELLOW_DOOR = 'b'
    YELLOW_KEY = 'a'
    GHOST_RANGE = 'r'
    GHOST = 'z'

class Positions(enum.Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# In this method, we will read the maze from the file, we will store it in a dictionary ,
# which the key will be a string with "position x,position y" concatenated and separated by a comma,
# and  as value one of the options: 0 1 s e g f c d i h 2 3 4 ...We will also save last x, last y , start x and
# start y in a global variable for later use
def readfile(filename):
    global LAST_Y
    global LAST_X
    global START_Y
    global START_X
    global DESTINATION_X
    global DESTINATION_Y
    global positionssaved
    global shortestpath
    global NB_OF_ELEMENT_PER_LINE
    global NB_OF_ELEMENT_PER_COLUMN
    global n
    global F1_PRESSED

    with open(filename, 'r') as f:
        posx = 0  # initialize x
        posy = 0  # initialize y
        for line in f:
            linestripped = line.replace(" ", "").rstrip("\n")  # remove "\n from line and white spaces"
            NB_OF_ELEMENT_PER_LINE += 1  # len(line) of txt
            for character in linestripped:              
                if character is Values.START.value:  # if it is the start position we need to save its coordinates
                    START_X = posx
                    START_Y = posy
                if character is Values.END_POINT.value:  # if it is the start position we need to save its coordinates
                    DESTINATION_X = posx
                    DESTINATION_Y = posy

                key = str(posx) + "," + str(
                    posy)  # we used the combination "x,y" as the key of each element in the dictionnary because it is unique
                maze[key] = character  # for the key "x,y" , we add character as its value
                posx += 1  # increment x when moving right
            LAST_X = posx  # store the last x index for later use
            posx = 0
            posy += 1  # increment y when moving down
            LAST_Y += 1  # store the last y index for later use
    a=3
    NB_OF_ELEMENT_PER_COLUMN = len(linestripped)
    #  file closed

    # change the maze depending on the ghost range
    manageghosts()

    # findshortestpath(positionssaved,END_X,END_Y)
    followpath(START_X, START_Y, 0,
               positionssaved)  # call the algorithm on the starting position, first time the direction will be empty
    #print( managedoors(DESTINATION_X, DESTINATION_Y))
    shortestpath =  managedoors(DESTINATION_X, DESTINATION_Y)

    print(shortestpath)



def iteratelist(tuple,list,k):
    for i in range (0,k):
        if tuple in list[i]:
            return 0
    return 1


def fetchshortestpath(destx, desy):
    i = 0  # number of steps
    j = 1  # number of paths
    paths = {}
    paths[0]=[(destx,desy)]


    counter = 0
    x = destx
    y = desy
    while i <= len(positionssaved):  # until we go from the end point to the starting point
        i += 1
        vai = 1
        for l in range(0, j):
            tuplexy= paths[l][len(paths[l]) - 1]
            x = tuplexy[0]
            y = tuplexy[1]

            tuple1 = (x - 1,y)

            if tuple1 in positionssaved and iteratelist(tuple1,paths,j):

                paths[l].append(tuple1)
                counter += 1

            tuple2 = (x + 1, y)
            if tuple2 in positionssaved and iteratelist(tuple2,paths,j):
                if counter > 0:
                    j = j + 1
                    fakepath=paths[l].copy()
                    fakepath.pop()
                    paths[j - 1] = fakepath
                    vai = 0
                if vai:
                    paths[l].append(tuple2)
                    counter += 1
                    vai = 1


            tuple3 = (x, y + 1)
            if tuple3 in positionssaved and iteratelist(tuple3,paths,j):
                if counter > 0:
                    j = j + 1
                    fakepath = paths[l].copy()
                    fakepath.pop()
                    paths[j - 1] = fakepath
                    vai= 0
                if vai:
                    paths[l].append(tuple3)
                    counter += 1
                    vai=1

            tuple4 = (x , y - 1)
            if tuple4 in positionssaved and iteratelist(tuple4,paths,j):
                if counter > 0:
                    j = j + 1
                    fakepath = paths[l].copy()
                    fakepath.pop()
                    paths[j - 1] = fakepath
                    vai=0
                if vai:
                    paths[l].append(tuple4)
                    counter += 1
                    vai = 1

            counter = 0
    return paths

def managedoors(destx, desy):
    paths = fetchshortestpath(destx, desy)
    #store key paths
    keypaths = {}
    fastestpath=[]
    ls=[]
    fastestkeypaths={}
    for lst  in paths.values():
        for elmnt in lst:
            if maze[str(elmnt[0]) + "," + str(elmnt[1])] in [Values.BLUE_KEY.value, Values.RED_KEY.value, Values.YELLOW_KEY.value, Values.GREEN_KEY.value]:  # if keys are found , store them
                keycolor=maze[str(elmnt[0]) + "," + str(elmnt[1])]
                keypaths=fetchshortestpath(elmnt[0], elmnt[1])

                for k in keypaths.values():
                    if (START_X, START_Y) in k:
                        ind = k.index((START_X, START_Y))
                        del k[ind + 1: len(k)]  # found the fastest route without considering  doors

                        if keycolor == Values.RED_KEY.value:
                            doorcolor = Values.RED_DOOR.value
                        if keycolor == Values.BLUE_KEY.value:
                            doorcolor = Values.BLUE_DOOR.value
                        if keycolor == Values.GREEN_KEY.value:
                            doorcolor = Values.GREEN_DOOR.value
                        if keycolor == Values.YELLOW_KEY.value:
                            doorcolor = Values.YELLOW_DOOR.value
                        fastestkeypaths[doorcolor] = k.copy() # find fastest paths from keys to starting position and store it in fastestkeypaths

    for lst in paths.values():
        if  (START_X,START_Y) in lst:
            ind=lst.index((START_X,START_Y))
            del lst [ ind + 1 : len(lst)]
            fastestpathWithoutKeys=lst.copy()
    ls= foundnewdoor(fastestpathWithoutKeys, fastestkeypaths)
            #print(ls)
    return ls
    

def foundnewdoor(fastestpathWithoutKeys,fastestkeypaths):
    fastestpathtoreturn=[fastestpathWithoutKeys.copy()]



    for elmnt in fastestpathWithoutKeys:
        fastestpathWithoutKeys.remove(elmnt)
        checkdoorsandfindkeys(fastestpathtoreturn,fastestpathWithoutKeys,elmnt,fastestkeypaths)

    for q in range(0,len(fastestpathtoreturn)-2):
        if fastestpathtoreturn[q]==fastestpathtoreturn[q+1]:
            fastestpathtoreturn.pop(q)

    finallist = []

    for elm in list(reversed(fastestpathtoreturn[0])):
        finallist.append(elm);


    for i in range(0, len(fastestpathtoreturn) - 1):
        inter = intersection(fastestpathtoreturn[i],fastestpathtoreturn[i + 1]) # intersection between each 2 lists

        intersection_as_list=[]
        if inter:
            intersection_as_list = list(inter)
            intersection_index = fastestpathtoreturn[i].index(intersection_as_list[0])
            del fastestpathtoreturn[i][intersection_index:] #delete the intersection

        if i != 0 and fastestpathtoreturn[i]:
            ind=0
            for elm in list(reversed(fastestpathtoreturn[i])):
                if ind!=0:
                    finallist.append(elm);

        if fastestpathtoreturn[i] and inter:
            for i3 in range(1, len(fastestpathtoreturn[i])):   # add the part to return to the initial common point
                finallist.append(fastestpathtoreturn[i][i3])

        if inter:
            ls = list(reversed(fastestpathtoreturn[i + 1]))
            intersection_index = ls.index(intersection_as_list[0])
            for r in range(intersection_index, len(ls) ):
                finallist.append(ls[r])

    return finallist


def intersection(lst1, lst2):
    lst3=lst1.copy()
    for it1 in lst1:
        for it2 in lst2:
            if it1==it2:
                del lst3[:lst1.index(it1)]
                return lst3
    return 0


def checkdoorsandfindkeys(fastestpathtoreturn,fastestpathWithoutKeys, elmnt,fastestkeypaths):
    if maze[str(elmnt[0]) + "," + str(elmnt[1])] in [Values.BLUE_DOOR.value, Values.RED_DOOR.value,Values.YELLOW_DOOR.value,Values.GREEN_DOOR.value]:  # if the fastest route contains a door
        doorcolor = maze[str(elmnt[0]) + "," + str(elmnt[1])]
        keypathofdoor = fastestkeypaths[doorcolor]
        fastestpathtoreturn.insert(0, keypathofdoor)

        for keyp in keypathofdoor:
            if maze[str(keyp[0]) + "," + str(keyp[1])] in [Values.BLUE_DOOR.value, Values.RED_DOOR.value, Values.YELLOW_DOOR.value,Values.GREEN_DOOR.value]:  # if the fastest route contains a door
                checkdoorsandfindkeys(fastestpathtoreturn,fastestpathWithoutKeys, keyp,fastestkeypaths)


def manageghosts():
    for key, value in maze.items():
        if value not in Values._value2member_map_:  # if it is a ghost
            ghostrange = int(value)
            # split key
            keySplit = key.split(",")
            posx = int(keySplit[0])
            posy = int(keySplit[1])
            strposx = str(posx)
            strposy = str(posy)
            maze[str(posx) + "," + str(posy)] = Values.GHOST.value #substitute the representation of the maze by "z"
            for i in range(1, ghostrange):
                if posx + i <= LAST_X-1 and posy - i >=0:
                    if not (maze[str(posx + i) + "," + str(posy - i)] != '0' or maze[str(posx + i -1) + "," + str(posy - i + 1)] == Values.WALL.value or (maze[str(posx) + "," + str(posy - 1)] == '1' and maze[str(posx + 1) + "," + str(posy)] == '1')):

                        diagtopright = value  # ghost influence on diaguonal  top right side
                if posx - i >= 0 and posy + i <=LAST_Y-1:
                    diagbotleft=maze[str(posx - i) + "," + str(posy + i)]
                    if not (diagbotleft != '0' or maze[str(posx - i +1) + "," + str(posy + i -1)] == Values.WALL.value  or (maze[str(posx) + "," + str(posy + 1)] == '1' and maze[str(posx - 1) + "," + str(posy)] == '1')):
                        maze[str(posx - i) + "," + str(posy + i)] = Values.GHOST_RANGE.value   # ghost influence on diaguonal  bottom left side
                if posx - i >= 0 and posy - i >=0:
                    diagtopleft = maze[str(posx - i) + "," + str(posy - i)]
                    if not(diagtopleft != '0' or maze[str(posx - i + 1) + "," + str(posy - i + 1)] == Values.WALL.value  or (maze[str(posx) + "," + str(posy - 1)] == '1' and maze[str(posx - 1) + "," + str(posy)] == '1')):
                        maze[str(posx - i) + "," + str(posy - i)] = Values.GHOST_RANGE.value   # ghost influence on diaguonal top left  side
                if posx + i <= LAST_X-1 and posy + i <= LAST_Y-1:
                    diagbotright=maze[str(posx + i) + "," + str(posy + i)]
                    if not(diagbotright != '0' or maze[str(posx) + "," + str(posy)] == Values.WALL.value  or  (maze[str(posx) + "," + str(posy + 1)] == '1' and maze[str(posx + 1) + "," + str(posy)] == '1')):
                        maze[str(posx + i) + "," + str(posy + i)] = Values.GHOST_RANGE.value   # ghost influence on diaguonal bottom right  side
                if posx - i >=0:
                    leftside=maze[str(posx - i) + "," + strposy]
                    if leftside== '0' and maze[str(posx - i + 1) + "," + str(posy)] !=Values.WALL.value :
                        maze[str(posx - i) + "," + strposy] = Values.GHOST_RANGE.value   # ghost influence on left side
                if posy - i >=0:
                    topside=maze[strposx + "," + str(posy - i)]
                    if topside == '0' and maze[str(posx) + "," + str(posy - i + 1)] !=Values.WALL.value :
                        maze[strposx + "," + str(posy - i)] = Values.GHOST_RANGE.value   # ghost influence on top side
                if posx + i <= LAST_X-1:
                    rightside=  maze[str(posx + i) + "," + strposy]
                    if rightside == '0' and maze[str(posx + i -1) + "," + str(posy)] !=Values.WALL.value :
                        maze[str(posx + i) + "," + strposy] = Values.GHOST_RANGE.value   # ghost influence on right side
                if posy + i <= LAST_Y-1:
                    bottomside=maze[strposx + "," + str(posy + i)]
                    if bottomside == '0' and maze[str(posx) + "," + str(posy + i - 1)] !=Values.WALL.value :
                        maze[strposx + "," + str(posy + i)] = Values.GHOST_RANGE.value  # ghost influence on bottom side
            #break


# Recursive algorithm
# A recursive algorithm will be launched starting from the first position. The method will call 4  recursive calls to followpath,
# one for each direction(left,right,up,down).
def followpath(x, y, direction, positionssaved):
    if x > LAST_X or y > LAST_Y:  # out of maze- stop condition
        return 0

    # get the value from the position
    currentValue = maze[str(x) + "," + str(y)]  # this is the value of our actual position

    if currentValue not in Values._value2member_map_:
        return 0
    if currentValue is Values.WALL.value:
        return 0
    if currentValue is Values.GHOST_RANGE.value or currentValue is Values.GHOST.value:
        return 0

    # save the position in array
    tupletoadd=(x,y)
    if tupletoadd not in positionssaved:
        positionssaved.append((x,y))
    else:
        return 0

    if direction != Positions.DOWN:  # don't  try going up if the direction is down,because we were there already
        followpath(x, y - 1, Positions.UP, positionssaved)  # up

    if direction != Positions.UP:  # don't  try going down if the direction is down,because we were there already
        followpath(x, y + 1, Positions.DOWN, positionssaved)  # down

    if direction != Positions.RIGHT:  # don't  try going left if the direction is down,because we were there already
        followpath(x - 1, y, Positions.LEFT, positionssaved)  # left

    if direction != Positions.LEFT:  # don't  try going right if the direction is down,because we were there already
        followpath(x + 1, y, Positions.RIGHT, positionssaved)  # right

# Execution
readfile("txt/Maze4.txt")
# dimensions of the window
WIDTH = PIXEL_IMAGE * NB_OF_ELEMENT_PER_COLUMN
HEIGHT = PIXEL_IMAGE * NB_OF_ELEMENT_PER_LINE

#  sprites
player = Actor(maze_objects["s"], anchor=(0, 0), pos=(START_X * PIXEL_IMAGE, START_Y * PIXEL_IMAGE))

def close_app():
    # Close game after Game Over
    exit()

def update():
    if keyboard.escape:
        exit()

def draw():

    global F1_PRESSED, ENDPOINT, PLAYER_MOVE

    if game_over == 1: # if it enters a ghost cell
        screen.draw.text("Game over", (WIDTH/2, HEIGHT/2), color="white",
            fontsize=100, background="black", #owidth=1, ocolor="red",
            shadow=(1.0,1.0), scolor="red",  anchor=(0.5,0.5))
        clock.schedule(close_app,10.0)
    elif ENDPOINT == 1:
        if PLAYER_MOVE == len(shortestpath)-1:
            screen.draw.text("You Found the Shortest Path ", (WIDTH / 2, HEIGHT / 2), color="white",
                         fontsize=85, background="black",  # owidth=1, ocolor="red",
                         shadow=(1.0, 1.0), scolor="blue", anchor=(0.5, 0.5))
            clock.schedule(close_app, 10.0)
        else:
            screen.draw.text("not the shortest Path. Game Over! ", (WIDTH / 2, HEIGHT / 2), color="white",
                             fontsize=75, background="black",  # owidth=1, ocolor="red",
                             shadow=(1.0, 1.0), scolor="red", anchor=(0.5, 0.5))
            clock.schedule(close_app, 10.0)

    elif F1_PRESSED == 1: # show the shortest path on screen
        screen.clear()
        for i in range(len(shortestpath)):
            x_sp = shortestpath[i][0] * PIXEL_IMAGE
            y_sp = shortestpath[i][1] * PIXEL_IMAGE
            screen.blit(maze_objects["0"], (x_sp,y_sp))

    else: # display the maze
        screen.clear()
        # Build the Maze
        # knowing that I used a dictionnary, I want to check the type of
        # the sprite to be sure to insert the correct element

        for k, v in maze.items():
            splitted_key_pos = k.split(",")
            key_x = splitted_key_pos[0]
            key_y = splitted_key_pos[1]
            x = int(key_x) * PIXEL_IMAGE
            y = int(key_y) * PIXEL_IMAGE
            if v == "s":  # starting_point
                screen.blit(maze_objects["0"], (x, y))
            else:
                screen.blit(maze_objects[v], (x, y))

        player.draw()

def on_key_down(key):

    global has_blue_key
    global has_green_key 
    global has_red_key 
    global has_yellow_key 
    global game_over
    global ENDPOINT
    global F1_PRESSED
    global PLAYER_MOVE
    
    row = int(player.y / PIXEL_IMAGE)
    column = int(player.x / PIXEL_IMAGE)
    if key == keys.UP:
        row = row - 1
        PLAYER_MOVE += 1
    if key == keys.DOWN:
        row = row + 1
        PLAYER_MOVE += 1
    if key == keys.LEFT:
        column = column - 1
        PLAYER_MOVE += 1
    if key == keys.RIGHT:
        column = column + 1
        PLAYER_MOVE += 1
    if key == keys.F1:
        F1_PRESSED = 1
        draw()
    if key == keys.F2:
        F1_PRESSED = 0
        draw()

    pos_in_str = str(column) + "," + str(row)
    sprite = maze_objects[maze[pos_in_str]]

    if sprite == "path" or sprite == "pacman":
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x, y))
    elif sprite == "reward":
        player.x = column * PIXEL_IMAGE
        player.y = row * PIXEL_IMAGE
        print("You Reached the end")
        ENDPOINT = 1

    elif sprite == "ghost" or sprite == "pink_cell":
        print("Game Over!")
        game_over = 1
        draw()

        
    #Yellow
    elif sprite == "yellow_door":
        if has_yellow_key == 1:
            x = column * PIXEL_IMAGE
            y = row * PIXEL_IMAGE
            animate(player, duration=0.15, pos=(x, y))
        else:
            print("Find the yellow key first!")
    elif sprite == "yellow_key":
        has_yellow_key = 1
        print("You have the yellow Key")
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x, y))
        maze[pos_in_str] = "0"

    #Blue
    elif sprite == "blue_door":
        if has_blue_key == 1:
            x = column * PIXEL_IMAGE
            y = row * PIXEL_IMAGE
            animate(player, duration=0.15, pos=(x, y))
        else:
            print("Find the blue key first!")
    elif sprite == "blue_key":
        has_blue_key = 1
        print("You have the blue Key")
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x, y))
        maze[pos_in_str] = "0"

    #Red
    elif sprite == "red_door":
        if has_red_key == 1:
            x = column * PIXEL_IMAGE
            y = row * PIXEL_IMAGE
            #
            animate(player, duration=0.15, pos=(x, y))
        else:
            print("Find the red key first!")
    elif sprite == "red_key":
        has_red_key = 1
        print("You have the red Key")
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x, y))
        maze[pos_in_str] = "0"

    #Green
    elif sprite == "green_door":
        if has_green_key == 1:
            x = column * PIXEL_IMAGE
            y = row * PIXEL_IMAGE
            animate(player, duration=0.15, pos=(x, y))
        else:
            print("Find the green key first!")
    elif sprite == "green_key":
        has_green_key = 1
        print("You have the green Key")
        x = column * PIXEL_IMAGE
        y = row * PIXEL_IMAGE
        animate(player, duration=0.15, pos=(x, y))
        maze[pos_in_str] = "0"
    else:
        pass

pgzrun.go()