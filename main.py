import pygame
import random
import math
from pygame import mixer

pygame.init()

screen= pygame.display.set_mode((800,600))

#background
background= pygame.image.load('bg1.jpg')

#add music
mixer.music.load('avengers.mpeg')
mixer.music.play(-1)



#caption n icon 
pygame.display.set_caption("SpiderMan")
icon= pygame.image.load('spider.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('spiderman.png')
playerX=370
playerY=480
playerX_change=0

#enemy
enemyImg= []
enemyX= []
enemyY= []
enemyX_change= []
enemyY_change= []

num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('lizard.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(1)
	enemyY_change.append(40)

#web
webImg=pygame.image.load('web.png')
webX= 0
webY= 480
webX_change=1
webY_change=5
web_state="ready"

#score
score=0
font = pygame.font.Font('freesansbold.ttf',32)
textX =10
textY =10

#game over text
over_font= pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
	sc= font.render("Score :" + str(score),True,(255,255,255))
	screen.blit(sc,(x,y))

def game_over_text():
	over_text= over_font.render("GAME OVER" ,True,(255,255,255))
	screen.blit(over_text,(200,250))

def player(x,y): 
	screen.blit(playerImg, (x, y))

def enemy(x,y,i):
	screen.blit(enemyImg[i], (x, y))

def fire_web(x,y):
	global web_state
	web_state="fire"
	screen.blit(webImg,(x+16,y+14))

def isCollision(enemyX,enemyY,webX,webY):
	distance= math.sqrt(math.pow(enemyX- webX,2) + (math.pow(enemyY- webY,2)))
	if distance < 27:
		return True
	else:
		return False

#gameloop
running= True
while running:

	screen.fill((0,0,0))
	#bg image
	screen.blit(background,(0,0))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

	#keystrokes
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -2
			if event.key == pygame.K_RIGHT:
				playerX_change= 2
			if event.key == pygame.K_SPACE:
				if web_state is "ready":
					web_Sound=mixer.Sound('laser.wav')
					web_Sound.play()
					webX= playerX
					fire_web(webX,webY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change= 0

	playerX= playerX+playerX_change

	if playerX<=0:
		playerX=0
	elif playerX>=736:
		playerX=736

	#enemy movement

	for i in range(num_of_enemies):		

		#game over
		if enemyY[i]>440:
			for j in range(num_of_enemies):	
				enemyY[j]=2000
			game_over_text()
			break

		enemyX[i]= enemyX[i]+enemyX_change[i]
		if enemyX[i]<=0:
			enemyX_change[i]=1
			enemyY[i]+= enemyY_change[i]
		elif enemyX[i]>=736:
			enemyX_change[i]=-1
			enemyY[i]+= enemyY_change[i]

		#collision
		collision = isCollision(enemyX[i],enemyY[i],webX,webY)
		if collision:
			explosion_Sound=mixer.Sound('explosion.wav')
			explosion_Sound.play()
			webY= 480
			web_state= "ready"
			score+=1
			print(score)
			enemyX[i]= random.randint(0,735)
			enemyY[i]= random.randint(50,150)

		enemy(enemyX[i],enemyY[i], i)

	#web movement
	if webY<=0:
		webY=480
		web_state="ready"

	if web_state is "fire":
		fire_web(webX,webY)
		webY-=webY_change

	


	player(playerX,playerY)
	show_score(textX,textY)
	pygame.display.update()