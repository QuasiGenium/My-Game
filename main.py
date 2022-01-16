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
player_image = load_image('testhero.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def move(self, ke):
        if ke == 'w' or ke == 'ц':
            self.pos_y -= 5
        elif ke == 's' or ke == 'ы':
            self.pos_y += 5
        elif ke == 'd' or ke == 'в':
            self.pos_x += 5
        elif ke == 'a' or ke == 'ф':
            self.pos_x -= 5

        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)


def main():
    hero = Player(500, 300)
    run = True
    key = ''
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
                    key = ''
        hero.move(key)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    main()
