from __future__ import annotations

import random
import tcod
from typing import Tuple, TYPE_CHECKING

from game_map import GameMap
import entity_factories
import tile_types

if TYPE_CHECKING:
    from engine import Engine


class RectangularRoom:
    """Object representing RectangularRoom"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self):
        """Returns center of the room"""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self):
        """Returns inner area of the room"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)  # adds 1 to not include walls

    def intersects(self, other):
        """Return True if this room overlaps with another RectangularRoom."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def place_entities(
        room: RectangularRoom, dungeon: GameMap, maximum_monsters: int
):
    """Placing entities in random positions in the room"""

    number_of_monsters = random.randint(0, maximum_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)   # 0.2 chance for the orc
            else:
                entity_factories.troll.spawn(dungeon, x, y)    # 0.8 chance for the orc


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
):
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    engine: Engine,
):
    """Returns generated dungeon with rooms and tunnels"""

    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms = []
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor  # Populating inner area of the room with floor tiles

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)  # Places the player in the first room
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor  # Populating inner area of the tunnel with floor tiles

        place_entities(new_room, dungeon, max_monsters_per_room)  # Populating rooms with entities

        rooms.append(new_room)

    return dungeon
