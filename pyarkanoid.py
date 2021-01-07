# -*- coding: utf-8 -*-

# 1. 공이 모든 블럭들을 다 깨면 성공
# 2. 공이 바닥에 닿는다면 실패
# 3. 시간이 다되면 타임오버

import pygame
import os
import random
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
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "img") # 이미지 폴더 위치

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 가상의 stage
stage_height = 50 # 막대를 화면 바닥보다 50만큼 띄워줄 것이다.

# (움직이는) 막대 만들기
bar = pygame.image.load(os.path.join(image_path, "bar.png"))
bar_size = bar.get_rect().size
bar_width = bar_size[0]
bar_height = bar_size[1]
bar_x_pos = (screen_width / 2 ) - (bar_width / 2)
bar_y_pos = screen_height - stage_height - bar_height

# 막대 움직임 제어
bar_to_x = 0
bar_speed = 0.2

# 공 만들기 (5x5 size)
ball = pygame.image.load(os.path.join(image_path, "ball.png"))
ball_size = ball.get_rect().size
ball_width = ball_size[0]
ball_height = ball_size[1]
ball_x_pos = (screen_width / 2 ) - (ball_width / 2)
ball_y_pos = screen_height - stage_height - bar_height - ball_height

# 공 움직임 제어
ball_speed_x = 0.1
ball_speed_y = 0.1 
ball_max_speed_x = 0.5
ball_max_speed_y = 0.5

# 벽돌들
blocks = []
block_rows = 5
block_cols = 10
block_to_remove = -1

block_img = pygame.image.load(os.path.join(image_path, "block_square.png"))
block_size = block_img.get_rect().size
block_width = block_size[0]
block_height = block_size[1]

# 벽돌들을 위치시켜 준다.
for i in range(block_rows):
    for j in range(block_cols):
        block_x_pos = (screen_width / 2) - (block_width * block_cols / 2) + (block_width * j)
        block_y_pos = 50 + i * block_height

        # 벽돌들은 필요한 정보가 위치 정보 뿐이므로 위치 정보를 등록시킨다.
        blocks.append({
            "block_x_pos": block_x_pos,
            "block_y_pos": block_y_pos,
        })

# 폰트 정의
game_font = pygame.font.Font(None, 40)

# 게임 제한 시간
total_time = 500
start_ticks = pygame.time.get_ticks() # 시작 시간

# 게임 종료 메세지
# Time Out
# Mission Complete
# Game Over
game_result = "Game Over"
###############################################################




# 이벤트 루프
running = True # 게임이 진행 중인가?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

###############################################################

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 키보드 이벤트 처리 : 막대의 좌우 움직임만 처리하면 된다.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bar_to_x -= bar_speed
            elif event.key == pygame.K_RIGHT:
                bar_to_x += bar_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                bar_to_x = 0    

    # 바 위치 변경 (dt를 곱해서 FPS에 맞게 속도를 맞춰준다)
    bar_x_pos += bar_to_x * dt
    
    if bar_x_pos < 0:
        bar_x_pos = 0
    elif bar_x_pos > screen_width - bar_width:
        bar_x_pos = screen_width - bar_width


    # 공의 위치 및 움직임 
    ball_x_pos += ball_speed_x * dt
    ball_y_pos += ball_speed_y * dt

    # 화면의 가장자리(위, 오른쪽, 왼쪽)와 충돌 했을 경우에 공을 튕겨낸다.    
    if ball_x_pos < 0:
        ball_x_pos = 0
        ball_speed_x = -ball_speed_x
    elif ball_x_pos > screen_width - ball_width:
        ball_x_pos = screen_width - ball_width
        ball_speed_x = -ball_speed_x
    if ball_y_pos < 0:
        ball_y_pos = 0
        ball_speed_y = -ball_speed_y
    # 볼이 화면 아래로 나가는 경우: 게임오버
    elif ball_y_pos > screen_height - ball_height:
        ball_y_pos = screen_height - ball_height
        game_result = "Game Over"
        running = False
###############################################################

    

###############################################################
    # 충돌 처리

    # 막대 정보 읽어오기
    bar_rect = bar.get_rect()
    bar_rect.left = bar_x_pos
    bar_rect.top = bar_y_pos
    
    # 공 정보 읽어오기
    ball_rect = ball.get_rect()
    ball_rect.left = ball_x_pos
    ball_rect.right = ball_x_pos + ball_rect.size[0]
    ball_rect.top = ball_y_pos
    ball_rect.bottom = ball_y_pos + ball_rect.size[1]

    # 블럭 정보 읽어오고 공과 충돌 처리
    for block_idx, block_val in enumerate(blocks):
        block_pos_x = block_val["block_x_pos"]
        block_pos_y = block_val["block_y_pos"]

        block_rect = block_img.get_rect()
        block_rect.left = block_pos_x
        block_rect.right = block_pos_x + block_rect.size[0]
        block_rect.top = block_pos_y
        block_rect.bottom = block_pos_y + block_rect.size[1]

        # 볼과 블럭의 충돌을 처리한다.
        # 일단 충돌했는지 파악하고, 충돌했으면 옆면으로 부딪혔는지, 위아래 면으로 부딪혔는지 파악해서
        # 공을 수직으로 튕겨낼 것인지 수평으로 튕겨낼 것인지 결정한다.
        # TODO: 디버깅 요망
        if ball_rect.colliderect(block_rect):
            side_overlap = min(abs(block_rect.left - ball_rect.right), abs(block_rect.right - ball_rect.left)) 
            topdown_overlap = min(abs(block_rect.top - ball_rect.bottom), abs(block_rect.bottom - ball_rect.top)) 
            if side_overlap > topdown_overlap: 
                print("updown collision")
                ball_speed_y *= -1
            else:
                print("side collision")
                ball_speed_x *= -1
            
            block_to_remove = block_idx
            break
        
    # 충돌한 블럭은 지워준다.
    if block_to_remove >= 0:
        del blocks[block_to_remove]
        block_to_remove = -1

    # 모든 블럭을 다 없앨 경우 성공
    if len(blocks) == 0:
        running = False
        game_result = "Mission Complete"

    # 공과 바가 충돌했을 때. y축 속도를 바꾸고, x축 속도도 랜덤하게 바꾼다.
    if ball_rect.colliderect(bar_rect):
        ball_speed_y = -(ball_speed_y)
        # new_ball_speed_x = ball_speed_x + random.uniform(-0.05, 0.05) * dt
        # if new_ball_speed_x * ball_speed_x > 0:
        #     ball_speed_x = new_ball_speed_x
###############################################################


    
###############################################################
    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(bar, (bar_x_pos, bar_y_pos))
    screen.blit(ball, (ball_x_pos, ball_y_pos))
    
    for idx, val in enumerate(blocks):
        block_x_pos = val["block_x_pos"]
        block_y_pos = val["block_y_pos"]
        screen.blit(block_img, (block_x_pos, block_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

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
