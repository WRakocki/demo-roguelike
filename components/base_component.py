from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    """Base Component for creating future components"""
    entity: Entity = None  # Owning entity instance.

    @property
    def engine(self):
        return self.entity.game_map.engine