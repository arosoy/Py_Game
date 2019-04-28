import pygame
import os
import random


#
# Функции: Проба

# обработка текстур
def load_image(name, colorkey=None):
    _ = colorkey
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image


# перемещение персонажа с помощью напровления
def turning_step(ay):
    nch = [(-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)]
    return nch[ay]


class Pers(pygame.sprite.Sprite):
    hero = [load_image('pic/igrml_.png'), load_image('pic/igrmz_.png'), load_image('pic/igrmp_.png'),
            load_image('pic/igrms_.png')]
    kast = [load_image('pic/igrml_a.png'), load_image('pic/igrmz_a.png'), load_image('pic/igrmp_a.png'),
            load_image('pic/igrms_a.png')]
    xp_max = 1000
    mp_max = 100

    def __init__(self):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.r = 0
        self.n = 3
        self.xp = Pers.xp_max
        self.mp = Pers.mp_max
        self.image = Pers.hero[3]
        self.rect = self.image.get_rect()
        self.rect.x = size[0] / 2 - self.image.get_width() / 2
        self.rect.y = size[1] / 2 - self.image.get_height() / 2

    def turn(self, n1, r):
        self.r = r
        self.n = n1

    def step(self):
        return

    def shift(self, n1):
        return

    def update(self):

        # self.image = Pers.kast[0]
        if self.r == 0:
            self.image = Pers.hero[self.n].copy()
        elif self.r == 1:
            self.image = Pers.kast[self.n].copy()
        pygame.draw.rect(self.image, (255, 0, 0), (25, 0, 40, 4), 1)
        pygame.draw.rect(self.image, (0, 0, 255), (25, 7, 40, 4), 1)
        self.xp += Pers.xp_max * 0.001
        self.mp += Pers.mp_max * 0.001
        # font = pygame.font.Font(None, 20)
        # text = font.render((str(int(x_pers)) + " " + str(int(y_pers))), 1, (255, 255, 255))
        # self.image.blit(text, (0, 40))
        if self.xp > Pers.xp_max:
            self.xp = Pers.xp_max
        if self.mp > Pers.mp_max:
            self.mp = Pers.mp_max
        pygame.draw.rect(self.image, (255, 0, 0), (25, 0, int(40 * (self.xp / Pers.xp_max)), 4), 0)
        pygame.draw.rect(self.image, (0, 0, 255), (25, 7, int(40 * (self.mp / Pers.mp_max)), 4), 0)

    def damage_to_me(self, d):
        if self.xp >= d:
            self.xp -= d
        else:
            if self.xp >= 0:
                self.xp = 0
        return

    def damage_from_me(self):
        return

    def back_step(self):
        return

    def get_xp(self):
        return self.xp

    def long_attack(self):
        if self.mp >= 20:
            fb = LongRangeAttack(self.n, x_pers, y_pers)
            all_sprites_fire.add(fb)
            self.mp -= 20
            all_sprites.add(fb)
        return


