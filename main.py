import pygame
import random
from pygame import mixer
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Corona Wars")
icon = pygame.image.load("assets/img/logo.png")
pygame.display.set_icon(icon)

levelAttr = [[0.5,5],[0.6,6],[0.7,7],[0.8,7],[0.7,6]]
currLevel = 1

numBullets = 10
scoreValue = 0
font = pygame.font.Font("assets/font/gameFont.ttf", 32)
instructionFont = pygame.font.Font("assets/font/gameFont.ttf",24)
levelFont = pygame.font.Font("assets/font/gameFont.ttf", 64)
titleFont = pygame.font.Font("assets/font/gameFont.ttf", 72)
textX = 10
textY = 10

backgroundImage = pygame.image.load("assets/img/background.png")

mixer.music.load("assets/sound/background.mp3")
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
    },
    "quit":{
        "x":250,
        "y":350
    }
}

class gameMenu:
    def __init__(self):
        self.state = "start"
        self.mode = "main"
        self.cursorX =  menuPositions["start"]["x"]-20
        self.cursorY = menuPositions["start"]["y"]
    
    def goDown(self):
        shootSound = mixer.Sound("assets/sound/shoot.wav")
        shootSound.play()
        if(self.state == "start"):
            self.state = "instructions"
            self.cursorX =  menuPositions["instructions"]["x"]-20
            self.cursorY = menuPositions["instructions"]["y"]

        elif(self.state == "instructions"):
            self.state = "credits"
            self.cursorX =  menuPositions["credits"]["x"]-20
            self.cursorY = menuPositions["credits"]["y"]
        
        elif(self.state == "credits"):
            self.state = "quit"
            self.cursorX =  menuPositions["quit"]["x"]-20
            self.cursorY = menuPositions["quit"]["y"]
    
    def goUp(self):
        shootSound = mixer.Sound("assets/sound/shoot.wav")
        shootSound.play()
        if(self.state == "instructions"):
            self.state = "start"
            self.cursorX =  menuPositions["start"]["x"]-20
            self.cursorY = menuPositions["start"]["y"]

        elif(self.state == "credits"):
            self.state = "instructions"
            self.cursorX =  menuPositions["instructions"]["x"]-20
            self.cursorY = menuPositions["instructions"]["y"]
        
        elif(self.state == "quit"):
            self.state = "credits"
            self.cursorX =  menuPositions["credits"]["x"]-20
            self.cursorY = menuPositions["credits"]["y"]
    
    def displayInstructions(self):
        title = titleFont.render("- Corona Wars -", True, (0,0,0))
        instructions1 = instructionFont.render("        Welcome to Corona Wars!!", True, (0,0,0))
        instructions2 = instructionFont.render("* Use 'SPACE' to shoot drops", True, (0,0,0))
        instructions3 = instructionFont.render("* Use left and right key to move sanitizer.", True, (0,0,0))
        instructions4 = instructionFont.render("* For each level you are given 10 drops.",True,(0,0,0))
        instructions5 = instructionFont.render("* Collect powerups like masks and vaccines" ,True, (0,0,0))
        instructions6 = instructionFont.render("* Powerups increase drop count",True,(0,0,0))


        returnInstruct = instructionFont.render("     Press 'ENTER' to go Back", True, (0,0,0))
        screen.blit(title, (100,50))
        screen.blit(instructions1,(200,200))
        screen.blit(instructions2,(200,230))
        screen.blit(instructions3,(200,260))
        screen.blit(instructions4,(200,290))
        screen.blit(instructions5,(200,320))
        screen.blit(instructions6,(200,350))
        screen.blit(returnInstruct,(200,400))

    
    def displayCredits(self):
        title = titleFont.render("- Corona Wars -", True, (0,0,0))
        credit1 = font.render("  Developed by Samarth Singh", True, (0,0,0))
        credit2 = font.render("  Inspired by space arcade", True, (0,0,0))
        credit3 = font.render("Developed during Hash-Cade 2021",True,(0,0,0))

        returnInstruct = font.render("    Press 'ENTER' to go Back", True, (0,0,0))
        screen.blit(title, (100,50))
        screen.blit(credit1,(200,200))
        screen.blit(credit2,(200,240))
        screen.blit(credit3,(200,280))
        screen.blit(returnInstruct,(200,400))
    
    def displayMenu(self):
        title = titleFont.render("- Corona Wars -", True, (0,0,0))

        item1 = font.render("Start Game", True,(0,0,0))
        item2 = font.render("Instructions", True, (0,0,0))
        item3 = font.render("Credits", True, (0,0,0))
        item4 = font.render("Quit", True, (0,0,0))
        cursor = font.render(">",True, (0,0,0))

        screen.blit(title, (100,50))
        screen.blit(item1, (menuPositions["start"]["x"], menuPositions["start"]["y"]))
        screen.blit(item2, (menuPositions["instructions"]["x"], menuPositions["instructions"]["y"]))
        screen.blit(item3, (menuPositions["credits"]["x"], menuPositions["credits"]["y"]))
        screen.blit(item4, (menuPositions["quit"]["x"], menuPositions["quit"]["y"]))
        screen.blit(cursor, (self.cursorX, self.cursorY))

        
        
