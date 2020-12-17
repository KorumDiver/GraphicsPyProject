import pygame
import random
import numpy as np


class Planet:
    def __init__(self, position, velocity, color, radius):
        self.position = np.array(position, dtype=np.float)
        self.velocity = np.array(velocity, dtype=np.float)
        self.color = color
        self.radius = radius

        self.size_window = pygame.display.get_surface().get_size()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.astype(int), self.radius)

    def move(self):
        self.position += self.velocity
        if self.position[0] > self.size_window[0]:
            self.position[0] = self.position[0] % self.size_window[0]

        if self.position[0] < 0:
            self.position[0] = self.size_window[0] + self.position[0] % self.size_window[0]

        if self.position[1] > self.size_window[1]:
            self.position[1] = self.position[1] % self.size_window[1]

        if self.position[1] < 0:
            self.position[1] = self.size_window[1] + self.position[1] % self.size_window[1]


class Game:
    def __init__(self, size):
        self.size_window = size
        pygame.init()
        self.sc = pygame.display.set_mode(self.size_window)

        # Create game objects
        self.palnets = []
        for _ in range(10):
            self.palnets.append(Planet([random.randint(50, size[0] - 50), random.randint(50, size[1] - 50)],
                                       [0, 0],
                                       self.__random_color(), 10))

    def animation_loop(self, fps):
        clock = pygame.time.Clock()

        while True:
            # Update display
            self.sc.fill((0, 0, 0))

            # Draw all objects
            self.draw()
            # State change objects
            self.interactions()
            # Processing events
            self.events()

            # Delay and update display
            clock.tick(fps)
            pygame.display.flip()

    def draw(self):
        if len(self.palnets) > 0:
            [i.draw(self.sc) for i in self.palnets]

    def interactions(self):
        if len(self.palnets) > 0:
            for planet_1 in self.palnets:
                for planet_2 in self.palnets:
                    v = (planet_2.position - planet_1.position)
                    norm_v = v @ v
                    if norm_v != 0:
                        v = v / norm_v
                        planet_1.velocity += 3 * v
            [i.move() for i in self.palnets]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    @staticmethod
    def __random_color():
        levels = range(32, 256, 32)
        return tuple(random.choice(levels) for _ in range(3))


if __name__ == '__main__':
    Game((800, 600)).animation_loop(60)
