from random import randint
from entity import Entity

class Action():

    """
    A class representing an action to be performed by an entity.
    Functions:
    roll: Rolls a randomised stat check.
    effect: Modifies the mood of the target
    """

    def __init__(self, *, perp: Entity = None, target: Entity):
        self.perp = perp
        self.target = target

    def roll(self, stat_checks: list, hi_lo: bool, buff: int = 0) -> bool:
        """
        Check if the target's mood stats pass a series of checks.
        Parameters:
            stat_checks (list): A list of mood stats to check.
            hi_lo (bool): If True:
                          Check if the stat is higher than the target's mood stat minus the buff. 
                          If False:
                          Check if the stat is lower than the target's mood stat plus the buff.
            buff (int, optional): The buff value to add or subtract from the target's mood stat. 
                                  Defaults to 0.
        Returns:
            bool: True if all the mood stats pass the checks, False otherwise.
        """
        for stat in stat_checks:
            stats = (self.target.mood_stats
                     if stat in self.target.mood_stats
                     else self.target.personality_stats)
            if hi_lo:
                if randint(0, 100) <= stats[stat] - buff:
                    return False
            elif not hi_lo:
                if randint(0, 100) >= stats[stat] + buff:
                    return False
            return True

    def mood_effect(self, stat: str, value: int, statlet: dict = None):
        """
        Modify the given mood stat of the target by the specified value.

        Args:
            stat (str): The name of the mood stat to be modified.
            value (int): The value by which the mood stat should be modified.
            statlet (dict, optional): A dictionary containing information about the statlet. 
                                      Defaults to None.
                                      {'value': :int, 'decay': :float, 'decay_sign': :bool}.
        """
        if stat in self.target.mood_stats:
            self.target.mood_stats[stat] += value
            if statlet is not None:
                self.target.create_statlet(target=stat,
                                           value=statlet['value'],
                                           decay=statlet['decay'],
                                           decay_sign=statlet['decay_sign'])
