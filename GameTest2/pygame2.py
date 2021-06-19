import pygame, sys, os, random
from pygame.locals import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# LOADING STUFFS #

dirt = pygame.image.load('dirt.png')
grass = pygame.image.load('grass.png')
map_frame = pygame.image.load("assets/hud/map_frame.png")
empty_bar = pygame.image.load("assets/item_bar/not_selected.png")
selected_bar = pygame.image.load("assets/item_bar/selected.png")

fall_off_sound = pygame.mixer.Sound('sfx/fall_off.wav')
jump_sound = pygame.mixer.Sound('sfx/jump.wav')
grass_sounds = [pygame.mixer.Sound('sfx/grass_0.wav'),pygame.mixer.Sound('sfx/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)
fall_off_sound.set_volume(0.3)
pygame.mixer.music.load('sfx/music.wav')
pygame.mixer.music.set_volume(0.7)

#pygame.mixer.music.play(-1)

####################

# MAIN DEFİNİTİONS #

clock = pygame.time.Clock()

FPS = 90
WINDOW_SIZE = (600,400)
TILE_SIZE = grass.get_width()
window = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300,200))
pygame.display.set_caption('GameDev')
background_object = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[-20,40,40,400]],[0.5,[70,90,100,400]],[0.5,[250,80,120,400]],[0.5,[400,50,140,400]]]

global animationFrames
animationFrames = {}

grass_sound_timer = 0

#####################

# FUNCTIONS #

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

def load_animation(path, frameDurations):
    global animationFrames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frameDurations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_image.set_colorkey((255,255,255))
        animationFrames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data, animation_image

def load_item_bar():

    image_name = "selected_"
    n = 0
    image_list = []

    while True:

        try:
            image_path = "assets/item_bar/"+image_name+str(n)+".png"
            image = pygame.image.load(image_path)
            image_list.append(image)
            print(image)
            n += 1

        except FileNotFoundError as error:
            break

    return image_list


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


def restart_game():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def remove_block(block_index):

    for y in range(len(game_map)):


        try:
            if block_index >= len(game_map[y]):

                block_index -= len(game_map[y])

            else:

                game_map[y][block_index] = '0'
                break

        except IndexError as e:
            pass

def add_block(block_index,block_id):

    for y in range(len(game_map)):

        try:
            if block_index >= len(game_map[y]):

                block_index -= len(game_map[y])

            elif game_map[y][block_index] == '0' and item_bar_empty == False:
                game_map[y][block_index] = block_id
                break

        except IndexError as e:
            pass
def print_1():

    print("SLOT SELECTED")

def left_click():


    if inventory_is_open == False:
        for i in range(len(tile_rects)):

            tile_coor_x1 = tile_rects[i][0] - scroll[0]
            tile_coor_x2 = tile_rects[i][0] - scroll[0] + 32

            tile_coor_y1 = tile_rects[i][1] - scroll[1]
            tile_coor_y2 = tile_rects[i][1] - scroll[1] + 32

            if mouse_pos[0]/2 > tile_coor_x1 and mouse_pos[0]/2 < tile_coor_x2 and mouse_pos[1]/2 > tile_coor_y1 and mouse_pos[1]/2 < tile_coor_y2:
                remove_block(i)

    if inventory_is_open:

        for i in range(len(slot_list_with_coors)):

            for i2 in range(len(slot_list_with_coors[i])):
                slot_coor_x1 = slot_list_with_coors[i][i2][0]
                slot_coor_x2 = slot_list_with_coors[i][i2][0] + 32

                slot_coor_y1 = slot_list_with_coors[i][i2][1]
                slot_coor_y2 = slot_list_with_coors[i][i2][1] + 32

                if mouse_pos[0] > slot_coor_x1 and mouse_pos[0] < slot_coor_x2 and mouse_pos[1] > slot_coor_y1 and mouse_pos[1] < slot_coor_y2:
                    selected_slot[0] = i
                    selected_slot[1] = i2
                    print("SELECTED SLOT: ",i,i2)
                    break

