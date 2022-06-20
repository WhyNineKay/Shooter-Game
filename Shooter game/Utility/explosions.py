import math
import pygame
from Utility import globs
import random
from Utility import constants
from Utility.Tools import tools


class Particle:
    def __init__(self, x: int, y: int, direction: int, speed: int, color: tuple[int, int, int],
                 size: int = 3, shape: str = 'circle', lifespan: int = None, fade: bool = False,
                 fade_time: float = 0.5, fade_to_color: tuple[int, int, int] = (0, 0, 0),
                 die_when_faded: bool = True, fade_alpha: bool = True) -> None:
        """
        Particle. Should only be used by explosions.

        :param x: X position.
        :param y: Y position.
        :param direction: Direction in degrees. (0, 360)
        :param speed: Speed in pixels (* delta time).
        :param color: Color of the particle. (R, G, B)
        :param size: Size of the shape.
        :param shape: Shape of the object. Can be 'circle' or 'square'.
        :param lifespan: Lifespan of the particle in frames (* delta time).
        :param fade: If the particle should fade out to the selected fade color.
        :param fade_time: Speed of the fade in seconds.
        :param fade_to_color: Color of the fade. (R, G, B)
        """

        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.color = color
        self.size = size
        self.shape = shape
        self.fade = fade
        self.fade_alpha = fade_alpha
        self.fade_to_color = fade_to_color
        self.fade_time = fade_time
        self.is_dead = False
        self.die_when_faded = die_when_faded
        self.dt = globs.dt

        if lifespan is None:
            self.lifespan = constants.FPS * fade_time
        else:
            self.lifespan = lifespan

        # Check what shape the particle should be.
        if self.shape.lower() == "circle":
            self.draw_function = self.draw_circle
        elif self.shape.lower() == "square":
            self.draw_function = self.draw_square
        elif self.shape.lower() == "both":
            if tools.true_or_false():
                self.draw_function = self.draw_circle
            else:
                self.draw_function = self.draw_square
        else:
            raise ValueError("Shape must be 'circle' or 'square'.")


    def _change_color(self) -> None:
        to_change = [self.fade_to_color[i] - self.color[i]
                     for i in range(len(self.color))]

        step = [to_change[i] / self.lifespan * globs.dt
                for i in range(len(self.color))]

        self.color = [self.color[i] + step[i] * globs.dt
                      for i in range(len(self.color))]

        self.lifespan -= 1 * globs.dt

        # Check if the color is the same as the fade color.
        if (self.color[0] == self.fade_to_color[0]
                and self.color[1] == self.fade_to_color[1]
                and self.color[2] == self.fade_to_color[2]):
            self.is_dead = True

        for i in range(len(self.color)):
            if self.color[i] < 0:
                self.color[i] = 0
            elif self.color[i] > 255:
                self.color[i] = 255

    def _change_alpha(self):
        if len(self.color) == 3:
            self.color = self.color + (255,)

        to_change = self.color[3] - self.color[3]

        step = to_change / self.lifespan * globs.dt

        self.color = self.color[:3] + (self.color[3] + step,)

        self.lifespan -= 1 * globs.dt

        if self.color[3] < 0:
            self.color = self.color[:3] + (0,)
        elif self.color[3] > 255:
            self.color = self.color[:3] + (255,)





    def update(self) -> None:
        """
        Update the particle.
        :return: None
        """
        # Update x and y position.
        self.x += self.speed * math.cos(math.radians(self.direction)) * self.dt
        self.y += self.speed * math.sin(math.radians(self.direction)) * self.dt

        # Update the lifespan.
        if self.lifespan is not None:
            self.lifespan -= 1 * self.dt
            # Check if the particle is dead.
            if self.lifespan <= 0:
                self.is_dead = True

        # Check if the particle should fade.
        if self.fade_alpha:
            self._change_alpha()

        elif self.fade:
            self._change_color()

    def draw(self, screen=constants.SCREEN) -> None:
        """
        Draws the particle to the screen.
        :return:
        """
        self.draw_function(screen)

    def draw_circle(self, screen=constants.SCREEN) -> None:
        """
        Draws a circle to the screen.
        :return:
        """
        color = (int(self.color[0]), int(self.color[1]), int(self.color[2]))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

    def draw_square(self, screen=constants.SCREEN) -> None:
        """
        Draws a square to the screen.
        :return:
        """
        color = (int(self.color[0]), int(self.color[1]), int(self.color[2]))
        pygame.draw.rect(screen, color, (int(self.x), int(self.y), self.size, self.size))



