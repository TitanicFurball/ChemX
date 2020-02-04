import os
import sys
import pygame

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        print(message)
        raise SystemExit(message)
    if color_key == -2:
        pass
    elif color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert_alpha()
    else:
        image = image.convert_alpha()
    return image


class Main:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((1000, 600))
        #self.width = pygame.display.Info().current_w 
        #self.height = pygame.display.Info().current_h
        self.size = (self.width, self.height)
        self.fps = 60
        self.clock = pygame.time.Clock()
        
        if self.start_screen():
            if self.start_game():
                self.end_screen()
    # Заставка
    def start_screen(self):
        intro_text = ["ChemX", "Продолжить", "Новая игра", "Выйти"]
        screen_buttons_rects = []
        self.screen.fill((115, 219, 230))
        intro_picture = load_image('intro.png', -1)
        intro_picture = pygame.transform.scale(intro_picture,
                                            (900, 400))
        intro_p_rect = intro_picture.get_rect()
        intro_p_rect.x, intro_p_rect.y = -20, 10
        font1 = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 35)
        text_coord = 50
        self.screen.blit(intro_picture, intro_p_rect)
        for line in range(len(intro_text)):
            if line == 0:
                string_rendered = font1.render(intro_text[line],\
                                          1, pygame.Color('black'))
            else:
                string_rendered = font2.render(intro_text[line],\
                                          1, pygame.Color('black'))                
            intro_rect = string_rendered.get_rect()
            if line == 0:
                text_coord += 35
            else:
                text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 30
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
            rect_button = pygame.Rect(intro_rect)
            rect_button.x -= 5 
            rect_button.y -= 10
            rect_button.w += 20
            rect_button.h += 8
            screen_buttons_rects.append(rect_button)
            pygame.draw.rect(self.screen, (0, 0, 0), rect_button, 1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_buttons_rects[1].x <= event.pos[0] <=\
                                               screen_buttons_rects[1].x + \
                                               screen_buttons_rects[1].w\
                    and screen_buttons_rects[1].y <= event.pos[1] <= \
                                               screen_buttons_rects[1].y + \
                                               screen_buttons_rects[1].h:
                        print('HOOOOOOOORAY')
                        return True
                    elif screen_buttons_rects[3].x <= event.pos[0] <=\
                         screen_buttons_rects[3].x + \
                         screen_buttons_rects[3].w\
                         and screen_buttons_rects[3].y <= event.pos[1] <= \
                         screen_buttons_rects[3].y + \
                         screen_buttons_rects[3].h:
                        print('STOP')
                        self.terminate()
                
            pygame.display.flip()
            self.clock.tick(10)
            
    # закрывает игру
    def terminate(self):
        pygame.quit()
        sys.exit()
        
    # экран, говорящий о победе
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
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(10)

    # Сама игра
    def start_game(self):
        global all_sprites
        background_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.LayeredUpdates()
        flask_group = pygame.sprite.GroupSingle()
        pipette_group = pygame.sprite.Group() 
        matches_group = pygame.sprite.GroupSingle()
        burner_group = pygame.sprite.GroupSingle()
        book_group = pygame.sprite.GroupSingle()
        elem_group = pygame.sprite.Group()
        save_group = pygame.sprite.Group()
        test_group = pygame.sprite.GroupSingle()
    
        bck = Background(self.size, background_group)
        all_sprites.add(bck, layer=-1)
        
        main_flask = Flask((384, 300), flask_group)
        all_sprites.add(main_flask, layer=1)
        
        
        pipette_x = 595
        for i in range(3):
            pipette = Pipette((pipette_x, 400), pipette_group)
            all_sprites.add(pipette, layer=0) 
            pipette_x += 25
        
        matches = Matches((90, 340), matches_group)
        all_sprites.add(matches, layer=0)
        
        burner = Burner((715, 240), burner_group)
        all_sprites.add(burner, layer=0)
        
        book = Encyclopaedia((0, 0), book_group)
        all_sprites.add(book, layer=0)
        
        # pos, normal_state, color, quantity, name, *groups
        self.spis_el = [Substance((0, 0), 'solid', 'yellow', 2, 'S',\
                                  elem_group),\
                        Substance((0, 0), 'solid', 'dark grey', 2, 'Na', \
                                  elem_group),\
                        Substance((0, 0), 'liquid', '#00BFFF', 3, 'H2O',\
                                  elem_group),\
                        Substance((0, 0), 'liquid', 'grey', 2, 'H2SO4',\
                                  elem_group),\
                        Substance((0, 0), 'gas', '#b7c71b', 1, 'Cl',\
                                  elem_group)]
        table = Table_of_elements(8, 1, self.screen, self.spis_el)
        table.set_view(200, 0)
        
        #level = load_level("level5.txt")
        player = checkpoint = start_checkpoint = None
        #camera = Camera(groups_to_update_with_camera)
        '''for y in range(len(level)):
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
                    all_sprites.add(end, layer=2)'''

        left, right, up = False, False, False
        actions_list = [left, right, up]
        checkpoint = start_checkpoint
        dragging = False
        saved_el = None
        print(elem_group)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
             # Сигналы, получаемые от игрока     
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    try:
                        coords = table.get_cell(event.pos)
                        print(coords)
                        if coords!= None:
                            x, y = coords[0], coords[1]
                            saved_el = self.spis_el[x]
                            dragging = True
                            mouse_x, mouse_y = event.pos
                            test = Test_Substance((mouse_x, mouse_y), \
                                                  saved_el.normal_state,\
                                                  saved_el.color,\
                                                  saved_el.name,\
                                                  test_group)
                            all_sprites.add(test, layer=2)
                            '''if saved_el.mask.get_at((event.pos[0] - saved_el.rect.x,\
                                                           event.pos[1]\
                                                           - saved_el.rect.y)):
                            print(True)
                            dragging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = saved_el.rect.x - mouse_x
                            offset_y = saved_el.rect.y - mouse_y'''                
                    except Exception:
                        continue
                         
                if event.type == pygame.MOUSEMOTION:
                    if dragging and saved_el != None:
                        mouse_x, mouse_y = event.pos
                        test.change_pos((mouse_x, mouse_y))  
                        
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    try:
                        dragging = False
                        saved_el = None
                        if pygame.sprite.collide_mask(test, main_flask):
                            main_flask.change(test.color)
                        test.kill()
                    except Exception as e:
                        print(e)
                                     

                if event.type == pygame.KEYUP:
                    if event.key in DCT_FOR_MOVING_PLAYER.keys():
                        actions_list[DCT_FOR_MOVING_PLAYER[event.key]] = False

            '''for enemy in enemy_group:
                if enemy.image_name != 'robot.png':
                    enemy.move()
                else:
                    enemy.move(bullet_group, all_sprites)'''
            # Возвращение экрана к дефолту
            self.screen.fill((0, 0, 0))
            #camera.update(player)
            '''for bullet in bullet_group: 
                bullet.update(enemy_group if bullet.flag_to_diff == 'enemy'
                              else player, platforms_group, SCREEN_WIDTH)'''         
            '''for end in end_group:
                if end.update(player):
                    sleep(1)
                    return True'''
            '''for group in groups_to_update_with_camera:
                for sprite in group:
                    camera.apply(sprite)
            camera.word_r, camera.word_l = False, False
            camera.word_up, camera.word_down = False, False
            checkpoint = player.update(*actions_list, platforms_group,
                                       bullet_group,
                                       [fire_group, enemy_group],
                                       checkpoint, save_group)'''            

            all_sprites.draw(self.screen)
            table.render()
            pygame.display.flip()
            self.clock.tick(self.fps)


class Background(pygame.sprite.Sprite):
    def __init__(self, size, background_group):
        super().__init__(background_group)
        self.image = pygame.transform.scale(load_image('table_texture.jpg'),
                                            size)
        self.rect = self.image.get_rect()


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, image_filename, color_key, *groups):
        super().__init__(*groups)
        self.image = load_image(image_filename, color_key=color_key)
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self, pos):
        self.rect.topleft = (pos[0], pos[1])
     
    def kill(self):
        super().kill()
     
    def add(self, *groups):
        super().add(*groups)
    
    def groups(self):
        return super().groups()  


