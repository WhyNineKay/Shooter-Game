from Utility import constants
from Utility import explosions
from Utility.Tools import tools
from Utility import globs
import random
import pygame
import math



class Bullet:
    def __init__(self, x: int, y: int, destination_x: int, destination_y: int, color: (int, int, int)) -> None:
        self.x = x
        self.y = y
        self.angle = math.atan2(destination_y - y, destination_x - x)
        self.color = color
        self.radius = constants.BULLET_RADIUS

    def update(self) -> None:
        self.x += constants.BULLET_SPEED * math.cos(self.angle) * globs.dt
        self.y += constants.BULLET_SPEED * math.sin(self.angle) * globs.dt

    def draw(self) -> None:
        pygame.draw.circle(constants.SCREEN, self.color, (int(self.x), int(self.y)), self.radius)




class Player:
    def __init__(self) -> None:
        self.x = constants.SCREEN_WIDTH / 2
        self.y = constants.SCREEN_HEIGHT / 2
        self.vx = 0
        self.vy = 0
        self.coins = 0
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, constants.PLAYER_SIZE, constants.PLAYER_SIZE)
        self.bullets = []
        self.bullet_timer = 0
        self.ammo = 100


    def spawn(self) -> None:
        """
        Spawn the player ensuring that it doesn't spawn inside a wall.
        :return:
        """

        x = random.randint(0, constants.SCREEN_WIDTH - constants.PLAYER_SIZE)
        y = random.randint(0, constants.SCREEN_HEIGHT - constants.PLAYER_SIZE)

        while tools.collides_with_wall(pygame.Rect(x, y, constants.PLAYER_SIZE, constants.PLAYER_SIZE)):
            x = random.randint(0, constants.SCREEN_WIDTH - constants.PLAYER_SIZE)
            y = random.randint(0, constants.SCREEN_HEIGHT - constants.PLAYER_SIZE)

        self.x = x
        self.y = y




    def _controls(self) -> None:
        """
        Controls for the player.
        :return:
        """


        keys = pygame.key.get_pressed()

        if keys[constants.CONTROLS["left"]]:
            self.vx -= constants.ACCELERATION * globs.dt

        if keys[constants.CONTROLS["right"]]:
            self.vx += constants.ACCELERATION * globs.dt

        if keys[constants.CONTROLS["up"]]:
            self.vy -= constants.ACCELERATION * globs.dt

        if keys[constants.CONTROLS["down"]]:
            self.vy += constants.ACCELERATION * globs.dt

        if keys[constants.CONTROLS["shoot"]]:
            if self.bullet_timer >= constants.BULLET_COOLDOWN:
                if self.ammo > 0:
                    self.ammo -= 1
                    mouse_pos = pygame.mouse.get_pos()
                    self.bullets.append(Bullet(self.x, self.y, mouse_pos[0], mouse_pos[1], (200, 200, 200)))
                    self.bullet_timer = 0

                    constants.SOUNDS["gun_shoot"].play()

    def damage(self) -> None:
        self.health -= constants.BOMB_DAMAGE


    def update(self) -> None:
        self._controls()

        # Apply Deceleration
        self.vx *= 1 - constants.DECELERATION * globs.dt * globs.dt
        self.vy *= 1 - constants.DECELERATION * globs.dt * globs.dt

        # Check if player velocity is higher than max speed
        if self.vx * globs.dt > constants.MAX_SPEED * globs.dt:
            self.vx = constants.MAX_SPEED * globs.dt * globs.dt

        if self.vx * globs.dt < -constants.MAX_SPEED * globs.dt:
            self.vx = -constants.MAX_SPEED * globs.dt * globs.dt

        if self.vy * globs.dt > constants.MAX_SPEED * globs.dt:
            self.vy = constants.MAX_SPEED * globs.dt * globs.dt

        if self.vy * globs.dt < -constants.MAX_SPEED * globs.dt:
            self.vy = -constants.MAX_SPEED * globs.dt * globs.dt


        # Check if player is out of bounds
        if self.x + self.vx * globs.dt > constants.SCREEN_WIDTH - constants.PLAYER_SIZE:
            self.x = constants.SCREEN_WIDTH - constants.PLAYER_SIZE
            self.vx = 0
        elif self.x + self.vx * globs.dt < 0:
            self.x = 0
            self.vx = 0

        if self.y + self.vy * globs.dt > constants.SCREEN_HEIGHT - constants.PLAYER_SIZE:
            self.y = constants.SCREEN_HEIGHT - constants.PLAYER_SIZE
            self.vy = 0
        elif self.y + self.vy * globs.dt < 0:
            self.y = 0
            self.vy = 0


        # check wall collision

        for wall in globs.walls:

            if pygame.Rect(self.x + self.vx * globs.dt, self.y, constants.PLAYER_SIZE, constants.PLAYER_SIZE).colliderect(wall.rect):
                self.vx = 0
            elif pygame.Rect(self.x, self.y + self.vy * globs.dt, constants.PLAYER_SIZE, constants.PLAYER_SIZE).colliderect(wall.rect):
                self.vy = 0


        # Update player position

        self.x += self.vx * globs.dt
        self.y += self.vy * globs.dt

        self.rect.topleft = (self.x, self.y)

        self.bullet_timer += globs.dt


        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            # Check if bullet is off the screen
            if bullet.x < 0 or bullet.x > constants.SCREEN_WIDTH or bullet.y < 0 or bullet.y > constants.SCREEN_HEIGHT:
                self.bullets.remove(bullet)


    def draw(self, screen) -> None:
        for bullet in self.bullets:
            bullet.draw()

        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if constants.PLAYER_DEBUG:
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 3)
            pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), 5)


