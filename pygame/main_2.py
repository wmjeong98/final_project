import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
BOSS_ATTACK_COOLDOWN = 60

coinImage = ['./img/coin01.png', './img/coin02.png', './img/coin03.png',
             './img/coin04.png', './img/coin05.png', './img/coin06.png']

fighterImages = ['./img/fighter1.png', './img/fighter2.png', './img/fighter3.png']
selectedFighterIndex = 0

def showIntro():
    global gamePad
    infoFont = pygame.font.Font('./font/DungGeunMo.ttf', 40)

    # 제목 이미지 불러오기 (예: './img/title.png')
    titleImg = pygame.image.load('./img/title.png')  # 파일 없으면 주석 처리 가능
    titleImg = pygame.transform.scale(titleImg, (480, 680))  # 이미지 크기 조절

    while True:
        gamePad.fill((0, 0, 0))
        infoText = infoFont.render("PRESS ENTER TO START", True, (255, 255, 255))

        gamePad.blit(titleImg, (0, 0))  # 중앙 상단에 이미지
        gamePad.blit(infoText, infoText.get_rect(center=(padWidth // 2, 500)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def showGameOver():
    global gamePad
    font = pygame.font.Font('./font/DungGeunMo.ttf', 60)
    infoFont = pygame.font.Font('./font/DungGeunMo.ttf', 24)
    
    gameOverImg = pygame.image.load('./img/gameover.png')  # 파일 없으면 주석 처리 가능
    gameOverImg = pygame.transform.scale(gameOverImg, (150, 150))  # 이미지 크기 조절
    while True:
        gamePad.fill((0, 0, 0))
        overText = font.render("GAME OVER", True, (255, 0, 0))
        infoText = infoFont.render("PRESS ENTER TO RESTART", True, (255, 255, 255))

        gamePad.blit(gameOverImg, (padWidth // 2 - 75, 100))  # 중앙 상단에 이미지
        gamePad.blit(overText, overText.get_rect(center=(padWidth // 2, padHeight // 2 - 50)))
        gamePad.blit(infoText, infoText.get_rect(center=(padWidth // 2, 400)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
def writeText(text, size, color, center):
    font = pygame.font.Font('./font/DungGeunMo.ttf', size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center = center)
    gamePad.blit(rendered, rect)

def characterSelect():
    global gamePad, selectedFighterIndex
    
    fighterImgs = [pygame.transform.scale(pygame.image.load(img), (80, 100)) for img in fighterImages]
    total = len(fighterImgs)
    selectedFighterIndex = 0
    
    while True:
        gamePad.fill((0, 0, 0))
        writeText("밈캐릭터 선택", 40, (255, 255, 0), (padWidth // 2, 100))
        
        for i, img in enumerate(fighterImgs):
            x = 80 + i * 110
            y = 200
            drawObject(img, x, y)
            if i == selectedFighterIndex:
                pygame.draw.rect(gamePad, (0, 255, 0), (x - 5, y - 5, 90, 110), 3)
        writeText("← → 방향키로 선택 후 Enter", 24, (255, 255, 255), (padWidth // 2, 500))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selectedFighterIndex = (selectedFighterIndex - 1) % total
                elif event.key == pygame.K_RIGHT:
                    selectedFighterIndex = (selectedFighterIndex + 1) % total
                elif event.key == pygame.K_RETURN:
                    return selectedFighterIndex

def writeScore(count):
    global gamePad
    font = pygame.font.Font('./font/DungGeunMo.ttf', 20)
    text = font.render('얻은 코인 수 : ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('./font/DungGeunMo.ttf', 20)
    text = font.render('놓친 코인 수 : ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (320, 0))

def drawStage(stage):
    global gamePad
    font = pygame.font.Font('./font/DungGeunMo.ttf', 28)
    text = font.render(f'스테이지 {stage}', True, (255, 255, 0))
    text_rect = text.get_rect(center=(padWidth // 2, 30))
    gamePad.blit(text, text_rect)

def showStageClear(stage):
    global gamePad
    font = pygame.font.Font('./font/DungGeunMo.ttf', 40)
    text = font.render(f'스테이지 {stage} 클리어!', True, (0, 255, 0))
    text_rect = text.get_rect(center=(padWidth // 2, padHeight // 2))
    gamePad.blit(text, text_rect)
    pygame.display.update()
    sleep(2)

def wrtieMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('./font/DungGeunMo.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect(center=(padWidth / 2, padHeight / 2))
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)

def crash():
    wrtieMessage('도지 사망!')
    gameOver()

def coinout():
    wrtieMessage('코인 버려?')
    gameOver()

def gameOver():
    gameOverSound.play()
    showGameOver()
    main()

def getCoinCountForStage(stage):
    if stage <= 3:
        return 1
    elif stage <= 6:
        return 2
    elif stage <= 9:
        return 3
    else:
        return 4

def showEndingStory():
    global gamePad
    storyFont = pygame.font.Font('./font/NanumGothic.ttf', 28)
    endingImg = pygame.image.load('./img/ending_credit1.png')
    endingImg = pygame.transform.scale(endingImg, (480, 640))
    story_lines = [
        "밈 코인들이 마침내 우주 해적들을 물리치고\n모든 코인을 되찾았습니다.",
        "그리고 그들은 평화로운 행성으로 돌아가 \n함께 성대한 축제를 열었습니다!"
    ]

    for line in story_lines:
        gamePad.fill((0, 0, 0))
        lines = line.split("\n")
        gamePad.blit(endingImg, (0, 0))
        for i, txt in enumerate(lines):
            rendered = storyFont.render(txt, True, (255, 255, 255))
            text_rect = rendered.get_rect(center=(padWidth // 2, 550 + i * 40))
            gamePad.blit(rendered, text_rect)
        pygame.display.update()
        sleep(3)

def showEndingCredit():
    global gamePad
    creditFont = pygame.font.Font('./font/NanumGothic.ttf', 30)
    infoFont = pygame.font.Font('./font/NanumGothic.ttf', 20)

    while True:
        gamePad.fill((0, 0, 0))
        creditText = creditFont.render("제작자: 정우민", True, (0, 255, 0))
        thanksText = infoFont.render("Thanks for playing!", True, (255, 255, 255))
        restartText = infoFont.render("PRESS ENTER TO RESTART", True, (200, 200, 200))

        gamePad.blit(creditText, creditText.get_rect(center=(padWidth // 2, 250)))
        gamePad.blit(thanksText, thanksText.get_rect(center=(padWidth // 2, 310)))
        gamePad.blit(restartText, restartText.get_rect(center=(padWidth // 2, 380)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def initGame():
    global gamePad, clock, background, missile, explosion, missileSound, gameOverSound
    pygame.init()
    pygame_icon = pygame.image.load('./img/icon.png')
    pygame.display.set_icon(pygame_icon)
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('코인으로 화성가기')
    background = pygame.image.load('./img/background.png')
    # fighter = pygame.transform.scale(pygame.image.load(fighterImages[selectedFighterIndex]), (60, 70))
    missile = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('./img/missile.png'), -90), (40, 50))
    explosion = pygame.transform.scale(pygame.image.load('./img/explosion.png'), (60, 60))
    pygame.mixer.music.load('./bgm/music.flac')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('./bgm/missile.wav')
    gameOverSound = pygame.mixer.Sound('./bgm/gameover.wav')
    clock = pygame.time.Clock()

def runGame(selectedFighterIndex):
    global gamePad, clock, background, missile, explosion, missileSound
    global bossImage, bossHP, fighterImages

    fighter = pygame.transform.scale(pygame.image.load(fighterImages[selectedFighterIndex]), (80, 80))
    fighterX, fighterY = 0, 0
    fighterWidth, fighterHeight = fighter.get_size()
    x, y = padWidth * 0.45, padHeight * 0.9

    stage = 1
    maxStage = 10
    coinSpeed = 2

    while stage <= maxStage:
        missileXY = []
        shotCount = 0
        coinPassed = 0
        destorySound = pygame.mixer.Sound('./bgm/coin.wav')
        isBossStage = (stage == 5 or stage == 10)

        bossMissiles = []
        bossAttackDelay = 0

        if isBossStage:
            if stage == 5:
                bossImage = pygame.transform.scale(pygame.image.load('./img/miniboss.png'), (120, 120))
                bossHP = 30
            else:
                bossImage = pygame.transform.scale(pygame.image.load('./img/boss.png'), (150, 150))
                bossHP = 60
            bossX = (padWidth - bossImage.get_width()) // 2
            bossY = 50
        else:
            coinCount = getCoinCountForStage(stage)
            coins = []
            for _ in range(coinCount):
                img = pygame.transform.scale(pygame.image.load(random.choice(coinImage)), (60, 60))
                coins.append({'image': img, 'x': random.randint(0, padWidth - 60), 'y': 0})

        onStage = True
        while onStage:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: fighterX = -5
                    elif event.key == pygame.K_RIGHT: fighterX = 5
                    elif event.key == pygame.K_UP: fighterY = -5
                    elif event.key == pygame.K_DOWN: fighterY = 5
                    elif event.key == pygame.K_SPACE:
                        missileSound.play()
                        missileXY.append([x + fighterWidth / 2, y - fighterHeight])
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: fighterX = 0
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]: fighterY = 0

            x = max(0, min(x + fighterX, padWidth - fighterWidth))
            y = max(0, min(y + fighterY, padHeight - fighterHeight))

            bg_width, bg_height = background.get_size()
            bg_x = (padWidth - bg_width) // 2
            bg_y = (padHeight - bg_height) // 2
            gamePad.blit(background, (bg_x, bg_y))
            drawStage(stage)
            drawObject(fighter, x, y)

            for bxy in missileXY:
                bxy[1] -= 10
            missileXY = [b for b in missileXY if b[1] > 0]
            for bx, by in missileXY:
                drawObject(missile, bx, by)

            if isBossStage:
                bossAttackDelay += 1
                if bossAttackDelay > BOSS_ATTACK_COOLDOWN:
                    bossAttackDelay = 0
                    missile_img = pygame.transform.scale(pygame.image.load(random.choice(coinImage)), (40, 40))
                    dx = random.randint(-3, 3)
                    dy = random.randint(3, 6)
                    bossMissiles.append({'image': missile_img, 'x': bossX + bossImage.get_width() // 2, 'y': bossY + bossImage.get_height(), 'dx': dx, 'dy': dy})

                for boss_msl in bossMissiles[:]:
                    boss_msl['x'] += boss_msl['dx']
                    boss_msl['y'] += boss_msl['dy']
                    drawObject(boss_msl['image'], boss_msl['x'], boss_msl['y'])
                    if pygame.Rect(x, y, fighterWidth, fighterHeight).colliderect(
                        pygame.Rect(boss_msl['x'], boss_msl['y'], boss_msl['image'].get_width(), boss_msl['image'].get_height())):
                        bossMissiles.remove(boss_msl)
                        crash()
                    elif boss_msl['y'] > padHeight:
                        bossMissiles.remove(boss_msl)

                font = pygame.font.Font('./font/DungGeunMo.ttf', 24)
                hp_text = font.render(f'\u2665 보스 HP : {bossHP}', True, (255, 0, 0))
                gamePad.blit(hp_text, (padWidth // 2 - hp_text.get_width() // 2, 80))

                drawObject(bossImage, bossX, bossY)

                boss_rect = pygame.Rect(bossX, bossY, bossImage.get_width(), bossImage.get_height())
                for bxy in missileXY[:]:
                    missile_rect = pygame.Rect(bxy[0], bxy[1], missile.get_width(), missile.get_height())
                    if boss_rect.colliderect(missile_rect):
                        missileXY.remove(bxy)
                        bossHP -= 1
                        destorySound.play()
                        if bossHP <= 0:
                            showStageClear(stage)
                            stage += 1
                            coinSpeed += 0.2
                            onStage = False
                            break

                if pygame.Rect(x, y, fighterWidth, fighterHeight).colliderect(boss_rect):
                    crash()

            else:
                for coin in coins:
                    coin['y'] += coinSpeed
                    drawObject(coin['image'], coin['x'], coin['y'])

                for coin in coins[:]:
                    if y < coin['y'] + 60 and ((coin['x'] > x and coin['x'] < x + fighterWidth) or (coin['x'] + 60 > x and coin['x'] + 60 < x + fighterWidth)):
                        crash()

                    for bxy in missileXY:
                        if bxy[1] < coin['y'] + 60 and coin['x'] < bxy[0] < coin['x'] + 60:
                            drawObject(explosion, coin['x'], coin['y'])
                            destorySound.play()
                            coins.remove(coin)
                            missileXY.remove(bxy)
                            shotCount += 1
                            new_img = pygame.transform.scale(pygame.image.load(random.choice(coinImage)), (60, 60))
                            coins.append({'image': new_img, 'x': random.randint(0, padWidth - 60), 'y': 0})

                for coin in coins[:]:
                    if coin['y'] > padHeight:
                        coins.remove(coin)
                        coinPassed += 1
                        new_img = pygame.transform.scale(pygame.image.load(random.choice(coinImage)), (60, 60))
                        coins.append({'image': new_img, 'x': random.randint(0, padWidth - 60), 'y': 0})

                writeScore(shotCount)
                writePassed(coinPassed)

                if coinPassed >= 3:
                    coinout()
                if shotCount >= stage * 5:
                    showStageClear(stage)
                    stage += 1
                    coinSpeed += 0.2
                    onStage = False

            pygame.display.update()
            clock.tick(60)

    wrtieMessage('전부 클리어!')
    showEndingStory()
    showEndingCredit()
    main()

def main():
    initGame()
    showIntro()
    selectedIndex = characterSelect()
    runGame(selectedIndex)

main()
