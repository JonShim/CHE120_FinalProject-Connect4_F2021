# Four-In-A-Row, by Al Sweigart al@inventwithpython.com
# (Pygame) Play against the computer, dropping tiles to connect four.
#test #2!!!!!!!!! -MC
#test -JS

#hello-ST
#adding data produced by other applications-ST
import random, copy, sys, pygame
from pygame.locals import *

BOARDWIDTH = 7  # how many spaces wide the board is
BOARDHEIGHT = 6 # how many spaces tall the board is
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

DIFFICULTY = 2 # how many moves to look ahead. (>2 is usually too much)

SPACESIZE = 50 # size of the tokens and individual board spaces in pixels

FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels

# making sure the game is centered-ST
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)

#colour and dimensions-ST
BRIGHTBLUE = (0, 50, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0) #new color for buttons, can be changed later -JS
GREEN = (0, 255, 0) #other button colors
RED = (255, 0, 0) #other button colors

#background and textcolour-ST
BGCOLOR = BRIGHTBLUE
TITLECOLOR = BLACK
TEXTCOLOR = WHITE
MENUCOLOR = BRIGHTBLUE #Temporary menu color value, can be changed later -JS
BUTTONCOLOR = BLACK #temporary button color - JS
BUTTONCOLOR_HIGHLIGHTED = GREEN #another temporary button color

#colour of tokens and program knowledge of whether a spot is empty or filled by each player-ST
RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'

#main function that sets up the layout of the game-ST
def main():
    #declaring global variables-ST
    global FPSCLOCK, DISPLAYSURF, REDPILERECT, BLACKPILERECT, REDTOKENIMG
    global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
    global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG

    #setting up initial factors-ST
    pygame.init()
    #example setting up a time function-ST
    FPSCLOCK = pygame.time.Clock()
    #setting up display-ST
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Four in a Row')
    
    #setting up display of the game-ST
    #importing images-ST
    #scaling surfaces to an arbitrary size smoothly-ST
    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
    REDTOKENIMG = pygame.image.load('4row_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('4row_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))
    BOARDIMG = pygame.image.load('4row_board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

    #importing images for human and player's status at the end of game
    HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
    COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
    TIEWINNERIMG = pygame.image.load('4row_tie.png')
    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    ARROWIMG = pygame.image.load('4row_arrow.png')
    ARROWRECT = ARROWIMG.get_rect()
    ARROWRECT.left = REDPILERECT.right + 10
    ARROWRECT.centery = REDPILERECT.centery

    isFirstGame = True
    isMenu = True #menu state variable, initialize the game in the menu -JS
    #while loop for running the game-ST
    while True:
        menu(isMenu) #call menu by default and loop to it after running each game -JS
        runGame(isFirstGame)
        isFirstGame = False

def text_objects(text, font, color):
    #text rendering helper function made by JS
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def menu(isMenu):
    '''
    -display surface
    -colors
    -buttons: play, exit

    Function by JS
    '''
    #Menu function -JS
    while isMenu:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        #Render the display for the menu and the title text
        DISPLAYSURF.fill(BGCOLOR)
        titleFont = pygame.font.Font('freesansbold.ttf', int(WINDOWWIDTH/10))
        TextSurf, TextRect = text_objects("CONNECT 4", titleFont, TITLECOLOR)
        TextRect.center = ((WINDOWWIDTH /2), ((WINDOWHEIGHT / 2) - (WINDOWHEIGHT / 6))) #title
        DISPLAYSURF.blit(TextSurf, TextRect)

        #Get the mouse coordinates to make buttons interactive
        mouse = pygame.mouse.get_pos()
        
        #Get the mouse click to enable the game to run or exit
        click = pygame.mouse.get_pressed()
        
        #play button
        if ((WINDOWWIDTH/4) + (WINDOWWIDTH/2)) > mouse[0] > (WINDOWWIDTH/4) and ((WINDOWHEIGHT/2) + (WINDOWHEIGHT/6)) > mouse[1] > (WINDOWHEIGHT/2) :
            pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR_HIGHLIGHTED, ((WINDOWWIDTH/4), (WINDOWHEIGHT/2), (WINDOWWIDTH/2), (WINDOWHEIGHT/6)))                                                                    
            #if mouse over the play button, color it with the highlight color
            if click[0] == 1:
                #print("CLICK")
                isMenu == False
                break
                
        else:
            pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, ((WINDOWWIDTH/4), (WINDOWHEIGHT/2), (WINDOWWIDTH/2), (WINDOWHEIGHT/6)))
        
        #exit button
        if ((WINDOWWIDTH/4) + (WINDOWWIDTH/2)) > mouse[0] > (WINDOWWIDTH/4) and ((WINDOWHEIGHT/2) + (WINDOWHEIGHT/4) + (WINDOWHEIGHT/6)) > mouse[1] > ((WINDOWHEIGHT/2) + (WINDOWHEIGHT/4)):
            pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR_HIGHLIGHTED, ((WINDOWWIDTH/4), ((WINDOWHEIGHT/2) + (WINDOWHEIGHT/4)), (WINDOWWIDTH/2), (WINDOWHEIGHT/6)))
            if click[0] == 1:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, ((WINDOWWIDTH/4), ((WINDOWHEIGHT/2) + (WINDOWHEIGHT/4)), (WINDOWWIDTH/2), (WINDOWHEIGHT/6)))

        #settings button? If included, need to resize other buttons+title/display as well

        #button text:
        
        buttonFont = pygame.font.Font('freesansbold.ttf', int(WINDOWWIDTH/20))

        playTextSurf, playTextRect = text_objects("PLAY", buttonFont, TEXTCOLOR)
        playTextRect.center = (( (WINDOWWIDTH/4) + ((WINDOWWIDTH/2)/2)), ((WINDOWHEIGHT/2) + ((WINDOWHEIGHT/6)/2)))
        DISPLAYSURF.blit(playTextSurf, playTextRect)

        exitTextSurf, exitTextRect = text_objects("EXIT", buttonFont, TEXTCOLOR)
        exitTextRect.center = (( (WINDOWWIDTH/4) + ((WINDOWWIDTH/2)/2)), ((WINDOWHEIGHT/2) +(WINDOWHEIGHT/4) + ((WINDOWHEIGHT/6)/2)))
        DISPLAYSURF.blit(exitTextSurf, exitTextRect)

        pygame.display.update()
        



