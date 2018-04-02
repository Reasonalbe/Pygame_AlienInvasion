import pygame.sysfont
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_settings, screen, stats):
        """初始化得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #显示得分信息的字体属性
        self.text_color = (30, 30, 30)
        self.font = pygame.sysfont.SysFont(None, 48)

        #初始得分图像
        self.pre_score()
        self.pre_high_score()
        self.pre_level()
        self.pre_ships()

    def pre_high_score(self):
        """将最高分渲染成图像"""
        # 将得分圆整
        rounded_high_score = int(round(self.stats.high_score, -1))
        #用逗号分隔千分位
        score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在右上角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def pre_score(self):
        """将得分渲染成图像"""
        # 将得分圆整
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        #将得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def pre_level(self):
        """将等级转渲染为图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        #将等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def pre_ships(self):
        self.ships = Group()
        for ship_menber in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_menber * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect )
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

