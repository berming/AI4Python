# bermin@live.cn  2024-06-26


import pygame
import random

# 初始化pygame
pygame.init()

# 设置屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('简单的视觉交互小游戏')

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 游戏变量
player_size = 50
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size]
enemy_size = 50
enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

# 设置游戏时钟
clock = pygame.time.Clock()

# 定义函数：绘制玩家和敌人
def draw_elements(player_pos, enemy_list):
    screen.fill(WHITE)
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    pygame.draw.rect(screen, (0, 0, 255), (player_pos[0], player_pos[1], player_size, player_size))

# 定义函数：更新敌人位置
def update_enemy_positions(enemy_list):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += 20
        else:
            enemy_list.pop(idx)

# 定义函数：碰撞检测
def collision_check(player_pos, enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

# 游戏主循环
game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            player_pos = [x, y]

    screen.fill(WHITE)

    update_enemy_positions(enemy_list)
    if collision_check(player_pos, enemy_list):
        game_over = True
        break

    draw_elements(player_pos, enemy_list)

    pygame.display.update()

    clock.tick(30)

pygame.quit()
