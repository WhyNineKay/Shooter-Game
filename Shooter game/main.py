import pygame
from Utility import constants
from Utility import hud
from Utility import entities
from Utility import globs
from Utility.Tools import debug
from Utility import map_gen

pygame.font.init()
pygame.mixer.init()


class Main:
    def __init__(self):
        self.screen = constants.SCREEN
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont(constants.SYSTEM_FONT, 30)
        self.player = entities.Player()
        self.bomb_handler = entities.BombHandler()
        self.coin_handler = entities.CoinHandler()

        map_gen.create_walls()

        self.player.spawn()

        for i in range(5):
            self.coin_handler.add_coin()
            if constants.ENABLE_BOMBS:
                self.bomb_handler.add_bomb()

    def run(self):
        while self.running:
            globs.dt = self.clock.tick(constants.FPS) / 10

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.player.spawn()


    def update(self):

        self.player.update()
        self.coin_handler.update(self.player)
        self.bomb_handler.update(self.player)
        hud.health_bar.update(self.player.health)
        hud.ammo_counter.update(self.player.ammo)
        hud.coin_counter.update(self.player.coins)

        if self.player.health <= 0:
            self.running = False

        if self.player.health > 100:
            self.player.health = 100
        else:
            self.player.health += 0.1

        if constants.PLAYER_INVINCIBLE:
            self.player.health = 100

        if constants.INFINITE_BULLETS:
            self.player.ammo = 10

    def draw(self):
        self.screen.fill(constants.BACKGROUND_COLOR)

        for wall in globs.walls:
            wall.draw(self.screen)

        self.bomb_handler.draw(self.screen)
        self.coin_handler.draw(self.screen)
        self.player.draw(self.screen)

        hud.health_bar.draw(self.screen)
        hud.ammo_counter.draw(self.screen)
        hud.coin_counter.draw(self.screen)

        debug.debug("FPS: " + str(round(self.clock.get_fps(), 2)))


        pygame.display.flip()


main = Main()
main.run()
