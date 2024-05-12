from __future__ import annotations

from typing import TYPE_CHECKING
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    """Engine object is responsible for updating fov, handling turns and rendering a whole game"""

    game_map: GameMap = None

    def __init__(self, player: Entity):
        self.event_handler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self):
        """Handles enemy turns (placeholder for now)"""
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} is making a move!')

    def update_fov(self):
        """Updates fov with the help of TCOD"""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context):
        """Renders a game to the screen"""
        self.game_map.render(console)

        context.present(console)

        console.clear()
