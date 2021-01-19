# -*- coding: utf-8 -*-

# 1. 공이 모든 블럭들을 다 깨면 성공
# 2. 공이 바닥에 닿는다면 실패
# 3. 시간이 다되면 타임오버

import pygame
import os
import random

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "img") # 이미지 폴더 위치


###############################################################
# 클래스 선언
class GameObj(pygame.sprite.Sprite):
    def __init__(self, img_src, x, y):
        super(GameObj, self).__init__()
        # This needs to be updated when the item happens.
        self.image = pygame.image.load(img_src)
        self.rect = self.image.get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.rect.x = x
        self.rect.y = y
    
    def update_rect(self, x, y):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        

class Bar(GameObj):

    img_src = os.path.join(image_path, "bar.png")

    def __init__(self, x, y):
        super(Bar, self).__init__(self.img_src, x, y)
        # This needs to be updated when the item happens.
        self.speed = 0.4
        self.delta_x = 0
        self.is_wide = False

    def get_wide(self):
        if not self.is_wide:
            prev_x = self.rect.x
            prev_y = self.rect.y
            self.image = pygame.transform.scale(pygame.image.load(self.img_src), (self.width * 2, self.height))
            self.is_wide = True
            self.update_rect(prev_x, prev_y)

    def get_narrow(self):
        if self.is_wide:
            prev_x = self.rect.x
            prev_y = self.rect.y
            self.image = pygame.transform.scale(pygame.image.load(self.img_src), (self.width * 1/2, self.height))
            self.is_wide = False
            self.update_rect(prev_x, prev_y)




class Ball(GameObj):

    ball_src = os.path.join(image_path, "ball.png")
    fireball_src = os.path.join(image_path, "fireball.png")

    def __init__(self, x, y):
        super(Ball, self).__init__(self.ball_src, x, y)
        # This needs to be updated when the item happens.
        self.speed_x = 0.2
        self.speed_y = 0.2
        self.max_speed = 0.5
        self.delta_x = 0.0
        self.delta_y = 0.0
        self.is_fireball = False
    
    def do_fireball(self):
        prev_x = self.rect.x
        prev_y = self.rect.y
        self.image = pygame.image.load(self.fireball_src)
        self.update_rect(prev_x, prev_y)
        self.is_fireball = True

    def undo_fireball(self):
        prev_x = self.rect.x
        prev_y = self.rect.y
        self.image = pygame.image.load(self.ball_src)
        self.update_rect(prev_x, prev_y)
        self.is_fireball = False

class Block(GameObj):

    img_src = os.path.join(image_path, "block_square.png")

    def __init__(self, x, y):
        super(Block, self).__init__(self.img_src, x, y)
        # item = 0 : 아이템 없음
        # item = 1 : 파이어볼
        # item = 2 : 와이드
        self.item = 0
        self.rect.left = self.rect.x
        self.rect.right = self.rect.x + self.width
        self.rect.top = self.rect.y
        self.rect.bottom = self.rect.y + self.height



###############################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() # 초기화

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름 설정
pygame.display.set_caption("PyArkanoid")

# FPS
clock = pygame.time.Clock()
###############################################################



###############################################################
# 디렉토리 설정


# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 가상의 stage
stage_height = 50 # 막대를 화면 바닥보다 50만큼 띄워줄 것이다.

# 막대 만들기
bar = Bar(0, 0)
bar.rect.x = (screen_width / 2 ) - (bar.width / 2)
bar.rect.y = screen_height - stage_height - bar.height

# 공 만들기
ball = Ball(0, 0)
ball.rect.x = (screen_width / 2 ) - (ball.width / 2)
ball.rect.y = screen_height - stage_height - bar.height - ball.height

# 막대와 공을 같이 관리
sprites = pygame.sprite.Group()
sprites.add(bar)
sprites.add(ball)

# 벽돌 그룹 만들기
blocks = pygame.sprite.Group()

block_rows = 5
block_cols = 10
blocks_to_check = []
block_to_remove = -1

block_img = pygame.image.load(os.path.join(image_path, "block_square.png"))
block_size = block_img.get_rect().size
block_width = block_size[0]
block_height = block_size[1]

# 벽돌들을 위치시켜 준다.
for i in range(block_rows):
    for j in range(block_cols):
        idx = block_cols * i + j
        block_x_pos = (screen_width / 2) - (block_width * block_cols / 2) + (block_width * j)
        block_y_pos = 50 + i * block_height

        # 벽돌들은 필요한 정보가 위치 정보 뿐이므로 위치 정보를 등록시킨다.
        block = Block(block_x_pos, block_y_pos)
        if idx == 48:
            block.item = 1
        blocks.add(block)


# 폰트 정의
game_font = pygame.font.Font(None, 40)

# 게임 제한 시간
total_time = 500
fireball_duration = 10.0
start_ticks = pygame.time.get_ticks() # 시작 시간
fireball_start_ticks = start_ticks

# 게임 종료 메세지
# Time Out
# Mission Complete
# Game Over
game_result = "Game Over"
###############################################################




# 이벤트 루프
running = True # 게임이 진행 중인가?
while running:
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정