def mouse_on_inventory():

    if inventory_is_open:

        for i in range(len(slot_list_with_coors)):

            for i2 in range(len(slot_list_with_coors[i])):
                slot_coor_x1 = slot_list_with_coors[i][i2][0]
                slot_coor_x2 = slot_list_with_coors[i][i2][0] + 32

                slot_coor_y1 = slot_list_with_coors[i][i2][1]
                slot_coor_y2 = slot_list_with_coors[i][i2][1] + 32

                if mouse_pos[0] > slot_coor_x1 and mouse_pos[0] < slot_coor_x2 and mouse_pos[1] > slot_coor_y1 and mouse_pos[1] < slot_coor_y2:
                    mouse_on_slot[0] = i
                    mouse_on_slot[1] = i2
                    #print("SELECTED: ",i,i2)
                    break

def left_click_pressing():

    if inventory_is_open:

        for i in range(len(slot_list_with_coors)):

            for i2 in range(len(slot_list_with_coors[i])):
                slot_coor_x1 = slot_list_with_coors[i][i2][0]
                slot_coor_x2 = slot_list_with_coors[i][i2][0] + 32

                slot_coor_y1 = slot_list_with_coors[i][i2][1]
                slot_coor_y2 = slot_list_with_coors[i][i2][1] + 32

                if mouse_pos[0] > slot_coor_x1 and mouse_pos[0] < slot_coor_x2 and mouse_pos[1] > slot_coor_y1 and mouse_pos[1] < slot_coor_y2:
                    #print("SELECTED: ",i,i2)
                    selected_item[0] = i
                    selected_item[1] = i2
                    drag_item(i,i2)


def drag_item(i1_x,i2_x):

    index1 = i1_x
    index2 = i2_x
    selected2 = False
    global bool1, bool2

    for i in range(len(slot_coors)):

        for i2 in range(len(slot_coors[i])):

            try:

                if i == index1 and i2 == index2:
                    #print(slot_coors[i][i2][0],slot_coors[i][i2][1])


                    if slot_list_with_item_id[i][i2] in item_list:
                        #print("SELECTED ITEM: ", slot_list_with_coors[i])
                        if slot_list_with_item_id[i][i2] == 'dirt' and bool2 == False:
                            slot_coors[i][i2][0] = mouse_pos[0] - 16
                            slot_coors[i][i2][1] = mouse_pos[1] - 16
                            bool1 = True
                            selected2 = True

                        elif slot_list_with_item_id[i][i2] != 'dirt' and bool1 == False:
                            slot_coors[i][i2][0] = mouse_pos[0] - 16
                            slot_coors[i][i2][1] = mouse_pos[1] - 16
                            bool2 = True
                            selected2 = True

                        else:
                            pass

                    break

            except IndexError as error:
                pass
                # SLOT COORS DEGİSECEK CUNKU ONA GORE ITEM CIZILIYOR

        if selected2:
            break



def right_click(block_id):


    if inventory_is_open == False:
        for i in range(len(tile_rects)):

            tile_coor_x1 = tile_rects[i][0] - scroll[0]
            tile_coor_x2 = tile_rects[i][0] - scroll[0] + 32

            tile_coor_y1 = tile_rects[i][1] - scroll[1]
            tile_coor_y2 = tile_rects[i][1] - scroll[1] + 32

            tile_middle_coor = [tile_coor_x1 + 16, tile_coor_y1 + 16]


            if mouse_pos[0]/2 > tile_coor_x1 and mouse_pos[0]/2 < tile_coor_x2 and mouse_pos[1]/2 > tile_coor_y1 and mouse_pos[1]/2 < tile_coor_y2:
                add_block(i,block_id)

    else:
        #print(slot_list)
        pass

def draw_item_bar(x,y):

    x_pos = x
    y_pos = y
    for i in range(9):

        if i == pressed_number - 1:
            window.blit(selected_bar,(x_pos,y_pos))
        else:
            window.blit(empty_bar,(x_pos,y_pos))
        x_pos += 32

def put_item_on_item_bar(x,y):

    x_pos = x
    y_pos = y
    scale_x = 20
    scale_y = 20
    grass_image = pygame.transform.scale(grass, (scale_x,scale_y))
    dirt_image = pygame.transform.scale(dirt, (scale_x,scale_y))

    for i in range(9):

        if i == 0:
            window.blit(dirt_image,(x_pos + (empty_bar.get_width() - scale_x) / 2, y_pos + (empty_bar.get_height() - scale_y) / 2))

        if i == 1:
            window.blit(grass_image,(x_pos + (empty_bar.get_width() - scale_x) / 2, y_pos + (empty_bar.get_height() - scale_y) / 2))

        else:
            pass
        x_pos += 32

