import pygame
from pygame.locals import *
import random
import time
import os
import pygame.freetype

pygame.init()

pygame.mixer.init()

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREY = (192, 192, 192)
GREY = (96, 96, 96)

colors = [(255, 229, 204),
          (255, 204, 204), 
          (255, 204, 153),
          (255, 153, 153),
          (255, 178, 102),
          (255, 102, 102),
          (255, 153, 51),
          (255, 51, 51),
          (255, 128, 0),
          (255, 0, 0),
          (204, 102, 0),
          (204, 0, 0)]

texts = ["2",
         "4",
         "8",
         "16",
         "32",
         "64",
         "128",
         "256",
         "512",
         "1024",
         "2048",
         "4096"]

'''texts = ["D",
         "D+",
         "C-",
         "C",
         "C+",
         "B-",
         "B",
         "B+",
         "A-",
         "A",
         "A+"]'''

N = 4
SPACE = 10
BLOCK_SIZE = 100
FONT_SIZE = 20
TOP_ROW = 0
SCREEN_WIDTH = N * BLOCK_SIZE + (N + 1) * SPACE
SCREEN_HEIGHT = SCREEN_WIDTH + TOP_ROW

locs = []
for i in range(N):
    tmp = []
    for j in range(N):
        tmp.append((SPACE + j * (SPACE + BLOCK_SIZE), SPACE + i * (SPACE + BLOCK_SIZE)))
    locs.append(tmp)

#print(locs)

surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))

class Board(pygame.sprite.Sprite):

    class Block(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.lvl = 0

        def combine(self, other):
            if self.lvl == other.lvl:
                other.lvl += 1
                return True
            return False

    def __init__(self):
        super().__init__()
        self.blocks = [[None for i in range(N)] for j in range(N)]

    def add(self):
        lst = []
        for i in range(N):
            for j in range(N):
                if self.blocks[i][j] is None:
                    lst.append(i * N + j)
        if lst != []:
            k = lst[random.randint(0, len(lst) - 1)]
            self.blocks[k // N][k % N] = self.Block()
            return True
        else:
            return False

    def update(self, pressed_keys):
        flag1 = False
        flag2 = True
        if pressed_keys[K_LEFT]:
            for i in range(N):
                for j in range(1, N):
                    if self.blocks[i][j] == None:
                        flag2 = False
                        continue
                    else:
                        k = j
                        while k > 0:
                            if self.blocks[i][k - 1] == None:
                                self.blocks[i][k - 1] = self.blocks[i][k]
                                self.blocks[i][k] = None
                                flag1 = True
                            else:
                                if self.blocks[i][k].lvl == self.blocks[i][k - 1].lvl:
                                    self.blocks[i][k - 1].lvl += 1
                                    self.blocks[i][k] = None
                                    flag1 = True
                                break
                            k -= 1
        elif pressed_keys[K_RIGHT]:
            for i in range(N):
                for j in range(N - 2, -1, -1):
                    if self.blocks[i][j] == None:
                        flag2 = False
                        continue
                    else:
                        k = j
                        while k < N - 1:
                            if self.blocks[i][k + 1] == None:
                                self.blocks[i][k + 1] = self.blocks[i][k]
                                self.blocks[i][k] = None
                                flag1 = True
                            else:
                                if self.blocks[i][k].lvl == self.blocks[i][k + 1].lvl:
                                    self.blocks[i][k + 1].lvl += 1
                                    self.blocks[i][k] = None
                                    flag1 = True
                                break
                            k += 1
        elif pressed_keys[K_UP]:
            for j in range(N):
                for i in range(1, N):
                    if self.blocks[i][j] == None:
                        flag2 = False
                        continue
                    else:
                        k = i
                        while k > 0:
                            if self.blocks[k - 1][j] == None:
                                self.blocks[k - 1][j] = self.blocks[k][j]
                                self.blocks[k][j] = None
                                flag1 = True
                            else:
                                if self.blocks[k][j].lvl == self.blocks[k - 1][j].lvl:
                                    self.blocks[k - 1][j].lvl += 1
                                    self.blocks[k][j] = None
                                    flag1 = True
                                break
                            k -= 1
        elif pressed_keys[K_DOWN]:
            for j in range(N):
                for i in range(N - 2, -1, -1):
                    if self.blocks[i][j] == None:
                        flag2 = False
                        continue
                    else:
                        k = i
                        while k < N - 1:
                            if self.blocks[k + 1][j] == None:
                                self.blocks[k + 1][j] = self.blocks[k][j]
                                self.blocks[k][j] = None
                                flag1 = True
                            else:
                                if self.blocks[k][j].lvl == self.blocks[k + 1][j].lvl:
                                    self.blocks[k + 1][j].lvl += 1
                                    self.blocks[k][j] = None
                                    flag1 = True
                                break
                            k += 1
        return flag1 or flag2

board = Board()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

playing = True

try:
    pygame.mixer.music.load("Soul&Mind.mp3")
except:
    try:
        pygame.mixer.music.load("/Users/zephyr/Desktop/CS/SE/2048/Soul&Mind.mp3")
    except:
        pygame.mixer.music.load("2048/Soul&Mind.mp3")
pygame.mixer.music.play(loops = -1)

running = True

best_idx = 0

while running:

    screen.fill(LIGHT_GREY)

    playing = False

    font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
    text1 = font.render("Press Esc to exit", True, BLACK)
    text2 = font.render("Press any other button to begin", True, BLACK)
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()

    d = 10
    textRect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - d)
    textRect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + d)

    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                playing = False
                running = False
            else:
                playing = True
        elif event.type == QUIT:
            playing = False
            running = False

    board.add()

    while playing:

        screen.fill(LIGHT_GREY)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    playing = False
                    running = False
                else:
                    pressed_keys = pygame.key.get_pressed()
                    if board.update(pressed_keys):
                        if not board.add():
                            playing = False

                            font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
                            text1 = font.render("You lost!", True, BLACK)
                            text2 = font.render("Try again?", True, BLACK)
                        
                            textRect1 = text1.get_rect()
                            textRect2 = text2.get_rect()

                            d = 10
                            textRect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - d)
                            textRect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + d)

                            screen.blit(text1, textRect1)
                            screen.blit(text2, textRect2)
                            pygame.display.update()

            elif event.type == QUIT:
                playing = False
                running = False
            
        for i in range(N):
            for j in range(N):
                if board.blocks[i][j] is not None:
                    lvl = board.blocks[i][j].lvl
                    surf.fill(colors[lvl])
                    screen.blit(surf, locs[i][j])

                    font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
                    text = font.render(texts[lvl], True, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (locs[i][j][0] + BLOCK_SIZE / 2, locs[i][j][1] + BLOCK_SIZE / 2)
                    screen.blit(text, textRect)

                    if lvl > best_idx:
                        best_idx = lvl
                else:
                    surf.fill(GREY)
                    screen.blit(surf, locs[i][j])

        caption = "Best score: " + texts[best_idx]
        pygame.display.set_caption(caption)

        pygame.display.update()

        '''if best_idx == 10:

            playing = False

            font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
            text1 = font.render("You won!", True, BLACK)
            text2 = font.render("Try again?", True, BLACK)
                        
            textRect1 = text1.get_rect()
            textRect2 = text2.get_rect()

            d = 10
            textRect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - d)
            textRect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + d)

            screen.blit(text1, textRect1)
            screen.blit(text2, textRect2)

            pygame.display.update()'''

    for i in range(N):
        for j in range(N):
            board.blocks[i][j] = None
    
pygame.quit()
quit()

#os.system("pyinstaller --onefile 2048_demo.py")