###############################################################

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 키보드 이벤트 처리 : 막대의 좌우 움직임만 처리하면 된다.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bar.delta_x -= bar.speed
            elif event.key == pygame.K_RIGHT:
                bar.delta_x += bar.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                bar.delta_x = 0    

    # 바 위치 변경 (dt를 곱해서 FPS에 맞게 속도를 맞춰준다)
    bar.rect.x += bar.delta_x * dt
    
    if bar.rect.x < 0:
        bar.rect.x = 0
    elif bar.rect.x > screen_width - bar.width:
        bar.rect.x = screen_width - bar.width


    # 공의 위치 및 움직임 
    ball.rect.x += ball.speed_x * dt
    ball.rect.y += ball.speed_y * dt

    # 화면의 가장자리(위, 오른쪽, 왼쪽)와 충돌 했을 경우에 공을 튕겨낸다.    
    if ball.rect.x < 0:
        ball.rect.x = 0
        ball.speed_x = -ball.speed_x
    elif ball.rect.x > screen_width - ball.width:
        ball.rect.x = screen_width - ball.width
        ball.speed_x = -ball.speed_x
    if ball.rect.y < 0:
        ball.rect.y = 0
        ball.speed_y = -ball.speed_y
    # 볼이 화면 아래로 나가는 경우: 게임오버
    elif ball.rect.y > screen_height - ball.height:
        ball.rect.y = screen_height - ball.height
        game_result = "Game Over"
        running = False
###############################################################

    

###############################################################
    # 충돌 처리

    # 막대 정보 읽어오기
    # bar_rect = bar.get_rect()
    bar.rect.left = bar.rect.x
    bar.rect.top = bar.rect.y
    
    # 공 정보 읽어오기
    # ball.rect = ball.get_rect()
    ball.rect.left = ball.rect.x
    ball.rect.right = ball.rect.x + ball.rect.size[0]
    ball.rect.top = ball.rect.y
    ball.rect.bottom = ball.rect.y + ball.rect.size[1]

    # 블럭 정보 읽어오고 공과 충돌 처리
    for block_idx, block in enumerate(blocks.sprites()):

        # 볼과 블럭의 충돌을 처리한다.
        # 일단 충돌했는지 파악하고, 충돌했으면 옆면으로 부딪혔는지, 위아래 면으로 부딪혔는지 파악해서

        # 공이 충돌했을 때 valid한 충돌인지 계산
        # 공을 한번에 하나씩만 지울것이라 for loop 밖에서 돌것이다.
        if ball.rect.colliderect(block.rect):
            left_overlap = ball.rect.right - block.rect.left
            right_overlap = block.rect.right - ball.rect.left
            top_overlap = ball.rect.bottom - block.rect.top
            bottom_overlap = block.rect.bottom - ball.rect.top
            
            collision_side_list = []
            # 공의 타당한 충돌방향과 충돌 후 지난 시간을 구해준다.
            if left_overlap > 0 and ball.speed_x > 0:
                direction = 'horizontal'
                t_after_col = left_overlap / abs(ball.speed_x)
                collision_side_list.append((direction, t_after_col))
            if right_overlap > 0 and ball.speed_x < 0:
                direction = 'horizontal'
                t_after_col = right_overlap / abs(ball.speed_x)
                collision_side_list.append((direction, t_after_col))
            if top_overlap > 0 and ball.speed_y > 0:
                direction = 'vertical'
                t_after_col = top_overlap / abs(ball.speed_y)
                collision_side_list.append((direction, t_after_col))
            if bottom_overlap > 0 and ball.speed_y < 0:
                direction = 'vertical'
                t_after_col = bottom_overlap / abs(ball.speed_y)
                collision_side_list.append((direction, t_after_col))
            
            # 충돌 후 시간이 가장 큰 것을 구해서 가장 먼저 충돌했을 면을 구한다.
            min_direction = None
            min_t = 0

            for direction, t_after_col in collision_side_list:
                if t_after_col < min_t or min_direction == None:
                    min_t = t_after_col
                    min_direction = direction

            blocks_to_check.append({
                'idx': block_idx,
                'side': min_direction,
                't_after_col': min_t
            })

    # 여러 블럭이 다 충돌했을 것 같은 경우에 충돌 후 시간이 가장 많이 지난 블럭만 지운다.
    min_idx = -1
    min_t = 0
    min_side = None
    for block in blocks_to_check:
        if block['t_after_col'] < min_t or min_side == None:
            min_idx = block['idx']
            min_t = block['t_after_col']
            min_side = block['side']
    
    # 충돌한 블럭은 지워준다.
    if min_idx >= 0:
        print(min_idx)
        # 필요한 속도를 반대 방향으로 바꾸어 준다.
        # 파이어볼 모드이면 그대로 진행한다.
        if not ball.is_fireball:
            if min_side == 'horizontal':
                ball.speed_x = -ball.speed_x
            else:
                ball.speed_y = -ball.speed_y
        blocks_tocheck = blocks.sprites()
        block_to_remove = blocks_tocheck[min_idx]
        if block_to_remove.item == 1:
            ball.do_fireball()

        blocks.remove(block_to_remove)
    blocks_to_check = []

    # 모든 블럭을 다 없앨 경우 성공
    if len(blocks.sprites()) == 0:
        running = False
        game_result = "Mission Complete"

    # 공과 바가 충돌했을 때. y축 속도를 바꾸고, x축 속도도 랜덤하게 바꾼다.
    if ball.rect.colliderect(bar.rect):
        ball.speed_y = -(ball.speed_y)
        
###############################################################


    
###############################################################
    # 경과 시간 계산
    current_ticks = pygame.time.get_ticks()
    elapsed_time = (current_ticks - start_ticks) / 1000
    fireball_elapsed_time = (current_ticks - fireball_start_ticks) / 1000
    if ball.is_fireball and fireball_elapsed_time > fireball_duration:
        ball.undo_fireball()
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    
    # 화면에 그리기
    screen.blit(background, (0, 0))
    blocks.draw(screen)
    sprites.draw(screen)
    screen.blit(timer, (10, 10))

    pygame.display.update() # 게임 화면을 다시 그리기 
###############################################################


###############################################################
# 게임 종료 처리
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