class Flask(Object):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'Flask.png', None, *groups)
        self.pos = pos
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.counter = 0
    
    def change(self, color):
        self.counter += 1
        if self.counter == 1:
            self.image = load_image('Flask_filled_1.png', -1)
        elif self.counter == 2:
            self.image = load_image('Flask_filled_2.png', -1)
        elif self.counter == 3:
            self.image = load_image('Flask_filled_3.png', -1)
        elif self.counter == 4:
            self.image = load_image('Flask_filled_4.png', -1)
        elif self.counter == 5:
            self.image = load_image('Flask_filled_5.png', -1)            
        self.image = pygame.transform.scale(self.image, (250, 250))
        pixels = pygame.PixelArray(self.image)
        colors_appearance = {}
        colors_freq = []
        for i in range(len(pixels)):
            for j in range(len(pixels[i])):
                if pixels[i][j] not in colors_appearance:
                    colors_appearance[pixels[i][j]] = 1
                else:
                    colors_appearance[pixels[i][j]] += 1
        for i in colors_appearance.keys():
            colors_freq.append([i, colors_appearance[i]])
        colors_freq = sorted(colors_freq, key=lambda x: x[1], reverse=True)
        colors_freq = list(map(lambda x: self.image.unmap_rgb(x[0]),\
                               colors_freq))
        #print(colors_freq)
        colors_freq = list(filter(lambda x: 203 - 10 <= x.r <= 203 + 15,\
                                  colors_freq))
        #print(colors_freq)
        for i in colors_freq:
            pixels.replace(i, pygame.Color(color))
        colorImage = pixels.make_surface()
        pixels.close()
        self.image.blit(colorImage, (0, 0))
                

