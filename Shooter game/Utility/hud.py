import pygame
from Utility import constants
from Utility.fonts import font_manager


class AmmoCounter:
    def __init__(self) -> None:
        """
        Ammo counter to display the amount of ammo.
        :return:
        """

        self.font = font_manager.create_font(constants.SYSTEM_FONT, constants.TEXT_SIZE)
        self.text_color = (255, 255, 255)
        self.text = self.font.render(str(0), True, self.text_color)
        self.pos_x = constants.SCREEN_WIDTH - self.text.get_width() - 10
        self.pos_y = constants.TEXT_POS_MARGIN
        self.image = pygame.transform.scale(constants.IMAGES["BULLET_COUNT"], (constants.TEXT_SIZE, constants.TEXT_SIZE))

    def draw(self, screen: pygame.Surface) -> None:
        """
        :param screen:
        :return:
        """

        screen.blit(self.text, (self.pos_x, self.pos_y))
        screen.blit(self.image, (self.pos_x - self.image.get_width() - 10, self.pos_y))

    def update(self, ammo: int) -> None:
        """
        :param ammo: Ammo count of the player.
        :return:
        """

        self.text = self.font.render(str(ammo), True, self.text_color)
        self.pos_x = constants.SCREEN_WIDTH - self.text.get_width() - 10
        if ammo == 0:
            self.text_color = (255, 0, 0)


class CoinCounter:
    def __init__(self):
        """
        Coin counter to display the amount of coins.
        :return:
        """

        self.font = font_manager.create_font(constants.SYSTEM_FONT, constants.TEXT_SIZE)
        self.text_color = (255, 255, 255)
        self.text = self.font.render(str(0), True, self.text_color)
        self.pos_x = constants.TEXT_POS_MARGIN
        self.pos_y = constants.TEXT_POS_MARGIN
        self.image = pygame.transform.scale(constants.IMAGES["COIN_COUNT"], (constants.TEXT_SIZE, constants.TEXT_SIZE))

    def update(self, coins: int) -> None:
        """
        :param coins: Coin count of the player.
        :return:
        """

        self.text = self.font.render(str(coins), True, self.text_color)


    def draw(self, screen: pygame.Surface) -> None:
        """
        :param screen:
        :return:
        """

        screen.blit(self.text, (self.pos_x + self.image.get_width(), self.pos_y))
        screen.blit(self.image, (self.pos_x, self.pos_y))


class HealthBar:
    def __init__(self) -> None:
        self.width = constants.HEALTH_BAR_WIDTH
        self.height = constants.HEALTH_BAR_HEIGHT
        self.x = constants.HEALTH_BAR_MARGIN
        self.y = constants.SCREEN_HEIGHT - constants.HEALTH_BAR_MARGIN

        self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.percent = 100 / 100
        self.healthRect = pygame.Rect(self.x, self.y, (self.width / self.percent), self.height)

    def update(self, player_health: int) -> None:
        self.percent = 100 / player_health
        self.healthRect = pygame.Rect(self.x, self.y, (self.width / self.percent), self.height)

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, (200, 0, 0), self.Rect)
        pygame.draw.rect(screen, (0, 200, 0), self.healthRect)



health_bar = HealthBar()
ammo_counter = AmmoCounter()
coin_counter = CoinCounter()