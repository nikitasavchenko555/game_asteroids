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
score=10
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
#скорость перемещения
speed_int = 0

fpsClock = pygame.time.Clock()
     
def init_window():
    # Инициализируем pygame
    pygame.init()
    # Создаём игровое окно 
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

def input(events, check_dist):
    global x_coord, y_coord, x_speed, y_speed, life, f_speed_x, fai_true
    # Перехватываем нажатия клавиш на клавиатуре
    #speed_int = 0 
    #print("зашли в функцию перехвата")
    #print(events)
    for event in events:
        print("зашли в цикл функции перехвата")
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость НЛО
        # чтобы оно летело
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN):
            check_dist.append(event)
            speed_nlo(event, check_dist)
        # Когда стрелки не нажаты скорость ставим в ноль
        elif event.type == pygame.KEYUP:
            check_dist.clear()
            speed_nlo(event, check_dist)
            if event.key == pygame.K_LEFT: x_speed=0
            if event.key == pygame.K_RIGHT: x_speed=0
            if event.key == pygame.K_UP: y_speed=0
            if event.key == pygame.K_DOWN: y_speed=0
            speed_int = 0
        elif  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
    
    
def speed_nlo(event, check_dist):
    print("вызов функции изменения скорости")
    global speed_int, x_speed, y_speed
    if len(check_dist) > 0:
        if speed_int <= 10:
            speed_int  = speed_int +1
        elif speed_int > 10:
            speed_int = 0
        print("скорость:", speed_int)
        if event.key == pygame.K_LEFT: 
             x_speed=-(speed_int*2)
        elif event.key == pygame.K_RIGHT: 
             x_speed=(speed_int*2)
        elif event.key == pygame.K_UP: 
             y_speed=-(speed_int*2)
        elif event.key == pygame.K_DOWN: 
             y_speed=(speed_int*2)
    #speed_int = 0

    

def action(bk):
    global x_coord, y_coord, score, shag, go1, go2, go3, f_speed_x, fai_true
    screen = pygame.display.get_surface()
    # Создаём НЛО и астероиды
    nlo = Nlo(1,320) 
    asterow=[]
    air = [] 
    check_dist = []
    air.append(nlo)
    faier_bools = []
    #счетчик пропущенных астероидов
    ast_miss = 0
    #счетчик уничтоженных астероидов
    ast_dest = 0
    #faier_bools.append(fai)
    # Рисуем их
    asteroid = Asteroid(950,random.randint(100,700))
    faier = pygame.sprite.RenderPlain(faier_bools)
    asteroids=pygame.sprite.RenderPlain(asterow)
    nlos = pygame.sprite.RenderPlain(air)
    timer = pygame.time.Clock()
    t_start_ast = 0
    # Запускаем бесконечный цикл
    while 1:
        fpsClock.tick(50)
        input(pygame.event.get(), check_dist)
        asteroid = Asteroid(950,random.randint(100,700))
        #манипуляции для интервального старта астероидов
        #print(timer.tick())
        if timer.tick() >= 15:
           t_start_ast = t_start_ast +1
           #print("tick start", t_start_ast)
           if t_start_ast == 90:
              asterow.append(asteroid)
              #print("+астероид")
              asteroids = pygame.sprite.RenderPlain(asterow)
              t_start_ast = 0
        for a in asterow.copy():
           a.rect.x = a.rect.x - 5
           if a.rect.x < 10:
              asterow.remove(a)
              ast_miss +=1
              #уменьшаем на одну жизнь, если пропущено каждые десять астероидов
              if ast_miss % 10 == 0:
                 score -=1
              asteroids.remove(a)
              asteroids.update()
        #обновляем координаты нло
        nlo.rect.x=x_coord
        nlo.rect.y=y_coord
        ast_del = pygame.sprite.spritecollide(nlo, asteroids, True)
        if  len(ast_del) == 1:
            #ast_del = pygame.sprite.spritecollide(nlo, asteroids, True)
            for ast in ast_del:
                asterow.remove(ast)
                asteroids.remove(ast)
                asteroids.update()
                #print("Кол-во астероидов:",asteroids)
            asteroids.remove(ast_del)
            #print(pygame.sprite.spritecollide(nlo, asteroids, True))
            score  -=1
            #print("-жизнь")
            asteroids.draw(screen)
            nlos.draw(screen) 
            if(score<1):
                break
        if fai_true == True:
            faier = pygame.sprite.RenderPlain(faier_bools)
            fai = Faier(x_coord+10, y_coord)
            faier_bools.append(fai)
        for f in faier.copy():
           f.rect.x = f.rect.x+10
           blocks_fai_list = pygame.sprite.spritecollide(f, asteroids, True)
           #print(blocks_fai_list)
           if blocks_fai_list:
               faier.remove(f)
               faier.update()
               #print(type(blocks_fai_list))
               for a in blocks_fai_list:
                     ast_dest +=1
                     asterow.remove(a)
                     asteroids.update()
                     #print("Кол-во астероидов:",asteroids)
                     print(asteroids)
           #print("Изменение кол-ва файеров {}".format(len(faier)))
           if f.rect.x >= 950:
               faier.remove(f)
               faier.update()
               #print("изменение кол-ва файеров из выхода за границу {}".format(len(faier)))
        # Заново прорисовываем объекты
        screen.blit(bk, (0, 0))
        font = pygame.font.Font("freesansbold.ttf", 18)
        white   = ( 255, 255, 255)
        text_life = font.render("Жизнь: "+str(score),True,white)
        text_miss = font.render("Пропущено:"+str(ast_miss),True,white)
        text_destroy = font.render("Уничтожено:"+str(ast_dest),True,white)
        # Рисуем надпись с жизнями
        faier.update()
        nlos.update()
        asteroids.update()
        asteroids.draw(screen)
        nlos.draw(screen)
        faier.draw(screen)
        screen.blit(text_life, [10,10])
        screen.blit(text_miss, [200,10])
        screen.blit(text_destroy, [400,10])
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