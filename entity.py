from __future__ import annotations
import copy

from typing import Tuple, TypeVar, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """Object representing various entities like player, enemies, items etc."""

    def __init__(
            self,
            game_map: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,  # Describes if the entity can move
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: T, game_map: GameMap, x: int, y: int):
        """Spawning entities"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, game_map: Optional[GameMap] = None):
        """Place this entity at a new location, handles moving across GameMaps"""
        self.x = x
        self.y = y

        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int):
        """Moving the entity"""
        self.x += dx
        self.y += dy
