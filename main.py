import pygame
import sys
import random
import math

FPS = 120
WIN_WIDTH = 800
WIN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 155)


def if_next_collision(c1, c2):
    return math.sqrt((c1.y + c1.dy - c2.y - c2.dy) ** 2 + (c1.x + c1.dx - c2.x - c2.dx) ** 2) < c1.r + c2.r


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Atom:
    def __init__(self, r, cl=GREEN, virus=False):
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 550)
        self.r = r
        self.color = cl
        if virus:
            self.dy = 0
            self.dx = 0
        else:
            self.dy = random.choice([i for i in range(-3, 0)] + [i for i in range(1, 4)])
            self.dx = random.choice([i for i in range(-3, 0)] + [i for i in range(1, 4)])

    def check_border(self):
        if self.y + self.dy >= WIN_HEIGHT - self.r or self.y + self.dy <= self.r:
            self.dy *= -1
        if self.x + self.dx >= WIN_WIDTH - self.r or self.x + self.dx <= self.r:
            self.dx *= -1


class Molecules:
    def __init__(self, sc_, count=0):
        self.sc = sc_

        # is not used
        self.stop = False

        self.moles = []
        self.big_mole = Atom(60, BLUE, True)

        if count != 0:
            for _ in range(count):
                a = Atom(10)
                if not if_next_collision(a, self.big_mole):
                    if not (True in [if_next_collision(a, ml) for ml in self.moles]):
                        self.moles.append(a)

    def temperature(self):
        t = 0
        for mole in self.moles:
            t += abs(mole.dy) + abs(mole.dx)
        return t

    def do_move(self):
        self.calc_next_pos(self.big_mole, self.moles)
        for i in range(len(self.moles) - 1):
            self.calc_next_pos(self.moles[i], self.moles[i + 1:])

        self.big_mole.check_border()
        self.big_mole.x += self.big_mole.dx
        self.big_mole.y += self.big_mole.dy
        pygame.draw.circle(self.sc, self.big_mole.color, (self.big_mole.x, self.big_mole.y), self.big_mole.r)

        for mole in self.moles:
            mole.check_border()
            mole.x += mole.dx
            mole.y += mole.dy
            pygame.draw.circle(self.sc, mole.color, (mole.x, mole.y), mole.r)

    def calc_next_pos(self, one_mole, mls):
        if not self.stop:
            for mole in mls:
                if if_next_collision(mole, one_mole):
                    if id(one_mole) == id(self.big_mole):
                        one_mole.dx += mole.dx * 0.1
                        one_mole.dy += mole.dy * 0.1

                        mole.dy *= -1
                        mole.dy += one_mole.dy

                        mole.dx *= -1
                        mole.dx += one_mole.dx
                    else:
                        one_mole.dy *= -1
                        one_mole.dx *= -1

                        mole.dy *= -1
                        mole.dx *= -1


#if __name__ == '__main__':
pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Molecules go!")
molls = Molecules(sc, 20)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    sc.fill(BLACK)
    molls.do_move()
    draw_text(sc, str(round(molls.temperature())), 20, int(molls.big_mole.x), int(molls.big_mole.y - 10))
    pygame.display.update()

    clock.tick(FPS)
