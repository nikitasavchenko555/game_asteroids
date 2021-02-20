import pygame
import sys
import random

fpsClock = pygame.time.Clock()


def init_window():
    # Инициализируем pygame
    pygame.init()
    # Создаём игровое окно
    window = pygame.display.set_mode((1500, 800))
    # Ставим свой заголовок окна
    pygame.display.set_caption('Астероиды')
    return window


def draw_background():
    # Получаем поверхность, на которой будем рисовать
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    return background


class Fire(pygame.sprite.Sprite):
    def __init__(self, cX, cY):
        pygame.sprite.Sprite.__init__(self)
        #screen = pygame.display.get_surface()
        #self.rect = screen.get_rect()
        self.image = pygame.Surface((60, 60))
        self.rect = self.image.get_rect()
        self.image.fill((0, 255, 255))
        self.rect.x = cX
        self.rect.y = cY

    def update(self):
        if self.rect.x < 1500:
            self.rect.x += 10
        else:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, cX, cY):
        pygame.sprite.Sprite.__init__(self)
        #screen = pygame.display.get_surface()
        self.image = pygame.Surface((60, 60))
        self.rect = self.image.get_rect()
        self.image.fill((255, 255, 1))
        self.rect.x = cX
        self.rect.y = cY

    def update(self):
        if self.rect.x >= 0:
            self.rect.x -= 5
        elif self.rect.x < 0:
            self.kill()
    # print(self.rect, self.rect.x)


class NLO(pygame.sprite.Sprite):
    def __init__(self, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        #screen = pygame.display.get_surface()
        self.image = pygame.Surface((200, 100))
        self.rect = self.image.get_rect()
        self.image.fill((0, 10, 255))
        # Перемещаем картинку в её начальные координаты
        self.rect.x = 0
        self.rect.y = 400

    def update(self, change_coor):
        self.rect.y = self.rect.y + change_coor
        if self.rect.y > 720:
            self.rect.y = 720

        elif self.rect.y < 0:
            self.rect.y = 0
        # print(self.rect.y)


def action():
    screen = pygame.display.get_surface()
    #print(screen.get_rect())
    nlo = NLO(0, 400)
    fire_bols = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    pygame.display.flip()
    while 1:
        fpsClock.tick(60)
        for event in pygame.event.get():
            # print('count asteroids {}'.format(len(asteroids)))
            # print('count fires {}'.format(len(fire_bols)))
            if len(asteroids) <= 10:
                asteroids.add(Asteroid(1500, random.randint(50, 720)))
            elif len(asteroids) > 10:
                asteroids.remove()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    nlo.update(-40)
                elif event.key == pygame.K_DOWN:
                    nlo.update(40)
                if event.key == pygame.K_SPACE:
                    fire_bols.add(Fire(200, nlo.rect.y))
            pygame.display.flip()
            dict_group_col = pygame.sprite.groupcollide(fire_bols, asteroids, True, True)
            print(dict_group_col)
        fire_bols.update()
        asteroids.update()
        screen.fill((0, 0, 0))
        screen.blit(nlo.image, nlo.rect)
        fire_bols.draw(screen)
        asteroids.draw(screen)
        # pygame.draw.rect(screen, (0, 10, 255), nlo, 0)
        pygame.display.flip()


def main():
    init_window()
    draw_background()
    action()


if __name__ == '__main__':
    main()
