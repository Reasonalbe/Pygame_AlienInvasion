import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """响应鼠标和键盘事件"""
    for event in pygame.event.get():
        # 退出游戏
        if event.type == pygame.QUIT:
            sys.exit()
        #键盘事件
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        #鼠标按下事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, mouse_x, mouse_y):
    """在玩家按下play后开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏鼠标
        pygame.mouse.set_visible(False)
        #重置统计信息
        stats.reset_stats()
        stats.game_active = True
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        #创建新的外星人并使飞船剧中
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #重置记分牌
        sb.pre_high_score()
        sb.pre_level()
        sb.pre_score()
        sb.pre_ships()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕图像，并切换到新屏幕"""
    #针对每一个可移动对象，应将其位置移动和屏幕显示分开处理，此处主要用于将已经更改后的对象位置绘制在屏幕上
    # 每次循环都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    #绘制飞船
    ship.blitme()
    #绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #绘制外星人
    aliens.draw(screen)
    #绘制按钮
    if not stats.game_active:
        play_button.draw_button()
    #绘制记分牌
    sb.show_score()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_setting, screen, stats, sb, bullets, ship, aliens):
    """更新子弹位置并删除已消失子弹"""
    # 更新子弹位置
    bullets.update()
    #删除消失子弹
    for bullet in bullets.copy():
        #for循环中不应从列表或编组中删除条目，故遍历副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_coliisions(ai_setting, screen, stats, sb, bullets, ship, aliens)


def check_bullet_alien_coliisions(ai_setting, screen, stats, sb, bullets, ship, aliens):
    """检测子弹与外星人的碰撞，若发生碰撞则删除相应子弹和外星人"""
    # pygame.sprite.groupcollide()会检测两个group类中的sprite对象的rect属性是否发生重叠
    # 该函数返回一个字典，字典的键和值分别对应两个碰撞对象，两个实参表示碰撞后是否删除碰撞对象
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #击中外星人后加分
    if collisions:
        for aliens in collisions.values():
            #此处是检查是否有一个子弹消灭多种外星人的情形
            stats.score += ai_setting.alien_points * len(aliens)
            sb.pre_score()
        #检测最高分变动
        check_high_score(stats, sb)
    # 检查外星人是否被完全消灭，若完全消灭则删除现有子弹并生成新的外星人，并提升游戏难度
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        creat_fleet(ai_setting, screen, ship, aliens)
        #提高等级
        stats.level += 1
        sb.pre_level()

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹未达到上限则创建一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, ship, screen)
        bullets.add(new_bullet)

def get_number_alien_x(ai_settings, alien_width):
    """计算每行可以容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_row(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳外星人的行数"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def creat_alien(ai_settings, screen, aliens, alien_number, row_number):
    """  创建一个外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #此处创建一个外星人对象只是为了获取其图像宽度及高度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_row(ai_settings, ship.rect.height, alien.rect.height)
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings, screen, aliens, alien_number, number_row)

def check_fleet_edge(ai_settings, screen, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
         if alien.check_edge():
             change_fleet_direction(ai_settings, aliens)
             break

def change_fleet_direction(ai_settings, aliens):
    """将舰队下移并改变移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1

def update_alien(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """更新所有外星人位置"""
    check_fleet_edge(ai_settings, screen, aliens)
    aliens.update()

    #检测外星人与飞船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    #检测外星人与屏幕底部碰撞
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应外星人碰撞飞船"""
    if stats.ship_left > 0:
        # 将ship_left减1
        stats.ship_left -= 1

        #更新记分牌
        sb.pre_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船移至屏幕中间
        creat_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查外星人是否到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """检查是否出现了新分数"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.pre_high_score()




