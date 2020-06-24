#/usr/bin/python
#-*- coding: utf-8 -*-
#导入模块
import pygame
import random
import os
from pygame.locals import *
from sys import exit
from os import path
from pygame.math import Vector2

#游戏声音和路径加载
img_dir = path.join(path.dirname(__file__), 'pic')
sound_dir = path.join(path.dirname(__file__), 'sounds')

#颜色以及尺寸
GRAY = (128, 128, 128)
RED = (255, 0, 0)              
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)                  
GREEN_LIGHT = (0, 220, 0)
GOLD = (205, 155, 29)
GOLD_LIGHT = (255, 215, 0)
display_width = 480
display_height = 600
POWERTIME = 5000    
blood_length = 100  #玩家血条长度
blood_boss_lenghth = 200 #BOSS血条长度
blood_width = 10    #血条宽度（玩家/BOSS通用）
power_value = 500   #用于释放大招
power_value_tmp = 0 #用于记录大招充能

level = 1 #用于记录关卡

voice = 50#初始音量大小

#游戏初始化
pygame.init()#界面
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (400, 70)#控制屏幕出现的位置
pygame.mixer.init()#音效
screen = pygame.display.set_mode((display_width, display_height), 0, 32)#大小
pygame.display.set_caption("Aircraft Wars")#标题
clock = pygame.time.Clock() #时钟

#背景图片加载
background_img = {}
background_img['background_NoStart'] = pygame.image.load(path.join(img_dir, 'back.jpg')).convert()
background_img['background_Start'] = pygame.image.load(path.join(img_dir, 'start.png')).convert()
background_img1 = pygame.image.load(path.join(img_dir, 'back11.jpg')).convert()
background_img2 = pygame.image.load(path.join(img_dir, 'back11.jpg')).convert()
help_img_tmp = pygame.image.load(path.join(img_dir, 'help.png')).convert()
help_img = pygame.transform.scale(help_img_tmp,(display_width, display_height))

#初始界面的动态效果图