#function that runs the first game that shows how to play-ST

def runGame(isFirstGame):
    if isFirstGame:
        # Let the computer go first on the first game, so the player
        # can see how the tokens are dragged from the token piles.
        turn = COMPUTER
        showHelp = True
    else:
        # Randomly choose who goes first.
        if random.randint(0, 1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN
        showHelp = False

    # Set up a blank board data structure.
    mainBoard = getNewBoard()
#loop for what the human player can do on their turn-ST
    while True: # main game loop
        if turn == HUMAN:
            # Human player's turn.
            getHumanMove(mainBoard, showHelp)
            #if human player presses show help-ST
            if showHelp:
                # turn off help arrow after the first move
                showHelp = False
            #if human player wins-ST
            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG
                break
            turn = COMPUTER # switch to other player's turn
        else:
            # Computer player's turn.
            column = getComputerMove(mainBoard)
            animateComputerMoving(mainBoard, column)
            makeMove(mainBoard, BLACK, column)
            if isWinner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG
                break
            turn = HUMAN # switch to other player's turn

        if isBoardFull(mainBoard):
            # A completely filled board means it's a tie.
            winnerImg = TIEWINNERIMG
            break
    while True:
        # Keep looping until player clicks the mouse or quits.
        drawBoard(mainBoard)
        DISPLAYSURF.blit(winnerImg, WINNERRECT)
        pygame.display.update()
        FPSCLOCK.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return
#note: next section starts here -JS

def makeMove(board, player, column):
    """
    This function is a helper function used by the computer to generate possible moves
    Input: a board (list), the current player, and a column (int)
    Output: A possible update to a value on the input board
    -JS
    """
    lowest = getLowestEmptySpace(board, column)
    #if the lowest row in a given column is open on the board, assign that space to the input player (usually the computer) - JS
    if lowest != -1:
        board[column][lowest] = player 


def drawBoard(board, extraToken=None):
    """
    This function draws the board state for the game.
    Inputs : a board (list) and an optional extra token (dictionary) defining the parameters of the token
    extraToken defaults to None as that is only used when animating the token drops on the board.
    Output: The visuals for the game display.
    -JS
    """
    #Fills the background of the display surface with the predefined color - JS
    #Note: Color can be changed in the variable initialized at the top of the file - JS
    DISPLAYSURF.fill(BGCOLOR) 

    # draw tokens
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:
                DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

    # draw the extra token
    if extraToken != None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # draw board over the tokens
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect)

    # draw the red and black tokens off to the side
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right


def getNewBoard():
    """
    This function generates an empty board data structure (list of lists) with the predefined width and height.
    Output: An empty board (list).
    -JS
    """
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)
    return board


