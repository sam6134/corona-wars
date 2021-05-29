import pygame
import random
from pygame import mixer
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Corona Wars")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)

levelAttr = [[0.5,5],[0.6,6],[0.7,7],[0.8,8],[0.8,9]]
currLevel = 1

scoreValue = 0
font = pygame.font.Font("gameFont.ttf", 32)
levelFont = pygame.font.Font("gameFont.ttf", 64)
textX = 10
textY = 10

backgroundImage = pygame.image.load("background.png")

mixer.music.load("background.mp3")
mixer.music.play(-1)

menuPositions = {
    "start":{
        "x":250,
        "y":200
    },
    "instructions":{
        "x":250,
        "y":250
    },
    "credits":{
        "x":250,
        "y":300
    }
}

class gameMenu:
    def __init__(self):
        self.state = "start"
        self.cursorX =  4



enemyImgs = []
enemyInitX = []
enemyInitY = []
enemyState = []
enemyXchange = []
enemyYchange = []
enemiesAlive = levelAttr[currLevel-1][1]

def InitializeEnemies(numEnemies, lvl):
    enemyImgs.clear()
    enemyInitX.clear()
    enemyInitY.clear()
    enemyState.clear()
    enemyXchange.clear()
    enemyYchange.clear()
    for _ in range(numEnemies):
        enemyImgs.append(pygame.image.load("coronavirus.png"))
        enemyInitX.append(random.randint(0,700))
        enemyInitY.append(random.randint(50,150))
        enemyState.append(1)
        enemyXchange.append(levelAttr[lvl-1][0])
        enemyYchange.append(40)
    



bulletImg = pygame.image.load("drop.png")
bulletX = 370
bulletY = 480
bulletState = "ready"

playerImg = pygame.image.load("hand-sanitizer.png")
initX = 370
initY = 480

def showLevel(x,y):
    level = levelFont.render("Level- "+str(currLevel),True,(0,0,0))
    screen.blit(level,(x,y))

def showScore(x,y):
    score = font.render("Score- "+str(scoreValue),True,(0,0,0))
    screen.blit(score,(x,y))

def showOver(x,y):
    gameOver = levelFont.render("Game Over", True, (0,0,0))
    screen.blit(gameOver,(x,y))

def showWin(x,y):
    gameWin = levelFont.render("You Win !!", True, (0,0,0))
    screen.blit(gameWin,(x,y))

def isCollision(bulletX, bulletY, enemyInitX, enemyInitY):
    distance = (bulletX - enemyInitX)**2 + (bulletY - enemyInitY)**2
    distance = (distance)**(0.5)
    if(distance<36):
        return True
    else:
        return False

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImgs[i],(x,y))

def fireBullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg,(x+16,y+10))

running = True
changeX = 0
changeY = 0

levelChange = True
levelTimer = 0
gameOver = False
gameWin = False

while running:

    screen.fill((0,0,0))
    screen.blit(backgroundImage,(0,0))
    if( (not levelChange) and (not gameOver) and (not gameWin)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    changeX = -0.5
                if event.key == pygame.K_RIGHT:
                    changeX = 0.5
                if event.key == pygame.K_SPACE:
                    if bulletState == "ready":
                        shootSound = mixer.Sound("shoot.wav")
                        shootSound.play()
                        bulletX = initX
                        bulletY = initY
                        fireBullet(bulletX, bulletY)
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    changeX = 0
        
        initX += changeX
        if(initX < 0):
            initX = 0
        if(initX > 736):
            initX = 736
        for i in range(levelAttr[currLevel-1][1]):
            if(enemyState[i]):
                if(enemyInitY[i]>400):
                    gameOver = True
                    break
                enemyInitX[i] += enemyXchange[i]
                if(enemyInitX[i] < 0):
                    enemyXchange[i] = -enemyXchange[i]
                    enemyInitY[i] += enemyYchange[i]
                if(enemyInitX[i] > 736):
                    enemyXchange[i] = -enemyXchange[i]
                    enemyInitY[i] += enemyYchange[i]
        
        if(bulletY<0):
            bulletY = 480
            bulletState = "ready"

        if(bulletState == "fire"):
            fireBullet(bulletX, bulletY)
            bulletY -= 0.7


        for i in range(levelAttr[currLevel-1][1]):
            if(enemyState[i]):
                collisionState = isCollision(bulletX, bulletY, enemyInitX[i], enemyInitY[i])
                if(collisionState):
                    killSound = mixer.Sound("kill.wav")
                    killSound.play()
                    bulletX = 370
                    bulletY = 480
                    bulletState = "ready"
                    scoreValue += 1
                    enemyState[i] = 0
                    enemiesAlive -= 1

        showScore(textX,textY)
        player(initX,initY)
        for i in range(levelAttr[currLevel-1][1]):
            if(enemyState[i]):
                enemy(enemyInitX[i], enemyInitY[i], i)
        if(enemiesAlive == 0 and currLevel<5):
            currLevel += 1
            levelChange = True
        elif(enemiesAlive == 0):
            gameWin = True
    elif(levelChange):
        showLevel(250,250)
        levelTimer += 1
        if(levelTimer>1000):
            levelTimer = 0
            InitializeEnemies(levelAttr[currLevel-1][1], currLevel)
            print(enemyInitX)
            enemiesAlive = levelAttr[currLevel-1][1]
            levelChange = False
    elif(gameOver):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showOver(250, 250)
    elif(gameWin):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        showWin(250, 250)
    
    pygame.display.update()