from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Action:
    """A general class of the Action for modeling other Actions in the game"""
    def __init__(self, entity: Entity):
        super().__init__()
        self.entity = entity

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.game_map.engine

    def perform(self):
        """Perform this action with the objects needed to determine its scope.
        `engine` is the scope this action is being performed in.
        `entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """Exits the game"""
    def perform(self):
        raise SystemExit()


class WaitAction(Action):
    """Simply: waits"""
    def perform(self):
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self):
        """Returns destination coordinates of the entity"""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self):
        """Returns entity blocking at the following destination"""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    def perform(self):
        """Must be overriden by the subclasses"""
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """Action of attacking the enemies"""
    def perform(self):
        target = self.blocking_entity

        if not target:
            return

        print(f'{target.name} is attacked!')


class MovementAction(ActionWithDirection):
    """Action of moving the entity"""
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity
        # print(f"{self.entity.name} makes the move")
        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """Checks if the entity is blocking direction, if true attacks the enemy, otherwise moves the entity"""
    def perform(self):
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

