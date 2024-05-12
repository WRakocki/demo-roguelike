from components.base_component import BaseComponent


class Fighter(BaseComponent):
    """
    Component holding information related to combat.
    If an entity can fight it will have this component attached
    """
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
