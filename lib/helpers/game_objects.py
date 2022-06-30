import pygame
import time


class Sprite(object):

    def __init__(self, image: pygame.Surface, size: tuple) -> None:

        self.image = image
        self.size = size

class BaseBlock(object):

    def __init__(self, position: tuple, sprite: Sprite) -> None:

        self.sprite = sprite

        self.rect = pygame.Rect(position[0], position[1], sprite.size[0], sprite.size[1])

        self.sub_sprites = []

        self.visible = True
        self.sub_sprites_visible = True
        self.can_collide = True

    def add_sub_sprite(self, sprite) -> None:
        self._sub_sprite.append(sprite)


class Humanoid(BaseBlock):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.health = 100
        self.speed = 1

        self.sub_sprites = {}

        self.idle_image = self.sprite.image

        self.move_animation_images = []
        self.move_ptr = None

        self.next_image_anim_time = time.time()
        self.next_image_anim_gap = 0.2

        self.state = 'idle'

    def initialize_animations(self):
        """
        only should be called after set_sprites was used
        """

        for anim_name, image in self.sub_sprites.items():
            if 'move' in anim_name:
                self.move_animation_images.append(image)
        
        self.move_ptr = iter(self.move_animation_images)

    def update_animation_images(self):

        if self.state == 'move':
            if self.next_image_anim_time <= time.time():
                self.next_image_anim_time = time.time() + self.next_image_anim_gap
                
                try:
                    self.sprite.image = next(self.move_ptr)
                except StopIteration:
                    self.sprite.image = self.move_animation_images[0]
                    self.move_ptr = iter(self.move_animation_images)

        elif self.state == 'idle':
            if self.sprite.image != self.idle_image:
                self.sprite.image = self.idle_image

    def play_move_animation(self):

        self.state = 'move'
        self.sprite.image = self.move_animation_images[0]

        self.next_image_anim_time = time.time() + self.next_image_anim_gap

    def stop_move_animation(self):

        self.state = 'idle'

    def set_sprites(self, sprites: dict) -> None:
        self.sub_sprites = sprites

    def __call__(self) -> Sprite:
        self.update_animation_images()
        return self.sprite.image


class Player(Humanoid):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.render_distance_x = 2000
        self.render_distance_y = 2000