class Pipette(Object):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'Pipette.png', None, *groups)
        self.pos = pos
        self.image = pygame.transform.scale(self.image, (80, 120))
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)


class Matches(Object):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'matches1.png', -1, *groups)
        self.pos = pos
        self.image = pygame.transform.scale(self.image, (270, 280))
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)


class Burner(Object):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'burner_inactive.png', -1, *groups)
        self.pos = pos
        self.image = pygame.transform.scale(self.image, (165, 230))
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.state = 'inactive'


class Encyclopaedia(Object):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'book.png', -1, *groups)
        self.pos = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect().move(pos[0], pos[1])


class Table_of_elements:
    def __init__(self, width, height, screen, el):
        self.width = width
        self.height = height
        self.screen = screen
        self.board = [[0] * width for _ in range(height)]
        for i in range(len(el)):
            self.board[0][i] = el[i]  
            
        self.left = 10
        self.top = 10
        self.cell_size = 100
    def set_view(self, left, top):
        self.left = left
        self.top = top
    def render(self):
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x, y,\
                                                                 self.cell_size,
                                                                 self.cell_size), 2)
                elif self.board[i][j] != 0:
                    pygame.draw.rect(self.screen, pygame.Color('black'), (x, y,\
                                                                 self.cell_size,
                                                                 self.cell_size), 2)
                    if (self.board[i][j]).normal_state == 'gas':
                        (self.board[i][j]).change_pos((x + 25, y + 20))
                    elif (self.board[i][j]).normal_state == 'liquid':
                        (self.board[i][j]).change_pos((x + 34, y + 20))
                    elif (self.board[i][j]).normal_state == 'solid':
                        (self.board[i][j]).change_pos((x + 25, y + 20))                    
                    all_sprites.add(self.board[i][j], layer=2)
                    
                x += self.cell_size
            x = self.left
            y += self.cell_size
    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.width * self.cell_size:
            curr_x = (mouse_pos[0] - self.left) // self.cell_size
        else:
            curr_x = None
            
        if self.top <= mouse_pos[1] <= self.top + self.height * self.cell_size:
            curr_y = (mouse_pos[1] - self.top) // self.cell_size
        else:
            curr_y = None
        
        if curr_x != None and curr_y != None:
            coords = (curr_x, curr_y)
            return coords
        else:
            return None
        
    def on_click(self, cell_coords):
        pass
'''while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    pygame.display.flip()'''


class Object_Substance(Object):
    def __init__(self, pos, normal_state, color, name, *groups):
        self.normal_state = normal_state
        if self.normal_state == 'solid':
            super().__init__(pos, 'solid.png', -1, *groups)
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif self.normal_state == 'liquid':
            super().__init__(pos, 'blob.png', -1, *groups)
            self.image = pygame.transform.scale(self.image, (40, 50))
        elif self.normal_state == 'gas':
            super().__init__(pos, 'gas.png', -1, *groups)
            self.image = pygame.transform.scale(self.image, (50, 50))
        self.name = name
        self.pos = pos
        self.color = color
        colorImage = pygame.Surface(self.image.get_size()).convert_alpha()
        colorImage.fill(pygame.Color(self.color))
        self.image.blit(colorImage, (0,0), \
                        special_flags = pygame.BLEND_RGB_MULT)        
        
        self.rect = self.image.get_rect().move(pos[0], pos[1])
        self.mask = pygame.mask.from_surface(self.image)
    
    def change_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]    
    
class Substance(Object_Substance):
    def __init__(self, pos, normal_state, color, quantity, name, *groups):
        super().__init__(pos, normal_state, color, name, *groups)
        self.quantity = quantity


class Test_Substance(Object_Substance):
    def __init__(self, pos, normal_state, color, name, *groups):
        super().__init__(pos, normal_state, color, name, *groups)
        self.pos = pos
        
           
if __name__ == '__main__':
    # Определение переменных

    END_BACKGROUND = 'end_background.png'
    LEVEL_FILENAME = 'level.txt'
    SYMB_FOR_PLATFORM_IN_LEVEL_FILE = '#'
    SYMB_FOR_PLAYER_IN_LEVEL_FILE = '@'
    SYMB_FOR_FIRE_IN_LEVEL_FILE = 'F'
    DCT_FOR_MOVING_PLAYER = {pygame.K_w: 2, pygame.K_a: 1, pygame.K_d: 0}

    main = Main()