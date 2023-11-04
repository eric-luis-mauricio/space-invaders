import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
state = STATE_START
paused = False

background = pygame.image.load('./images/fundo.png')
mixer.music.load('./sounds/background.wav')
mixer.music.play(-1)
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./images/ovni.png')
pygame.display.set_icon(icon)

playerimg = pygame.image.load('./characters/ship.png')
playerX = 370
playerY = 480
playerX_change = 0
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('./characters/enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append( 3)
    enemyY_change.append( 10)

bulletimg = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 5
bulletY_change = 15
bullet_state = 'ready'
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf',64)

#FUNCTIONS!!
def show_score(x,y):
    score = font.render("Score: " +str(score_value), True, (255,255,255) )
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255) )
    screen.blit(over_text, (200,250))

def player(x,y):
    screen.blit(playerimg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, ( x + 16, y + 10 ))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt (math.pow(enemyX-bulletX,2)) + math.pow(enemyY-bulletY,2)
    if distance < 60:
        return True
    else:
        return False

def start_screen():
    start_text = font.render('PRESS SPACE TO START', True, (255, 255, 255))
    screen.blit(start_text, (200, 250))

def restart():

    global state, score_value
    score_value = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0,800)
        enemyY[i] = random.randint(50,150)
    state = STATE_PLAYING

def unpause_game():
    global paused
    paused = False
    mixer.music.unpause()

def pause_game():
    global paused
    paused = True
    mixer.music.pause()
    pause_text = font.render('PAUSED - PRESS P TO RESUME', True, (255, 255, 255))
    screen.blit(pause_text, (200, 250))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    unpause_game()

while True:

    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == STATE_START:
                if event.key == pygame.K_SPACE:
                    state = STATE_PLAYING
            elif state == STATE_PLAYING:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_sound = mixer.Sound('./sounds/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(playerX, bulletY)
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        pause_game()

            elif state == STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    restart()

        if event.type == pygame.KEYUP:
            if state == STATE_PLAYING:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if state == STATE_START:
        start_screen()

    elif state == STATE_PLAYING:
        playerX += playerX_change

        if playerX < 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                state = STATE_GAME_OVER
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            colission = isCollision(enemyX[i], enemyY[i], bulletX,bulletY)
            if colission:
                explosion_sound = mixer.Sound('./sounds/explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 100
                enemyX[i] = random.randint(0,800)
                enemyY[i] = random.randint(50,150)
            enemy(enemyX[i], enemyY[i], i)

        if bulletY <=0:
            bulletY = 480
            bullet_state = 'ready'
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        player(playerX, playerY)
        show_score(textX,textY)
    elif state == STATE_GAME_OVER:
        game_over_text()

    pygame.display.update()