class LongRangeAttack(pygame.sprite.Sprite):
    fireball_pix = [load_image('pic/al.png'), load_image('pic/av.png'), load_image('pic/ap.png'),
                    load_image('pic/an.png'), load_image('pic/boom1.png'), load_image('pic/boom2.png'),
                    load_image('pic/boom3.png')]
    dmg = 50

    def __init__(self, n2, x, y):
        global map_wall
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.n = n2
        self.xp = 1
        self.x = float(x)+0.5
        self.y = float(y)+0.5
        self.speed = 1.5
        self.image = LongRangeAttack.fireball_pix[self.n].copy()
        self.rect = self.image.get_rect()
        # x_, y_ = turning_step(n2)
        self.rect.x = size[0] / 2 - self.image.get_width() / 2
        self.rect.y = size[1] / 2 - self.image.get_height() / 2

    def turn(self, n2, r):
        return

    def step(self):
        global map_wall
        x_, y_ = turning_step(self.n)
        self.x += float(x_)/16.0 * self.speed
        self.y += float(y_)/16.0 * self.speed
        self.rect.x += 96 * float(x_)/16.0 * self.speed
        self.rect.y += 96 * float(y_)/16.0 * self.speed
        if (map_wall[int(self.y)][int(self.x)] >= 1) and (map_wall[int(self.y)][int(self.x)] <= 9):
            return
        else:
            if self.xp == 1:
                self.xp = 0
            self.n = 4

    def shift(self, n4):
        x_, y_ = turning_step(n4)
        self.rect.x -= 96 * float(x_)/16.0
        self.rect.y -= 96 * float(y_)/16.0

    def update(self):
        if self.xp <= 0:
            self.xp -= 1
            if self.xp == -1:
                self.image = LongRangeAttack.fireball_pix[-1].copy()
            elif self.xp == -3:
                self.image = LongRangeAttack.fireball_pix[-2].copy()
            elif self.xp == -5:
                self.image = LongRangeAttack.fireball_pix[-3].copy()
            elif self.xp == -7:
                self.kill()
        # font = pygame.font.Font(None, 20)
        # text = font.render((str(int(self.x)) + " " + str(int(self.y))), 1, (255, 255, 255))
        # self.image.blit(text, (0, 0))
        return

    def damage_to_me(self, d):
        if self.xp == 1:
            self.xp = 0 + d - d
        return

    @staticmethod
    def damage_from_me():
        return random.randint(int(LongRangeAttack.dmg * 0.9), int(LongRangeAttack.dmg * 1.1))

    def back_step(self):
        return


