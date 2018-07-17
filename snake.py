import pygame
import random

pygame.init()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 105, 0)

# size
size = 640, 480

# game with declarations and functions
def gameLoop():
    global dir
    # game window
    gameDisplay = pygame.display.set_mode(size)
    pygame.display.set_caption('Slither')

    # image
    snakeImage = pygame.image.load('snakeHead.png')
    appleImage = pygame.image.load('apple.png')

    # change
    change = 20
    x_change = 0
    y_change = 0
    appleSize = 20

    # choosing initial direction
    dirNum = random.randint(1, 4)
    if dirNum == 1:
        dir = "r"
        x_change = change
    elif dirNum == 2:
        dir = 'l'
        x_change = -change
    elif dirNum == 3:
        dir = 'u'
        y_change = -change
    else:
        dir = 'd'
        y_change = change

    # misc
    snakeList = []
    snakeLen = 1

    originalfps = 15
    fps = originalfps
    clock = pygame.time.Clock()
    sFont = pygame.font.SysFont("comicsansms", 15)
    mFont = pygame.font.SysFont("comicsansms", 35)
    lFont = pygame.font.SysFont("comicsansms", 50)

    gameExit = False
    gameOver = False

    # functions
    def msgToScreen(msg, colour,yDisplace = 0, fontSize = "s"):
        textSurf, textRect = text_objects(msg, colour, fontSize)
        textRect.center = size[0] // 2, size[1] // 2 + yDisplace
        gameDisplay.blit(textSurf, textRect)

    def text_objects(text, colour, fontSize = 's'):
        if fontSize == 's':
            textSurface = sFont.render(text, True, colour)
        elif fontSize == 'm':
            textSurface = mFont.render(text, True, colour)
        elif fontSize == 'l':
            textSurface = lFont.render(text, True, colour)
        return textSurface, textSurface.get_rect()

    def appleUpdate():
        return [random.randrange(0, size[0] - change, change), random.randrange(0, size[1] - change, change)]

    def snake(change, snakeList):
        if dir == 'r':
            head = pygame.transform.rotate(snakeImage, 270)
        elif dir == 'l':
            head = pygame.transform.rotate(snakeImage, 90)
        elif dir == 'u':
            head = snakeImage
        elif dir == 'd':
            head = pygame.transform.rotate(snakeImage, 180)

        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

        for l in snakeList[:-1]:
            pygame.draw.rect(gameDisplay, green, [l[0], l[1], change, change])

    # starting position
    place = [size[0] // 2, size[1] // 2]
    apple = appleUpdate()

    # game
    while not gameExit:
        # if game ends
        while gameOver:
            gameDisplay.fill(white)
            score = "Score: " + str(snakeLen - 1)
            msgToScreen(score, green, -50, fontSize= 'm')
            msgToScreen("Game Over!", blue, fontSize= 'l')
            msgToScreen("Press C to play again or Q to quit.", black, 50, fontSize= 'm')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False

        # key commands
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change = -change
                    y_change = 0
                    dir = 'l'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = change
                    y_change = 0
                    dir = 'r'
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_change = -change
                    x_change = 0
                    dir = 'u'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = change
                    x_change = 0
                    dir = 'd'
                elif event.key == pygame.K_ESCAPE:
                    gameOver = True
            elif event.type == pygame.QUIT:
                gameExit = True

        # REVERSED CONTROLS
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RIGHT or event.key == pygame.K_a:
        #             x_change = -change
        #             y_change = 0
        #             dir = 'l'
        #         elif event.key == pygame.K_LEFT or event.key == pygame.K_d:
        #             x_change = change
        #             y_change = 0
        #             dir = 'r'
        #         elif event.key == pygame.K_DOWN or event.key == pygame.K_w:
        #             y_change = -change
        #             x_change = 0
        #             dir = 'u'
        #         elif event.key == pygame.K_UP or event.key == pygame.K_s:
        #             y_change = change
        #             x_change = 0
        #             dir = 'd'
        #         elif event.key == pygame.K_ESCAPE:
        #             gameOver = True
        #     elif event.type == pygame.QUIT:
        #         gameExit = True

        # out of screen
        place[0] += x_change
        place[1] += y_change
        if place[0] >= size[0]:
            place[0] = 0
            snakeLen -= 1
        elif place[0] < 0:
            place[0] = size[0]
            snakeLen -= 1
        elif place[1] < 0:
            place[1] = size[1]
            snakeLen -= 1
        elif place[1] >= size[1]:
            place[1] = 0
            snakeLen -= 1
        if snakeLen == 0:
            snakeLen = 1

        # drawing objects
        gameDisplay.fill(white)
        gameDisplay.blit(appleImage, (apple[0], apple[1]))

        snakeHead = [place[0], place[1]]
        snakeList.append([place[0], place[1]])
        while len(snakeList) > snakeLen:
            del snakeList[0]
        if snakeList.count(snakeHead) >= 2:
            gameOver = True
        snake(change, snakeList)

        pygame.display.update()

        # if eaten
        if snakeHead[0] == apple[0] and snakeHead[1] == apple[1]:
             apple = appleUpdate()
             snakeLen += 1

        pygame.display.set_caption('Slither - Score: ' + str(snakeLen - 1))

        # speed of update
        fps = originalfps * (1 + snakeLen * 0.1)
        clock.tick(fps)
    quit()

# def gameStart():
#     gameDisplay = pygame.display.set_mode(size)
#     pygame.display.set_caption('Slither')
#     gameStart = True
#     while gameStart:
#         gameDisplay.fill(black)
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_s:
#                     gameStart = False
#                     break
#
# # main
# gameStart()
gameLoop()
