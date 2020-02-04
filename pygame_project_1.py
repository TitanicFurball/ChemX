import os
import sys
import pygame
from other_sprites import *
from helping_functions import *
from player import *
from time import sleep


SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 850
SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE = '.'

# загрузка уровня
def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width,
                                      SYMB_FOR_SPARE_PLACE_IN_LEVEl_FILE),
                    level_map))

# Функция, заканчивающая игру
def terminate():
    pygame.quit()
    sys.exit(0)
        
       
class Main:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.fps = FPS
        self.clock = pygame.time.Clock()

        if self.start_screen():
            if self.start_game():
                self.end_screen()
    # Заставка
    def start_screen(self):
        intro_text = ["ЗАСТАВКА", "", "Правила игры", "", "True"]
 
        background = pygame.transform.scale(load_image(START_BACKGROUND),
                                            (self.width, self.height))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
     
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return True
            pygame.display.flip()
            self.clock.tick(10)
            
    # Экран конца игры
    def end_screen(self):
        end_text = ["Конец", 'Вы победили',
                    "Нажмите любую кнопку,", "чтобы выйти"]

        background = pygame.transform.scale(load_image(END_BACKGROUND),
                                            (self.width, self.height))
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 20)
        text_coord = 200
        for line in end_text:
            string_rendered = font.render(line, 1, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                   event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
            pygame.display.flip()
            self.clock.tick(10)

    # Сама игра
    def start_game(self):
        background_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.LayeredUpdates()        
        player_group = pygame.sprite.GroupSingle()
        bullet_group = pygame.sprite.Group() 
        platforms_group = pygame.sprite.Group()
        fire_group = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        save_group = pygame.sprite.Group()
        end_group = pygame.sprite.Group()
        groups_to_update_with_camera = [player_group, platforms_group, 
                                        bullet_group, fire_group, enemy_group, 
                                        save_group, end_group] 
               
        bck = Background(background_group)
        all_sprites.add(bck, layer=-1)

        level = load_level("level5.txt")
        player = checkpoint = start_checkpoint = None
        camera = Camera(groups_to_update_with_camera)
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == SYMB_FOR_PLATFORM_IN_LEVEL_FILE:
                    plt = Platform((x, y), platforms_group)
                    all_sprites.add(plt, layer=0)
                    
                elif level[y][x] == SYMB_FOR_FIRE_IN_LEVEL_FILE:
                    fire = Fire((x, y), fire_group)
                    all_sprites.add(fire, layer=1)
                    
                elif level[y][x] == SYMB_FOR_PLAYER_IN_LEVEL_FILE:
                    start_checkpoint = Checkpoint_Tile((x, y), save_group)
                    player = Player((x, y), player_group)
                    all_sprites.add(player, layer=2)
                    player.groups = player.groups()                
                
                elif level[y][x] == 's':
                    snail = Snail((x, y - 0.70), enemy_group)
                    all_sprites.add(snail, layer=2) 
                    
                elif level[y][x] == 'R':
                    robot = Robot((x, y), enemy_group)
                    all_sprites.add(robot, layer=2)                
                
                elif level[y][x] == 'S':
                    checkpoint = Checkpoint_Tile((x, y), save_group)
                    all_sprites.add(checkpoint, layer=1)

                elif level[y][x] == 'E':
                    end = End_tile((x, y), end_group)
                    all_sprites.add(end, layer=2)

        left, right, up = False, False, False
        actions_list = [left, right, up]
        checkpoint = start_checkpoint
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
             # Сигналы, получаемые от игрока     
                if event.type == pygame.KEYDOWN:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = True
                    elif event.key == pygame.K_SPACE: 
                        player.shoot(bullet_group, all_sprites)                  
            
                if event.type == pygame.KEYUP:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = False
                                   
            for enemy in enemy_group:
                if enemy.image_name != 'robot.png':
                    enemy.move()
                else:
                    enemy.move(bullet_group, all_sprites)
            # Возвращение экрана к дефолту
            self.screen.fill((0, 0, 0))
            camera.update(player)
            for bullet in bullet_group: 
                bullet.update(enemy_group if bullet.flag_to_diff == 'enemy'
                              else player, platforms_group, SCREEN_WIDTH)           
            for end in end_group:
                if end.update(player):
                    sleep(1)
                    return True
            for group in groups_to_update_with_camera:
                for sprite in group:
                    camera.apply(sprite)
            camera.word_r, camera.word_l = False, False
            camera.word_up, camera.word_down = False, False
            checkpoint = player.update(*actions_list, platforms_group,
                                       bullet_group,
                                       [fire_group, enemy_group],
                                       checkpoint, save_group)                
   
            all_sprites.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)


# Фон
class Background(pygame.sprite.Sprite):
    def __init__(self, background_group):
        super().__init__(background_group)
        self.image = pygame.transform.scale(load_image(GAME_BACKGROUND),
                                            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        
# Камера 
class Camera:
    def __init__(self, update_group):
        self.update_group = update_group
        self.dx = SCREEN_WIDTH
        self.dy = SCREEN_HEIGHT
        self.word_r = False
        self.word_l = False
        self.word_up = False
        self.word_down = False

    def apply(self, obj):
        if self.word_r:
            obj.rect.x -= self.dx
        if self.word_l:
            obj.rect.x += self.dx
        if self.word_up:
            obj.rect.y -= self.dy
        if self.word_down:
            obj.rect.y += self.dy      
        
    def update(self, target):
        if target.rect.x >= SCREEN_WIDTH:
            self.word_r = True
        if target.rect.x <= 0:
            self.word_l = True
        if target.rect.y >= SCREEN_HEIGHT:
            self.word_up = True
        if target.rect.y <= 0:
            self.word_down = True
            

if __name__ == '__main__':
    # Определение переменных
    FPS = 60
    START_BACKGROUND = 'start_background.png'
    END_BACKGROUND = 'end_background.png'
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    SYMB_FOR_FIRE_IN_LEVEL_FILE = 'F'
    DCT_FOR_MOVING_PLAYER = {pygame.K_w: 2, pygame.K_a: 1, pygame.K_d: 0}
    GAME_BACKGROUND = 'game_background.png'

    main = Main()