class Monsters(pygame.sprite.Sprite):
    gobl_pix = [load_image('pic/gl.png'), load_image('pic/gz.png'), load_image('pic/gp.png'), load_image('pic/gs.png'),
                load_image('pic/gm2.png'), load_image('pic/gm1.png')]
    xp_max = 700
    dmg = 10

    def __init__(self, n5, x, y):
        global map_wall, x_pers, y_pers
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.re = 0
        self.n = n5
        self.need_turn = 0
        self.x = float(x) + 0.5
        self.y = float(y) + 0.5
        self.speed = 1.0
        self.xp_max = random.randint(int(Monsters.xp_max*0.8), int(Monsters.xp_max*1.2))
        self.dmg = random.randint(int(Monsters.dmg * 0.8), int(Monsters.dmg * 1.2))
        self.xp = self.xp_max
        self.skeep_step = 0
        self.image = Monsters.gobl_pix[self.n]
        self.rect = self.image.get_rect()
        # x_, y_ = turning_step(n5)
        self.old_gx = self.rect.x = size[0] / 2 - self.image.get_width() / 2 - (x_pers-x)*96
        self.old_gy = self.rect.y = size[1] / 2 - self.image.get_height() / 2 - (y_pers-y)*96

    def turn(self, nr, r):
        _ = nr
        _ = r
        self.old_gx = gx = self.rect.x
        self.old_gy = gy = self.rect.y
        _ = gx
        _ = gy
        if self.need_turn == 0:
            if (((x_pers - self.x) < 4) and ((x_pers - self.x) > -4)) and\
                    (((y_pers - self.y) < 4) and ((y_pers - self.y) > -4)):
                n6 = 2
                gx = self.rect.x
                gy = self.rect.y
                x = self.x
                y = self.y
                a1 = x_pers - self.x + 0.5
                b = y_pers - self.y + 0.5
                if a1 < 0 and b < 0:
                    if -a1 > -b:
                        n6 = 0
                    if -a1 < -b:
                        n6 = 1
                    if -a1 == -b:
                        if random.randint(0, 1):
                            n6 = 0
                        else:
                            n6 = 1

                if (a1 < 0) and (b > 0):
                    if -a1 > b:
                        n6 = 0
                    if -a1 < b:
                        n6 = 3
                    if -a1 == b:
                        if random.randint(0, 1):
                            n6 = 0
                        else:
                            n6 = 3
                if a1 > 0 and b > 0:
                    if a1 > b:
                        n6 = 2
                    if a1 < b:
                        n6 = 3
                    if a1 == b:
                        if random.randint(0, 1):
                            n6 = 2
                        else:
                            n6 = 3

                if (a1 > 0) and (b < 0):
                    if a1 > -b:
                        n6 = 2
                    if a1 < -b:
                        n6 = 1
                    if a1 == -b:
                        if random.randint(0, 1):
                            n6 = 2
                        else:
                            n6 = 1

                if a1 > 0 and b == 0:
                    n6 = 2
                if a1 < 0 and b == 0:
                    n6 = 0
                if a1 == 0 and b < 0:
                    n6 = 1
                if a1 == 0 and b > 0:
                    n6 = 3
                x_01, y_01 = turning_step(n6)
                self.rect.x += float(x_01) * 96
                self.rect.y += float(y_01) * 96
                x += float(x_01)
                y += float(y_01)
                if map_wall[int(y)][int(x)] == 1:
                    # blocks_hit_list = pygame.sprite.spritecollide(self, all_sprites_monsters, False)
                    # if len(blocks_hit_list) <= 1:
                    if 1:
                        if self.n != n6:
                            self.n = n6
                            self.skeep_step = 16
                        else:
                            self.skeep_step = 16
                        self.need_turn = 16
                        self.image = Monsters.gobl_pix[self.n]
                        return
                self.rect.x = gx
                self.rect.y = gy
            else:

                spisok = [0, 1, 2, 3]
                self.old_gx = gx = self.rect.x
                self.old_gy = gy = self.rect.y
                for i1 in range(4):
                    x = self.x
                    y = self.y
                    self.rect.x = gx
                    self.rect.y = gy
                    rand = random.randint(0, 3 - i1)
                    k = spisok[rand]
                    x_01, y_01 = turning_step(k)
                    self.rect.x += float(x_01) * 96
                    self.rect.y += float(y_01) * 96
                    x += float(x_01)
                    y += float(y_01)
                    if map_wall[int(y)][int(x)] == 1:
                        blocks_hit_list1 = pygame.sprite.spritecollide(self, all_sprites_monsters, False)
                        if len(blocks_hit_list1) <= 1:
                            self.n = k
                            self.need_turn = random.randint(32, 160)
                            self.image = Monsters.gobl_pix[self.n]
                            self.skeep_step = 16
                            return
                    spisok.remove(k)
                self.rect.x = gx
                self.rect.y = gy

    def step(self):
        global person
        if self.xp > 0:
            if self.skeep_step != 0:
                self.skeep_step -= 1
                return
            global map_wall
            if self.need_turn != 0:
                x_, y_ = turning_step(self.n)
                vx = self.x + float(x_) / 16.0 * self.speed
                vy = self.y + float(y_) / 16.0 * self.speed
                if (map_wall[int(vy)][int(vx)] >= 1) and (map_wall[int(vy)][int(vx)] <= 9):
                    self.need_turn -= 1
                    vx = self.x
                    vy = self.y
                    gx = self.rect.x
                    gy = self.rect.y
                    self.x += float(x_) / 16.0 * self.speed
                    self.y += float(y_) / 16.0 * self.speed
                    self.rect.x = size[0] / 2 - self.image.get_width() / 2 - (x_pers - self.x) * 96 - 48
                    self.rect.y = size[1] / 2 - self.image.get_height() / 2 - (y_pers - self.y) * 96 - 48
                    blocks_hit_list1 = pygame.sprite.spritecollide(self, all_sprites, False)
                    if len(blocks_hit_list1) > 1:
                        for ji in blocks_hit_list1:
                            if ji == person:
                                person.damage_to_me(self.damage_from_me())
                                self.rect.x = gx
                                self.rect.y = gy
                                self.y = vy
                                self.x = vx
                    # self.rect.x += 96 * float(x_) / 16.0 * self.speed
                    # self.rect.y += 96 * float(y_) / 16.0 * self.speed
                else:
                    self.need_turn = 0

    def shift(self, n6):
        x_, y_ = turning_step(n6)
        self.rect.x -= 96 * float(x_) / 16.0
        self.rect.y -= 96 * float(y_) / 16.0

    def update(self):
        global goblin_killed
        if self.xp <= 0:
            self.xp -= 1
            if self.xp == -1:
                self.image = Monsters.gobl_pix[-1].copy()
            elif self.xp == -17:
                self.image = Monsters.gobl_pix[-2].copy()
            elif self.xp == -33:
                goblin_killed += 1
                self.kill()
        else:
            # if self.r == 0:
            self.image = Monsters.gobl_pix[self.n].copy()
            # elif self.r == 1:
            # self.image = Pers.kast[self.n]
            # font = pygame.font.Font(None, 20)
            # text = font.render((str(int(x_pers - self.x))+" " + str(y_pers - self.y)), 1, (255, 255, 255))
            # self.image.blit(text, (0, 0))
            pygame.draw.rect(self.image, (255, 0, 0), (25, 20, 40, 4), 1)
            pygame.draw.rect(self.image, (255, 0, 0), (25, 20, int(40 * (self.xp / self.xp_max)), 4), 0)

    def damage_to_me(self, d):
        if self.xp >= d:
            self.xp -= d
        else:
            if self.xp >= 0:
                self.xp = 0
        return

    def damage_from_me(self):
        return random.randint(int(self.dmg * 0.9), int(self.dmg * 1.1))

    def back_step(self):
        self.rect.x = self.old_gx
        self.rect.y = self.old_gy