#加载玩家图片
#将玩家的飞机转换成合适的大小
#将对应颜色设置成透明
player_img = pygame.image.load(path.join(img_dir,'player.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

#BOSS出现警告和BOSS
boss_warning_img = pygame.image.load(path.join(img_dir, 'warning.png')).convert()
boss_warning_img.set_colorkey(WHITE)
boss_img = pygame.image.load(path.join(img_dir, 'BOSS.png')).convert()
boss_img.set_colorkey(WHITE)
boss_bullet_img = pygame.image.load(path.join(img_dir, 'boss_bullet.png')).convert()
boss_bullet_img.set_colorkey(WHITE)
#第二关BOSS/BOSS子弹
boss_img2 = pygame.image.load(path.join(img_dir, 'BOSS2.png')).convert()
#boss_img2 = pygame.transform.scale(boss_img2_tmp, (230, 200))
boss_img2.set_colorkey(WHITE)
enemy_light_tmp = pygame.image.load(path.join(img_dir, 'enemy_light.png')).convert()
enemy_light = pygame.transform.scale(enemy_light_tmp, (25, 430))
enemy_light.set_colorkey(WHITE)

#加载炮弹
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert()
light_img = pygame.image.load(path.join(img_dir, 'light.png')).convert()
enemies_bullet_img = pygame.image.load(path.join(img_dir, 'enemies_bullet.png')).convert()

#加载盾牌闪电
powerup_img = {}
addblood_img_tmp = pygame.image.load(path.join(img_dir, 'addblood.png')).convert()
powerup_img['shield'] = pygame.transform.scale(addblood_img_tmp, (25, 25))
powerup_img['bulletup'] = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()
powerup_img['protect'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
powerup_img['protect'].set_colorkey(WHITE)

#用于判断游戏是否暂停
pause_img_tmp = pygame.image.load(path.join(img_dir, 'pause.png')).convert()
pause_img = pygame.transform.scale(pause_img_tmp, (10,10))
reuse_img_tmp = pygame.image.load(path.join(img_dir, 'reuse.png')).convert()
reuse_img = pygame.transform.scale(reuse_img_tmp,(20,20))
reuse_img.set_colorkey(WHITE)

#Set up界面的背景图片
setup_background = pygame.image.load(path.join(img_dir, 'backsetup.png')).convert()
backtointerface = pygame.image.load(path.join(img_dir, 'backtointerface.png')).convert()
backtointerfaceflag = pygame.image.load(path.join(img_dir, 'setupbackflag.png')).convert()
backtointerfaceflag.set_colorkey(WHITE)
set_up_flag = False #用于是否退出设置界面
#显示关卡选择
level1_img_tmp = pygame.image.load(path.join(img_dir, 'level_1.jpg')).convert()
level1_img = pygame.transform.scale(level1_img_tmp, (200, 50))
#level1_img.set_colorkey(WHITE)
level2_img_tmp = pygame.image.load(path.join(img_dir, 'level_2.jpg')).convert()
level2_img = pygame.transform.scale(level2_img_tmp, (200, 50))
level1_name_img = pygame.image.load(path.join(img_dir, 'level1_name.png')).convert()
level1_name_img.set_colorkey(WHITE)
level2_name_img = pygame.image.load(path.join(img_dir, 'level2_name.png')).convert()
level2_name_img.set_colorkey(WHITE)
#声音设置
vernier_img = pygame.image.load(path.join(img_dir, 'vernier.png')).convert()
vernier_img = pygame.transform.scale(vernier_img, (20, 60))
vernier_img.set_colorkey(WHITE)
set_up_back_img = pygame.image.load(path.join(img_dir, 'set_up_back.png')).convert()
set_up_back_img.set_colorkey(WHITE)
voice_set_img = pygame.image.load(path.join(img_dir, 'voice_img.png')).convert()
voice_set_img.set_colorkey(WHITE)
#导弹来袭
line_img = pygame.image.load(path.join(img_dir, 'line.png')).convert()
line_img.set_colorkey(WHITE)
mob_missile_img = pygame.image.load(path.join(img_dir, 'mob_missile.png')).convert()
mob_missile_img = pygame.transform.scale(mob_missile_img,(30, 80))
mob_missile_img.set_colorkey(WHITE)


#初始页面卡通动画
cartoon_light_img = pygame.image.load(path.join(img_dir, 'cartoon_light.png')).convert()
cartoon_light_img.set_colorkey(BLACK)
cartoon_bullet_img = pygame.image.load(path.join(img_dir,'bullet.png')).convert()
cartoon_bullet_img.set_colorkey(BLACK)

#敌机图片
enemies_img = []
lava_img = []
enemies_list = [
	'enemies1.png',
	'enemies2.png',
	'enemies3.png',
	'enemies4.png',
	'enemies5.png'
]
#障碍物——火山石
lavas_list = [
	'lava1.png',
	'lava2.png',
	'lava3.png',
	'lava4.png'
]
#第二关敌机
enemies_img2 = []
enemies_list2 = [
	'enemies21.png',
	'enemies22.png',
	'enemies23.png',
	'enemies24.png',
	'enemies25.png'
]

for image in enemies_list:#一次加载各种敌机图片
	tmp = pygame.image.load(path.join(img_dir, image)).convert()
	tmp = pygame.transform.scale(tmp, (80, 60)).convert()
	enemies_img.append(tmp)

for image in lavas_list:
	tmp = pygame.image.load(path.join(img_dir, image)).convert()
	lava_img.append(tmp)

#第二关敌机加载
for image in enemies_list2:#一次加载各种敌机图片
	tmp = pygame.image.load(path.join(img_dir, image)).convert()
	tmp = pygame.transform.scale(tmp, (80, 60)).convert()
	enemies_img2.append(tmp)

#加载爆炸动画
explosion_img = {}
explosion_img['big'] = []
explosion_img['small'] = []
explosion_img['player'] = []
explosion_img['enemies_missile'] = []
for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	tmp = pygame.image.load(path.join(img_dir, filename)).convert()
	tmp.set_colorkey(BLACK)
	big_img = pygame.transform.scale(tmp, (75,75))
	explosion_img['big'].append(big_img) 

	tmp = pygame.image.load(path.join(img_dir, filename)).convert()
	tmp.set_colorkey(BLACK)
	small_img = pygame.transform.scale(tmp, (32,32))
	explosion_img['small'].append(small_img)

	filename = 'sonicExplosion0{}.png'.format(i)
	tmp = pygame.image.load(path.join(img_dir, filename)).convert()
	tmp.set_colorkey(BLACK)
	explosion_img['player'].append(tmp)
for i in range(6):
	filename = 'boom_{}.png'.format(i)
	tmp = pygame.image.load(path.join(img_dir, filename)).convert()
	tmp.set_colorkey(WHITE)
	explosion_img['enemies_missile'].append(tmp)

add_score = []
for i in range(8):
	filename = 'xx_{}.png'.format(i)
	tmp = pygame.image.load(path.join(img_dir, filename)).convert()
	tmp.set_colorkey(BLACK)
	tmp = pygame.transform.scale(tmp, (30, 30))
	add_score.append(tmp)

#声音加载
#子弹，导弹发射的声音
shooting_sound = pygame.mixer.Sound(path.join(sound_dir, 'shooting.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_dir, 'rocket.ogg'))

#敌机，火山石爆炸的声音
explosion_sounds = []
for sound in ['expl3.wav']:
	explosion_sounds.append(pygame.mixer.Sound(path.join(sound_dir, sound)))
pygame.mixer.music.set_volume(voice/100.0)#调节声音大小
player_die_sound = pygame.mixer.Sound(path.join(sound_dir, 'rumble1.ogg'))

#定义组群
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
mobs = pygame.sprite.Group()
lavas = pygame.sprite.Group()
playerone = pygame.sprite.Group()#主要是为了捕捉其位置
playerlight = pygame.sprite.Group()
bosses = pygame.sprite.Group()
bosses_bullet = pygame.sprite.Group()
bosses_light = pygame.sprite.Group()
score_add_sprites = pygame.sprite.Group()
enemies_missile = pygame.sprite.Group() #敌方导弹来袭
cartoon_group = pygame.sprite.Group()#初始动画
cartoon_enemies_group = pygame.sprite.Group()#初始动画中的敌方
cartoon_bullet_group = pygame.sprite.Group()

#玩家子弹类
class PlayerBullet(pygame.sprite.Sprite):
	"""玩家子弹类"""
	def __init__(self, x, y):
		#x是player的rect的某个位置
		#单火力就是中间，双火力就是两边，三火力就是中间加两边
		#y是player的顶部
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:#如果超出界限就消失
			self.kill()		

#玩家导弹类
class PlayerMissile(pygame.sprite.Sprite):
	"""导弹类"""
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = missile_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()			

#玩家大招类
class PlayerLight1(pygame.sprite.Sprite):
	"""大招"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = light_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect() 
		self.rect.centerx = 120
		self.rect.centery = 400
		self.stay_time = 5000
		self.shoot_delay = 200
		self.start_time = self.shoot_time = pygame.time.get_ticks()
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.start_time > self.stay_time:
			self.start_time = now 		
			self.kill()
		if now - self.shoot_time > self.shoot_delay:
			self.shoot_time = now
			self.shoot()			
	def shoot(self):
		length = self.rect.width/5
		bullet1 = PlayerBullet(self.rect.left, self.rect.top)
		bullet2 = PlayerBullet(self.rect.left+length, self.rect.top)
		bullet3 = PlayerMissile(self.rect.left+length*2, self.rect.top)
		bullet4 = PlayerBullet(self.rect.left+length*3, self.rect.top)
		bullet5 = PlayerBullet(self.rect.left+length*4, self.rect.top)
		all_sprites.add(bullet1)#将子弹加入一个组里面， 便于一下全部update
		all_sprites.add(bullet2)
		all_sprites.add(bullet3)
		all_sprites.add(bullet4)
		all_sprites.add(bullet5)
		player_bullets.add(bullet1)#将子弹组加到一个组里面， 便于检查碰撞
		player_bullets.add(bullet2)
		player_bullets.add(bullet3)
		player_bullets.add(bullet4)
		player_bullets.add(bullet5)
		#shooting_sound.play()#播放音乐

class PlayerLight2(pygame.sprite.Sprite):
	"""大招"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = light_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect() 
		self.rect.centerx = 360
		self.rect.centery = 400
		self.stay_time = 5000
		self.shoot_delay = 200
		self.start_time = self.shoot_time = pygame.time.get_ticks()
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.start_time > self.stay_time:
			self.start_time = now 		
			self.kill()
		if now - self.shoot_time > self.shoot_delay:
			self.shoot_time = now
			self.shoot()			
	def shoot(self):
		length = self.rect.width/5
		bullet1 = PlayerBullet(self.rect.left, self.rect.top)
		bullet2 = PlayerBullet(self.rect.left+length, self.rect.top)
		bullet3 = PlayerMissile(self.rect.left+length*2, self.rect.top)
		bullet4 = PlayerBullet(self.rect.left+length*3, self.rect.top)
		bullet5 = PlayerBullet(self.rect.left+length*4, self.rect.top)
		all_sprites.add(bullet1)#将子弹加入一个组里面， 便于一下全部update
		all_sprites.add(bullet2)
		all_sprites.add(bullet3)
		all_sprites.add(bullet4)
		all_sprites.add(bullet5)
		player_bullets.add(bullet1)#将子弹组加到一个组里面， 便于检查碰撞
		player_bullets.add(bullet2)
		player_bullets.add(bullet3)
		player_bullets.add(bullet4)
		player_bullets.add(bullet5)
		#shooting_sound.play()#播放音乐

#敌机子弹类
class EnemiesBullet(pygame.sprite.Sprite):
	"""敌机子弹类"""
	def __init__(self, x, y):
		#x是敌机中间的位置， y是敌机的底部，注意两者是相向而行
		pygame.sprite.Sprite.__init__(self)
		self.image = enemies_bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = y
		self.speedy = 6
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom > display_height:
			self.kill()

#玩家类
class Player(pygame.sprite.Sprite):
	"""玩家类"""
	def __init__(self, blood = 100, lives = 3):
		pygame.sprite.Sprite.__init__(self)#初始化
		#注意image变量时特定变量
		self.image = pygame.transform.scale(player_img, (50, 38))#加载飞机图片,并转换大小
		self.image.set_colorkey(BLACK)
		self.speedx = 0#定义初始速度
		self.speedy = 0
		self.rect = self.image.get_rect()
		self.rect.centerx = display_width / 2#定义初始位置
		self.rect.centery = display_height - 20
		self.blood = blood #设置血量
		self.shoot_delay = 250 #射击延时
		self.lastshoot_time = pygame.time.get_ticks()#获取最后一次射击的时间，如果下一次射击与现在的时间间隔超过此延迟，则重新射出子弹
		self.lives = lives#生命条数
		self.hidden = False
		self.hide_time = pygame.time.get_ticks()#此方法是用来使飞机消失然后出现以此来表示重生
		self.power = 1
		self.power_time = pygame.time.get_ticks()

	def update(self):
		global power_value_tmp
		if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERTIME:
			self.power -= 1
			self.power_time = pygame.time.get_ticks()
		if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
			self.hidden = False
			self.rect.centerx = display_width / 2
			self.rect.bottom= display_height-30
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[K_LEFT]:
			self.speedx = -6;
		if keystate[K_RIGHT]:
			self.speedx = 6
		if keystate[K_UP]:
			self.speedy = -6
		if keystate[K_DOWN]:
			self.speedy = 6
		if not self.hidden:
			if keystate[K_SPACE]:
				self.shoot()
			if keystate[K_b]:
				if power_value_tmp == 100:
					self.power1()
					power_value_tmp = 0
		if not self.hidden:
			if self.rect.right > display_width:
				self.rect.right = display_width
			if self.rect.left < 0:
				self.rect.left = 0
			if self.rect.top < 0:
				self.rect.top = 0
			if self.rect.bottom > display_height:
				self.rect.bottom = display_height
		self.rect.x += self.speedx
		self.rect.y += self.speedy

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.lastshoot_time > self.shoot_delay:
			self.lastshoot_time = now
			#单火力
			if self.power == 1:
				bullet1 = PlayerBullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet1)#将子弹加入一个组里面， 便于一下全部update
				player_bullets.add(bullet1)#将子弹组加到一个组里面， 便于检查碰撞
				shooting_sound.play()#播放音乐

			elif self.power == 2:
				bullet1 = PlayerBullet(self.rect.left, self.rect.top)
				bullet2 = PlayerBullet(self.rect.right, self.rect.top)
				all_sprites.add(bullet1)#将子弹加入一个组里面， 便于一下全部update
				all_sprites.add(bullet2)
				player_bullets.add(bullet1)#将子弹组加到一个组里面， 便于检查碰撞
				player_bullets.add(bullet2)
				shooting_sound.play()#播放音乐
			else:
				bullet1 = PlayerBullet(self.rect.left, self.rect.top)
				bullet2 = PlayerBullet(self.rect.right, self.rect.top)
				bullet3 = PlayerMissile(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet1)#将子弹加入一个组里面， 便于一下全部update
				all_sprites.add(bullet2)
				all_sprites.add(bullet3)
				player_bullets.add(bullet1)#将子弹组加到一个组里面， 便于检查碰撞
				player_bullets.add(bullet2)
				player_bullets.add(bullet3)
				shooting_sound.play()#播放音乐
				#missile_sound.play()
	
	def powerup(self):
		self.power += 1
		self.power_time = pygame.time.get_ticks()
	
	def hide(self):
		self.hidden = True
		self.hide_time = pygame.time.get_ticks()
		self.rect.center = (display_width/2, display_height+200)
	
	def power1(self):
		light1 = PlayerLight1()
		light2 = PlayerLight2()
		all_sprites.add(light1)
		all_sprites.add(light2)
		playerlight.add(light1)
		playerlight.add(light2)		

#补给类
class Pow(pygame.sprite.Sprite):
	"""补给类"""
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'bulletup', 'protect'])
		self.image = powerup_img[self.type]
		if self.type == 'protect' or self.type == 'bulletup':
			self.image.set_colorkey(BLACK)
		else:
			self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 3
	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > display_height:
			self.kill()

#敌机类
class Mob(pygame.sprite.Sprite):
	"""敌机类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_choose = random.choice(enemies_img)#随机选择敌机的种类出现
		#？万一4次全部选到一种怎么办？
		#解决办法是多放几种敌机
		self.image_choose.set_colorkey(BLACK)
		self.image = self.image_choose.copy()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, display_width-self.rect.width)#让其随机出现在屏幕的上方
		self.rect.y = random.randrange(-150,-100)
		self.speedy = random.randrange(3,5)
		self.speedx = random.randrange(-3,3)
		self.shoot_delay = 1000
		self.lastshoot_time = pygame.time.get_ticks()
	
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if random.randrange(10) > 8:#控制敌机子弹发射的频率
			self.enemies_shoot()
		if (self.rect.top > display_height+self.rect.height) or (self.rect.right > display_width+self.rect.width) or (self.rect.left < -self.rect.width):
			self.rect.x = random.randrange(0, display_width-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,6)

	def enemies_shoot(self):
		now = pygame.time.get_ticks()
		if now - self.lastshoot_time > self.shoot_delay:
			self.lastshoot_time = now
			bullet1 = EnemiesBullet(self.rect.centerx, self.rect.bottom)
			all_sprites.add(bullet1)
			enemies_bullets.add(bullet1)
			shooting_sound.play()

#第二关敌机
class Mob2(pygame.sprite.Sprite):
	"""第二关敌机类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_choose = random.choice(enemies_img2)#随机选择敌机的种类出现
		self.image_choose.set_colorkey(WHITE)
		self.image = self.image_choose.copy()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, display_width-self.rect.width)#让其随机出现在屏幕的上方
		self.rect.y = random.randrange(-150,-100)
		self.speedy = random.randrange(3,5)
		self.speedx = random.randrange(-3,3)
		self.shoot_delay = 1000
		self.lastshoot_time = pygame.time.get_ticks()
	
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if random.randrange(10) > 8:#控制敌机子弹发射的频率          #修改2，频率增加
			self.enemies_shoot()
		if (self.rect.top > display_height+self.rect.height) or (self.rect.right > display_width+self.rect.width) or (self.rect.left < -self.rect.width):
			self.rect.x = random.randrange(0, display_width-self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,6)

	def enemies_shoot(self):
		now = pygame.time.get_ticks()
		if now - self.lastshoot_time > self.shoot_delay:
			self.lastshoot_time = now
			if random.randrange(10) > 8:
				bullet1 = EnemiesBullet(self.rect.right, self.rect.bottom)   #修改1:添加子弹
				bullet2 = EnemiesBullet(self.rect.left, self.rect.bottom)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				enemies_bullets.add(bullet1)
				enemies_bullets.add(bullet2)
				#shooting_sound.play()
			else:
				bullet1 = EnemiesBullet(self.rect.centerx, self.rect.bottom)   #修改1:添加子弹
				all_sprites.add(bullet1)
				enemies_bullets.add(bullet1)

#第一关BOSS
class Boss(pygame.sprite.Sprite):
	"""Boss类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = boss_img
		self.rect = self.image.get_rect()
		self.rect.centerx = 240
		self.rect.centery = 100
		self.shoot_delay = 1000
		self.shoot_time = pygame.time.get_ticks()
		self.speedx = 1
		self.blood = 1000
	
	def update(self):
		if self.rect.right > 480 or self.rect.left < 0:
			self.speedx = -self.speedx
		self.rect.centerx += self.speedx
		now = pygame.time.get_ticks()
		if now - self.shoot_time > self.shoot_delay:
			self.shoot_time = now
			bullet1 = BOSS_bullet(self.rect.left, self.rect.bottom)
			bullet2 = BOSS_bullet(self.rect.right, self.rect.bottom)
			bullet3 = BOSS_bullet(self.rect.centerx, self.rect.bottom)
			all_sprites.add(bullet1)
			bosses_bullet.add(bullet1)
			all_sprites.add(bullet2)
			bosses_bullet.add(bullet2)
			all_sprites.add(bullet3)
			bosses_bullet.add(bullet3)

#BOSS子弹
class BOSS_bullet(pygame.sprite.Sprite):
	"""docstring for BOSS_bullet"""
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = boss_bullet_img
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.destination = Vector2()
		a, b = 0, 0
		for each in playerone:
			a = each.rect.centerx
			b = each.rect.centery
		self.pos = (a + 50, b + 38)#加上玩家飞机的宽和高
		self.destination = Vector2(*self.pos) - Vector2(self.rect.centerx, self.rect.centery)
		self.speedx = self.destination.get_x()/100.0
		self.speedy = self.destination.get_y()/100.0

	def update(self):
		if self.rect.top > 600:
			self.kill()
		self.rect.centerx += self.speedx
		self.rect.centery += self.speedy	

#第二关BOSS
class Boss2(pygame.sprite.Sprite):
	"""第二关Boss类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = boss_img2
		self.rect = self.image.get_rect()
		self.rect.centerx = 240
		self.rect.centery = 100
		self.shoot_delay = 1000
		self.light_delay = 10000
		self.shoot_time = pygame.time.get_ticks()
		self.light_time = pygame.time.get_ticks()
		self.speedx = 1
		self.blood = 1000
		self.light = BOSS_Light()
		all_sprites.add(self.light)
		bosses_light.add(self.light)
	
	def update(self):
		if self.rect.right > 480 or self.rect.left < 0:
			self.speedx = -self.speedx
		self.rect.centerx += self.speedx
		now = pygame.time.get_ticks()
		if now - self.shoot_time > self.shoot_delay:
			self.shoot_time = now
			bullet1 = BOSS_bullet(self.rect.left, self.rect.bottom)
			bullet2 = BOSS_bullet(self.rect.right, self.rect.bottom)
			bullet3 = BOSS_bullet(self.rect.centerx, self.rect.bottom)
			all_sprites.add(bullet1)
			bosses_bullet.add(bullet1)
			all_sprites.add(bullet2)
			bosses_bullet.add(bullet2)
			all_sprites.add(bullet3)
			bosses_bullet.add(bullet3)
			if now - self.light_time > self.light_delay:
				self.light_time = now
				self.light.display()

#第二关BOSS大招
class BOSS_Light(pygame.sprite.Sprite):
	"""Light for BOSS"""
	def __init__(self): #x是boss的底部，也是boss的中央
		pygame.sprite.Sprite.__init__(self)
		self.image = enemy_light
		self.rect = self.image.get_rect()
		self.rect.top = -10#大招初始位置
		self.rect.centerx = -10
		self.stay_time = 3000#大招持续时间
		self.start_time = pygame.time.get_ticks()#大招开始时间
		self.hidden = False   #false表示隐藏起来
	
	def update(self):
		now = pygame.time.get_ticks()
		if  now - self.start_time >= self.stay_time:
			self.hide()
		elif now - self.start_time < self.stay_time and self.hidden:
			for each in bosses:
				top = each.rect.bottom
				centerx = each.rect.centerx
			self.rect.top = top
			self.rect.centerx = centerx

	def hide(self):
		self.rect.top = -10
		self.rect.centerx = -10
		self.hidden = False
	
	def display(self):
		self.hidden = True     #True表示显示出来
		self.start_time = pygame.time.get_ticks()

#障碍物——火山石
class Lava(pygame.sprite.Sprite):
	"""火山石类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_choose = random.choice(lava_img)
		self.image_choose.set_colorkey(BLACK)
		self.image = self.image_choose.copy()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, display_width - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(2, 4)
		self.speedx = random.randrange(-2, 2)
		self.rotation = 0
		self.rotation_speed = random.randrange(-7, 7)#旋转的速度
		self.rotate_time = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.rotate_time > 50:
			self.rotate_time = now
			self.rotation = (self.rotation+self.rotation_speed)%360
			#先原地旋转，再移动
			new_image = pygame.transform.rotate(self.image_choose, self.rotation)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if (self.rect.top > display_height) or (self.rect.left < -self.rect.width) or (self.rect.right > display_width+self.rect.width):
			self.rect.x = random.randrange(0, display_width - self.rect.width)
			self.rect.y = random.randrange(-150, -100)
			self.speedy = random.randrange(2, 4)
			self.speedx = random.randrange(-2, 2)		

#爆炸类
class Explosion(pygame.sprite.Sprite):
	"""爆炸类"""
	def __init__(self, center, specie):
		pygame.sprite.Sprite.__init__(self)
		self.specie = specie
		self.image = explosion_img[self.specie][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.frame_rate = 75   #爆炸图片放出来的间断时间
		self.last_update_time = pygame.time.get_ticks()

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update_time > self.frame_rate:
			self.last_update_time = now
			self.frame += 1
			if self.frame == len(explosion_img[self.specie]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_img[self.specie][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#屏障类
class Protect(pygame.sprite.Sprite):
	"""盾牌类"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_tmp = pygame.image.load(path.join(img_dir, 'protect2.png')).convert_alpha()
		self.image = pygame.transform.scale(self.image_tmp, (70, 60))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = (-200, -200)
		self.exist_time = pygame.time.get_ticks()
		self.protect_time = 5000 #护盾存在的时间
		self.hidden = False

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.exist_time > self.protect_time:
			self.hide()
		else:
			if self.hidden:
				for element in playerone:
					center = element.rect.center
				self.rect.center = center
	
	def hide(self):#隐藏盾牌
		self.hidden = False
		self.rect.center = (-200, -200)
	
	def display(self):#显示盾牌
		self.hidden = True
		self.exist_time  = pygame.time.get_ticks()

#加分的星星
class Score(pygame.sprite.Sprite):
	"""docstring for Score"""
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.image = add_score[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.frame_rate = 150
		self.last_update_time = pygame.time.get_ticks()#用于转圈的初始化时间
		self.start_time = pygame.time.get_ticks()#用于记录星星存在的初始化时间
		self.stay_time = 5000#星星存在的时间
		self.speedy = 2
	
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.start_time > self.stay_time:
			self.kill()
		if now - self.last_update_time > self.frame_rate:
			self.frame += 1
			self.last_update_time = now
			if self.frame == 8:
				self.frame = 0
			center = self.rect.center
			self.image = add_score[self.frame]
			self.rect = self.image.get_rect()
			self.rect.center = center
		self.rect.centery += self.speedy
		if self.rect.top > 600:
			self.kill()

#导弹来袭提示
class Line(pygame.sprite.Sprite):
	"""docstring for Line"""
	def __init__(self, centerx):
		pygame.sprite.Sprite.__init__(self)
		self.image = line_img
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.centerx_save = centerx
		self.rect.top = 0
		self.rect.bottom = 600
		self.flicker_interval_time = 200   #线闪烁的间隔时间
		self.flicker_start_time = pygame.time.get_ticks()
		self.stay_start_time = pygame.time.get_ticks()
		self.stay_time = 2000#线存在的总时间
		self.exsitence = True

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.stay_start_time > self.stay_time:
			self.kill()
		if now - self.flicker_start_time > self.flicker_interval_time and self.exsitence:
			self.flicker_start_time = now
			self.hide()
		if now - self.flicker_start_time > self.flicker_interval_time and not self.exsitence:
			self.flicker_start_time = now
			self.display()

	def hide(self):
		self.rect.centerx = -20
		self.exsitence = False
	
	def display(self):
		self.rect.centerx = self.centerx_save
		self.exsitence = True

#导弹来袭
class Mob_missile(pygame.sprite.Sprite):
	"""docstring for Mob_missile"""
	def __init__(self, centerx):
		pygame.sprite.Sprite.__init__(self)
		self.image = mob_missile_img
		self.rect = self.image.get_rect()
		self.rect.bottom = 0
		self.rect.centerx = centerx
		self.speedy = 5

	def update(self):
		self.rect.centery += self.speedy
		if self.rect.top > 600:
			self.kill()

#初始动画中的星星
class Cartoon_Score(pygame.sprite.Sprite):
	"""docstring for Score"""
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.image = add_score[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.frame_rate = 150
		self.speedx = random.randrange(-9, 9)
		self.speedy = random.randrange(-9, 9)
		self.move_time = 500
		self.move_start_time = pygame.time.get_ticks()#开始移动的时间
		self.last_update_time = pygame.time.get_ticks()#用于转圈的初始化时间
		self.start_time = pygame.time.get_ticks()#用于记录星星存在的初始化时间
		self.stay_time = 3000#星星存在的时间
		self.speedy = 2
	
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.move_start_time < self.move_time:
			self.rect.centerx += self.speedx
			self.rect.centery += self.speedy
		else:
			if now - self.start_time > self.stay_time:
				self.kill()
			if now - self.last_update_time > self.frame_rate:
				self.frame += 1
				self.last_update_time = now
				if self.frame == 8:
					self.frame = 0
				center = self.rect.center
				self.image = add_score[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center
			self.rect.centery += self.speedy

#初始动画大招
class Cartoon_light(pygame.sprite.Sprite):
	"""docstring for Cartoon_light"""
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = cartoon_light_img
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speed = 3

	def update(self):
		if self.rect.top < 100:
			expl = Explosion(self.rect.center,'enemies_missile')
			cartoon_group.add(expl)
			stars1 = Cartoon_Score((self.rect.right, self.rect.centery))
			stars2 = Cartoon_Score((self.rect.right, self.rect.centery))
			stars3 = Cartoon_Score((self.rect.right, self.rect.centery))
			stars4 = Cartoon_Score((self.rect.right, self.rect.centery))
			stars5 = Cartoon_Score((self.rect.right, self.rect.centery))
			stars6 = Cartoon_Score((self.rect.right, self.rect.centery))
			cartoon_group.add(stars1)
			cartoon_group.add(stars2)
			cartoon_group.add(stars3)
			cartoon_group.add(stars4)
			cartoon_group.add(stars5)
			cartoon_group.add(stars6)
			self.kill()
		else:
			self.rect.bottom -= self.speed

#初始动画子弹
class Cartoon_bullet(pygame.sprite.Sprite):
		"""docstring for Cartoon_bullet"""
		def __init__(self, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.image = cartoon_bullet_img
			self.rect = self.image.get_rect()
			self.rect.centerx = x
			self.rect.bottom = y
			self.speed = 8
		
		def update(self):
			self.rect.bottom -= self.speed
			if self.rect.top < 100:
				self.kill()

#初始动画飞机
class Cartoon(pygame.sprite.Sprite):
	"""docstring for """
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50, 38))#加载飞机图片,并转换大小
		self.image.set_colorkey(BLACK)		
		self.rect = self.image.get_rect()
		self.rect.top = 600 - self.image.get_height()
		self.rect.left = 50
		self.light_stay_time = 3000
		self.fire_delay = 500
		self.light_start_time = pygame.time.get_ticks()
		self.fire_start = pygame.time.get_ticks()
		self.speedx = 2

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.light_start_time > self.light_stay_time:
			self.light_start_time = now
			cartoon_light1 = Cartoon_light(self.rect.centerx, self.rect.top)
			cartoon_group.add(cartoon_light1)
			
		if now - self.fire_start > self.fire_delay:
			self.fire_start = now
			bullet1 = Cartoon_bullet(self.rect.left, self.rect.top)
			bullet2 = Cartoon_bullet(self.rect.right, self.rect.top)
			cartoon_group.add(bullet1)
			cartoon_group.add(bullet2)
			cartoon_bullet_group.add(bullet1)
			cartoon_bullet_group.add(bullet2)

		if self.rect.right >= 480 or self.rect.left <= 0:
			self.speedx = -self.speedx

		self.rect.centerx += self.speedx

#初始动画的敌方类
class Cartoon_enemies(pygame.sprite.Sprite):
	"""docstring for Cartoon_enemies"""
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_choose = random.choice(enemies_img)#随机选择敌机的种类出现
		self.image_choose.set_colorkey(BLACK)
		self.image = self.image_choose
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(20, 400)#让其随机出现在屏幕的上方
		self.rect.y = random.randrange(-60, -30)
		self.speedy = random.randrange(1, 3)

	def update(self):
		self.rect.y += self.speedy
		if self.rect.y >= 600:
			self.rect.y = random.randrange(-60,-30)

#添加敌机
def AddMob():
	tmp = Mob()
	all_sprites.add(tmp)
	mobs.add(tmp)

#第二关添加敌机
def AddMob2():
	tmp = Mob2()
	all_sprites.add(tmp)
	mobs.add(tmp)

#添加初始动画敌机
def Add_Cartoon_Enemies():
	tmp = Cartoon_enemies()
	cartoon_group.add(tmp)
	cartoon_enemies_group.add(tmp)

#添加火山石
def AddLava():
	tmp = Lava()
	all_sprites.add(tmp)
	lavas.add(tmp)

#显示按钮里面的字
def text_write(text, font):
	textSurface = font.render(text, True, BLACK)
	return textSurface, textSurface.get_rect()

#按键
def button(msg, x, y, w, h, first_color, last_color, action = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
	#判断鼠标是否放在button上
		pygame.draw.rect(screen, first_color, (x, y, w, h))
		if click[0] ==1 and action != None:
			action()
	else:
		pygame.draw.rect(screen, last_color, (x, y, w, h))
	smallText = pygame.font.Font('font.ttf',20)
	textSurface, textRect = text_write(msg, smallText)
	#将字放在button的正中央
	textRect.center = ((x+w/2), (y+h/2))
	screen.blit(textSurface, textRect)

#显示血量
def draw_blood(surf, x, y, pct):
	pct = max(pct, 0)
	#外面的框框
	outline_rect = pygame.Rect(x, y, blood_length, blood_width)
	fill_rect = pygame.Rect(x, y, pct, blood_width)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2) 

def draw_boss_blood(surf, x, y, pct):
	pct = max(pct, 0) / 5
	outline_rect = pygame.Rect(x, y, blood_boss_lenghth, blood_width)
	fill_rect = pygame.Rect(x, y, pct, blood_width)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)
	
#显示字
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font('font.ttf',size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

#画生命条数
def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x+30*i
		img_rect.y = y
		surf.blit(img, img_rect)

#游戏暂停
def draw_pause(surf, x, y, img):
	pause = False
	surf.blit(img, (x, y))
	rect = img.get_rect()
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+rect.width > mouse[0] > x and y+rect.height > mouse[1] > y:
		if click[0] == 1:
			pause = True
	while pause:
		draw_text(surf,"The Game has Been Paused!", 20, display_width/2,display_height/3)
		draw_text(surf,"Press ESC to Return to the Game!", 20, display_width/2,display_height/3+50)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause = False
		pygame.display.update()

#飞机能量
def draw_power(surf, x, y, power_value_tmp):
	outline_rect = pygame.Rect(x, y, blood_length, blood_width)
	fill_rect = pygame.Rect(x, y, power_value_tmp, blood_width)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2) 

#BOSS来袭的警告
def draw_warning(surf):
	surf.blit(boss_warning_img, (0, display_height/4))

#显示游戏结束并回到初始界面
def game_over(score):
	f = open('score.txt','r')#如果直接以写方式打开里面的内容就没了
	line  = f.read()
	score_record = int(line)
	f.close()
	if score > score_record:
		f = open('score.txt','w')
		f.write(str(score))
		f.close()
		screen.fill(BLACK)
		draw_text(screen,"Congratulations!", 40, display_width/2,display_height/3)
		draw_text(screen,"You Got " + str(score) + " points",30,display_width/2,display_height/3+50)
		draw_text(screen,"And You have Broken the Record!", 30, display_width/2, display_height/3+100)
		pygame.display.update()
		pygame.time.wait(5000)
		for sprite in all_sprites:
			sprite.kill()
	else:
		screen.fill(BLACK)
		draw_text(screen,"Your Plane has Crashed!", 40, display_width/2,display_height/3)
		draw_text(screen,"You Got " + str(score) + " points",30,display_width/2,display_height/3+50)
		draw_text(screen,"Hope You Do Better Next Time!", 30, display_width/2, display_height/3+100)
		pygame.display.update()
		pygame.time.wait(5000)
		for sprite in all_sprites:
			sprite.kill()

#通关
def clearance(score):
	f = open('score.txt','r')#如果直接以写方式打开里面的内容就没了
	line  = f.read()
	score_record = int(line)
	f.close()
	if score_record > score:
		f = open('score.txt','w')
		f.write(str(score))
		f.close()
	draw_text(screen,"Congratulations!", 40, display_width/2,display_height/3)
	draw_text(screen,"You Got " + str(score) + " points",30,display_width/2,display_height/3+50)
	draw_text(screen,"And You Pass All the Checkpoint", 30, display_width/2, display_height/3+100)
	pygame.display.update()
	pygame.time.wait(5000)
	for sprite in all_sprites:
		sprite.kill()

#选择关卡成功
def choose_success():
	global level
	draw_text(screen,"You have Chosed Level " + str(level), 40, display_width/2,50)
	draw_text(screen,"You Can Play Now ", 40, display_width/2,100)
	screen.blit(level1_name_img,(10, 310))
	screen.blit(level2_name_img,(10, 380))
	screen.blit(level1_img, (220, 310))
	screen.blit(level2_img, (220, 380))
	pygame.display.update()
	pygame.time.wait(2000)

#清空所有Group中的元素
def empty_sprite():
	for each in all_sprites:
		each.kill()
	for each in lavas:
		each.kill()
	for each in mobs:
		each.kill()
	for each in lavas:
		player_bullets.kill()
	for each in enemies_bullets:
		each.kill()
	for each in powerups:
		each.kill()
	for each in bosses_bullet:
		each.kill()
	for each in bosses:
		each.kill()
	for each in playerone:
		each.kill()
	for each in playerlight:
		each.kill()
	for each in score_add_sprites:
		each.kill()

def game_help():
	flag = True
	help_img.set_colorkey(BLACK)
	while flag:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					flag = False
		screen.blit(help_img,(0,0))
		pygame.display.update()

#关卡之间的过渡
def transition():
	global level
	draw_text(screen,"Congratulations!", 40, display_width/2,display_height/3)
	draw_text(screen,"You have Passed Level " + str(level-1) ,30,display_width/2,display_height/3+50)
	draw_text(screen,"It's gon na be harder. Ready?", 30, display_width/2, display_height/3+100)
	draw_text(screen,"Let's go", 30, display_width/2, display_height/3+150)
	pygame.display.update()
	pygame.time.wait(2000)

#游戏初始化界面
def game_introduce():
	#播放游戏初始界面音乐
	global voice
	menu_song = pygame.mixer.music.load(path.join(sound_dir, 'menu.ogg'))
	pygame.mixer.music.set_volume(voice/100.0)#调节声音大小
	#循环播放
	pygame.mixer.music.play(-1)
	flag = True
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
		clock.tick(60)	
		screen.blit(background_img['background_NoStart'],(0, 0))
		cartoon_group.update()
		if flag:
			for i in range(4):
				Add_Cartoon_Enemies()	
			cartoon1 = Cartoon()
			cartoon_group.add(cartoon1)
			flag = False
		cartoon_group.draw(screen)
		
		hits = pygame.sprite.groupcollide(cartoon_bullet_group, cartoon_enemies_group, True, True)
		for hit in hits:
			death_explosion = Explosion(hit.rect.center,'big')
			cartoon_group.add(death_explosion)
			Add_Cartoon_Enemies()

		title = pygame.font.Font('font.ttf',50)
		textSurface, textRect = text_write('Aircraft Wars', title)
		textRect.center = (display_width/2, 100)
		screen.blit(textSurface, textRect)
		button("Start Game", display_width/2-85, 170, 180, 50, GREEN_LIGHT, GREEN, game_loop)
		button("Level Selection", display_width/2-85, 240, 180, 50, GREEN_LIGHT, GREEN, LevelSelection)
		button("Set Up", display_width/2-85, 310, 180, 50, GREEN_LIGHT, GREEN, SoundSettings)
		button("Help", display_width/2-85, 380, 180, 50, GREEN_LIGHT, GREEN, game_help)
		button("Quit", display_width/2-85, 450, 180, 50,GREEN_LIGHT, GREEN,game_quit)
		pygame.display.update()

#关卡选择
def LevelSelection():
	global level
	flag_level = False
	x1 = 220
	x2 = 220
	y1 = 310
	y2 = 380
	flag_on = True
	width1 = level1_img.get_width()
	height1 = level1_img.get_height()
	width2 = level2_img.get_width()
	height2 = level2_img.get_height()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					flag_level = True
		if flag_level:
			break
		screen.blit(setup_background, (0, 0))
		screen.blit(backtointerfaceflag, (80, 170))
		screen.blit(level1_name_img, (10, 310))
		screen.blit(level2_name_img, (10, 380))
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if 220 + width1 > mouse[0] > 220 and y1 + height1 > mouse[1] > y1:
			x1 = 240
			if click[0] ==1:
				level = 1
				choose_success()
				x1 = 220
		else:
			x1 = 220

		if 220 + width2 > mouse[0] > 220 and y2 + height2 > mouse[1] > y2:
			x2 = 240
			if click[0] ==1:
				level = 2
				choose_success()
				x2 = 220
		else:
			x2 = 220		
		screen.blit(level1_img, (x1, y1))
		screen.blit(level2_img, (x2, y2))
		pygame.display.update()

#声音选择的滑动框条
def create_scales(height):
	red_scale_surface = pygame.surface.Surface((640, height))
	for x in range(640):
		c = int((x/640.)*255.)
		red = (c, 0, 0)
		line_rect = Rect(x, 0, 1, height)
		pygame.draw.rect(red_scale_surface, red, line_rect)
	return red_scale_surface

#声音设置
def SoundSettings():
	red_scale = create_scales(20)
	flag_set_up = False
	global voice
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					flag_set_up = True
		if flag_set_up:
			break
		x, y = pygame.mouse.get_pos()

		if pygame.mouse.get_pressed()[0]:
			if y > display_height/2 and y < display_height/2+20:
				voice = int((x/479.0)*100.0)
		pos = (int((voice/100.0)*479.0), display_height/2-20)
		screen.fill((0, 0, 0))
		screen.blit(set_up_back_img,(0,0))
		screen.blit(red_scale, (0, display_height/2))
		screen.blit(vernier_img, pos)
		screen.blit(voice_set_img, (30, display_height/2+40))
		draw_text(screen, str(voice), 30, 280, display_height/2+45)
		#因为声音大小会因为播放的改变而重置，所以将其放在循环中
		pygame.mixer.music.set_volume(voice/100.0)#调节声音大小  
		pygame.display.update()

#退出游戏
def game_quit():
	exit()

#游戏开始的循环
def game_loop():
	global power_value_tmp   #用于记录能量值
	global level       #关卡数
	score = 0      #记录分数
	#记录每一关之后的血量和生命条数，用于下一关的创建
	blood = 100
	lives = 3
	flag1_2 = False #判断是否由一过渡到第二关
	if level == 1:
		height = -936  #用于实现屏幕的滚动
		running = True
		build = True
		flag = False #判断是否返回主界面的标志
		flag1 = True #判断是否杀掉所有小敌机
		flag2 = True #判断是否创建BOSS
		time = 30000
		time_start = pygame.time.get_ticks()
		warning_time = 3000
		warning_sart_time = pygame.time.get_ticks()
		mob_missile_start_time = pygame.time.get_ticks()
		mob_missile_time = 8000      #两次导弹间隔时间
		missile_width1 = 0
		missile_width2 = 0
		missile_width3 = 0
		flag3 = False #用于判断地方是否可以发射导弹
		while running:
			if build:#只用创建一遍就可以了
				pygame.mixer.music.stop()
				pygame.mixer.music.load(path.join(sound_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))       
				pygame.mixer.music.play(-1)
				build = False			
				protect1 = Protect()#直接创建护盾类，有需要再添加
				all_sprites.add(protect1)
				player = Player()     #创建玩家 ，每一关都是这个
				playerone.add(player)
				all_sprites.add(player)				
				for i in range(4):
					AddMob()
				for i in range(4):#添加
					AddLava()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						flag = True
			if flag:#如果按esc键就退出到最开始
				for sprite in all_sprites:
					sprite.kill()
				break

			clock.tick(60)#帧率
			all_sprites.update()

			#敌机的导弹
			#导弹来袭提示
			now = pygame.time.get_ticks()
			if now - mob_missile_start_time > mob_missile_time:
				missile_width1 = random.randrange(20,100)
				missile_width2 = random.randrange(100,300)
				missile_width3 = random.randrange(300,460)
				line1 = Line(missile_width1)
				line2 = Line(missile_width2)
				line3 = Line(missile_width3)
				all_sprites.add(line1)
				all_sprites.add(line2)
				all_sprites.add(line3)
				mob_missile_start_time = now
				flag3 = True
			
			if flag3:
				if not line1.alive():
					xx1 = Mob_missile(missile_width1)
					xx2 = Mob_missile(missile_width2)
					xx3 = Mob_missile(missile_width3)
					all_sprites.add(xx1)
					all_sprites.add(xx2)
					all_sprites.add(xx3)
					enemies_missile.add(xx1)
					enemies_missile.add(xx2)
					enemies_missile.add(xx3)
					flag3 = False #只发射一轮导弹攻击

			#玩家与敌方导弹的碰撞
			hits = pygame.sprite.spritecollide(player, enemies_missile, True, pygame.sprite.collide_rect)
			for hit in hits:
				player.blood -= 30
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#敌方导弹和我方飞机的子弹相撞
			hits = pygame.sprite.groupcollide(enemies_missile, player_bullets, True, True)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌方导弹与保护膜相撞
			pygame.sprite.spritecollide(protect1, enemies_missile, True, pygame.sprite.collide_rect)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌方导弹与玩家大招相撞
			hits = pygame.sprite.groupcollide(enemies_missile, playerlight, True, False)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌机和玩家子弹碰撞检测
			hits = pygame.sprite.groupcollide(mobs, player_bullets, True, True)
			for hit in hits:
				score += 50
				power_value_tmp += 5
				random.choice(explosion_sounds).play()
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				if random.random() > 0.1:
					pow = Pow(hit.rect.center) #在撞击处产生补给
					all_sprites.add(pow)
					powerups.add(pow)
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				AddMob()

			#当BOSS出现时
			if not flag2   :
				#BOSS与玩家子弹相碰
				hits = pygame.sprite.groupcollide(bosses, player_bullets, False, True)
				for hit in hits:
					score += 50
					power_value_tmp += 5
					boss.blood -= 10

				#BOSS与玩家相撞
				hits = pygame.sprite.spritecollide(player, bosses, False , pygame.sprite.collide_circle)
				for hit in hits:
					boss.blood -= 10
					player.blood -= 100
					if player.blood <= 0:
						death_explosion = Explosion(player.rect.center,'player')
						all_sprites.add(death_explosion)
						player.hide()
						player.power = 1
						player.lives -= 1
						player.blood = 100

				#玩家与BOSS子弹相撞
				hits = pygame.sprite.spritecollide(player, bosses_bullet, True, pygame.sprite.collide_circle)
				for hit in hits:
					player.blood -= 30
					if player.blood <= 0:
						death_explosion = Explosion(player.rect.center,'player')
						all_sprites.add(death_explosion)
						player.hide()
						player.power = 1
						player.lives -= 1
						player.blood = 100

				#BOSS子弹与保护罩相碰
				pygame.sprite.spritecollide(protect1, bosses_bullet, True, pygame.sprite.collide_circle)
				pygame.sprite.groupcollide(bosses_bullet, playerlight, True, False)

			#敌机与大招相撞
			hits = pygame.sprite.groupcollide(mobs, playerlight, True, False)
			for hit in hits:
				score += 50
				random.choice(explosion_sounds).play()
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				if random.random() > 0.1:
					pow = Pow(hit.rect.center) #在撞击处产生补给
					all_sprites.add(pow)
					powerups.add(pow)
				AddMob()

			#大招与火山石相撞
			hits = pygame.sprite.groupcollide(lavas, playerlight, True, False)
			for hit in hits:
				score += 20
				expl = Explosion(hit.rect.center, 'small')
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				all_sprites.add(expl)
				AddLava()

			#火山石与玩家子弹碰撞
			hits = pygame.sprite.groupcollide(lavas, player_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 20
				power_value_tmp += 5
				expl = Explosion(hit.rect.center, 'small')
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				all_sprites.add(expl)
				AddLava()

			#玩家与普通敌机碰撞
			hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 25
				expl = Explosion(hit.rect.center,'small')
				all_sprites.add(expl)
				AddMob()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#玩家与火山石的碰撞
			hits = pygame.sprite.spritecollide(player, lavas, True, pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 10
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#玩家与敌机炮弹的碰撞
			hits = pygame.sprite.spritecollide(player, enemies_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 20
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#敌机炮弹与玩家大招相撞敌机炮弹直接消失
			hits = pygame.sprite.groupcollide(enemies_bullets, playerlight, True, False)

			#玩家与补给碰撞的检测
			hits = pygame.sprite.spritecollide(player, powerups, True)
			for hit in hits:              #可以添加一个加生命值的功能
				if hit.type == 'shield':
					player.blood += random.randrange(5, 10)
					if player.blood >= 100:
						player.blood = 100
				elif hit.type == 'protect':
					protect1.display()
				else: 
					player.powerup()
			
			# 玩家与加分的星星相撞
			hits = pygame.sprite.spritecollide(player, score_add_sprites, True)
			for hit in hits:
				score += random.randrange(100, 150)

			#敌机/火山石/子弹与盾牌之间的检测
			pygame.sprite.spritecollide(protect1, enemies_bullets, True, pygame.sprite.collide_circle)
			hits = pygame.sprite.spritecollide(protect1, lavas, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 20
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
			hits = pygame.sprite.spritecollide(protect1, mobs, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 50
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				AddMob()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)

			#生命值用光
			if player.lives == 0 and not death_explosion.alive():
				game_over(score)
				all_sprites.empty()
				lavas.empty()
				mobs.empty()
				player_bullets.empty()
				enemies_bullets.empty()
				powerups.empty()
				bosses_bullet.empty()
				bosses.empty()
				flag = True
		
			screen.fill(BLACK)
			screen.blit(background_img['background_Start'], (0, height))
			height += 1
			if height >= -168:
				height = -936
		
			all_sprites.draw(screen)
			if power_value_tmp >= 100:
				power_value_tmp = 100
			draw_text(screen, "score: "+str(score), 18, display_width/2,10)
			draw_lives(screen,display_width-100, 10, player.lives,player_mini_img)
			draw_blood(screen,10, 10, player.blood)
			draw_power(screen,10,30,power_value_tmp)
			draw_pause(screen,10, 50, reuse_img)

			time_end = pygame.time.get_ticks()
			if time_end - time_start > time and flag1:
				for each in enemies_bullets:
					each.kill()
				for each in mobs:
					expl = Explosion(each.rect.center, 'big')
					all_sprites.add(expl)
					each.kill()
				warning_sart_time = pygame.time.get_ticks()
				flag1 = False
		
			if not flag1 and pygame.time.get_ticks() - warning_sart_time < warning_time:
				draw_warning(screen)
		
			if not flag1 and pygame.time.get_ticks() - warning_sart_time > warning_time and flag2:
				boss = Boss()	
				all_sprites.add(boss)
				bosses.add(boss)
				flag2 = False
		 
			#当boss出现时，画血条
			if not flag2:
				draw_boss_blood(screen, boss.rect.left+20, boss.rect.bottom+2, boss.blood)
				if boss.blood == 0:
					blood = player.blood
					lives = player.lives
					empty_sprite()
					flag = True
					level += 1        #加一是为了进入下一关卡
					flag1_2 = True
			pygame.display.flip()
	
	if flag1_2:
		transition()

	#第二关	
	if level == 2:
		x1, y1 = 0, 0   #用于实现屏幕的滚动
		x2, y2 = 0, -768
		running = True
		build = True
		flag = False #判断是否返回主界面的标志
		flag1 = True #判断是否杀掉所有小敌机
		flag2 = True #判断是否创建BOSS
		time = 40000
		time_start = pygame.time.get_ticks()
		warning_time = 3000
		warning_sart_time = pygame.time.get_ticks()
		mob_missile_start_time = pygame.time.get_ticks()
		mob_missile_time = 8000      #两次导弹间隔时间
		missile_width1 = 0
		missile_width2 = 0
		missile_width3 = 0
		flag3 = False #用于判断地方是否可以发射导弹
		while running:
			if build:#只用创建一遍就可以了
				pygame.mixer.music.stop()
				pygame.mixer.music.load(path.join(sound_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))       
				pygame.mixer.music.play(-1)
				build = False			
				protect1 = Protect()#直接创建护盾类，有需要再添加
				all_sprites.add(protect1)
				player = Player(blood, lives)     #创建玩家 ，每一关都是这个
				playerone.add(player)
				all_sprites.add(player)				
				for i in range(4):
					AddMob2()
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						flag = True
			if flag:#如果按esc键就退出到最开始
				for sprite in all_sprites:
					sprite.kill()
				break
			clock.tick(60)
			all_sprites.update()
			#敌机和玩家子弹碰撞检测

			#敌机的导弹
			#导弹来写提示
			now = pygame.time.get_ticks()
			if now - mob_missile_start_time > mob_missile_time:
				missile_width1 = random.randrange(20,100)
				missile_width2 = random.randrange(100,300)
				missile_width3 = random.randrange(300,460)
				line1 = Line(missile_width1)
				line2 = Line(missile_width2)
				line3 = Line(missile_width3)
				all_sprites.add(line1)
				all_sprites.add(line2)
				all_sprites.add(line3)
				mob_missile_start_time = now
				flag3 = True
			
			if flag3:
				if not line1.alive():
					xx1 = Mob_missile(missile_width1)
					xx2 = Mob_missile(missile_width2)
					xx3 = Mob_missile(missile_width3)
					all_sprites.add(xx1)
					all_sprites.add(xx2)
					all_sprites.add(xx3)
					enemies_missile.add(xx1)
					enemies_missile.add(xx2)
					enemies_missile.add(xx3)
					flag3 = False #只发射一轮导弹攻击

			#玩家飞机和敌方导弹的碰撞
			hits = pygame.sprite.spritecollide(player, enemies_missile, True, pygame.sprite.collide_rect)
			for hit in hits:
				player.blood -= 30
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#敌方导弹和我方飞机的子弹相撞
			hits = pygame.sprite.groupcollide(enemies_missile, player_bullets, True, True)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌方导弹与保护膜相撞
			pygame.sprite.spritecollide(protect1, enemies_missile, True, pygame.sprite.collide_rect)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌方导弹与玩家大招相撞
			hits = pygame.sprite.groupcollide(enemies_missile, playerlight, True, False)
			for hit in hits:
				enemies_missile_boom_img = Explosion(hit.rect.center, 'enemies_missile')
				all_sprites.add(enemies_missile_boom_img)

			#敌机与我方飞机子弹的碰撞
			hits = pygame.sprite.groupcollide(mobs, player_bullets, True, True)
			for hit in hits:
				score += 50
				power_value_tmp += 5
				random.choice(explosion_sounds).play()
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				if random.random() > 0.1:
					pow = Pow(hit.rect.center) #在撞击处产生补给
					all_sprites.add(pow)
					powerups.add(pow)
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				AddMob2()

			#当BOSS出现时
			if not flag2:
				#BOSS与玩家子弹相碰
				hits = pygame.sprite.groupcollide(bosses, player_bullets, False, True)
				for hit in hits:
					score += 50
					power_value_tmp += 5
					boss.blood -= 10

				#BOSS与玩家相撞
				hits = pygame.sprite.spritecollide(player, bosses, False , pygame.sprite.collide_circle)
				for hit in hits:
					boss.blood -= 10
					player.blood -= 100
					if player.blood <= 0:
						death_explosion = Explosion(player.rect.center,'player')
						all_sprites.add(death_explosion)
						player.hide()
						player.power = 1
						player.lives -= 1
						player.blood = 100

				#玩家与BOSS子弹相撞
				hits = pygame.sprite.spritecollide(player, bosses_bullet, True, pygame.sprite.collide_circle)
				for hit in hits:
					player.blood -= 30
					if player.blood <= 0:
						death_explosion = Explosion(player.rect.center,'player')
						all_sprites.add(death_explosion)
						player.hide()
						player.power = 1
						player.lives -= 1
						player.blood = 100

				#玩家与BOSS大招相撞
				#这里不跟子弹一样，必须设置成collide_rect，因为大招是矩形
				hits = pygame.sprite.spritecollide(player, bosses_light, False, pygame.sprite.collide_rect)
				for hit in hits:
					player.blood -= 2
					if player.blood <= 0:
						death_explosion = Explosion(player.rect.center,'player')
						all_sprites.add(death_explosion)
						player.hide()
						player.power = 1
						player.lives -= 1
						player.blood = 100

				#BOSS子弹与保护罩相碰
				pygame.sprite.spritecollide(protect1, bosses_bullet, True, pygame.sprite.collide_circle)
				pygame.sprite.groupcollide(bosses_bullet, playerlight, True, False)

			#敌机与大招相撞
			hits = pygame.sprite.groupcollide(mobs, playerlight, True, False)
			for hit in hits:
				score += 50
				random.choice(explosion_sounds).play()
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				if random.random() > 0.1:
					pow = Pow(hit.rect.center) #在撞击处产生补给
					all_sprites.add(pow)
					powerups.add(pow)
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				AddMob2()

			# 玩家与加分的星星相撞
			hits = pygame.sprite.spritecollide(player, score_add_sprites, True)
			for hit in hits:
				score += random.randrange(100, 150)

			#大招与火山石相撞
			hits = pygame.sprite.groupcollide(lavas, playerlight, True, False)
			for hit in hits:
				score += 20
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)

			#火山石与玩家子弹碰撞
			hits = pygame.sprite.groupcollide(lavas, player_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 20
				power_value_tmp += 5
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)

			#玩家与普通敌机碰撞
			hits = pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 25
				expl = Explosion(hit.rect.center,'small')
				all_sprites.add(expl)
				AddMob2()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#玩家与火山石的碰撞
			hits = pygame.sprite.spritecollide(player, lavas, True, pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 10
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
				if random.random() > 0.3:
					lava_score = Score(hit.rect.center)
					all_sprites.add(lava_score)
					score_add_sprites.add(lava_score)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#玩家与敌机炮弹的碰撞
			hits = pygame.sprite.spritecollide(player, enemies_bullets, True, pygame.sprite.collide_circle)
			for hit in hits:
				player.blood -= 20
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				if player.blood <= 0:
					death_explosion = Explosion(player.rect.center,'player')
					all_sprites.add(death_explosion)
					player.hide()
					player.power = 1
					player.lives -= 1
					player.blood = 100

			#敌机炮弹与玩家大招相撞敌机炮弹直接消失
			hits = pygame.sprite.groupcollide(enemies_bullets, playerlight, True, False)

			#玩家与补给碰撞的检测
			hits = pygame.sprite.spritecollide(player, powerups, True)
			for hit in hits:              #可以添加一个加生命值的功能
				if hit.type == 'shield':
					player.blood += random.randrange(5, 10)
					if player.blood >= 100:
						player.blood = 100
				elif hit.type == 'protect':
					protect1.display()
				else: 
					player.powerup()
		
			#敌机/火山石/子弹与盾牌之间的检测
			pygame.sprite.spritecollide(protect1, enemies_bullets, True, pygame.sprite.collide_circle)
			hits = pygame.sprite.spritecollide(protect1, lavas, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 20
				expl = Explosion(hit.rect.center, 'small')
				all_sprites.add(expl)
				AddLava()
			hits = pygame.sprite.spritecollide(protect1, mobs, True, pygame.sprite.collide_circle)
			for hit in hits:
				score += 50
				expl = Explosion(hit.rect.center, 'big')
				all_sprites.add(expl)
				AddMob2()

			#生命值用光
			if player.lives == 0 and not death_explosion.alive():
				game_over(score)
				all_sprites.empty()
				lavas.empty()
				mobs.empty()
				player_bullets.empty()
				enemies_bullets.empty()
				powerups.empty()
				bosses_bullet.empty()
				bosses.empty()
				flag = True

			#all_sprites.update()      #这儿是个错误，当两次调用这个方法时，就会以两倍的速度运行
			#实现屏幕滚动
			screen.blit(background_img1, (x1, y1))
			screen.blit(background_img2, (x2, y2))
			y1 += 1
			y2 += 1
			if y1 == 768:
				y1 = 0
				y2 = -768
			all_sprites.draw(screen)
			if power_value_tmp >= 100:
				power_value_tmp = 100
			draw_text(screen, "score: "+str(score), 18, display_width/2,10)
			draw_lives(screen,display_width-100, 10, player.lives,player_mini_img)
			draw_blood(screen,10, 10, player.blood)
			draw_power(screen,10,30,power_value_tmp)
			draw_pause(screen,10, 50, reuse_img)
			time_end = pygame.time.get_ticks()
			if time_end - time_start > time and flag1:
				for each in enemies_bullets:
					each.kill()
				for each in mobs:
					expl = Explosion(each.rect.center, 'big')
					all_sprites.add(expl)
					each.kill()
				warning_sart_time = pygame.time.get_ticks()
				flag1 = False
		
			if not flag1 and pygame.time.get_ticks() - warning_sart_time < warning_time:
				draw_warning(screen)
		
			if not flag1 and pygame.time.get_ticks() - warning_sart_time > warning_time and flag2:
				boss = Boss2()	
				all_sprites.add(boss)
				bosses.add(boss)
				flag2 = False
		 
			#当boss出现时，画血条
			if not flag2:
				draw_boss_blood(screen, boss.rect.left+20, boss.rect.bottom+2, boss.blood)
				if boss.blood <= 0:
					empty_sprite()
					clearance(score)
					flag = True
			pygame.display.flip()

if __name__ == '__main__':
	game_introduce()