class BossVillian:
    def __init__(self):
        self.Img = pygame.image.load("assets/img/boss.png")
        self.dizzyImg = pygame.image.load("assets/img/dizzy.png")
        self.bossX = random.randint(200,400)
        self.bossY = random.randint(50,60)
        self.health = 5
        self.bossXchange = 0.5
        self.bossYchange = 20
        self.bossState = "good"
        self.dizzyTimer = 0
        self.sound = mixer.Sound("assets/sound/boss.wav")
    
    def show(self):
        self.sound.set_volume(0.1)
        self.sound.play()
        if(self.bossState == "dizzy"):
            self.dizzyTimer += 1
            screen.blit(self.dizzyImg,(self.bossX,self.bossY))
            if(self.dizzyTimer > 50):
                self.dizzyTimer = 0
                self.bossState="good"
        else:
            screen.blit(self.Img,(self.bossX,self.bossY))


def isbossHit(bulletX, bulletY, bossX, bossY):
    x1,y1 = bossX+128, bossY+128
    distance = (bulletX - x1)**2 + (bulletY - y1)**2
    distance = distance**(0.5)
    if(distance <= 128):
        return True
    return False


class MaskPowerUP:
    def __init__(self):
        self.state = "idle"
        self.value = 2
        self.Img = pygame.image.load("assets/img/mask.png")
        self.X = random.randint(0,700)
        self.Y = 0
        self.speed = 0.3
    
    def show(self):
        if(self.state == "falling"):
            screen.blit(self.Img,(self.X,self.Y))

class VaccinePowerUP:
    def __init__(self):
        self.state = "idle"
        self.value = 5
        self.Img = pygame.image.load("assets/img/syringe.png")
        self.X = random.randint(0,700)
        self.Y = 0
        self.speed = 0.3
    
    def show(self):
        if(self.state == "falling"):
            screen.blit(self.Img, (self.X, self.Y))



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
        enemyImgs.append(pygame.image.load("assets/img/coronavirus.png"))
        enemyInitX.append(random.randint(0,700))
        enemyInitY.append(random.randint(50,150))
        enemyState.append(1)
        enemyXchange.append(levelAttr[lvl-1][0])
        enemyYchange.append(40)
    



bulletImg = pygame.image.load("assets/img/drop.png")
bulletX = 370
bulletY = 480
bulletState = "ready"

playerImg = pygame.image.load("assets/img/hand-sanitizer.png")
initX = 370
initY = 480

def showBullets(x,y):
    bulletStatus = font.render("Drops Rem- "+str(numBullets),True,(0,0,0))
    screen.blit(bulletStatus, (x,y))

def showLevel(x,y):
    if(currLevel < 5):
        level = levelFont.render("Level- "+str(currLevel),True,(0,0,0))
    else:
        level = levelFont.render("Boss Level",True,(0,0,0))
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
showMenu = True
startGame = False

gm = gameMenu()
bv = BossVillian()
maskP = MaskPowerUP()
vaccineP = VaccinePowerUP()
collectSound = mixer.Sound("assets/sound/collect.wav")

