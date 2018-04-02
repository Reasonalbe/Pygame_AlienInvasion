class GameStats:
    """跟踪统计游戏信息"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        #最高分不应该被重置
        self.high_score = 0

    def reset_stats(self):
        """初始化游戏中可能变化的统计信息"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1