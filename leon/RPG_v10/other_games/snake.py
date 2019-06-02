#!/usr/bin/env python
import pygame, sys, time, random
from pygame.locals import *

# 定義顏色變數
redColour = pygame.Color(255, 0, 0)
blackColour = pygame.Color(0, 0, 0)
whiteColour = pygame.Color(255, 255, 255)
greyColour = pygame.Color(150, 150, 150)


# 定義gameOver函數
def gameOver(playSurface):
    gameOverFont = pygame.font.SysFont('arial', 72)
    gameOverSurf = gameOverFont.render('Game Over', True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    time.sleep(1)
    return False


# 定義gameWin函數
def gameWin(playSurface):
    gameWinFont = pygame.font.SysFont('arial', 72)
    gameWinSurf = gameWinFont.render('Game Win', True, greyColour)
    gameWinRect = gameWinSurf.get_rect()
    gameWinRect.midtop = (320, 10)
    playSurface.blit(gameWinSurf, gameWinRect)
    pygame.display.flip()
    time.sleep(1)
    return True


# 定義main函數
def main():
    # 初始化pygame
    # pygame.init()
    fpsClock = pygame.time.Clock()
    # 創建pygame顯示層
    playSurface = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Raspberry Snake')

    # 初始化變數
    snakePosition = [100, 100]
    snakeSegments = [[100, 100], [80, 100], [60, 100]]
    raspberryPosition = [300, 300]
    raspberrySpawned = 1
    direction = 'right'
    changeDirection = direction
    eaten_count = 0
    win_count = 1
    while True:
        # 檢測例如按鍵等pygame事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判斷鍵盤事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
        # 判斷是否輸入了反方向
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'left' and not direction == 'right':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection
        # 根據方向移動蛇頭的坐標
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20
        # 增加蛇的長度
        snakeSegments.insert(0, list(snakePosition))
        # 判斷是否吃掉了樹莓
        if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
            # 判断吃掉的树莓数目是否达成胜利条件
            eaten_count += 1
            if eaten_count >= win_count:
                return gameWin(playSurface)
            raspberrySpawned = 0
        else:
            snakeSegments.pop()
        # 如果吃掉樹莓，則重新生成樹莓
        if raspberrySpawned == 0:
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            raspberryPosition = [int(x * 20), int(y * 20)]
            raspberrySpawned = 1
        # 繪製pygame顯示層
        playSurface.fill(blackColour)
        for position in snakeSegments:
            pygame.draw.rect(playSurface, whiteColour, Rect(position[0], position[1], 20, 20))
            pygame.draw.rect(playSurface, redColour, Rect(raspberryPosition[0], raspberryPosition[1], 20, 20))

        # 刷新pygame顯示層
        pygame.display.flip()
        # how to know they are die
        if snakePosition[0] > 620 or snakePosition[0] < 0:
            return gameOver(playSurface)
        if snakePosition[1] > 460 or snakePosition[1] < 0:
            for snakeBody in snakeSegments[1:]:
                if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
                    return gameOver(playSurface)
        # 控制游戲速度
        fpsClock.tick(5)


if __name__ == "__main__":
    main()