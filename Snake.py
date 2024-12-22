import random
from copy import deepcopy

import pygame


class Board:
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.screen = screen
        self.count = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        self.screen.fill((0, 255, 255))
        z = self.cell_size + 1
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                x1 = self.left + x * z
                y1 = self.top + y * z
                if self.board[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x1 + 2, y1 + 2, z - 4, z - 4))
                elif self.board[y][x] == 2:
                    g = (z) / 2
                    pygame.draw.circle(self.screen, (255, 0, 0), (x1 + g, y1 + g), g)
                pygame.draw.rect(self.screen, (255, 255, 255), (x1, y1, z, z), 2)
        pygame.display.flip()


class Snake(Board):
    def __init__(self, screen, w=17, h=15):
        super().__init__(screen, w, h)
        self.body = [(7, 1, (0, 1)), (7, 2, (0, 1)), (7, 3, (0, 1))]
        self.ate = 0
        self.direction = (0, 1)
        self.board[7][1] = 1
        self.board[7][2] = 1
        self.board[7][3] = 1
        self.apple = (7, 11)
        self.board[7][11] = 2
        self.render()
        self.do = False
        self.wait = False

    def change_direction(self, event):
        if not self.wait:
            if event.key == pygame.K_UP and self.direction != (1, 0):
                self.direction = (-1, 0)
                self.do = True
                self.wait = True
            elif event.key == pygame.K_DOWN and self.direction != (-1, 0):
                self.direction = (1, 0)
                self.do = True
                self.wait = True
            elif event.key == pygame.K_LEFT and self.direction != (0, 1):
                self.direction = (0, -1)
                self.do = True
                self.wait = True
            elif event.key == pygame.K_RIGHT and self.direction != (0, -1):
                self.direction = (0, 1)
                self.do = True
                self.wait = True

    def set_board(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                self.board[y][x] = 0
        for i in self.body:
            self.board[i[0]][i[1]] = 1
        self.board[self.apple[0]][self.apple[1]] = 2

    def update(self):
        if self.do:
            if len(self.body) == self.width * self.height:
                return self.end('All field eaten')
            last = (self.body[0][0], self.body[0][1])
            g = self.body[0][2]
            self.body[-1] = (self.body[-1][0], self.body[-1][1], self.direction)
            for i in range(len(self.body)):
                x = self.body[i][0] + self.body[i][2][0]
                y = self.body[i][1] + self.body[i][2][1]
                if i + 1 == len(self.body):
                    d = self.body[i][2]
                else:
                    d = self.body[i + 1][2]
                self.body[i] = (x, y, d)

            i = self.body[-1]
            k = 0
            for f in self.body:
                if (f[0], f[1]) == (i[0], i[1]):
                    k += 1
            if k > 1:
                return self.end('Killed by body')
            if i[0] > self.height - 1 or i[0] < 0 or i[1] > self.width - 1 or i[1] < 0:
                return self.end('Killed by field')

            del i, k, x, y, d
            if (self.body[-1][0], self.body[-1][1]) == self.apple:
                self.body.reverse()
                self.body.append((last[0], last[1], g))
                self.body.reverse()
                t = [(i[0], i[1]) for i in self.body]
                self.apple = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
                while t.__contains__(self.apple):
                    self.apple = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
                self.ate += 1
                del t
            self.set_board()
            self.wait = False
        self.render()  # Баг когда яблоко в черве несъедаемо может уже решено хз я не тестировщик

    def end(self, message):
        """
        Возвращает количество съеденных яблок и то как закончилась игра
        :return:
        """
        return self.ate, message


if __name__ == '__main__':
    # ИСПОЛЬЗОВАНИЕ
    pygame.init()
    screen1 = pygame.display.set_mode((562, 500))
    snake = Snake(screen1)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                snake.change_direction(event)
        a = snake.update()
        if type(a) == tuple:
            run = False
            print(a)
        pygame.time.Clock().tick(5)
