from re import X
from lib.helpers.game_objects import BaseBlock, Sprite

import random


class GameManager(object):

    def __init__(self, config_data: dict, images: dict) -> None:

        self.config_data = config_data
        self.images = images

        self.bioms = [
            'lobby',
        ]

        self.grid = {}

        self._generate_biome((0, 0), 'lobby')

    def _merge_grid_data(self, a: dict, b: dict) -> dict:
        """
        merges b into a
        """

        for x_position, x_value in b.items():
            for y_position, block in x_value.items():

                if not a.get(x_position):
                    a[x_position] = {}

                a[x_position][y_position] = block

        return a

    def _generate_block(self, position: tuple, biome: str) -> BaseBlock:

        if biome == 'lobby':

            sprite = Sprite(
                self.images['blocks']['floor']['base_floor'],
                (
                    self.images['blocks']['floor']['base_floor'].get_width(),
                    self.images['blocks']['floor']['base_floor'].get_height()
                )
            )

        new_block = BaseBlock(
            position, sprite
        )

        return new_block

    def _generate_chunk(self, position: tuple, biome: str) -> dict:

        blocks = {}

        for x in range(self.config_data['chunk_size']):
            x = x * self.config_data['block_size'] + position[0]

            for y in range(self.config_data['chunk_size']):
                y = y * self.config_data['block_size'] + position[1]

                block = self._generate_block((x, y), biome)

                if not blocks.get(str(x)):
                    blocks[str(x)] = {}

                blocks[str(x)][str(y)] = block
        
        return blocks

    def _generate_biome(self, position: tuple, biome: str) -> None:

        chunks = {}

        for x in range(self.config_data['biome_size']):
            x = x * (self.config_data['block_size'] * self.config_data['chunk_size']) + position[0]

            for y in range(self.config_data['biome_size']):
                y = y * (self.config_data['block_size'] * self.config_data['chunk_size']) + position[1]

                chunk = self._generate_chunk((x, y), biome)

                chunks = self._merge_grid_data(chunks, chunk)

        self.grid = self._merge_grid_data(self.grid, chunks)







