from asyncio import create_subprocess_exec
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
        blocks_allowed_spots = []
            
        to_do = []
        for i in range(self.config_data['chunk_size']):
            to_do.append(i)

        existing_spots_x = []

        for multiplier in to_do:
            
            starter_x = self.grid.get(str(position[0] + self.config_data['block_size'] * multiplier))

            if starter_x:
                existing_spots_x.append(starter_x)

        existing_spots_y = []

        for multiplier in to_do:
            
            starter_y = self.grid.get(str(position[1] + self.config_data['block_size'] * multiplier))

            if starter_y:
                existing_spots_y.append(starter_y)

        if len(existing_spots_x) == 0:
            chosen_x = position[0] + self.config_data['block_size'] * random.choice(to_do)
        else:
            chosen_x = int(list(random.choice(existing_spots_x).keys())[0])

        if len(existing_spots_y) == 0:
            chosen_y = position[1] + self.config_data['block_size'] * random.choice(to_do)
        else:
            chosen_y = int(list(random.choice(existing_spots_y).keys())[0])

        for _ in range(self.config_data['chunk_lines']):

            cur_x = chosen_x
            cur_y = position[1]

            while True:

                blocks_allowed_spots.append((cur_x, cur_y))

                to_move = random.randint(1, 3)

                if to_move == 1:
                    if cur_x - self.config_data['block_size'] >= position[0]:
                        cur_x = cur_x - self.config_data['block_size']
                    else:
                        continue
                elif to_move == 2:
                    if cur_y + self.config_data['block_size'] <= position[1] + self.config_data['block_size'] * to_do[-1]:
                        cur_y = cur_y + self.config_data['block_size']
                    else:
                        break
                else:
                    if cur_x + self.config_data['block_size'] <= position[0] + self.config_data['block_size'] * to_do[-1]:
                        cur_x = cur_x + self.config_data['block_size']
                    else:
                        continue

            cur_x = position[0]
            cur_y = chosen_y

            while True:

                blocks_allowed_spots.append((cur_x, cur_y))

                to_move = random.randint(1, 3)

                if to_move == 1:
                    if cur_y - self.config_data['block_size'] >= position[1]:
                        cur_y = cur_y - self.config_data['block_size']
                    else:
                        continue
                elif to_move == 2:
                    if cur_x + self.config_data['block_size'] <= position[0] + self.config_data['block_size'] * to_do[-1]:
                        cur_x = cur_x + self.config_data['block_size']
                    else:
                        break
                else:
                    if cur_y + self.config_data['block_size'] <= position[1] + self.config_data['block_size'] * to_do[-1]:
                        cur_y = cur_y + self.config_data['block_size']
                    else:
                        continue

        for x in range(self.config_data['chunk_size']):
            x = x * self.config_data['block_size'] + position[0]

            for y in range(self.config_data['chunk_size']):
                y = y * self.config_data['block_size'] + position[1]

                if not (int(x), int(y)) in blocks_allowed_spots:
                    continue

                block = self._generate_block((x, y), biome)

                if not blocks.get(str(x)):
                    blocks[str(x)] = {}

                blocks[str(x)][str(y)] = block
        
        return blocks

    def _generate_biome(self, position: tuple, biome: str) -> None:

        for x in range(self.config_data['biome_size']):
            x = x * (self.config_data['block_size'] * self.config_data['chunk_size']) + position[0] + x * 20

            for y in range(self.config_data['biome_size']):
                y = y * (self.config_data['block_size'] * self.config_data['chunk_size']) + position[1] + y * 20

                chunk = self._generate_chunk((x, y), biome)
                self.grid = self._merge_grid_data(self.grid, chunk)
                







