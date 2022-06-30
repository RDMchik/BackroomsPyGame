import pygame


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

    def set_sprites(self, sprites: dict) -> None:
        self.sub_sprites = sprites


class Player(Humanoid):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)