class DefaultExplosion:
    def __init__(self, x: int, y: int, particle_count: int = 70) -> None:
        """
        Default explosion.
        :param x: X position of the explosion.
        :param y: Y position of the explosion.
        """

        self.x = x
        self.y = y
        self.particles = []
        self.particle_count = particle_count
        self.is_dead = False

        # Create the particles.
        for _ in range(self.particle_count):
            self.particles.append(Particle(self.x, self.y, tools.random_angle(), random.randint(1, 5),
                                           tools.random_color_from_range((255, 0, 0), (255, 255, 0)),
                                           3, "circle", None, True, random.uniform(0.1, 0.8), (0, 0, 0), True, True))

    def update(self) -> None:
        """
        Update the explosion.
        :return: None
        """
        # Update and remove dead particles.
        for particle in self.particles:
            particle.update()
            if particle.is_dead:
                self.particles.remove(particle)

        if len(self.particles) == 0:
            self.is_dead = True

    def draw(self, screen=constants.SCREEN) -> None:
        """
        Draw the explosion.
        :return: None
        """
        for particle in self.particles:
            particle.draw(screen)



class BombTimeoutExplosion:
    def __init__(self, x: int, y: int, particle_count: int = 20) -> None:
        """
        :param x:
        :param y:
        :param particle_count:
        """

        self.x = x
        self.y = y
        self.particles = []
        self.particle_count = particle_count
        self.is_dead = False

        # Create particles
        for _ in range(self.particle_count):
            self.particles.append(Particle(self.x, self.y, tools.random_angle(), random.randint(1, 5),
                                           tools.random_color_from_range((255, 255, 255), (150, 150, 150), to_grayscale=True),
                                           random.randint(2, 5), "square", None, True, random.uniform(0.2, 1), (0, 0, 0), True, True))

    def update(self) -> None:
        """
        Updates the explosion.
        :return:
        """
        # Update and remove dead particles.
        for particle in self.particles:
            particle.update()
            if particle.is_dead:
                self.particles.remove(particle)

        if len(self.particles) == 0:
            self.is_dead = True

    def draw(self, screen=constants.SCREEN) -> None:
        """
        Draw the explosion.
        :return: None
        """
        for particle in self.particles:
            particle.draw(screen)



class ConfettiExplosion:
    def __init__(self, x: int, y: int, particle_count: int = 20) -> None:
        """
        Confetti
        :param x:
        :param y:
        :param particle_count:
        """


        self.x = x
        self.y = y
        self.particles = []
        self.particle_count = particle_count
        self.is_dead = False

        # Create particles
        for _ in range(self.particle_count):
            self.particles.append(Particle(self.x, self.y, tools.random_angle(), random.randint(1, 5),
                                           tools.random_vibrant_rgb(), random.randint(2, 5), "both",
                                           None, True, random.uniform(0.2, 1), (0, 0, 0), True, True))

    def update(self) -> None:
        """
        Updates the explosion.
        :return:
        """
        # Update and remove dead particles.
        for particle in self.particles:
            particle.update()
            if particle.is_dead:
                self.particles.remove(particle)

        if len(self.particles) == 0:
            self.is_dead = True

    def draw(self, screen=constants.SCREEN) -> None:
        """
        Draw the explosion.
        :return: None
        :param screen: Pygame screen object
        """
        for particle in self.particles:
            particle.draw(screen)