class Key(pygame.sprite.Sprite):
    pix = [load_image('pic/key0.png'), load_image('pic/key01.png'), load_image('pic/key1.png'),
           load_image('pic/key11.png'), load_image('pic/key2.png'), load_image('pic/key21.png'),
           load_image('pic/key3.png'), load_image('pic/key31.png'), load_image('pic/zast.png'),
           load_image('pic/zast2.png'), load_image('pic/zast3.png')]
    koord = [[168, 140], [216, 960], [216, 265], [236, 360]]

    def __init__(self, n6):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__()
        self.n = n6
        self.image = Key.pix[self.n * 2]
        self.rect = self.image.get_rect()
        self.rect.x = Key.koord[self.n][0]
        self.rect.y = Key.koord[self.n][1]

    def yes(self):
        self.image = Key.pix[self.n * 2 + 1]
        self.rect.x = Key.koord[self.n][0]
        self.rect.y = Key.koord[self.n][1]

    def no(self):
        self.image = Key.pix[self.n * 2]
        self.rect.x = Key.koord[self.n][0]
        self.rect.y = Key.koord[self.n][1]

    def upr(self, n6):
        self.image = Key.pix[n6]
        self.rect.x = 0
        self.rect.y = 0


#


# инициализация pygame:

pygame.init()
# размеры окна:
size = width, height = 672, 672
# screen — холст, на котором нужно рисовать:

screen = pygame.display.set_mode(size)
background = pygame.Surface((864, 864))

#


# создаю переменные

