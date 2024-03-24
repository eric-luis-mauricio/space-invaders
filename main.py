import pygame
from pygame import mixer
import random
import math
from tkinter import *

pygame.init()

screen = pygame.display.set_mode((1000,600))

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK
        self.text = text
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
state = STATE_START
paused = False
fase = 1
BLACK = (0,0,0)
WHITE = (255,255,255)

#BACKGROUND IMAGE
background = pygame.image.load('../assets/images/background.jpeg')

#MUSIO PLAYER
mixer.music.load('../assets/sounds/theme.mp3')
mixer.music.play(-1)

#WINDOW ICON
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('../assets/images/ovni.png')
pygame.display.set_icon(icon)

#SCORE VARIABLE
score_value = 0

#FONT
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf',64)

#PLAYER (SHIP)
playerX = 370
playerY = 480
player_width = 80
player_height = 80
playerimg = pygame.transform.scale(pygame.image.load('../assets/characters/nave.png'), (player_width, player_height))
playerX_change = 0

#ENEMYS (ALIEN)
enemy_width = 70
enemy_height = 70
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

enemy_image_paths = ['../assets/characters/enemy2.png',
                     '../assets/characters/enemy3.png']

for i in range(num_of_enemies):
        random_enemy_img_path = random.choice(enemy_image_paths)
        enemyimg.append(pygame.transform.scale(pygame.image.load(random_enemy_img_path), (enemy_width, enemy_height)))
        enemyX.append(random.randint(0, 100))
        enemyY.append(random.randint(90, 500))
        enemyX_change.append( 5)
        enemyY_change.append( 10)

bullet_width = 5
bullet_height= 30
bulletimg = pygame.transform.scale(pygame.image.load('../assets/characters/projectil.png'), (bullet_width, bullet_height))
bulletX = 0
bulletY = 480
bulletX_change = 5
bulletY_change = 15
bullet_state = True

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

def start_screen_one():
    start_text = font.render('PRESS SPACE TO START LEVEL 1', True, (255, 255, 255))
    screen.blit(start_text, (200, 250))

def restart():
    start_text = font.render('PRESS SPACE TO RESTART THE LEVEL', True, (255, 255, 255))
    screen.blit(start_text, (200,250))
    global state, score_value
    score_value = 0
    enemy_positions = set()  
    for i in range(num_of_enemies):
        while True:
            enemy_pos = (random.randint(0, 800), random.randint(50, 150))
            if enemy_pos not in enemy_positions:
                enemy_positions.add(enemy_pos)
                enemyX[i], enemyY[i] = enemy_pos
                break
    state = STATE_PLAYING

def unpause_game():
    global paused
    paused = False
    mixer.music.unpause()

def pause_game():
    global paused
    paused = True
    mixer.music.pause()

    button_resume = Button(100, 100, 200, 50, 'Resume', unpause_game)
    button_restart = Button(100, 200, 200, 50, 'Restart', restart)

while True:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if state == STATE_START:
                if event.key == pygame.K_SPACE:
                    state = STATE_PLAYING
                    
            elif state == STATE_PLAYING:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2
                    
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2
                    
                if event.key == pygame.K_SPACE:
                    if bullet_state == True:
                        bullet_sound = mixer.Sound('../assets/sounds/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(playerX, bulletY)
                        
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        pause_game()
                        mixer.music.load()

            elif state == STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    restart()

        if event.type == pygame.KEYUP:
            if state == STATE_PLAYING:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if state == STATE_START:
        start_screen_one()

    elif state == STATE_PLAYING:
        playerX += playerX_change

        if playerX < 0:
            playerX = 10
        elif playerX >= 926:
            playerX = 926

        for i in range(num_of_enemies):     
            if enemyY[i] > 440:
                state = STATE_GAME_OVER
                game_over_text()
                break
            
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 946:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            colission = isCollision(enemyX[i], enemyY[i], bulletX,bulletY)
            if colission:
                #explosion_sound = mixer.Sound('../assets/sounds/explosion.wav')
                #explosion_sound.play()
                bulletY = 480
                bullet_state = True
                score_value += 100
                enemyX[i] = random.randint(400,900)
                enemyY[i] = random.randint(30,150)
            
            enemy(enemyX[i], enemyY[i], i)

        if bulletY <=0:
            bulletY = 480
            bullet_state = True
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        player(playerX, playerY)
        show_score(textX,textY)
    elif state == STATE_GAME_OVER:
        game_over_text()
    
        # restart()  

    pygame.display.update()