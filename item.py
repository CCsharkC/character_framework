from action import Action
from entity import Entity

class ItemEffect():
    """
    Example Effect
    Name: 'Example'
    type: 'Mood'
    Info: {'stat': 'example', 'value': 10, 'decay': 0.5, 'decay_sign': True}
    """

    def __init__(self, name: str, effect_type: str, info: dict = None):
        self.name = name
        self.type = effect_type
        self.info = info

    def change_effect(self, name: str = None, effect_type: str = None, info: dict = None):
        """
        Change the effect of the object.
        Args:
            name (str, optional): The new name for the object. Defaults to None.
            effect_type (str, optional): The new type of effect for the object. Defaults to None.
            info (dict, optional): Additional information about the effect. Defaults to None.
        """
        self.name = name if name is not None else self.name
        self.type = effect_type if effect_type is not None else self.type
        self.info = info if info is not None else self.info

    def get_effect(self):
        """
        Returns a dictionary containing the name, type, and info of the object.
                 - name (str): The name of the object.
                 - type (str): The type of the object.
                 - info (str): Additional information about the object.
        """
        return {'name': self.name, 'type': self.type, 'info': self.info}

class Item():
    
    def __init__(self, *, name: str, item_id: (int, str), effects: dict = None,):
        self.name = name
        self.item_id = item_id
        self.effects = effects

    def add_effect(self, effect_id, effect: ItemEffect):
        """
        Adds an effect to the item.
        Args:
            effect_id (str): The ID of the effect.
            effect (ItemEffect): The effect to be added.
        """
        self.effects[effect_id] = effect

    def use_item(self, *, user: Entity = None, target: Entity):
        """
        Applies the effects of using an item on a target entity.

        Args:
            user (Entity): The entity using the item. Defaults to None.
            target (Entity): The entity being targeted by the item.
        """
        for effect in self.effects.values():
            if effect.effect_type == 'Mood':
                event = Action(perp=user, target=target)
                event.mood_effect(stat=effect.info['stat'],
                                  value=effect.info['value'],
                                  statlet={
                                    'value': effect.info['value'],
                                    'decay': effect.info['decay'],
                                    'decay_sign': effect.info['decay_sign']
                                })