game_mode = 'start'
map_pic = []
map_wall = []
pix_map = [load_image('pic/1.png'), load_image('pic/2.png'), load_image('pic/3.png'), load_image('pic/4.png'),
           load_image('pic/5.png'), load_image('pic/6.png'), load_image('pic/7.png'), load_image('pic/8.png'),
           load_image('pic/9.png'), load_image('pic/10.png'), load_image('pic/11.png'), load_image('pic/12.png'),
           load_image('pic/13.png'), load_image('pic/14.png'), load_image('pic/15.png'), load_image('pic/16.png'),
           load_image('pic/17.png'), load_image('pic/18.png'), load_image('pic/19.png'), load_image('pic/20.png'),
           load_image('pic/21.png'), load_image('pic/22.png'), load_image('pic/23.png'), load_image('pic/24.png'),
           load_image('pic/25.png'), load_image('pic/26.png'), load_image('pic/27.png'), load_image('pic/28.png'),
           load_image('pic/29.png'), load_image('pic/30.png'), load_image('pic/31.png'), load_image('pic/32.png'),
           load_image('pic/33.png'), load_image('pic/34.png')]
x_pers = 27.
y_pers = 206.
x_pers_new = int(27)
y_pers_new = int(206)
x_animate = -96
y_animate = -96
animate = 0
goblin_killed = 0
turning = 3


#


all_sprites = pygame.sprite.Group()
all_sprites_key = pygame.sprite.Group()
all_sprites_monsters = pygame.sprite.Group()
all_sprites_fire = pygame.sprite.Group()
ke = Key(0)
all_sprites_key.add(ke)
for i in range(4):
    ke = Key(i)
    all_sprites_key.add(ke)

person = Pers()
all_sprites.add(person)

# получаю данные из папки

with open('pic/map.txt', 'r') as f:
    for i in range(222):
        a = f.readline()
        map_pic.append(list(map(int, a.split())))
with open('pic/map_gobl.txt', 'r') as f:
    for j in range(222):
        a = f.readline()
        map01 = []
        shyot = -1
        for sad in a.split():
            shyot += 1
            if sad[0] == '#':
                map01.append(0)
            elif sad[0] == '.':
                map01.append(1)
                if len(sad) > 1:
                    for df in sad.split('.'):
                        if len(df) > 0 and df[0] == 'g':
                            for _ in range(int(df[1:])):
                                gob = Monsters(2, shyot, j)
                                all_sprites.add(gob)
                                all_sprites_monsters.add(gob)
        map_wall.append(map01)

clock = pygame.time.Clock()
running = True

#
sost_klav = 2
znach = 0
kast_anim = 0
upr = 0
upr2 = 0