def create_inventory_list_with_coors(x,y,slot_list_with_coors):

    x_pos = x
    y_pos = y
    for i in range(6):

        for i2 in range(9):

            if len(slot_list_with_coors[i]) < 9:
                slot_list_with_coors[i].append([x_pos,y_pos])

            x_pos += 32

        x_pos = x
        y_pos += 32

def create_inventory(x,y,slot_list):

    for i in range(6):

        for i2 in range(9):

            if len(slot_list[i]) < 9:
                slot_list[i].append(0)

def open_inventory(x,y):

    x_pos = x
    y_pos = y
    for i in range(len(slot_list)):

        for i2 in range(len(slot_list[i])):

            if slot_list[i][i2] == 0:
                window.blit(empty_bar,(x_pos,y_pos))
                x_pos += 32
            elif slot_list[i][i2] == 1:
                window.blit(selected_bar,(x_pos,y_pos))
                x_pos += 32


            try:
                if i == selected_slot[0] and i2 == selected_slot[1]:

                    slot_list[i][i2] = 1
                    selected_last_slot[0] = selected_slot[0]
                    selected_last_slot[1] = selected_slot[1]

                else:
                    slot_list[i][i2] = 0

            except IndexError as error:
                print(selected_slot)

        x_pos = x
        y_pos += 32

"""def put_item_on_inventory(x,y):

    x_pos = x # X VE Y PARAMETRE OLARAK GELEN OBJENİN KOORDİNATLARI OLACAK VE SOL TIK İLE SÜRÜKLENDİĞİ ZAMAN OBJENİN KOORDİNATLARI DEĞİŞECEK LİSTEDEN
    y_pos = y
    scale_x = 20
    scale_y = 20
    grass_image = pygame.transform.scale(grass, (scale_x,scale_y))
    dirt_image = pygame.transform.scale(dirt, (scale_x,scale_y))


    for i in range(len(slot_list_with_item_id)):

        for i2 in range(len(slot_list_with_item_id[i])):

            if slot_list_with_item_id[i][i2] == 'dirt':
                window.blit(dirt_image,(x_pos + (empty_bar.get_width() - scale_x) / 2, y_pos + (empty_bar.get_height() - scale_y) / 2))
                x_pos += 32

            elif slot_list_with_item_id[i][i2] == 'grass':
                window.blit(grass_image,(x_pos + (empty_bar.get_width() - scale_x) / 2, y_pos + (empty_bar.get_height() - scale_y) / 2))
                x_pos += 32
            else:
                pass"""

def put_item_on_inventory(x,y):

    scale_x = 20
    scale_y = 20
    grass_image = pygame.transform.scale(grass, (scale_x,scale_y))
    dirt_image = pygame.transform.scale(dirt, (scale_x,scale_y))


    for i in range(len(slot_list_with_item_id)):

        for i2 in range(len(slot_list_with_item_id[i])):



            if slot_list_with_item_id[i][i2] == 'dirt':
                window.blit(dirt_image,(slot_list_with_coors[i][i2][0] + (empty_bar.get_width() - scale_x) / 2 , slot_list_with_coors[i][i2][1] + (empty_bar.get_height() - scale_y) / 2))


            elif slot_list_with_item_id[i][i2] == 'grass':
                window.blit(grass_image,(slot_list_with_coors[i][i2][0] + (empty_bar.get_width() - scale_x) / 2 , slot_list_with_coors[i][i2][1] + (empty_bar.get_height() - scale_y) / 2))

            else:
                pass


def add_item_to_inventory_list(id):

    added = False
    for i in range(len(slot_list_with_item_id)):

        for i2 in range(len(slot_list_with_item_id[i])):


            if slot_list_with_item_id[i][i2] == '0':

                slot_list_with_item_id[i][i2] = id
                #print("EKLENDI")
                added = True
                break

        if added:
            break


def create_slot_list_with_item_id():

    for i in range(len(slot_list_with_item_id)):

        for i2 in range(9):

            slot_list_with_item_id[i].append("0")

    #print(slot_list_with_item_id)


