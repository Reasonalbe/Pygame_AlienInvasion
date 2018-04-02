import pygame
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象以及一个包含了设置参数的对象
    pygame.init()
    #此处为整个项目唯一一个保存了游戏设置的对象，因此在项目中任何地方对其进行修改也会反映在其他地方
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    #创建唯一一个保存游戏统计信息的实例
    stats = GameStats(ai_settings)
    #创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    #创建飞船
    ship = Ship(ai_settings, screen)
    #创建一个管理bullet的group
    bullets = Group()
    #创建一个管理alien的group
    aliens = Group()
    #创建外星人舰队
    gf.creat_fleet(ai_settings, screen, ship, aliens)
    #创建按钮
    play_button = Button(ai_settings, screen, 'Play')

    #开始游戏的主循环
    while True:
        #事件监视
        gf.check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        if stats.game_active:
            # 更新飞船位置
            ship.update()
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats, sb, bullets, ship, aliens)
            # 更新外星人位置
            gf.update_alien(ai_settings, stats, sb, screen, ship, aliens, bullets)

        #更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

if __name__ == '__main__':
    run_game()
