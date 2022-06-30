from ctypes.wintypes import PLARGE_INTEGER
from dis import dis
from lib.helpers.game_manager import GameManager
from lib.helpers.game_objects import Player, Sprite

from lib.utils.load_json import LoadJson

import pygame


pygame.init()
pygame.mixer.init()

config_data = LoadJson.load('config.json')

clock = pygame.time.Clock()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

images = {
    'blocks': {
        'floor': {
            'base_floor': 'static/images/floor.jpg'
        },
        'wall': {
            'base_wall': 'static/images/wall.jpg'
        }
    },
    'humanoids': {
        'player': {
            'idle': 'static/images/player_idle.png',
        }
    }
}

# --------- functions responsible for proper images setup ------------

def load_animation(parent_name: str, animation_name: str, animation_length: int, is_jpg: bool) -> None:

    ending = '.jpg' if is_jpg else '.png'

    for i in range(animation_length):
        images['humanoids'][parent_name][animation_name + str(i + 1)] = 'static/images/%s%s' % (parent_name + '_' + animation_name + str(i + 1), ending)

def load_image(image_directory: str) -> pygame.Surface:

    image = pygame.image.load(image_directory)
    image = pygame.transform.scale(image, (image.get_width() * config_data['block_size'], image.get_height() * config_data['block_size'])).convert_alpha()

    return image

def go_through_value(value: any) -> None:

    if isinstance(value, dict):
        for key, new_value in value.items():
            got = go_through_value(new_value)
            if got:
                value[key] = got
    elif isinstance(value, str):
        return load_image(value)

    return None

def finalize_images() -> None:

    go_through_value(images)

# --------- functions responsible for proper images setup ------------

# --------- other functions ------------

def get_distance(a: tuple, b: tuple) -> tuple:

    if a[0] > a[1]:
        xd = a[0] - a[1]
    else:
        xd = a[1] - a[0]
    
    if b[0] > b[1]:
        yd = b[0] - b[1]
    else:
        yd = b[1] - b[0]

    return (xd, yd)

# --------- other functions ------------

load_animation('player', 'move', 2, False)

# ------- final setup ---------

finalize_images()

manager = GameManager(config_data, images)

player_sprite = Sprite(
    images['humanoids']['player']['idle'],
    (
        images['humanoids']['player']['idle'].get_width(),
        images['humanoids']['player']['idle'].get_height()
    )
)

player = Player((100, 100), player_sprite)
player.set_sprites(images['humanoids']['player'])

# ------- final setup ---------

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for x_position, x_value in manager.grid.items():
        for y_position, block in x_value.items():

            if block.visible == False:
                continue

            x_position = int(x_position)
            y_position = int(y_position)

            distance = get_distance((player.rect.x, player.rect.y), (x_position, y_position))

            if distance[0] < 200 and distance[1] < 200:

                display.blit(block.sprite.image, (block.rect.x, block.rect.y))

                if block.sub_sprites_visible == False:
                    continue

                for sub_sprite in block.sub_sprites:
                    display.blit(block.sub_sprite.image, (block.rect.x, block.rect.y))

            continue

    pygame.display.flip()

    clock.tick(config_data['fps'])
