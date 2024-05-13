from __future__ import annotations
from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    """
    Component holding information related to combat.
    If an entity can fight it will have this component attached
    """
    entity: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense  # Reduced damage
        self.power = power  # Attack power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        """Sets the hp. Will never be less than 0 but never higher than max_hp"""
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self):
        if self.engine.player is self.entity:
            death_message = "You died! Game Over"
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message_color = color.enemy_die
            death_message = f"{self.entity.name} is dead!"

        self.entity.char = "X"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"dead body of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