def getHumanMove(board, isFirstMove):
    """
    This function handles the inputs necessary to get the human player's movement of the tokens, animate the movement, and update the board visual and data structure.
    This function also shows the help arrow visual for the first human move of the game.
    Inputs: A board (list), and a boolean.
    Outputs: Depending on the inputs given, this function can exit the game, display animations for the human player, and update the board visuals.
    -JS
    """
    #initialize these variables: token is not being moved, and its coordinates are thus not on the display. -JS
    draggingToken = False
    tokenx, tokeny = None, None
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                #Exit the game -JS
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                #checks if the mouse is pressed, token is not currently being dragged, and if the cursor is on the "token stack" Rect structure for the red tokens -JS
                # start of dragging on red token pile.
                draggingToken = True
                tokenx, tokeny = event.pos #updates the visual of the token on its starting point -JS
            elif event.type == MOUSEMOTION and draggingToken:
                # update the position of the red token being dragged
                tokenx, tokeny = event.pos
            elif event.type == MOUSEBUTTONUP and draggingToken:
                # let go of the token being dragged
                if tokeny < YMARGIN and tokenx > XMARGIN and tokenx < WINDOWWIDTH - XMARGIN:
                    # let go at the top of the screen.
                    column = int((tokenx - XMARGIN) / SPACESIZE) #determines which column to drop the token on based on the area on the display where it is released -JS
                    if isValidMove(board, column):
                        #if the move is valid, animate the token drop, update the board data structure, and draw the updated board -JS
                        animateDroppingToken(board, column, RED)
                        board[column][getLowestEmptySpace(board, column)] = RED
                        drawBoard(board)
                        pygame.display.update()
                        return
                #If the token is let go elsewhere than above the board, or if the move is not a valid move, the token will just reset to its initial state -JS
                tokenx, tokeny = None, None
                draggingToken = False
        if tokenx != None and tokeny != None:
            #draw the red player token at its specified x and y coordinates -JS
            drawBoard(board, {'x':tokenx - int(SPACESIZE / 2), 'y':tokeny - int(SPACESIZE / 2), 'color':RED})
        else:
            #no animation if the token is not being moved -JS
            drawBoard(board)

        if isFirstMove:
            # Show the help arrow for the player's first move.
            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)
        #update the display to show the token's movement as often as the fps variable allows -JS
        pygame.display.update()
        FPSCLOCK.tick()


def animateDroppingToken(board, column, color):
    """
    This function is a helper function used to model the gravitational physics of dropping the tokens onto the board as an animation.
    Inputs: a board (list), a column number (int), and a color (string, maybe color tuple as well)
    Output: an animation for a token of the input color dropping in the input column down to the lowest available space in the column.
    -JS
    """
    #initialize the coordinates where the dropping animation begins (effectively centers it on the desired column), and the initial velocity of the token. -JS
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE
    dropSpeed = 1.0
    
    lowestEmptySpace = getLowestEmptySpace(board, column) #fetches the lowest available space which the token will be dropped into -JS

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5 #token accelerates -JS
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            #when the y-coordinate of the falling token becomes greater or equal to the value of the lowest empty board space, stop the animation -JS
            #note: y values increase going from top to bottom -JS
            # -> stops the drop when it reaches the lowest valid point, breaking the loop with the return -JS
            return
        #draw the board with the extra dropping token, and updates as often as the fps variable allows -JS
        drawBoard(board, {'x':x, 'y':y, 'color':color}) 
        pygame.display.update() 
        FPSCLOCK.tick() 


def animateComputerMoving(board, column):
    """
    This function animates the token movement for the computer.
    Inputs: a board (list) and a column (int)
    Outputs: an animation for the token moving from the computer's token pile up to the top of the board, across to the desired column, and dropping the token in the desired column
    -JS
    """
    #initialize variables based on the coordinates of the edges of the computer's black token pile Rect structure, as well as the initial speed -JS
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 1.0
    
    # moving the black tile up
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed) #move upwards -JS
        speed += 0.5 #acceleration -JS
        #draw the display with the token moving, update as often as the fps variable allows -JS
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK}) 
        pygame.display.update()
        FPSCLOCK.tick()
    # moving the black tile over
    y = YMARGIN - SPACESIZE #re-initialize y at the top of the display -JS
    speed = 1.0 #re-initialize the speed -JS
    while x > (XMARGIN + column * SPACESIZE):
        x -= int(speed) #move horizontally to the left -JS
        speed += 0.5 #acceleration -JS
        #draw the display with the token moving, update as often as the fps variable allows -JS
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    # dropping the black tile
    #this uses the helper function above -JS
    animateDroppingToken(board, column, BLACK)

#note: next section starts here - JS

