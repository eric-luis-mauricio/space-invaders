import pygame
from pygame import mixer

import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

# Defining states
STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
state = STATE_START

#background
background = pygame.image.load('space invaders/fundo.png')

#background sound
mixer.music.load('space invaders/background.wav')
mixer.music.play(-1)

#Caption and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('space invaders/ovni.png')
pygame.display.set_icon(icon)

#Player
playerimg = pygame.image.load('space invaders/ship.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('space invaders/enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append( 3)
    enemyY_change.append( 40)

#Bullet
bulletimg = pygame.image.load('space invaders/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 5
bulletY_change = 15
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf',64)

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
    if distance < 27:
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

#Game Loop
running = True
while running:

    screen.fill((0,0,0))
    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #if keastroke is pressed check wheter its right or left
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
                    if bullet_state is 'ready':
                        bullet_sound = mixer.Sound('space invaders/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(playerX, bulletY)
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
        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 - 5 + 0.1
        playerX += playerX_change

        if playerX < 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        #Enemy movement
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

            #collision
            colission = isCollision(enemyX[i], enemyY[i], bulletX,bulletY)
            if colission:
                explosion_sound = mixer.Sound('space invaders/explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 100
                enemyX[i] = random.randint(0,800)
                enemyY[i] = random.randint(50,150)

            enemy(enemyX[i], enemyY[i], i)

        #Bullet movement
        if bulletY <=0:
            bulletY = 480
            bullet_state = 'ready'

        if bullet_state is 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX,textY)
    elif state == STATE_GAME_OVER:
        game_over_text()

    pygame.display.update()
