import os
import sys
import pygame

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = pygame.display.Info().current_w 
        self.height = pygame.display.Info().current_h
        self.size = (self.width, self.height)
        self.fps = 60
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

if __name__ == '__main__':
    # Определение переменных
    START_BACKGROUND = 'start_background.png'
    END_BACKGROUND = 'end_background.png'
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    SYMB_FOR_FIRE_IN_LEVEL_FILE = 'F'
    DCT_FOR_MOVING_PLAYER = {pygame.K_w: 2, pygame.K_a: 1, pygame.K_d: 0}
    GAME_BACKGROUND = 'game_background.png'

    main = Main()