def getComputerMove(board):
    '''This function excutes the potental moves the computer can make, checks if they are valid moves, checks which moves would be the best, and then
    randomly checks from the options given. -MC'''
    potentialMoves = getPotentialMoves(board, BLACK, DIFFICULTY)
    # get the best fitness from the potential moves
    bestMoveFitness = -1
    for i in range(BOARDWIDTH):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    # find all potential moves that have this best fitness
    bestMoves = [] #initializes the best moves list-MC
    for i in range(len(potentialMoves)):#loop that will repeat for each potential move given-MC
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i): #checks if each of the potiential moves would be a best move and adds to a list-MC
            bestMoves.append(i)#adds each best move to the list during each loop-MC
    return random.choice(bestMoves) #chooses randomly from the list of best moves-MC


def getPotentialMoves(board, tile, lookAhead):
    '''This function gives the potiential moves that the computer can make based on the difficulty and board status-MC'''
    if lookAhead == 0 or isBoardFull(board): #lookahead is the the input of difficulty, so this if statement is if difficulty is 0 or the board is full-MC
        return [0] * BOARDWIDTH #This means no potiential moves-MC

    if tile == RED: #If the player is red, the computer is black-MC
        enemyTile = BLACK
    else:
        enemyTile = RED #If the player is black, the computer is red-MC

    # Figure out the best move to make.
    potentialMoves = [0] * BOARDWIDTH
    for firstMove in range(BOARDWIDTH): #Only having the potiential to make a move in the range of the boardwidth. Creates a for loop.-MC
        dupeBoard = copy.deepcopy(board) #Copy the board-MC
        if not isValidMove(dupeBoard, firstMove): #If the first move is not valid: -MC
            continue #calculate other moves-MC
        makeMove(dupeBoard, tile, firstMove)
        if isWinner(dupeBoard, tile):
            # a winning move automatically gets a perfect fitness
            potentialMoves[firstMove] = 1
            break # don't bother calculating other moves
        else:
            # do other player's counter moves and determine best one
            if isBoardFull(dupeBoard):#if the board is full, potential moves=0 -MC
                potentialMoves[firstMove] = 0
            else: #If the board is not full -MC
                for counterMove in range(BOARDWIDTH): #Looks at the possible moves that are in the range of the board width-MC
                    dupeBoard2 = copy.deepcopy(dupeBoard)#Copy board again-MC
                    if not isValidMove(dupeBoard2, counterMove): #If the move is not valid, calculate more moves.-MC
                        continue
                    makeMove(dupeBoard2, enemyTile, counterMove)#
                    if isWinner(dupeBoard2, enemyTile):
                        # a losing move automatically gets the worst fitness
                        potentialMoves[firstMove] = -1
                        break 
                    else:
                        # do the recursive call to getPotentialMoves()
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves #Return the moves that can be made-MC


def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    for y in range(BOARDHEIGHT-1, -1, -1):#Checks if there is space to put a move in a colomn as if there is, the column height will have at least 1 empty spot.-MC
        if board[column][y] == EMPTY:
            return y #Return the coloumn that is empty-MC
    return -1 #The colomn is full-MC


def isValidMove(board, column):
    '''This function checks if a move is valid by seeing if the colomn is in the range of the board or if the colomn is full.-MC'''
    # Returns True if there is an empty space in the given column.
    # Otherwise returns False.
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        return False #Move is not valid-MC
    return True#Move is valid-MC


def isBoardFull(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(BOARDWIDTH):#A for loop to check every row-MC
        for y in range(BOARDHEIGHT):#A for loop to check each space in each row from the previous loop-MC
            if board[x][y] == EMPTY:#If any spaces are empty, then the board is not full.-MC
                return False#Board is not full-MC
    return True#Board is full-MC


def isWinner(board, tile):
    '''This function checks if the computer or human has won the game-MC'''
    # check horizontal spaces
    for x in range(BOARDWIDTH - 3):#Board width is 7, so you need to check a range of 4 (7-3 is 4)-MC
        for y in range(BOARDHEIGHT):#Needs to be in range of board height as well-MC
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:#If there is 4 concecutive same colour tiles in a row by using x value in board width loop-MC
                return True#There is a winner-MC
    # check vertical spaces
    for x in range(BOARDWIDTH):#Needs to be in range of board width-MC
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:#Checks if there is 4 concecutive same colour tiles in a coloumn by using y value in board height loop-MC
                return True#There is a winner-MC
    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:#Checks of there is 4 concecutive same colour tiles in a bottom left to top right direction-MC
                return True#There is a winner-MC
    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:#Checks if there is 4 concecutive same colour tiles in a top left to bottom right direction-MC
                return True#There is a winner-MC
    return False#No-one has won the game yet-MC


if __name__ == '__main__': #If the main fucntion is called, play the game-MC
    main()#The main code for the game-MC

