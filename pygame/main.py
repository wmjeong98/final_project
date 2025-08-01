import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
coinImage = ['./img/coin01.png','./img/coin02.png','./img/coin03.png',\
             './img/coin04.png','./img/coin05.png','./img/coin06.png',]

def getCoinCountForStage(stage):
    if stage <= 3:
        return 1
    elif stage <= 6:
        return 2
    elif stage <= 9:
        return 3
    else:
        return 4

def drawStage(stage):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 28)
    text = font.render(f'스테이지 {stage}', True, (255, 255, 0))
    text_rect = text.get_rect(center = (padWidth // 2, 30))
    gamePad.blit(text, text_rect)

def showStageClear(stage):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 28)
    text = font.render(f'스테이지 {stage} 클리어!', True, (0, 255, 0))
    text_rect = text.get_rect(center = (padWidth // 2, padHeight // 2))
    gamePad.blit(text, text_rect)
    pygame.display.update()
    sleep(2)

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
def writeScore(count):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 20)
    text = font.render('얻은 코인인 수 : ' + str(count), True, (255,255,255))
    gamePad.blit(text, (10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('./font/NanumGothic.ttf', 60)
    text = font.render('놓친 코인 수 : ' + str(count), True, (255,0,0))
    gamePad.blit(text, (320,0))
    
def wrtieMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('./font/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    wrtieMessage('도지 사망!')

def gameOver():
    global gamePad
    wrtieMessage('게임 오버!')

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('./img/background.png')
    original_fighter = pygame.image.load('./img/fighter.png')
    fighter = pygame.transform.scale(original_fighter, (60, 70))
    original_missile = pygame.image.load('./img/missile.png')
    rotate_missile = pygame.transform.rotate(original_missile, -90)
    missile = pygame.transform.scale(rotate_missile, (40, 50))
    original_explosion = pygame.image.load('./img/explosion.png')
    explosion = pygame.transform.scale(original_explosion, (60, 60))
    pygame.mixer.music.load('./bgm/music.flac')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('./bgm/missile.wav')
    gameOverSound = pygame.mixer.Sound('./bgm/gameover.wav')
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound
    
    missileXY = []
    
    original_coin = pygame.image.load(random.choice(coinImage))
    coin = pygame.transform.scale(original_coin, (60, 60))
    coinSize = coin.get_rect().size
    coinWidth = coinSize[0]
    coinHeight = coinSize[1]
    destorySound = pygame.mixer.Sound('./bgm/coin.wav')
    
    coinX = random.randrange(0, padWidth - coinWidth)
    coinY = 0
    coinSpeed = 2
    
    stage = 1
    maxStage = 10
    scoreToClear = 5 * stage
    
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    
    isShot = False
    shotCount = 0
    coinPassed = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX = -5
                elif event.key == pygame.K_RIGHT:
                    fighterX = 5
                elif event.key == pygame.K_UP:
                    fighterY = -5
                elif event.key == pygame.K_DOWN:
                    fighterY = 5
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    fighterX = 0
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    fighterY = 0
        #gamePad.fill(BLACK)
        bg_width, bg_height = background.get_size()
        bg_x = (padWidth - bg_width) // 2
        bg_y = (padHeight - bg_height) // 2
        drawObject(background, bg_x , bg_y)
        # drawObject(fighter, x, y)
        fighter_rect = fighter.get_rect()
        fighter_rect.center = (x + 45, y+25)  # ← 대충 중앙 보정 (수동 튜닝)
        gamePad.blit(fighter, fighter_rect)
        x += fighterX
        y += fighterY
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth 
        elif y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight 
        if y < coinY + coinHeight:
            if(coinX > x and coinX < x + fighterWidth) or \
                (coinX + coinWidth > x and coinX + coinWidth < x + fighterWidth):
                crash()
        if coinPassed == 3:
            gameOver()
        
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]
                
                if bxy[1] < coinY:
                    if bxy[0] > coinX and bxy[0] < coinX + coinWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
        
        writeScore(shotCount) 
        coinY += coinSpeed
        
        if coinY > padHeight:
            original_coin = pygame.image.load(random.choice(coinImage))
            coin = pygame.transform.scale(original_coin, (60, 60))
            coinSize = coin.get_rect().size
            coinWidth = coinSize[0]
            coinHeight = coinSize[1]
            coinX = random.randrange(0, padWidth - coinWidth)
            coinY = 0
            coinPassed += 1
        
        writePassed(coinPassed)
        
        if isShot:
            drawObject(explosion, coinX, coinY)
            destorySound.play()
            
            original_coin = pygame.image.load(random.choice(coinImage))
            coin = pygame.transform.scale(original_coin, (60, 60))
            coinSize = coin.get_rect().size
            coinWidth = coinSize[0]
            coinHeight = coinSize[1]
            coinX = random.randrange(0, padWidth - coinWidth)
            coinY = 0
            destorySound = pygame.mixer.Sound('./bgm/coin.wav')
            isShot = False
            
            coinSpeed += 0.02
            if coinSpeed > 10:
                coinSpeed = 10
            
        drawObject(coin, coinX, coinY)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    
initGame()
runGame()