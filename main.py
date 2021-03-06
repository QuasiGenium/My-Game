import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game')
fps = 100
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
stop_kadr = {'w': 20, 's': 0, 'a': 10, 'd': 30, 'ц': 20, 'ы': 0, 'ф': 10, 'в': 30}

rooms = [0, 'Ангар', 'Узкие коридоры', 'Путь к свободе']
level1_iron = [(200, 80), (80, 180), (390, 370), (190, 310), (320, 220), (12 * 50 + 25, 450)]
level1_iron.extend([(560 + i * 54, 120) for i in range(6)])
level1_iron.extend([(570 + i * 54, 180) for i in range(6)])
level1_o = [(150, 150)]
level1_o.extend([(450, (i + 1) * 50) for i in range(6)])
level1_o.extend([((i + 1) * 50, 450) for i in range(11)])
level1_o.extend([((i + 1) * 50, 450) for i in range(13, 22)])
level1_o.extend([(i * 50 + 500, 300) for i in range(9)])

level12_iron = [(490, 679), (330, 120)]
level12_iron.extend([(400, 350 + i * 50) for i in range(5)])
level12_iron.extend([(950 + i * 50, 250) for i in range(4)])
level2_o = []
level2_o.extend([(1100 - i * 50, 600) for i in range(19) if i != 8])
level2_o.extend([(150, 600 - i * 50) for i in range(5)])
level2_o.extend([((i + 1) * 50, 250) for i in range(18)])
level2_o.extend([(i * 50 + 200, 400) for i in range(19) if i != 4])
level2_o.extend([(i * 50 + 650, 550) for i in range(3)])
level2_o.extend([(350, 450 + i * 50) for i in range(2)])
level2_o.extend([(450, 450 + i * 50) for i in range(3)])
level3_iron = [(1000, 650), (1000, 700)]
level3_iron.extend([(618 + i * 50, 350) for i in range(4)])
level3_iron.extend([(640 + i * 50, 400) for i in range(3)])
level3_o = [(397, 89), (799, 168), (1056, 144), (1070, 235), (274, 609), (464, 690), (683, 580)]
level3_o.extend([(150, (i + 1) * 50) for i in range(14) if i != 6 and i != 7])
level3_o.extend([(1000, 300 + i * 50) for i in range(7)])
level3_o.extend([(850, 450 + i * 50) for i in range(6)])
level3_o.extend([(200 + i * 50, 450) for i in range(13) if i != 4 and i != 5])
level3_o.extend([(200 + i * 50, 300) for i in range(19) if i != 6 and i != 5])
level3_o.extend([(400 + i * 50, 250) for i in range(4)])
level3_o.extend([(350 + i * 50, 500) for i in range(4)])

