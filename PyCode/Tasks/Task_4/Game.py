import pygame
import random


class Const:
    SIDE_SIZE = 600
    WINDOW_SIZE = [SIDE_SIZE] * 2
    BACKGROUND_COLOR = (1, 1, 1)
    AMOUNT_CELL = 20
    SIZE_CELL = SIDE_SIZE // AMOUNT_CELL


class Obj:
    def __init__(self, pos, size):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.x = pos[0] * Const.SIZE_CELL
        self.rect.y = pos[1] * Const.SIZE_CELL
        self.background_color = Const.BACKGROUND_COLOR
        self.figure_color = self.background_color

    def get_surface(self):
        self.update_surface()
        self.draw()
        return self.surface

    def get_rect(self):
        return self.rect

    def update_surface(self):
        self.surface.fill(self.background_color)

    def move(self):
        pass

    def draw(self):
        pass

    def is_collide(self, game_obj):
        return self.rect.colliderect(game_obj.get_rect())


class Apple(Obj):
    def __init__(self, pos, size):
        super(Apple, self).__init__(pos, size)
        self.figure_color = (255, 0, 0)

    def move(self):
        self.rect.x = Const.SIZE_CELL * random.randint(0, Const.AMOUNT_CELL - 1)
        self.rect.y = Const.SIZE_CELL * random.randint(0, Const.AMOUNT_CELL - 1)

    def draw(self):
        pygame.draw.circle(self.surface, self.figure_color, [i // 2 for i in self.rect.size], min(self.rect.size) // 3)


class PartSnake(Obj):
    def __init__(self, pos, size):
        super(PartSnake, self).__init__(pos, size)
        self.figure_color = (0, 255, 0)
        self.indent = 3

        self.direction = [-Const.SIZE_CELL, 0]

    def move(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

    def draw(self):
        pygame.draw.rect(self.surface, self.figure_color,
                         (self.indent, self.indent, self.rect.size[0] - self.indent, self.rect.size[1] - self.indent))


class Map:
    def __init__(self, size_window):
        self.size_map = [Const.AMOUNT_CELL] * 2
        self.screen_map = pygame.display.set_mode(size_window)

        self.apple = Apple((Const.AMOUNT_CELL // 2, Const.AMOUNT_CELL // 2), (Const.SIZE_CELL, Const.SIZE_CELL))
        self.snake = [
            PartSnake((Const.AMOUNT_CELL // 2 + i, Const.AMOUNT_CELL // 2), (Const.SIZE_CELL, Const.SIZE_CELL))
            for i in range(8)]

        self.map_background_color = Const.BACKGROUND_COLOR

        self.score = 0
        self.font = pygame.font.SysFont('arial', 36)
        self.text_score = self.font.render(str(self.score), True, (255, 215, 0))

    def game_tact(self):
        self.__drawing()
        self.__event()
        self.__moving()

    def __event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake[0].direction != [Const.SIZE_CELL, 0]:
                    self.snake[0].direction = [-Const.SIZE_CELL, 0]
                    break
                elif event.key == pygame.K_RIGHT and self.snake[0].direction != [-Const.SIZE_CELL, 0]:
                    self.snake[0].direction = [Const.SIZE_CELL, 0]
                    break
                elif event.key == pygame.K_DOWN and self.snake[0].direction != [0, -Const.SIZE_CELL]:
                    self.snake[0].direction = [0, Const.SIZE_CELL]
                    break
                elif event.key == pygame.K_UP and self.snake[0].direction != [0, Const.SIZE_CELL]:
                    self.snake[0].direction = [0, -Const.SIZE_CELL]
                    break

    def __moving(self):
        pos_new_part_snake = [i // Const.SIZE_CELL for i in self.snake[-1].rect.topleft]
        direction_new_part_snake = self.snake[-1].direction
        [part.move() for part in self.snake]
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i].direction = self.snake[i - 1].direction

        if self.snake[0].rect.colliderect(self.apple):
            new_part_snake = PartSnake(pos_new_part_snake, (Const.SIZE_CELL, Const.SIZE_CELL))
            new_part_snake.direction = direction_new_part_snake
            self.snake.append(new_part_snake)
            self.score += 1
            self.text_score = self.font.render(str(self.score), True, (255, 215, 0))

        while -1 != self.apple.get_rect().collidelist(self.__get_rect_snake()):
            self.apple.move()

        if not (0 <= self.snake[0].rect.x <= Const.WINDOW_SIZE[0] - Const.SIZE_CELL
                and 0 <= self.snake[0].rect.y <= Const.WINDOW_SIZE[1] - Const.SIZE_CELL) \
                or -1 != self.snake[0].get_rect().collidelist(self.__get_rect_snake()[1:]):
            while True:
                self.screen_map.fill(self.map_background_color)
                font = pygame.font.SysFont('arial', 90)
                text_render = font.render("GAME OVER", True, (255, 215, 0))
                self.screen_map.blit(text_render, (
                (Const.SIDE_SIZE - text_render.get_rect().w) // 2, (Const.SIDE_SIZE - text_render.get_rect().h) // 2))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    def __drawing(self):
        self.screen_map.fill(self.map_background_color)
        self.screen_map.blit(self.apple.get_surface(), self.apple.get_rect())
        [self.screen_map.blit(part_snake.get_surface(), part_snake.get_rect()) for part_snake in self.snake]

        self.screen_map.blit(self.text_score, (15, 5))

    def __get_rect_snake(self):
        return [i.get_rect() for i in self.snake]


class MainGame:
    def __init__(self, size_window):
        pygame.init()
        pygame.font.init()
        self.map = Map(size_window)

    def loop(self, fps):
        clock = pygame.time.Clock()

        while True:
            self.map.game_tact()

            clock.tick(fps)
            pygame.display.flip()


if __name__ == '__main__':
    MainGame(Const.WINDOW_SIZE).loop(5)