while running:

    if(maskP.state == "idle"):
        if(random.randint(1,5000) == 5):
            maskP.state = "falling"
    if(vaccineP.state == "idle"):
        if(random.randint(1,7000) == 5):
            vaccineP.state = "falling"
    
    screen.fill((0,0,0))
    screen.blit(backgroundImage,(0,0))
    if(startGame):
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
                        if bulletState == "ready" and numBullets>0:
                            shootSound = mixer.Sound("assets/sound/shoot.wav")
                            shootSound.play()
                            bulletX = initX
                            bulletY = initY
                            fireBullet(bulletX, bulletY)
                            numBullets -= 1
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        changeX = 0

            if(maskP.state == "falling" and maskP.Y > 800):
                maskP.state = "idle"
                maskP.Y = 0
                maskP.X = random.randint(0,700)
            if(maskP.state == "falling"):
                maskP.Y += maskP.speed
            
            if(vaccineP.state == "falling" and vaccineP.Y > 800):
                vaccineP.state = "idle"
                vaccineP.Y = 0
                vaccineP.X = random.randint(0,700)
            if(vaccineP.state == "falling"):
                vaccineP.Y += vaccineP.speed
            
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

            if(currLevel == 5 and bv.health > 0):
                if(bv.bossY > 200):
                    gameOver = True
                else:
                    bv.bossX += bv.bossXchange
                    if(bv.bossX < 0):
                        bv.bossXchange = -bv.bossXchange
                        bv.bossY += bv.bossYchange
                    if(bv.bossX > 600):
                        bv.bossXchange = -bv.bossXchange
                        bv.bossY += bv.bossYchange
            

            if(bulletY<0):
                bulletY = 480
                bulletState = "ready"

            if(bulletState == "fire"):
                fireBullet(bulletX, bulletY)
                bulletY -= 0.7

            if(isCollision(maskP.X, maskP.Y, initX, initY)):
                collectSound.play()
                numBullets += maskP.value
                maskP.state = "idle"
                maskP.Y = 0
                maskP.X = random.randint(0,700)
            
            if(isCollision(vaccineP.X, vaccineP.Y, initX, initY)):
                collectSound.play()
                numBullets += vaccineP.value
                vaccineP.state = "idle"
                vaccineP.Y = 0
                vaccineP.X = random.randint(0,700)

            for i in range(levelAttr[currLevel-1][1]):
                if(enemyState[i]):
                    collisionState = isCollision(bulletX, bulletY, enemyInitX[i], enemyInitY[i])
                    if(collisionState):
                        killSound = mixer.Sound("assets/sound/kill.wav")
                        killSound.play()
                        bulletX = 370
                        bulletY = 480
                        bulletState = "ready"
                        scoreValue += 1
                        enemyState[i] = 0
                        enemiesAlive -= 1
            
            if(currLevel == 5 and bv.health>0):
                bossHit = isbossHit(bulletX, bulletY, bv.bossX, bv.bossY)
                if(bossHit):
                    killSound = mixer.Sound("assets/sound/kill.wav")
                    killSound.play()
                    bulletX = 370
                    bulletY = 480
                    bulletState = "ready"
                    scoreValue += 1
                    bv.health -= 1
                    bv.bossState = "dizzy"

            showScore(textX,textY)
            showBullets(textX+500,textY)
            player(initX,initY)
            maskP.show()
            vaccineP.show()

            if(currLevel == 5 and bv.health > 0):
                bv.show()

            for i in range(levelAttr[currLevel-1][1]):
                if(enemyState[i]):
                    enemy(enemyInitX[i], enemyInitY[i], i)
            if(enemiesAlive == 0 and currLevel<5):
                currLevel += 1
                levelChange = True
            elif(enemiesAlive == 0 and bv.health == 0):
                gameWin = True
        elif(levelChange):
            showLevel(250,250)
            numBullets = 10
            levelTimer += 1
            if(levelTimer>1000):
                levelTimer = 0
                InitializeEnemies(levelAttr[currLevel-1][1], currLevel)
                enemiesAlive = levelAttr[currLevel-1][1]
                levelChange = False
        elif(gameOver):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                        if(event.key == pygame.K_RETURN):
                            showMenu = True
                            startGame = False
                            gameOver = False
                            currLevel = 1
                            levelChange = True
                            scoreValue = 0
            showOver(250, 250)
        elif(gameWin):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                        if(event.key == pygame.K_RETURN):
                            showMenu = True
                            startGame = False
                            gameWin = False
                            currLevel = 1
                            levelChange = True
                            scoreValue = 0
            showWin(250, 250)
    elif(showMenu):
        downPress = False
        upPress = False
        if(gm.mode == "main"):
            gm.displayMenu()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            downPress = True
                        if event.key == pygame.K_UP:
                            upPress = True
                        if event.key == pygame.K_RETURN:
                            shootSound = mixer.Sound("assets/sound/shoot.wav")
                            shootSound.play()
                            if(gm.state == "start"):
                                startGame = True
                                showMenu = False
                            elif(gm.state == "instructions"):
                                gm.mode = "option"
                            elif(gm.state == "credits"):
                                gm.mode = "option"
                            elif(gm.state == "quit"):
                                running = False
            if(downPress):
                gm.goDown()
            if(upPress):
                gm.goUp()
        else:
            if(gm.state == "instructions"):
                gm.displayInstructions()
            elif(gm.state == "credits"):
                gm.displayCredits()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if(event.key == pygame.K_RETURN):
                            shootSound = mixer.Sound("assets/sound/shoot.wav")
                            shootSound.play()
                            gm.mode = "main"

            
    pygame.display.update()