# игровой цикл
key = 0
while running:
    # приема и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        #

        # обработка нажатий клавишь
        if event.type == pygame.KEYDOWN and game_mode == 'game' and key == 0:
            if event.key == pygame.K_LEFT:
                key = 1
                turning = 0
                person.turn(turning, 0)
                kast_anim = 0
            elif event.key == pygame.K_RIGHT:
                key = 1
                turning = 2
                person.turn(turning, 0)
                kast_anim = 0
            elif event.key == pygame.K_UP:
                key = 1
                turning = 1
                person.turn(turning, 0)
                kast_anim = 0
            elif event.key == pygame.K_DOWN:
                key = 1
                turning = 3
                person.turn(turning, 0)
                kast_anim = 0
            elif event.key == pygame.K_SPACE:
                key = 1
                kast_anim += 1
                if kast_anim == 2:
                    person.turn(turning, 0)
                    person.long_attack()
                    kast_anim = 0
                else:
                    person.turn(turning, 1)

            # _ шаг персонажа
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                key = 2
                x_0, y_0 = turning_step(turning)
                kast_anim = 0
                if map_wall[y_pers_new + y_0][x_pers_new + x_0] == 1:
                    y_pers_new += y_0
                    x_pers_new += x_0
            if kast_anim == 0:
                person.turn(turning, 0)
        elif event.type == pygame.KEYDOWN and game_mode == 'start':
            if event.key == pygame.K_UP:
                if sost_klav > 2:
                    if sost_klav == 4:
                        sost_klav = 3
                    sost_klav -= 1
            elif event.key == pygame.K_DOWN:
                if sost_klav < 5:
                    if sost_klav == 2:
                        sost_klav = 4
                    else:
                        sost_klav += 1
            elif event.key == 13:
                znach = 1
        elif event.type == pygame.KEYDOWN and game_mode == 'upr':
            if event.key == 27:
                upr = 1
        elif event.type == pygame.KEYDOWN and game_mode == 'upr2':
            if event.key == 27:
                upr2 = 1
    clock.tick(10)
    # отчистка экрана
    # screen.fill((0, 0, 0))
    if game_mode == 'game':
        if key != 0:
            for j in all_sprites_monsters:
                j.turn(0, 0)
            for j in all_sprites_monsters:
                j.back_step()
            # for j in all_sprites:
                # j.update()
        #

        # отрисовка текстур окружающий среды

            for i in range(9):
                for j in range(9):
                    n = map_pic[int(y_pers) + i - 4][int(x_pers) + j - 4] - 1
                    background.blit(pix_map[n], (j * 96, i * 96))
            # отрисовка текстур персонажа

            for i in range(16):

                for spfr in all_sprites_fire:
                    blocks_hit_list = pygame.sprite.spritecollide(spfr, all_sprites_monsters, False)
                    for spm in blocks_hit_list:
                        spm.damage_to_me(spfr.damage_from_me())
                    if len(blocks_hit_list) > 0:
                        spfr.damage_to_me(1)
                clock.tick(100)
                for j in all_sprites:
                    j.step()
                    if key == 2 and (x_pers_new != x_pers or y_pers_new != y_pers):
                        j.shift(turning)
                    j.update()
                if y_pers > float(y_pers_new):
                    y_pers -= 1/16
                    screen.blit(background, (-96, -96 + (i+1) * 6))
                    all_sprites.draw(screen)
                    pygame.display.flip()
                elif y_pers < float(y_pers_new):
                    y_pers += 1 / 16
                    screen.blit(background, (-96, -96 - (i+1) * 6))
                    all_sprites.draw(screen)
                    pygame.display.flip()
                elif x_pers > float(x_pers_new):
                    x_pers -= 1 / 16
                    screen.blit(background, (-96 + (i+1) * 6, -96))
                    all_sprites.draw(screen)
                    pygame.display.flip()
                elif x_pers < float(x_pers_new):
                    x_pers += 1 / 16
                    screen.blit(background, (-96 - (i+1) * 6, -96))
                    all_sprites.draw(screen)
                    pygame.display.flip()
                else:
                    screen.blit(background, (-96, -96))
                    all_sprites.draw(screen)
                    pygame.display.flip()
            # else:
                #
                #
                # print(1)
                #

        # screen.blit(hero[turning], (3 * 96, 3 * 96))

        #

        # отрисовка картинки на экран
            key = 0
            x_pers = float(x_pers_new)
            y_pers = float(y_pers_new)
        if person.get_xp() <= 0:
            exit(0)
    elif game_mode == 'start':
        a = 0
        for i in all_sprites_key:
            a += 1
            i.no()
            if a == sost_klav:
                i.yes()
            if a == 1:
                i.upr(8)
        if sost_klav == 2 and znach == 1:
            game_mode = 'game'
            key = 1
        if sost_klav == 3 and znach == 1:
            game_mode = 'upr2'
        if sost_klav == 4 and znach == 1:
            game_mode = 'upr'
        if sost_klav == 5 and znach == 1:
            exit(0)
        znach = 0
        all_sprites_key.draw(screen)
        pygame.display.flip()
    elif game_mode == 'upr':
        for i in all_sprites_key:
            a = 0
        i.upr(9)
        if upr:
            game_mode = 'start'
            upr = 0
        all_sprites_key.draw(screen)
        pygame.display.flip()
    elif game_mode == 'upr2':
        for i in all_sprites_key:
            a = 0
        i.upr(10)
        if upr2:
            game_mode = 'start'
            upr2 = 0
        all_sprites_key.draw(screen)
        pygame.display.flip()
