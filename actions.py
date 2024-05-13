from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from entity import Entity, Actor


class Action:
    """A general class of the Action for modeling other Actions in the game"""
    def __init__(self, entity: Actor):
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
    def __init__(self, entity: Actor, dx: int, dy: int):
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

    @property
    def target_actor(self):
        """Returns the actor at the action destination"""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self):
        """Must be overriden by the subclasses"""
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """Action of attacking the enemies"""
    def perform(self):
        target = self.target_actor

        if not target:
            return

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} points!", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


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
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