class Bomb:
    def __init__(self) -> None:
        self.color = tools.random_color_from_range((255, 0, 0), (150, 0, 0))

        self.vx = 0
        self.vy = 0

        if tools.true_or_false():
            self.x = random.randint(-1000, -100)
            self.y = random.randint(-1000, -100)
        else:
            self.x = random.randint(constants.SCREEN_WIDTH + 100, constants.SCREEN_WIDTH + 1000)
            self.y = random.randint(constants.SCREEN_HEIGHT + 100, constants.SCREEN_HEIGHT + 1000)

        self.rect = pygame.Rect(self.x, self.y, constants.COIN_WIDTH, constants.COIN_HEIGHT)
        self.timer = random.randint(3 * constants.FPS, 10 * constants.FPS)

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)


    def update(self, player_object: Player) -> None:

        # MOVE TOWARDS THE PLAYER


        # TODO: create pathfinding ai


        # APPLY DECELERATION
        self.vx *= 1 - constants.DECELERATION * globs.dt
        self.vy *= 1 - constants.DECELERATION * globs.dt

        # Check if player velocity is higher than max speed
        if self.vx > constants.MAX_SPEED * globs.dt:
            self.vx = constants.MAX_SPEED * globs.dt

        if self.vy > constants.MAX_SPEED * globs.dt:
            self.vy = constants.MAX_SPEED * globs.dt

        if self.vx < -constants.MAX_SPEED * globs.dt:
            self.vx = -constants.MAX_SPEED * globs.dt

        if self.vy < -constants.MAX_SPEED * globs.dt:
            self.vy = -constants.MAX_SPEED * globs.dt

        # Apply velocity
        self.rect.x += self.vx * 0.6
        self.rect.y += self.vy * 0.6

        self.timer -= 1 * globs.dt



class Coin:
    def __init__(self) -> None:
        self.x = random.randint(0 + constants.PLAYER_SIZE, constants.SCREEN_WIDTH - constants.PLAYER_SIZE)
        self.y = random.randint(0 + constants.PLAYER_SIZE, constants.SCREEN_HEIGHT - constants.PLAYER_SIZE)
        self.rect = pygame.Rect(self.x, self.y, constants.COIN_WIDTH, constants.COIN_HEIGHT)

        while tools.collides_with_wall(self.rect):
            self.x = random.randint(0 + constants.PLAYER_SIZE, constants.SCREEN_WIDTH - constants.PLAYER_SIZE)
            self.y = random.randint(0 + constants.PLAYER_SIZE, constants.SCREEN_HEIGHT - constants.PLAYER_SIZE)
            self.rect = pygame.Rect(self.x, self.y, constants.COIN_WIDTH, constants.COIN_HEIGHT)




    def draw(self, screen: constants.SCREEN) -> None:
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), constants.COIN_WIDTH / 2)



class BombHandler:
    def __init__(self) -> None:
        """
        Class to handle the bomb logic.
        """

        self.bombs = []
        self.explosions = []


    def update(self, player_object: Player) -> None:
        # Update the bombs
        for bomb in self.bombs:
            bomb.update(player_object)
            # Check if bomb is dead

            if bomb.timer <= 0 and not tools.get_distance(bomb.rect, player_object.rect) < constants.BOMB_FOLLOW_DISTANCE:
                self.bombs.remove(bomb)

                # Particle effect
                self.explosions.append(explosions.BombTimeoutExplosion(bomb.rect.x, bomb.rect.y))

                # Play sound
                constants.SOUNDS["bomb_die"].play()

                # Add another bomb
                self.bombs.append(Bomb())

            if bomb.rect.colliderect(player_object.rect):
                self.bombs.remove(bomb)

                # Particle effect
                self.explosions.append(explosions.DefaultExplosion(bomb.rect.x, bomb.rect.y))

                # Deal Damage
                player_object.damage()

                # Play sound
                constants.SOUNDS["explosion"].play()

                # Add another bomb
                self.bombs.append(Bomb())

            for bullet in player_object.bullets:
                if bomb.rect.collidepoint(bullet.x, bullet.y):
                    try:
                        self.bombs.remove(bomb)
                    except ValueError:
                        continue

                    # Particle effect
                    # TODO: Make this a different explosion

                    # Play sound
                    constants.SOUNDS["explosion"].play()

                    # Add another bomb
                    self.bombs.append(Bomb())

        for expl in self.explosions:
            expl.update()

            if expl.is_dead:
                self.explosions.remove(expl)


    def draw(self, screen) -> None:
        for bomb in self.bombs:
            bomb.draw(screen)

        for explosion in self.explosions:
            explosion.draw(screen)

    def add_bomb(self) -> None:
        self.bombs.append(Bomb())



class CoinHandler:
    def __init__(self):
        self.coins = []
        self.explosions = []

    def add_coin(self):
        self.coins.append(Coin())

    def draw(self, screen):
        for coin in self.coins:
            coin.draw(screen)

        for expl in self.explosions:
            expl.draw(screen)

    def update(self, player_object: Player):
        for coin in self.coins:
            if coin.rect.colliderect(player_object.rect):
                self.coins.remove(coin)
                self.add_coin()
                player_object.coins += 1

                # Particle effect
                self.explosions.append(explosions.ConfettiExplosion(coin.x, coin.y))

                # Play sound
                constants.SOUNDS["coin_pickup"].play()


        for expl in self.explosions:
            expl.update()
            if expl.is_dead:
                self.explosions.remove(expl)



class Wall:
    """Wall Object."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: constants.SCREEN) -> None:
        pygame.draw.rect(screen, constants.WALL_COLOR, self.rect)

    def update(self) -> None:
        pass


coin_handler = CoinHandler()