import pygame
import random
from . import bulletClass



class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x = None, kind = None, isred = None):
        pygame.sprite.Sprite.__init__(self)
        
        # ̹�˳���ǰ�����Ƿ񲥷�
        self.flash = False
        self.times = 90
        
        # ����:̹������      
        self.kind = kind
        if not kind:
            self.kind = random.choice([1, 2, 3, 4])     
            
        # ѡ��о�̹������        
        if self.kind == 1:
            self.enemy_x_0 = pygame.image.load(r"other_games\tankwar\image\enemy_1_0.png").convert_alpha()
            self.enemy_x_3 = pygame.image.load(r"other_games\tankwar\image\enemy_1_3.png").convert_alpha()
        if self.kind == 2:
            self.enemy_x_0 = pygame.image.load(r"other_games\tankwar\image\enemy_2_0.png").convert_alpha()
            self.enemy_x_3 = pygame.image.load(r"other_games\tankwar\image\enemy_2_3.png").convert_alpha()
        if self.kind == 3:
            self.enemy_x_0 = pygame.image.load(r"other_games\tankwar\image\enemy_3_1.png").convert_alpha()
            self.enemy_x_3 = pygame.image.load(r"other_games\tankwar\image\enemy_3_0.png").convert_alpha()
        if self.kind == 4:
            self.enemy_x_0 = pygame.image.load(r"other_games\tankwar\image\enemy_4_0.png").convert_alpha()
            self.enemy_x_3 = pygame.image.load(r"other_games\tankwar\image\enemy_4_3.png").convert_alpha()
        self.enemy_3_0 = pygame.image.load(r"other_games\tankwar\image\enemy_3_0.png").convert_alpha()
        self.enemy_3_2 = pygame.image.load(r"other_games\tankwar\image\enemy_3_2.png").convert_alpha()
        
        
        # ����:�Ƿ�Я��ʳ��
        self.isred = isred
        if not None:
            self.isred = random.choice((True, False, False, False, False))
        if self.isred:
            self.tank = self.enemy_x_3
        else:
            self.tank = self.enemy_x_0
        # ����:̹��λ��
        self.x = x
        if not self.x:
            self.x = random.choice([1, 2, 3])
        self.x -= 1
        
        # �˶��е�����ͼƬ
        self.tank_R0 = self.tank.subsurface(( 0, 48), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3 + 0 * 24
        
        # ̹���ٶ�   ����   ����   �ӵ�����   �ӵ��ӳ�
        self.speed = 1
        self.dir_x, self.dir_y = 0, 1
        self.life = 1
        self.bulletNotCooling = True
        self.bullet = bulletClass.Bullet()
        # �Ƿ�ײǽ��ײǽ��ı䷽��
        self.dirChange = False
        
        # ÿ��̹�˲�ͬ������
        if self.kind == 2:
            self.speed = 3
        if self.kind == 3:
            self.life = 3
        
    def shoot(self):
        # �����ӵ�����
        self.bullet.life = True
        self.bullet.changeImage(self.dir_x, self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top + 1
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom - 1
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
    
    def move(self, tankGroup, brickGroup, ironGroup):
        self.rect = self.rect.move(self.speed * self.dir_x, self.speed * self.dir_y)
        
        if self.dir_x == 0 and self.dir_y == -1:
            self.tank_R0 = self.tank.subsurface(( 0, 0),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 0),(48, 48))
        elif self.dir_x == 0 and self.dir_y == 1:
            self.tank_R0 = self.tank.subsurface(( 0, 48),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 48),(48, 48))
        elif self.dir_x == -1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 96),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 96),(48, 48))
        elif self.dir_x == 1 and self.dir_y == 0:
            self.tank_R0 = self.tank.subsurface(( 0, 144),(48, 48))
            self.tank_R1 = self.tank.subsurface((48, 144),(48, 48))
        
        
        # ��ײ��ͼ��Ե
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.bottom > 630 - 3:
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.left < 3:
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        elif self.rect.right > 630 - 3:
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
        # ��ײǽ�� ��̹��
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None) \
            or pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed * -self.dir_x, self.speed * -self.dir_y)
            self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
