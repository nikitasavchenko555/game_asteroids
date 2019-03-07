import sys, os, pygame, random, time
from pygame.locals import *

# Инициализируем переменные
# Начальное положение НЛО
x_coord=1
y_coord=320
# Начальная скорость НЛО
x_speed=0
y_speed=0
#начальная скорость огня
f_speed_x=0
# Количество жизненной энергии НЛО
score=500
# Переменная-счетчик определяет когда
# астероиды изменяют направление движения
shag=0
# Сдвиги по вертикали для астероидов
go1=0
go2=0
go3=0
#флаг открытия огня
fai_true = False
EnemyList = []
     
def init_window():
    # Инициализируем pygame
    pygame.init()
    # Создаём игровое окно 550*480
    window = pygame.display.set_mode((1000, 800))
    # Ставим свой заголовок окна
    pygame.display.set_caption('Астероиды')

# Функция отображения картинок
def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('C:\Soft\simple_game', name)
    # Загружаем картинку
    image = pygame.image.load(fullname)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
 
def draw_background():
    # Получаем поверхность, на которой будем рисовать
    screen = pygame.display.get_surface()
    # и ее размер
    background = pygame.Surface(screen.get_size()) 
    background = background.convert()
    # или загружаем картинку космоса
    back, back_rect = load_image("back.jpg")
    # и рисуем ее
    screen.blit(back, (0, 0))
    # переключаем буфер экрана
    pygame.display.flip() 
    return back

# Класс описывающий летающие объекты
class Skything(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY
    
    def die():
        global EnemyList
        EnemyList = [enemy for enemy in EnemyList if enemy.rect.x>=1000]

 
# Создаём дочерний класс NLO
class Nlo(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "1.jpg", cX, cY)

# Создаём дочерний класс Asteroid
class Asteroid(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "2_1.png", cX, cY)
# Создаём дочерний класс A
class Faier(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "3.png", cX, cY)

def input(events):
    global x_coord, y_coord, x_speed, y_speed, life, f_speed_x, fai_true
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость НЛО
        # чтобы оно летело
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: x_speed=-1
            if event.key == pygame.K_RIGHT: x_speed=1
            if event.key == pygame.K_UP: y_speed=-1
            if event.key == pygame.K_DOWN: y_speed=1
        # Когда стрелки не нажаты скорость ставим в ноль
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed=0
            if event.key == pygame.K_RIGHT: x_speed=0
            if event.key == pygame.K_UP: y_speed=0
            if event.key == pygame.K_DOWN: y_speed=0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print("открыт огонь")
            fai_true = True
            #f_speed_x=+1
    # Меняем положение НЛО не выходя за рамки окна
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if(x_coord<0): x_coord=0
    if(x_coord>1000): x_coord=1000
    if(y_coord<0): y_coord=0
    if(y_coord>800): y_coord=800

def action(bk):
    global x_coord, y_coord, score, shag, go1, go2, go3, f_speed_x, fai_true
    screen = pygame.display.get_surface()
    # Создаём НЛО и астероиды
    nlo = Nlo(1,320) 
    asteroid = Asteroid(950,random.randint(0,800)) 
    asteroid2 = Asteroid(950,random.randint(0,800)) 
    asteroid3 = Asteroid(950,random.randint(0,800))
    fai = Faier(x_coord, y_coord)
    faier = pygame.sprite.RenderPlain(fai)
    # Добавляем их в три массива
    asterow=[]
    asterow.append(asteroid)
    asterow.append(asteroid2)
    asterow.append(asteroid3)
    air = [] 
    air.append(nlo)
    faier_bools = []
    faier_bools.append(fai)
    # Рисуем их
    faier = pygame.sprite.RenderPlain(faier_bools)
    asteroids=pygame.sprite.RenderPlain(asterow)
    nlos = pygame.sprite.RenderPlain(air)
    
    timer = pygame.time.Clock()
    # Запускаем бесконечный цикл
    while 1:
        # Создаем паузу
        timer.tick(500)
        asteroids.draw(screen)
        #asteroids=pygame.sprite.RenderPlain(asterow)
        # Ждём нажатий клавиатуры
        asteroid = Asteroid(950,random.randint(100,700))
        asterow.append(asteroid)
        print("Кол-во астероидов", len(asterow))
        if len(asterow) < 10:
           asterow.append(asteroid)
           asteroids.draw(screen)
        input(pygame.event.get())
        # Проверяем столкновения
        blocks_hit_list = []
        blocks_hit_list = pygame.sprite.spritecollide(nlo, asteroids, True)
        if fai_true == True:
            fai = Faier(x_coord, y_coord)
            faier_bools.append(fai)
        blocks_fai_list = []
        for f in faier.copy():
           f.rect.x = f.rect.x+5
           blocks_fai_list = pygame.sprite.spritecollide(f, asteroids, True)
           #faier.remove(f)
           print("Изменение кол-ва файеров {}".format(len(faier)))
           print("Изменение кол-ва астероидов {}".format(len(asteroids)))
           if f.rect.x > 1000:
               faier.remove(f)
               faier.update()
               print("изменение кол-ва из выхода за границу {}".format(len(faier)))
        faier = pygame.sprite.RenderPlain(faier_bools)
        faier.update()
        #print(f_speed_x)
        if len(blocks_hit_list) == 1:
            score -=len(blocks_hit_list)
            asteroids.draw(screen)
            nlos.draw(screen)   
            if(score<1):
                break
        # Обновляем координаты НЛО
        nlo.rect.x=x_coord
        nlo.rect.y=y_coord
        # Изменяем положение астероидов
        print(asteroids)
        print(type(asteroids))
        for a in asteroids.copy():
               a.rect.x = a.rect.x-2
               if a.rect.x < 0:
                  for ast in asteroids:
                      print("Изменение кол-ва астероидов из-за выхода за границу, стало {}".format(len(asteroids)))
                      ast.kill()
               if(shag>100):
                  shag=0
                  go1=random.randint(-1,1)
                  a.rect.y += go1
        # Раз в 100 итераций астероиды
        # меняют направление движения
        
            #go2=random.randint(-1,1)
            #go3=random.randint(-1,1) 
        asteroid.rect.y+=go1 
        #asteroid2.rect.y+=go2
        #asteroid3.rect.y+=go3
        shag+=1
        # Заново прорисовываем объекты
        screen.blit(bk, (0, 0))
        font = pygame.font.Font("freesansbold.ttf", 18)
        white    = ( 255, 255, 255)
        text = font.render("Жизнь: "+str(score),True,white)
        # Рисуем надпись с жизнями
        screen.blit(text, [10,10])
        # Обновляем положение объектов
        asteroids.update() 
        #faier.update()
        nlos.update()
        # Обновляем кадр
        asteroids.draw(screen)
        nlos.draw(screen)
        faier.draw(screen)
        pygame.display.flip()
        fai_true = False
    font = pygame.font.Font("freesansbold.ttf", 55)
    finish = """Игра окончена"""
    text_finish = font.render(finish,True,white)
    screen.blit(text_finish, [250,350])
    pygame.display.flip()
    while(len(pygame.event.get()) == 0):
          timer.tick(500)
          input(pygame.event.get())
    pygame.quit()
    sys.exit()
     
def main():
    init_window()
    bk = draw_background()
    action(bk)

main()