def change_items_slot(i2_x,i2_y):

    i1_x = selected_item[0]
    i1_y = selected_item[1]

    slot_list_with_coors[i1_x][i1_y][0] = slot_list_with_coors[i2_x][i2_y][0]
    slot_list_with_coors[i1_x][i1_y][1] = slot_list_with_coors[i2_x][i2_y][1]




#############

# VARIABLES & BOOLEANS #

moveRight = False
moveLeft = False
falling = True
grass_sound_control = False
first_time = True
item_bar_empty = True
inventory_is_open = False
bool1 = False
bool2 = False
dragging = False

playerYMomentum = 0 # Player Vertical Momentum
airTimer = 0
global_slot_index = 2
dragging_items = 1
selected_slot = [50,50]
selected_last_slot = [50,50]
mouse_on_slot = [50,50]
selected_item = [50,50]

true_scroll = [0,0]

animation_database = {}
animation_database['run'],animation_image = load_animation('assets/run',[7,7])
animation_database['idle'],animation_image = load_animation('assets/idle',[7,7,15])

player_action = 'idle'
player_frame = 0
player_flip = 0

######################

# SECOND DEFINITIONS #

player_rect = pygame.Rect(50,50,animation_image.get_width(),animation_image.get_height())
game_map = load_map('map')
game_map.pop()
player_rect.x = 90
player_rect.y = 160
mouse_pos = [0,0]
slot_list = [[],[],[],[],[],[]]
slot_list_with_item_id = [[],[],[],[],[],[]]
slot_list_with_coors = [[],[],[],[],[],[]]
item_list = ['dirt','grass']
block_type = '1'
pressed_number = 0
mini_map = pygame.transform.scale(display, (150,100))

frame_difference = (map_frame.get_width() - mini_map.get_width()) / 2

item_bar_length = empty_bar.get_width() * 9
x_pos_of_item_bar = (WINDOW_SIZE[0] / 2) - (item_bar_length / 2)
y_pos_of_item_bar = WINDOW_SIZE[1] - empty_bar.get_height()

x_pos_of_inventory = (WINDOW_SIZE[0] / 2) - (item_bar_length / 2)
y_pos_of_inventory = (WINDOW_SIZE[1] / 2) - (item_bar_length / 2)

create_inventory_list_with_coors(x_pos_of_inventory-100,y_pos_of_inventory,slot_list_with_coors)
create_inventory(x_pos_of_inventory-100,y_pos_of_inventory,slot_list)

slot_coors = slot_list_with_coors

create_slot_list_with_item_id()

add_item_to_inventory_list("dirt")
print(slot_list_with_item_id[0])
add_item_to_inventory_list("grass")
print(slot_list_with_item_id[0])
print(slot_coors[0])
######################

while True:
    clock.tick(FPS)

    display.fill((46,124,180))

    mouse_pos = list(pygame.mouse.get_pos())

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

# SCROLL & PARALLAX #

    true_scroll[0] += (player_rect.x-true_scroll[0]-144)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-89)/20

    scroll = true_scroll.copy()
    scroll[1] = int(scroll[1])
    scroll[0] = int(scroll[0])

    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,150,600,200))
    for bg_object in background_object:
        obj_rect = pygame.Rect(bg_object[1][0]-scroll[0]*bg_object[0], bg_object[1][1]-scroll[1]*bg_object[0],bg_object[1][2],bg_object[1][3])
        if bg_object[0] == 0.5:
            pygame.draw.rect(display, (14,222,150),obj_rect)
        else:
            pygame.draw.rect(display, (9,100,95),obj_rect)

####################

    mouse_on_inventory()
    if pygame.mouse.get_pressed()[0]:

        left_click_pressing()

    else:
        bool1 = False
        bool2 = False



# DRAW MAP #

    tile_rects = []
    y =  0
    for row in game_map:
        x = 0
        for tile in row:

            if tile == '1':
                display.blit(dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '1' or tile == '2':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE , 0, 0))
            x += 1
        y += 1

#############

