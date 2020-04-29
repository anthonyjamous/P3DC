import enum


LAST_X = 0  # stores the last value of x in the maze
LAST_Y = 0  # stores the last value of Y in the maze
START_X = 0  # stores the starting position x in the maze
START_Y = 0  # stores the starting position y in the maze
DESTINATION_X = 0  # stores the ending position x in the maze
DESTINATION_Y = 0  # stores the ending position y in the maze
maze = {}
positionssaved = []


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

    with open(filename, 'r') as f:
        posx = 0  # initialize x
        posy = 0  # initialize y
        for line in f:
            linestripped = line.replace(" ", "").rstrip("\n")  # remove "\n from line and white spaces"
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
    #  file closed

    manageghosts()
    # change the maze depending on the ghost range

    # findshortestpath(positionssaved,END_X,END_Y)
    followpath(START_X, START_Y, 0,
               positionssaved)  # call the algorithm on the starting position, first time the direction will be empty
    lst = fetchshortestpath()
    print(lst)
def iteratelist(tuple,list,k):
    for i in range (0,k):
        if tuple in list[i]:
            return 0
    return 1


def fetchshortestpath():
    i = 0  # number of steps
    j = 1  # number of paths
    paths = {}
    paths[0]=[(DESTINATION_X,DESTINATION_Y)]


    counter = 0
    x = DESTINATION_X
    y = DESTINATION_Y
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

    for lst in paths.values():
        if lst[len(lst) - 1] == (START_X,START_Y):
            return lst
    a = 3


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
            maze[str(posx) + "," + str(posy)] = value
            for i in range(1, ghostrange):
                if posx + i <= LAST_X and posy + i <= LAST_Y:
                    maze[str(posx + i) + "," + str(posy + i)] = value  # ghost influence on diaguonal  top right side
                if posx + i >= START_X and posy + i >= START_Y:
                    maze[str(posx - i) + "," + str(posy - i)] = value  # ghost influence on diaguonal  bottom left side
                if posx + i >= START_X and posy + i <= LAST_Y:
                    maze[str(posx - i) + "," + str(posy + i)] = value  # ghost influence on diaguonal top left  side
                if posx + i <= LAST_X and posy + i >= START_Y:
                    maze[str(posx + i) + "," + str(posy - i)] = value  # ghost influence on diaguonal bottom right  side
                if posx + i <= LAST_X:
                    maze[str(posx + i) + "," + strposy] = value  # ghost influence on left side
                if posy + i <= LAST_Y:
                    maze[strposx + "," + str(posy + i)] = value  # ghost influence on top side
                if posx + i >= START_X:
                    maze[str(posx - i) + "," + strposy] = value  # ghost influence on right side
                if posy + i >= START_Y:
                    maze[strposx + "," + str(posy - i)] = value  # ghost influence on top side
            break


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

    # save the position in array
    positionssaved.append((x,y))

    if direction != Positions.DOWN:  # don't  try going up if the direction is down,because we were there already
        followpath(x, y - 1, Positions.UP, positionssaved)  # up

    if direction != Positions.UP:  # don't  try going down if the direction is down,because we were there already
        followpath(x, y + 1, Positions.DOWN, positionssaved)  # down

    if direction != Positions.RIGHT:  # don't  try going left if the direction is down,because we were there already
        followpath(x - 1, y, Positions.LEFT, positionssaved)  # left

    if direction != Positions.LEFT:  # don't  try going right if the direction is down,because we were there already
        followpath(x + 1, y, Positions.RIGHT, positionssaved)  # right



# Execution
readfile("Maze1.txt")
