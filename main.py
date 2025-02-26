import pygame
import os
import random


class Bird(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.def_bird = pygame.transform.scale(load_image('bird_1.png', -1), (55, 35))
        self.bird_up = pygame.transform.scale(load_image('bird_2.png', -1), (72, 52))
        self.bird_down = pygame.transform.scale(load_image('bird_3.png', -1), (65, 52))

        self.rect = self.def_bird.get_rect()
        self.rect.x = 200
        self.rect.y = 320

        self.count: int = 1
        self.down: int = 0

        self.mask = pygame.mask.from_surface(self.def_bird)
        group.add(self)

    def draw(self, screen):
        screen.blit(self.def_bird, self.rect)

    def check(self, image):
        if 120 <= self.down <= 135:
            self.def_bird = pygame.transform.rotate(image, -60)
            self.rect.y += 5
        elif self.down > 135:
            self.def_bird = pygame.transform.rotate(image, -90)
            self.rect.y += 20
        else:
            self.def_bird = pygame.transform.rotate(image, 30)

        return self.def_bird

    def moving(self, start, jump):
        if start:
            if self.rect.y >= -105:
                self.def_bird = self.check(random.choice([self.bird_up, self.bird_down]))

                if jump:
                    self.rect.y -= 70
                    self.down = 0

                self.rect.y += 15
                self.down += 15
            else:
                main(True)
        else:
            if self.count == 1 and self.rect.y <= 322:
                self.rect.y += 2
            else:
                self.count = 0

            if self.count == 0 and self.rect.y >= 318:
                self.rect.y -= 2
            else:
                self.count = 1


class ForCheckPipes(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.size_pipe_1 = self.size()
        self.pipe_up_1 = pygame.transform.scale(load_image('pipe_1.png', -1), (80, self.size_pipe_1[0]))
        self.pipe_down_1 = pygame.transform.scale(load_image('pipe_2.png', -1), (90, self.size_pipe_1[2]))
        self.rect_up_1 = self.pipe_up_1.get_rect()
        self.rect_up_1.x = 600
        self.rect_up_1.y = 0
        self.rect_down_1 = self.pipe_down_1.get_rect()
        self.rect_down_1.x = 600
        self.rect_down_1.y = self.size_pipe_1[1]

        self.size_pipe_2 = self.size()
        self.pipe_up_2 = pygame.transform.scale(load_image('pipe_1.png', -1), (80, self.size_pipe_2[0]))
        self.pipe_down_2 = pygame.transform.scale(load_image('pipe_2.png', -1), (90, self.size_pipe_2[2]))
        self.rect_up_2 = self.pipe_up_2.get_rect()
        self.rect_up_2.x = 600
        self.rect_up_2.y = 0
        self.rect_down_2 = self.pipe_down_2.get_rect()
        self.rect_down_2.x = 600
        self.rect_down_2.y = self.size_pipe_2[1]

        self.size_pipe_3 = self.size()
        self.pipe_up_3 = pygame.transform.scale(load_image('pipe_1.png', -1), (80, self.size_pipe_3[0]))
        self.pipe_down_3 = pygame.transform.scale(load_image('pipe_2.png', -1), (90, self.size_pipe_3[2]))
        self.rect_up_3 = self.pipe_up_3.get_rect()
        self.rect_up_3.x = 600
        self.rect_up_3.y = 0
        self.rect_down_3 = self.pipe_down_3.get_rect()
        self.rect_down_3.x = 600
        self.rect_down_3.y = self.size_pipe_3[1]

        self.for_check_1_up = ForCheckPipes(self.pipe_up_1, self.rect_up_1)
        self.for_check_1_down = ForCheckPipes(self.pipe_down_1, self.rect_down_1)
        self.for_check_2_up = ForCheckPipes(self.pipe_up_2, self.rect_up_2)
        self.for_check_2_down = ForCheckPipes(self.pipe_down_2, self.rect_down_2)
        self.for_check_3_up = ForCheckPipes(self.pipe_up_3, self.rect_up_3)
        self.for_check_3_down = ForCheckPipes(self.pipe_down_3, self.rect_down_3)

        self.lst_pipes = [(self.pipe_up_1, self.rect_up_1), (self.pipe_down_1, self.rect_down_1)]

        self.count: int = 0
        self.score: int = 0

        group.add(self)

    def size(self) -> (int, int, int):
        random_sizes = random.choice([(300, 450, 150), (200, 350, 250), (350, 500, 100)])

        size_up: int = random_sizes[0]
        y: int = random_sizes[1]
        size_down: int = random_sizes[2]

        return size_up, y, size_down

    def get_pipes(self):
        return [self.for_check_1_up, self.for_check_1_down, self.for_check_2_up, self.for_check_2_down,
                self.for_check_3_up,
                self.for_check_3_down]

    def get_score(self):
        return self.score

    def draw(self, screen):
        for im, rect in self.lst_pipes:
            screen.blit(im, rect)

    def moving(self):
        if self.rect_up_1.x <= 350 and self.count == 0:
            self.rect_up_2.x = 600
            self.rect_down_2.x = 600
            self.lst_pipes.append((self.pipe_up_2, self.rect_up_2))
            self.lst_pipes.append((self.pipe_down_2, self.rect_down_2))
            self.count: int = 1
        if self.rect_up_2.x <= 350 and self.count == 1:
            self.rect_up_3.x = 600
            self.rect_down_3.x = 600
            self.lst_pipes.append((self.pipe_up_3, self.rect_up_3))
            self.lst_pipes.append((self.pipe_down_3, self.rect_down_3))
            self.count: int = 2
        if self.rect_up_3.x <= 350 and self.count == 2:
            self.rect_up_1.x = 600
            self.rect_down_1.x = 600
            self.lst_pipes.append((self.pipe_up_1, self.rect_up_1))
            self.lst_pipes.append((self.pipe_down_1, self.rect_down_1))
            self.count: int = 0

        if self.rect_up_1.x == 250:
            self.score += 1
        if self.rect_up_2.x == 250:
            self.score += 1
        if self.rect_up_3.x == 250:
            self.score += 1
        with open('score', mode='w', encoding='utf-8') as f:
            f.write(str(self.score))

        if len(self.lst_pipes) > 6:
            self.lst_pipes = self.lst_pipes[2:]

        for im, rect in self.lst_pipes:
            rect.x -= 10


class ForCheckRoads(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)


class Road(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()

        self.road = pygame.transform.scale(load_image('road.png'), (570, 110))

        self.rect_road_1 = self.road.get_rect()
        self.rect_road_1.x = 0
        self.rect_road_1.y = 600

        self.rect_road_2 = self.road.get_rect()
        self.rect_road_2.x = 550
        self.rect_road_2.y = 600

        self.for_check_1 = ForCheckRoads(self.road, self.rect_road_1)
        self.for_check_2 = ForCheckRoads(self.road, self.rect_road_2)

        self.list_roads = [(self.road, self.rect_road_1), (self.road, self.rect_road_2)]

        group.add(self)

    def get_roads(self):
        return [self.for_check_1, self.for_check_2]

    def draw(self, screen) -> None:
        for im, rect in self.list_roads:
            screen.blit(im, rect)

    def moving(self) -> None:
        if self.rect_road_1.x <= -550:
            self.rect_road_1.x = 550
        if self.rect_road_2.x <= -550:
            self.rect_road_2.x = 550

        self.rect_road_1.x -= 10
        self.rect_road_2.x -= 10


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def main(end=False):
    pygame.init()

    size: (int, int) = 550, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Flappy Bird')

    bg = load_image('bg.png')
    crop_bg = pygame.transform.scale(bg, (570, 720))

    font_count = pygame.font.Font('flappy-font.ttf', 50)
    font_score = pygame.font.Font('flappy-font.ttf', 35)

    button_rect = pygame.Rect(189, 342, 170, 60)

    all_sprites = pygame.sprite.Group()
    bird = Bird(all_sprites)
    pipe = Pipe(all_sprites)
    road = Road(all_sprites)

    for_once: bool = True

    clock = pygame.time.Clock()

    running: bool = True
    start: bool = False
    jump: bool = False
    restart: bool = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    restart: bool = True
            if event.type == pygame.KEYDOWN:
                start: bool = True
                jump: bool = True

        if not end:
            screen.blit(crop_bg, (-5, -60))

            road.draw(screen)
            road.moving()

            bird.draw(screen)
            bird.moving(start, jump)

            if start:
                pipe.draw(screen)
                pipe.moving()

                pygame.image.save(screen, 'data//screen.png')

                text_count = font_count.render(str(pipe.get_score()), True, 'white')
                screen.blit(text_count, (255, 100))

            for i in road.get_roads():
                if pygame.sprite.collide_mask(bird, i):
                    main(True)
            for i in pipe.get_pipes():
                if pygame.sprite.collide_mask(bird, i):
                    main(True)

            pygame.display.flip()
            jump: bool = False
        else:
            if for_once is True:
                with open('best', mode='a', encoding='utf-8') as file:
                    with open('score', mode='r', encoding='utf-8') as f:
                        score = f.read()
                    file.write(f'{score}\n')
                    for_once: bool = False

            screen.blit(load_image('screen.png'), (0, 0))
            screen.blit(load_image('score.png', -1), (200, 150))
            screen.blit(load_image('restart.png', -1), (187, 340))

            score_show = font_score.render(score, True, 'white')
            screen.blit(score_show, (263, 208))

            with open('best', mode='r', encoding='utf-8') as f:
                best = max(list(map(lambda x: int(x.strip('\n')), f.readlines())))
            best_show = font_score.render(str(best), True, 'white')
            screen.blit(best_show, (263, 273))

            if restart:
                main()

            pygame.display.flip()
        clock.tick(15)
    pygame.quit()


if __name__ == '__main__':
    main()