#  PLAYER MOVEMENT & PHYSICS #

    player_movement = [0,0]

    if moveRight:
        player_movement[0] += 2

    if moveLeft:
        player_movement[0] -= 2
    player_movement[1] += playerYMomentum

    playerYMomentum += 0.2

    if playerYMomentum > 5:
        playerYMomentum = 5

    if player_movement[0] > 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = False

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')

    if player_movement[0] < 0:
        player_action,player_frame = change_action(player_action,player_frame,'run')
        player_flip = True

    player_rect, collisons = move(player_rect, player_movement, tile_rects)

    if collisons['right'] == True or collisons['left'] == True:
        grass_sound_control = False
    else:
        grass_sound_control = True

    if collisons['bottom']:
        playerYMomentum = 0
        airTimer = 0
        if grass_sound_control:
            if player_movement[0] != 0:
                if grass_sound_timer == 0:
                    grass_sound_timer = 30
                    random.choice(grass_sounds).play()
    else:
        airTimer += 1

    if collisons['top']:
        playerYMomentum = 0


    if airTimer > 10 and airTimer < 20:
        falling = True

    if collisons['bottom'] == True and falling == True and first_time == False:
        fall_off_sound.play()
        falling = False

    if player_rect.y > 500:
        player_rect.x = 50
        player_rect.y = 179
        airTimer = 0

###########################

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animationFrames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x - scroll[0], player_rect.y - scroll[1]))


# EVENT LISTENING #

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_RIGHT:
                moveRight = True
            if event.key == K_LEFT:
                moveLeft = True
            if event.key == K_UP:
                if airTimer < 5:
                    playerYMomentum = -5
                    jump_sound.play()
                    first_time = False
                    falling = True

            if event.key == K_d:
                moveRight = True

            if event.key == K_a:
                moveLeft = True

            if event.key == K_w:
                if airTimer < 5:
                    playerYMomentum = -5
                    jump_sound.play()
                    first_time = False
                    falling = True

            if event.key == K_F5:
                print("Restart")
                restart_game()

            if event.key == K_e:
                if inventory_is_open == False:
                    inventory_is_open = True
                elif inventory_is_open:
                    inventory_is_open = False

            if event.key == K_1:
                block_type = '1'
                pressed_number = 1
                item_bar_empty = False

            if event.key == K_2:
                block_type = '2'
                pressed_number = 2
                item_bar_empty = False

            if event.key == K_3:
                pressed_number = 3
                item_bar_empty = True

            if event.key == K_4:
                pressed_number = 4
                item_bar_empty = True

            if event.key == K_5:
                pressed_number = 5
                item_bar_empty = True

            if event.key == K_6:
                pressed_number = 6
                item_bar_empty = True

            if event.key == K_7:
                pressed_number = 7
                item_bar_empty = True

            if event.key == K_8:
                pressed_number = 8
                item_bar_empty = True

            if event.key == K_9:
                pressed_number = 9
                item_bar_empty = True

        if event.type == MOUSEBUTTONDOWN:

            if event.button == 3:
                right_click(block_type)

            if event.button == 1:
                left_click()
                pass

        if event.type == MOUSEBUTTONUP:

            if event.button == 1:
                print("RELEASED")
                mouse_on_inventory()

                change_items_slot(mouse_on_slot[0],mouse_on_slot[1])

        if event.type == KEYUP:

            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_LEFT:
                moveLeft = False

            if event.key == K_d:
                moveRight = False

            if event.key == K_a:
                moveLeft = False

####################


# UPDATE #

    surface = pygame.transform.scale(display, WINDOW_SIZE)
    mini_map = pygame.transform.scale(display, (150,100)) # 150 100 first
    current_image = empty_bar
    map_frame = pygame.transform.scale(map_frame, (170,120))

    window.blit(surface,(0,0))
    window.blit(mini_map,(WINDOW_SIZE[0]-mini_map.get_width()- frame_difference, frame_difference))
    window.blit(map_frame,(WINDOW_SIZE[0]-map_frame.get_width(),0))
    draw_item_bar(x_pos_of_item_bar,y_pos_of_item_bar)
    put_item_on_item_bar(x_pos_of_item_bar,y_pos_of_item_bar)

    if inventory_is_open:
        open_inventory(x_pos_of_inventory-100,y_pos_of_inventory)
        put_item_on_inventory(slot_coors[0][0][0],slot_coors[0][0][1])
    else:
        selected_slot = [50,50]

    #print(clock.get_fps())
    #window.blit(empty_bar,(227,368))
##########

    pygame.display.update()
