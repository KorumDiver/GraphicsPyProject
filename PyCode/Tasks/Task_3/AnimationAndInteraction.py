import pygame
import random
import math
import numpy as np


class Dot:
    def __init__(self, position, radius):
        self.__position = np.array(position)
        self.__radius = radius

        self.__color = (173, 216, 230)

    def draw(self, screen):
        pygame.draw.circle(screen, self.__color, self.__position, self.__radius)

    def get_pos(self):
        return self.__position

    def get_rad(self):
        return self.__radius


class Tesla:
    def __init__(self, window_size):
        self.__dots = []
        self.color_lightning = (255, 255, 255)
        self.window_size = window_size

    def draw(self, screen):
        d = 8
        if len(self.__dots) != 0:
            for dot_1 in self.__dots:
                for dot_2 in self.__dots:
                    distance = (dot_2.get_pos() - dot_1.get_pos())
                    distance = math.sqrt(distance @ distance)
                    if distance != 0 and distance < dot_1.get_rad() * 10:
                        x_cord = np.linspace(dot_1.get_pos()[0], dot_2.get_pos()[0], int(distance/10))
                        y_cord = np.linspace(dot_1.get_pos()[1], dot_2.get_pos()[1], int(distance/10))

                        cord = [dot_1.get_pos()]
                        for i in range(min(len(x_cord), len(y_cord))-2):
                            cord.append(
                                [int(x_cord[i] + random.randint(-d, d)), int(y_cord[i] + random.randint(-d, d))])
                        cord.append(dot_2.get_pos())
                        for i in range(1, len(cord)):
                            pygame.draw.line(screen, self.color_lightning, cord[i - 1], cord[i])
            [dot.draw(screen) for dot in self.__dots]

    def add_dot(self, dot):
        self.__dots.append(dot)


class MainInteractiveAnimation:
    def __init__(self, window_size):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)

        self.tesla = Tesla(window_size)

    def loop(self, fps):
        clock = pygame.time.Clock()

        while True:
            # Clear window
            self.update_window()
            # Processing events
            self.events()
            # Draw all objects
            self.draw()
            # State change objects
            self.interactions()

            clock.tick(fps)
            pygame.display.flip()

    def draw(self):
        self.tesla.draw(self.screen)

    def interactions(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.tesla.add_dot(Dot(event.pos, random.randint(5, 15)))

    def update_window(self):
        self.screen.fill((0, 0, 0))


if __name__ == '__main__':
    MainInteractiveAnimation((800, 600)).loop(60)