levels = [0, [level1_o, level1_iron, (1000, 630), (50, 50)], [level2_o, level12_iron, (50, 100), (1000, 645)],
          [level3_o, level3_iron, (1300, 350), (50, 350)]]


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.down_ani = self.frames[40:50]
        self.left_ani = self.frames[50:60]
        self.up_ani = self.frames[60:70]
        self.right_ani = self.frames[70:80]
        self.g = {0: self.down_ani, 10: self.left_ani, 20: self.up_ani, 30: self.right_ani}
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(pos_x, pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animation(self, k):
        try:
            self.cur_frame = (self.cur_frame + 1) % len(self.g[stop_kadr[k.lower()]])
            self.image = self.g[stop_kadr[k.lower()]][self.cur_frame]
        except Exception:
            pass

    def stop(self, k):
        if k.lower() in stop_kadr.keys():
            self.image = self.frames[stop_kadr[k.lower()]]

    def move(self, k):
        ke = k.lower()
        if ke == 'w' or ke == 'ц':
            self.pos_y -= 5
            for i in boxs_group:
                if pygame.Rect((self.pos_x + 13, self.pos_y + 10, 70, 1)).colliderect(i):
                    self.pos_y += 5

        elif ke == 's' or ke == 'ы':
            self.pos_y += 5
            for i in boxs_group:
                if pygame.Rect((self.pos_x + 13, self.pos_y + 98, 70, 1)).colliderect(i):
                    self.pos_y -= 5

        elif ke == 'd' or ke == 'в':
            self.pos_x += 5
            for i in boxs_group:
                if pygame.Rect((self.pos_x + 80, self.pos_y + 16, 1, 80)).colliderect(i):
                    self.pos_x -= 5

        elif ke == 'a' or ke == 'ф':
            self.pos_x -= 5
            for i in boxs_group:
                if pygame.Rect((self.pos_x + 6, self.pos_y + 16, 1, 80)).colliderect(i):
                    self.pos_x += 5

        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(boxs_group, all_sprites)
        self.pos_x = x
        self.pos_y = y
        self.image = load_image('box.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


class Portal(Box):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = load_image('portal.png')
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def in_portal(self, m):
        if m.rect.colliderect(self.rect):
            return True
        return False


class Iron_box(Box):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = load_image('iron_box.png')
        self.mag = False
        self.oy = 0
        self.ox = 0

    def magnit(self, m):
        try:
            if m.colliderect(self.rect):
                self.mag = True
                self.oy = m.y
                self.ox = m.x
            else:
                self.mag = False
                self.oy = 0
                self.ox = 0
        except Exception:
            self.mag = False
            self.oy = 0
            self.ox = 0

    def move(self, m):
        if self.mag:
            mox = m.x - self.ox
            moy = m.y - self.oy
            self.oy = 0
            self.ox = 0
            self.pos_x = self.pos_x + mox
            self.pos_y = self.pos_y + moy

            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
            for i in all_sprites:
                if i != self:
                    if self.rect.colliderect(i):
                        self.pos_x = self.pos_x - mox
                        self.pos_y = self.pos_y - moy
                        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
                        break


def image_text(a='', intro_text=[]):
    if a:
        fon = pygame.transform.scale(load_image(a), (width, height))
        screen.blit(fon, (0, 0))
    if intro_text:
        font = pygame.font.Font(None, 30)
        text_coord = 500
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = 730
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def main():
    hero = Player(load_image('beg.png'), 10, 8, 50, 50)
    level = 0
    left = [Box(0, i * 50) for i in range(16)]
    top = [Box((i + 1) * 50, 0) for i in range(23)]
    right = [Box(23 * 50, i * 50) for i in range(16)]
    bottom = [Box((i + 1) * 50, 15 * 50) for i in range(22)]
    other_o = []
    other_iron = []
    portal = Portal(1000, 650)
    run = True
    key = ''
    mouse = False
    p = 0
    mouserect = pygame.Rect((0, 0, 1, 1))
    pere = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key = event.unicode
            if event.type == pygame.KEYUP:
                if event.unicode == key:
                    hero.stop(key)
                    key = ''
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = True
                mouserect.x, mouserect.y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = False
                mouserect.x, mouserect.y = 0, 0
            if event.type == pygame.MOUSEMOTION:
                if mouse:
                    mouserect.x, mouserect.y = event.pos

        if mouse:
            for i in boxs_group:
                try:
                    i.move(mouserect)
                    i.magnit(mouserect)
                except Exception:
                    continue
        else:
            for i in boxs_group:
                try:
                    i.mag = False
                except Exception:
                    continue

        if key:
            if p == 1:
                hero.animation(key)
                p += 1
            else:
                p += 1
                p %= 4
        if portal.in_portal(hero) or level == 0:
            if level == (len(levels) - 1):
                return
            else:
                level += 1
                hero.stop(key)
                key = ''
                hero.pos_x, hero.pos_y = levels[level][3]
                hero.rect = hero.image.get_rect().move(hero.pos_x, hero.pos_y)
                portal.pos_x, portal.pos_y = levels[level][2]
                portal.rect = portal.image.get_rect().move(portal.pos_x, portal.pos_y)
                if len(other_o) < len(levels[level][0]):
                    for i in range(len(levels[level][0]) - len(other_o)):
                        other_o.append(Box(0, -50))
                for i in other_o:
                    i.pos_x = 0
                    i.pos_y = -50
                for i in range(len(levels[level][0])):
                    other_o[i].pos_x, other_o[i].pos_y = levels[level][0][i]
                for i in other_o:
                    i.rect = i.image.get_rect().move(i.pos_x, i.pos_y)

                if len(other_iron) < len(levels[level][1]):
                    for i in range(len(levels[level][1]) - len(other_iron)):
                        other_iron.append(Iron_box(0, -50))
                for i in other_iron:
                    i.pos_x = 0
                    i.pos_y = -50
                for i in range(len(levels[level][1])):
                    other_iron[i].pos_x, other_iron[i].pos_y = levels[level][1][i]
                for i in other_iron:
                    i.rect = i.image.get_rect().move(i.pos_x, i.pos_y)
                if level == 3:
                    for i in range(7, 10):
                        right[i].pos_x += 150
                        right[i].rect = right[i].image.get_rect().move(right[i].pos_x, right[i].pos_y)
                pere = True

        hero.move(key)
        screen.fill((0, 0, 0))
        screen.blit(load_image('fon.jpg'), (0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        if pere:
            image_text('pere.png', [f'Уровень {level}', str(rooms[level])])
        pere = False
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    image_text('start_screen.png')
    image_text('tutorial.png')
    image_text('suget.png')
    main()
    image_text('free.jpg')
    image_text('ending.png')
