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
fps = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
stop_kadr = {'w': 20, 's': 0, 'a': 10, 'd': 30, 'ц': 20, 'ы': 0, 'ф': 10, 'в': 30}


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
                if pygame.Rect((self.pos_x + 90, self.pos_y + 16, 1, 80)).colliderect(i):
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


def main():
    hero = Player(load_image('beg.png'), 10, 8, 500, 300)
    b = Box(150, 150)
    run = True
    key = ''
    p = 0
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
        if key:
            if p == 1:
                hero.animation(key)
                p += 1
            else:
                p += 1
                p %= 6
        hero.move(key)
        screen.fill((0, 0, 0))
        screen.blit(load_image('1611928591_30-p-zadnii-fon-dlya-igri-31.jpg'), (0, 0))
        all_sprites.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)
        boxs_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
